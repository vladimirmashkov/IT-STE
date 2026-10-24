"""Select, validate, and advance the compact IT-STE resume state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "docs/it-ste-state/current.json"
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
STATUSES = {"ready", "running", "done", "blocked", "needs-scope", "stopped"}
RESUME_POLICIES = {"auto", "retry", "await-owner", "running"}
COMMON_READ_SET = [
    {
        "path": "docs/it-ste-draft-handoff.md",
        "selector": "#current-checkpoint-read-before-historical-baseline",
    },
    {
        "path": "docs/it-ste-release-readiness-plan.md",
        "selector": "#current-checkpoint",
    },
    {
        "path": "docs/it-ste-research-method.md",
        "selector": "#bounded-research-and-decision-loop",
    },
]
STATE_FILES = [
    "docs/it-ste-state/current.json",
    "docs/it-ste-state/selector.json",
]


class StateError(ValueError):
    """A malformed or unsafe state document."""


def relative_path(value: str, *, runs_only: bool = False) -> str:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise StateError(f"path must be a relative repository path: {value!r}")
    candidate = (ROOT / value).resolve()
    try:
        relative = candidate.relative_to(ROOT).as_posix()
    except ValueError as exc:
        raise StateError(f"path escapes repository: {value!r}") from exc
    if runs_only and not (relative == "docs/it-ste-state/runs" or
                          relative.startswith("docs/it-ste-state/runs/")):
        raise StateError(f"run file must be under docs/it-ste-state/runs: {value!r}")
    return relative


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        try:
            name = path.relative_to(ROOT)
        except ValueError:
            name = path
        raise StateError(f"state file not found: {name}") from exc
    except json.JSONDecodeError as exc:
        try:
            name = path.relative_to(ROOT)
        except ValueError:
            name = path
        raise StateError(f"invalid JSON in {name}: {exc}") from exc
    if not isinstance(value, dict):
        raise StateError(f"JSON object expected: {path}")
    return value


def require(value: dict[str, Any], key: str, kind: type | tuple[type, ...]) -> Any:
    if key not in value or not isinstance(value[key], kind):
        raise StateError(f"missing or invalid field: {key}")
    return value[key]


def validate_run_id(value: Any) -> str:
    if not isinstance(value, str) or not RUN_ID.fullmatch(value):
        raise StateError(f"invalid run_id: {value!r}")
    return value


def validate_read_set(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise StateError("read_set must be a list")
    for item in value:
        if not isinstance(item, dict):
            raise StateError("each read_set item must be an object")
        relative_path(require(item, "path", str))
        if "selector" in item and not isinstance(item["selector"], str):
            raise StateError("read_set.selector must be a string")
    return value


def validate_paths(value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        raise StateError(f"{field} must be a list")
    for item in value:
        relative_path(item)
    return value


def validate_selector(value: dict[str, Any]) -> None:
    if value.get("schema") != 1:
        raise StateError("selector schema must be 1")
    require(value, "workflow", str)
    order = require(value, "phase_order", list)
    phases = require(value, "phases", dict)
    if not order or not all(isinstance(item, str) for item in order):
        raise StateError("selector.phase_order must contain phase names")
    for name in order:
        phase = require(phases, name, dict)
        require(phase, "skill", str)
        require(phase, "mode", str)
        for key in ("cursor", "size", "total"):
            number = require(phase, key, int)
            if isinstance(number, bool) or number < 0:
                raise StateError(f"selector phase {name}.{key} must be non-negative")
        if phase["size"] == 0 or phase["cursor"] > phase["total"]:
            raise StateError(f"invalid selector cursor for phase {name}")
        if "manifest" in phase:
            relative_path(phase["manifest"])
        if "directory" in phase:
            relative_path(phase["directory"])
        if "allowed_paths" in phase:
            validate_paths(phase["allowed_paths"], f"selector.{name}.allowed_paths")
        if "themes" in phase and not all(isinstance(item, str) for item in phase["themes"]):
            raise StateError(f"selector.{name}.themes must contain strings")
        if "scopes" in phase and not all(isinstance(item, str) for item in phase["scopes"]):
            raise StateError(f"selector.{name}.scopes must contain strings")


def validate_current(value: dict[str, Any]) -> None:
    if value.get("schema") != 1:
        raise StateError("current state schema must be 1")
    require(value, "workflow", str)
    require(value, "branch", str)
    status = require(value, "status", str)
    if status not in STATUSES:
        raise StateError(f"invalid current status: {status}")
    require(value, "phase", str)
    require(value, "skill", str)
    require(value, "scope", dict)
    validate_read_set(require(value, "read_set", list))
    validate_paths(require(value, "allowed_paths", list), "allowed_paths")
    require(value, "next_action", str)
    if "selector" in value:
        relative_path(require(value, "selector", str))
    if "resume_policy" in value and value["resume_policy"] not in RESUME_POLICIES:
        raise StateError(f"invalid resume_policy: {value['resume_policy']}")
    if "authorization" in value:
        authorization = require(value, "authorization", dict)
        if "auto_commit" not in authorization:
            raise StateError("current.authorization.auto_commit is required")
        if not isinstance(authorization["auto_commit"], (bool, str)):
            raise StateError("current.authorization.auto_commit must be boolean or policy string")
    if "active_run" in value and value["active_run"] is not None:
        active = require(value, "active_run", dict)
        validate_run_id(require(active, "id", str))
        relative_path(require(active, "input", str), runs_only=True)
        if "output" in active:
            relative_path(require(active, "output", str), runs_only=True)
    if "last_output" in value and value["last_output"] is not None:
        relative_path(require(value, "last_output", str), runs_only=True)


def validate_selection(value: dict[str, Any]) -> None:
    for key in ("phase", "source", "unit"):
        require(value, key, str)
    for key in ("cursor", "next_cursor", "total"):
        number = require(value, key, int)
        if isinstance(number, bool) or number < 0:
            raise StateError(f"selection.{key} must be non-negative")
    if value["next_cursor"] <= value["cursor"] or value["next_cursor"] > value["total"]:
        raise StateError("selection cursor range is invalid")


def validate_input(value: dict[str, Any]) -> None:
    if value.get("schema") != 1:
        raise StateError("input schema must be 1")
    validate_run_id(require(value, "run_id", str))
    for key in ("workflow", "skill", "phase", "question"):
        require(value, key, str)
    require(value, "scope", dict)
    validate_read_set(require(value, "read_set", list))
    validate_paths(require(value, "allowed_paths", list), "allowed_paths")
    validate_paths([require(value, "output_path", str)], "output_path")
    validate_selection(require(value, "selection", dict))
    require(value, "baseline", dict)
    authorization = require(value, "authorization", dict)
    if "auto_commit" not in authorization:
        raise StateError("authorization.auto_commit is required")
    if not isinstance(authorization["auto_commit"], bool):
        raise StateError("authorization.auto_commit must be boolean")


def validate_output(value: dict[str, Any]) -> None:
    if value.get("schema") != 1:
        raise StateError("output schema must be 1")
    validate_run_id(require(value, "run_id", str))
    status = require(value, "status", str)
    if status not in {"done", "blocked", "needs-scope", "stopped"}:
        raise StateError(f"invalid output status: {status}")
    require(value, "decision", str)
    evidence_refs = require(value, "evidence_refs", list)
    if not all(isinstance(item, str) for item in evidence_refs):
        raise StateError("evidence_refs must contain strings")
    validate_paths(require(value, "changed_paths", list), "changed_paths")
    validations = require(value, "validations", list)
    if not all(isinstance(item, dict) for item in validations):
        raise StateError("validations must contain objects")
    next_state = require(value, "next", dict)
    require(next_state, "action", str)
    if "phase" in next_state:
        require(next_state, "phase", str)
    if "skill" in next_state:
        require(next_state, "skill", str)
    if "scope" in next_state:
        require(next_state, "scope", dict)
    if "read_set" in next_state:
        validate_read_set(next_state["read_set"])
    if "allowed_paths" in next_state:
        validate_paths(next_state["allowed_paths"], "next.allowed_paths")
    if "resume_policy" in next_state and next_state["resume_policy"] not in RESUME_POLICIES:
        raise StateError(f"invalid output resume_policy: {next_state['resume_policy']}")
    commit = value.get("commit")
    if commit is not None and not isinstance(commit, dict):
        raise StateError("commit must be an object or null")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def print_json(value: dict[str, Any], compact: bool = True) -> None:
    if compact:
        print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


def git_output(*arguments: str) -> str:
    result = subprocess.run(
        ["git", "--no-optional-locks", *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise StateError(f"git command failed: {' '.join(arguments)}")
    return result.stdout.strip()


def baseline() -> dict[str, Any]:
    status = git_output("status", "--short", "--untracked-files=all")
    return {
        "head": git_output("rev-parse", "HEAD"),
        "status_clean": not status,
        "status_digest": hashlib.sha256(status.encode("utf-8")).hexdigest(),
        "captured_by": "tools/it_ste_resume.py",
    }


def load_current() -> dict[str, Any]:
    current = load_json(STATE_PATH)
    validate_current(current)
    return current


def load_selector(current: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    selector_relative = current.get("selector", "docs/it-ste-state/selector.json")
    selector_path = ROOT / relative_path(selector_relative)
    selector = load_json(selector_path)
    validate_selector(selector)
    if selector["workflow"] != current["workflow"]:
        raise StateError("selector workflow differs from current state")
    return selector_relative, selector


def phase_complete(phase: dict[str, Any]) -> bool:
    return phase["cursor"] >= phase["total"] or phase.get("status") == "complete"


def next_phase_name(selector: dict[str, Any], preferred: str | None = None) -> str | None:
    order = selector["phase_order"]
    phases = selector["phases"]
    if preferred in order and not phase_complete(phases[preferred]):
        return preferred
    for name in order:
        if not phase_complete(phases[name]):
            return name
    return None


def dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def read_item(path: str, selector: str | None = None) -> dict[str, str]:
    item = {"path": relative_path(path)}
    if selector is not None:
        item["selector"] = selector
    return item


def append_existing(read_set: list[dict[str, str]], path: str,
                    selector: str | None = None) -> None:
    relative = relative_path(path)
    if (ROOT / relative).exists():
        read_set.append(read_item(relative, selector))


def authorization_for_run(current: dict[str, Any]) -> dict[str, Any]:
    policy = current.get("authorization", {}).get("auto_commit", False)
    enabled = policy is True or policy == "per-resume-invocation"
    return {"auto_commit": enabled, "source": "explicit /it-ste-release-readiness resume"}


def run_id(phase: str, cursor: int, retry: bool = False) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    suffix = "-retry" if retry else ""
    return f"rr-{phase}-{cursor + 1:03d}{suffix}-{stamp}"


def build_input(current: dict[str, Any], selector: dict[str, Any],
                phase_name: str, retry: bool = False) -> tuple[str, dict[str, Any]] | None:
    phase = selector["phases"][phase_name]
    mode = phase["mode"]
    cursor = phase["cursor"]
    size = phase["size"]
    total = phase["total"]
    end = min(cursor + size, total)
    run = run_id(phase_name, cursor, retry)
    input_relative = f"docs/it-ste-state/runs/{run}.input.json"
    output_relative = f"docs/it-ste-state/runs/{run}.output.json"
    read_set = [dict(item) for item in COMMON_READ_SET]
    selected_paths: list[str] = []
    ids: list[str] = []
    theme: str | None = None
    unit = mode

    if mode == "manifest-rules":
        manifest_relative = relative_path(require(phase, "manifest", str))
        manifest = load_json(ROOT / manifest_relative)
        records = require(manifest, "records", list)
        rules = [item for item in records if isinstance(item, str) and "/rules/" in item]
        if len(rules) != total:
            raise StateError(f"selector W2 total {total} differs from manifest {len(rules)}")
        selected = rules[cursor:end]
        if not selected:
            raise StateError("selector W2 has no next rule slice")
        selected_paths = [relative_path(str(Path(manifest_relative).parent / item))
                          for item in selected]
        ids = [Path(item).stem for item in selected]
        themes = require(phase, "themes", list)
        theme = themes[(cursor // size) % len(themes)]
        append_existing(read_set, manifest_relative, "$.records")
        for path in selected_paths:
            append_existing(read_set, path, "$")
        question = f"Review W2 theme {theme} for {', '.join(ids)}"
        scope = {
            "kind": "w2-theme",
            "theme": theme,
            "ids": ids,
            "paths": selected_paths,
            "excluded": [],
        }
    elif mode == "vocabulary-batches":
        directory = relative_path(require(phase, "directory", str))
        batch_number = cursor + 1
        batch_path = relative_path(f"{directory}/batch-{batch_number:03d}.json")
        if not (ROOT / batch_path).exists():
            raise StateError(f"vocabulary batch not found: {batch_path}")
        selected_paths = [batch_path]
        append_existing(read_set, batch_path, "$")
        unit = f"batch-{batch_number:03d}"
        question = f"Review vocabulary batch {batch_number:03d}"
        scope = {
            "kind": "vocabulary-batch",
            "batch": f"{batch_number:03d}",
            "ids": [],
            "paths": selected_paths,
            "excluded": [],
        }
    elif mode == "gate-scopes":
        scopes = require(phase, "scopes", list)
        gate = scopes[cursor]
        note = "docs/it-ste-research/release-readiness-gates.md"
        append_existing(read_set, note, "#current-gate")
        question = f"Execute release-readiness gate: {gate}"
        unit = gate
        scope = {"kind": "release-gate", "gate": gate, "ids": [], "paths": [], "excluded": []}
    elif mode == "explicit-request":
        return None
    else:
        raise StateError(f"unknown selector mode: {mode}")

    allowed = dedupe(STATE_FILES + [input_relative, output_relative] +
                     list(phase.get("allowed_paths", [])) + selected_paths)
    payload = {
        "schema": 1,
        "run_id": run,
        "workflow": current["workflow"],
        "skill": phase["skill"],
        "phase": phase_name,
        "question": question,
        "scope": scope,
        "selection": {
            "phase": phase_name,
            "source": mode,
            "unit": unit,
            "cursor": cursor,
            "next_cursor": end,
            "total": total,
        },
        "read_set": read_set,
        "allowed_paths": allowed,
        "baseline": baseline(),
        "authorization": authorization_for_run(current),
        "output_path": output_relative,
    }
    validate_input(payload)
    return input_relative, payload


def activate_input(input_relative: str, payload: dict[str, Any],
                   current: dict[str, Any]) -> None:
    active = current.get("active_run")
    if active is not None:
        raise StateError(f"another run is active: {active['id']}")
    updated = dict(current)
    updated.update({
        "workflow": payload["workflow"],
        "status": "running",
        "resume_policy": "running",
        "phase": payload["phase"],
        "skill": payload["skill"],
        "active_run": {
            "id": payload["run_id"],
            "input": input_relative,
            "output": payload["output_path"],
            "selection": payload["selection"],
        },
        "scope": payload["scope"],
        "read_set": payload["read_set"],
        "allowed_paths": payload["allowed_paths"],
        "next_action": payload["question"],
    })
    write_json(STATE_PATH, updated)


def command_show(args: argparse.Namespace) -> int:
    current = load_current()
    print_json(current, args.compact)
    return 0


def command_validate(_: argparse.Namespace) -> int:
    current = load_current()
    selector_relative, selector = load_selector(current)
    print_json({
        "status": "valid",
        "state": STATE_PATH.relative_to(ROOT).as_posix(),
        "selector": selector_relative,
        "phase": current["phase"],
        "selector_cursor": selector["phases"].get(current["phase"], {}).get("cursor"),
    })
    return 0


def command_begin(args: argparse.Namespace) -> int:
    input_relative = relative_path(args.input, runs_only=True)
    payload = load_json(ROOT / input_relative)
    validate_input(payload)
    current = load_current()
    activate_input(input_relative, payload, current)
    print_json({"status": "running", "run_id": payload["run_id"], "input": input_relative})
    return 0


def command_next(args: argparse.Namespace) -> int:
    current = load_current()
    if current.get("active_run") is not None:
        active = current["active_run"]
        print_json({
            "status": "running",
            "run_id": active["id"],
            "input": active["input"],
            "action": "resume active run",
        })
        return 0
    policy = current.get("resume_policy", "auto")
    if current["status"] in {"blocked", "stopped", "needs-scope"} and policy not in {"auto", "retry"}:
        print_json({
            "status": current["status"],
            "phase": current["phase"],
            "skill": current["skill"],
            "action": current["next_action"],
        })
        return 0
    selector_relative, selector = load_selector(current)
    phase_name = next_phase_name(selector, current.get("phase"))
    if phase_name is None:
        raise StateError("selector has no remaining phase")
    phase = selector["phases"][phase_name]
    if phase["mode"] == "explicit-request":
        updated = dict(current)
        updated.update({
            "status": "needs-scope",
            "resume_policy": "await-owner",
            "phase": phase_name,
            "skill": phase["skill"],
            "scope": {"kind": "explicit-candidate-request", "ids": [], "paths": []},
            "allowed_paths": STATE_FILES,
            "next_action": "Explicitly request release-candidate packaging after Phases 1–5 pass.",
        })
        write_json(STATE_PATH, updated)
        print_json({
            "status": "needs-scope",
            "phase": phase_name,
            "skill": phase["skill"],
            "selector": selector_relative,
            "action": updated["next_action"],
        })
        return 0
    retry = current["status"] == "blocked" and policy == "retry"
    selected = build_input(current, selector, phase_name, retry=retry)
    if selected is None:
        raise StateError(f"phase {phase_name} requires explicit scope")
    input_relative, payload = selected
    write_json(ROOT / input_relative, payload)
    activate_input(input_relative, payload, current)
    print_json({
        "status": "running",
        "run_id": payload["run_id"],
        "input": input_relative,
        "phase": phase_name,
        "unit": payload["selection"]["unit"],
        "cursor": payload["selection"]["cursor"],
        "next_cursor": payload["selection"]["next_cursor"],
    })
    return 0


def command_finish(args: argparse.Namespace) -> int:
    output_relative = relative_path(args.output, runs_only=True)
    payload = load_json(ROOT / output_relative)
    validate_output(payload)
    current = load_current()
    active = current.get("active_run")
    if active is None or active["id"] != payload["run_id"]:
        raise StateError("output does not match the active run")
    input_payload = load_json(ROOT / active["input"])
    validate_input(input_payload)
    updated = dict(current)
    selector_changed = False
    selector = None
    selector_relative = current.get("selector")
    if selector_relative:
        selector_path = ROOT / relative_path(selector_relative)
        selector = load_json(selector_path)
        validate_selector(selector)
    if payload["status"] == "done" and selector is not None:
        selection = input_payload["selection"]
        phase = selector["phases"].get(selection["phase"])
        if phase is None:
            raise StateError(f"output phase is not present in selector: {selection['phase']}")
        if phase["cursor"] != selection["cursor"]:
            raise StateError("selector cursor changed while the run was active")
        phase["cursor"] = selection["next_cursor"]
        if phase_complete(phase):
            phase["status"] = "complete"
        selector_changed = True
        next_name = next_phase_name(selector)
        if next_name is None:
            raise StateError("selector completed without a candidate boundary")
        next_phase = selector["phases"][next_name]
        if next_phase["mode"] == "explicit-request":
            updated.update({
                "status": "needs-scope",
                "resume_policy": "await-owner",
                "phase": next_name,
                "skill": next_phase["skill"],
                "scope": {"kind": "explicit-candidate-request", "ids": [], "paths": []},
                "read_set": COMMON_READ_SET,
                "allowed_paths": STATE_FILES,
                "next_action": "Explicitly request release-candidate packaging after Phases 1–5 pass.",
            })
        else:
            updated.update({
                "status": "ready",
                "resume_policy": "auto",
                "phase": next_name,
                "skill": next_phase["skill"],
                "scope": {"kind": "automatic-selector", "phase": next_name,
                          "cursor": next_phase["cursor"]},
                "read_set": COMMON_READ_SET,
                "allowed_paths": STATE_FILES,
                "next_action": f"Automatically select the next {next_name} slice from selector.json.",
            })
    else:
        next_state = payload["next"]
        updated["status"] = payload["status"]
        updated["resume_policy"] = next_state.get("resume_policy", "await-owner")
        for key in ("phase", "skill", "scope", "read_set", "allowed_paths"):
            if key in next_state:
                updated[key] = next_state[key]
        updated["next_action"] = next_state["action"]
    if selector_changed and selector is not None and selector_relative is not None:
        write_json(ROOT / relative_path(selector_relative), selector)
    updated["last_run"] = {
        "id": payload["run_id"],
        "input": active["input"],
        "output": output_relative,
    }
    updated["last_output"] = output_relative
    updated["active_run"] = None
    write_json(STATE_PATH, updated)
    print_json({
        "status": payload["status"],
        "run_id": payload["run_id"],
        "output": output_relative,
        "next_action": updated["next_action"],
    })
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show", help="print the compact resume pointer")
    show.add_argument("--compact", action="store_true", help="emit one-line JSON")
    show.set_defaults(function=command_show)
    check = commands.add_parser("validate", help="validate current.json and selector.json")
    check.set_defaults(function=command_validate)
    next_command = commands.add_parser("next", help="select and activate the next bounded slice")
    next_command.add_argument("--compact", action="store_true", help="emit one-line JSON")
    next_command.set_defaults(function=command_next)
    begin = commands.add_parser("begin", help="activate a bounded input file")
    begin.add_argument("--input", required=True, help="repository-relative input JSON")
    begin.set_defaults(function=command_begin)
    finish = commands.add_parser("finish", help="advance state from an output file")
    finish.add_argument("--output", required=True, help="repository-relative output JSON")
    finish.set_defaults(function=command_finish)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.function(args)
    except StateError as exc:
        print(f"state error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
