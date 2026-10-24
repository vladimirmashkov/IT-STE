"""Validate and advance the compact IT-STE skill resume state."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "docs/it-ste-state/current.json"
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
STATUSES = {"ready", "running", "done", "blocked", "needs-scope", "stopped"}


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
        raise StateError(f"state file not found: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise StateError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise StateError(f"JSON object expected: {path.relative_to(ROOT)}")
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
    if "active_run" in value and value["active_run"] is not None:
        active = require(value, "active_run", dict)
        validate_run_id(require(active, "id", str))
        relative_path(require(active, "input", str), runs_only=True)
    if "last_output" in value and value["last_output"] is not None:
        relative_path(require(value, "last_output", str), runs_only=True)


def validate_input(value: dict[str, Any]) -> None:
    if value.get("schema") != 1:
        raise StateError("input schema must be 1")
    validate_run_id(require(value, "run_id", str))
    for key in ("workflow", "skill", "phase", "question"):
        require(value, key, str)
    require(value, "scope", dict)
    validate_read_set(require(value, "read_set", list))
    validate_paths(require(value, "allowed_paths", list), "allowed_paths")
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


def print_json(value: dict[str, Any], compact: bool) -> None:
    if compact:
        print(json.dumps(value, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


def command_show(args: argparse.Namespace) -> int:
    current = load_json(STATE_PATH)
    validate_current(current)
    print_json(current, args.compact)
    return 0


def command_validate(_: argparse.Namespace) -> int:
    current = load_json(STATE_PATH)
    validate_current(current)
    print_json({"status": "valid", "path": STATE_PATH.relative_to(ROOT).as_posix()}, True)
    return 0


def command_begin(args: argparse.Namespace) -> int:
    input_relative = relative_path(args.input, runs_only=True)
    input_path = ROOT / input_relative
    payload = load_json(input_path)
    validate_input(payload)
    current = load_json(STATE_PATH)
    validate_current(current)
    active = current.get("active_run")
    if active is not None:
        raise StateError(f"another run is active: {active['id']}")
    updated = dict(current)
    updated.update({
        "workflow": payload["workflow"],
        "status": "running",
        "phase": payload["phase"],
        "skill": payload["skill"],
        "active_run": {"id": payload["run_id"], "input": input_relative},
        "scope": payload["scope"],
        "read_set": payload["read_set"],
        "allowed_paths": payload["allowed_paths"],
        "next_action": payload["question"],
    })
    write_json(STATE_PATH, updated)
    print_json({"status": "running", "run_id": payload["run_id"], "input": input_relative}, True)
    return 0


def command_finish(args: argparse.Namespace) -> int:
    output_relative = relative_path(args.output, runs_only=True)
    output_path = ROOT / output_relative
    payload = load_json(output_path)
    validate_output(payload)
    current = load_json(STATE_PATH)
    validate_current(current)
    active = current.get("active_run")
    if active is None or active["id"] != payload["run_id"]:
        raise StateError("output does not match the active run")
    updated = dict(current)
    next_state = payload["next"]
    updated["status"] = payload["status"]
    for key in ("phase", "skill", "scope", "read_set", "allowed_paths"):
        if key in next_state:
            updated[key] = next_state[key]
    updated["next_action"] = next_state["action"]
    updated["last_run"] = {
        "id": payload["run_id"],
        "input": active["input"],
        "output": output_relative,
    }
    updated["last_output"] = output_relative
    updated["active_run"] = None
    write_json(STATE_PATH, updated)
    print_json({"status": payload["status"], "run_id": payload["run_id"],
                "output": output_relative}, True)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show", help="print the compact resume pointer")
    show.add_argument("--compact", action="store_true", help="emit one-line JSON")
    show.set_defaults(function=command_show)
    check = commands.add_parser("validate", help="validate current.json")
    check.set_defaults(function=command_validate)
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
