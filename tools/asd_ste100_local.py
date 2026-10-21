#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Build, publish, and query a token-efficient ASD-STE100 Issue 9 derivative.

The source PDF remains under .local/. Only the authorized derivative database,
manifest, and notices are published. The database is a retrieval aid, not a
replacement for the authoritative PDF.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Sequence
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = (ROOT / ".local").resolve()
PUBLISHED_ROOT = (
    ROOT / "standards/asd-ste100/versions/issue-9/revisions/r0001/reference"
).resolve()
DEFAULT_SOURCE = LOCAL_ROOT / "sources/ASD-STE100-issue-9.pdf"
PRIVATE_DATABASE = LOCAL_ROOT / "derived/asd-ste100/issue-9/reference.sqlite3"
PRIVATE_MANIFEST = PRIVATE_DATABASE.with_name("manifest.json")
DEFAULT_DATABASE = PUBLISHED_ROOT / "reference.sqlite3"
DEFAULT_MANIFEST = PUBLISHED_ROOT / "manifest.json"
DERIVATIVE_NOTICE = PUBLISHED_ROOT / "NOTICE.md"
PERMISSION_RECORD = ROOT / "docs/permissions/asd-ste100-issue-9-derivatives.md"
PERMISSION_RECORD_REFERENCE = "docs/permissions/asd-ste100-issue-9-derivatives.md"
PUBLICATION_NOTICE = (
    "Published machine-readable derivative. The source PDF is excluded. "
    "Mechanical extraction remains unreviewed and must be verified by page."
)
EXPECTED_SOURCE_SHA256 = "d1f4ea9e7cd6e46b47aa9057209f99e78c0e9cfc4e27a5b07895b05c1a166431"
EXPECTED_PAGES = 434
EXPECTED_DICTIONARY_ENTRIES = 2_196
MAX_RESULTS = 20
MAX_CONTEXT_WORDS = 80
MAX_EXCERPT_MATCH_WORDS = 32
SCHEMA_VERSION = "1.0.0"
STANDARD = "ASD-STE100"
ISSUE = "9"
ISSUE_DATE = "2025-01-15"

RULE_HEADING_RE = re.compile(r"^\s*Rule\s+(\d+\.\d+)\b(?:\s+(.*))?$")
GUIDANCE_HEADING_RE = re.compile(r"^\s*(GR-\d+)\b(?:\s+(.*))?$")
PRINTED_PAGE_RE = re.compile(r"\bPage\s+([12]-[0-9]+-[A-Z]?[0-9]+)\b")
POS_RE = re.compile(r"\((n|v|adj|adv|pron|art|prep|conj|prefix)\)(?=,|\s|$)")
TOKEN_RE = re.compile(r"[\w.-]+", re.UNICODE)

EXPECTED_RULE_IDS = {
    *(f"1.{number}" for number in range(1, 15)),
    *(f"2.{number}" for number in range(1, 3)),
    *(f"3.{number}" for number in range(1, 8)),
    *(f"4.{number}" for number in range(1, 6)),
    *(f"5.{number}" for number in range(1, 6)),
    *(f"6.{number}" for number in range(1, 7)),
    *(f"7.{number}" for number in range(1, 4)),
    *(f"8.{number}" for number in range(1, 8)),
    *(f"9.{number}" for number in range(1, 5)),
}
EXPECTED_GUIDANCE_IDS = {f"GR-{number}" for number in range(1, 9)}


class ReferenceError(RuntimeError):
    """A user-facing reference error."""


@dataclass(frozen=True)
class Page:
    number: int
    printed_page: str | None
    part: str
    text: str


@dataclass(frozen=True)
class VisualLine:
    column: int
    y: float
    x: float
    text: str


@dataclass
class BlockBuilder:
    block_id: str
    kind: str
    segments: list[tuple[int, str | None, list[str]]]


def private_path(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_relative_to(LOCAL_ROOT):
        raise ReferenceError(
            f"{label} must stay under the private local directory: {LOCAL_ROOT}\n"
            f"Received: {resolved}"
        )
    return resolved


def reference_path(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not (
        resolved.is_relative_to(LOCAL_ROOT)
        or resolved.is_relative_to(PUBLISHED_ROOT)
    ):
        raise ReferenceError(
            f"{label} must stay under .local/ or the published Issue 9 artifact directory\n"
            f"Received: {resolved}"
        )
    return resolved


def bounded_limit(value: str) -> int:
    try:
        limit = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("limit must be an integer") from error
    if not 1 <= limit <= MAX_RESULTS:
        raise argparse.ArgumentTypeError(f"limit must be between 1 and {MAX_RESULTS}")
    return limit


def bounded_context_words(value: str) -> int:
    try:
        context_words = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("context words must be an integer") from error
    if not 0 <= context_words <= MAX_CONTEXT_WORDS:
        raise argparse.ArgumentTypeError(
            f"context words must be between 0 and {MAX_CONTEXT_WORDS}"
        )
    return context_words


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def executable(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise ReferenceError(f"Required executable not found: {name}")
    return found


def run_text(command: Sequence[str], *, timeout: int = 180) -> str:
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip()
        raise ReferenceError(f"Command failed: {' '.join(command)}\n{detail}") from error
    except subprocess.TimeoutExpired as error:
        raise ReferenceError(f"Command timed out: {' '.join(command)}") from error
    return result.stdout


def split_pdf_pages(layout_text: str) -> list[str]:
    pages = layout_text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def printed_page(text: str) -> str | None:
    matches = PRINTED_PAGE_RE.findall(text)
    return matches[-1] if matches else None


def page_part(number: int) -> str:
    if 43 <= number <= 128:
        return "part-1"
    if 129 <= number <= 434:
        return "part-2"
    return "front-matter"


def extract_pages(source: Path) -> tuple[list[Page], str]:
    pdftotext = executable("pdftotext")
    layout = run_text(
        [pdftotext, "-layout", "-enc", "UTF-8", "-eol", "unix", str(source), "-"]
    )
    raw_pages = split_pdf_pages(layout)
    if len(raw_pages) != EXPECTED_PAGES:
        raise ReferenceError(
            f"Expected {EXPECTED_PAGES} PDF pages, extracted {len(raw_pages)}. "
            "Do not build an index from an unexpected source."
        )
    pages = [
        Page(number, printed_page(text), page_part(number), text.rstrip("\n"))
        for number, text in enumerate(raw_pages, 1)
    ]
    return pages, layout


def remove_page_furniture(text: str, *, part: str) -> list[str]:
    result: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        normalized = stripped.replace("–", "-")
        if re.fullmatch(r"ASD[- ]STE100 Simplified Technical English", normalized):
            continue
        if re.fullmatch(r"2025-01-15", stripped):
            continue
        if part == "part-1" and "Part 1 - Writing" in normalized and (
            "Issue 9" in normalized or "Page 1-" in normalized
        ):
            continue
        result.append(line.rstrip())
    while result and not result[0].strip():
        result.pop(0)
    while result and not result[-1].strip():
        result.pop()
    return result


def detail_lines(page: Page) -> list[str]:
    lines = remove_page_furniture(page.text, part=page.part)
    if not any("Summary of the rules" in line for line in lines):
        return lines

    headings: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = RULE_HEADING_RE.match(line)
        if match:
            headings.append((index, match.group(1)))
    if not headings:
        return []
    first_id = headings[0][1]
    repeated = [index for index, block_id in headings if block_id == first_id]
    return lines[repeated[1] :] if len(repeated) > 1 else []


def block_heading(line: str) -> tuple[str, str] | None:
    rule = RULE_HEADING_RE.match(line)
    if rule:
        return rule.group(1), "rule"
    guidance = GUIDANCE_HEADING_RE.match(line)
    if guidance:
        return guidance.group(1), "guidance"
    return None


def append_segment(
    builder: BlockBuilder,
    page_number: int,
    page_label: str | None,
    lines: list[str],
) -> None:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if lines:
        builder.segments.append((page_number, page_label, lines))


def extract_blocks(pages: Sequence[Page]) -> list[dict[str, object]]:
    blocks: list[BlockBuilder] = []
    current: BlockBuilder | None = None

    for page in pages[44:127]:  # Physical PDF pages 45 through 127.
        lines = detail_lines(page)
        if not lines:
            continue
        segment_lines: list[str] = []
        for line in lines:
            heading = block_heading(line)
            if heading:
                if current is not None:
                    append_segment(current, page.number, page.printed_page, segment_lines)
                    segment_lines = []
                block_id, kind = heading
                current = BlockBuilder(block_id, kind, [])
                blocks.append(current)
            if current is not None:
                segment_lines.append(line)
        if current is not None:
            append_segment(current, page.number, page.printed_page, segment_lines)

    found_rules = {block.block_id for block in blocks if block.kind == "rule"}
    found_guidance = {block.block_id for block in blocks if block.kind == "guidance"}
    duplicate_ids = [
        block_id
        for block_id in {block.block_id for block in blocks}
        if sum(block.block_id == block_id for block in blocks) != 1
    ]
    if found_rules != EXPECTED_RULE_IDS:
        raise ReferenceError(
            "Unexpected rule set. "
            f"Missing={sorted(EXPECTED_RULE_IDS - found_rules)} "
            f"extra={sorted(found_rules - EXPECTED_RULE_IDS)}"
        )
    if found_guidance != EXPECTED_GUIDANCE_IDS:
        raise ReferenceError(
            "Unexpected guidance set. "
            f"Missing={sorted(EXPECTED_GUIDANCE_IDS - found_guidance)} "
            f"extra={sorted(found_guidance - EXPECTED_GUIDANCE_IDS)}"
        )
    if duplicate_ids:
        raise ReferenceError(f"Duplicate block IDs: {sorted(duplicate_ids)}")

    records: list[dict[str, object]] = []
    for block in blocks:
        segment_records = []
        full_parts = []
        for page_number, page_label, lines in block.segments:
            text = "\n".join(lines).strip()
            if not text:
                continue
            segment_records.append(
                {"pdf_page": page_number, "printed_page": page_label, "text": text}
            )
            full_parts.append(text)
        full_text = "\n\n".join(full_parts)
        title = derive_block_title(block.block_id, full_text)
        page_numbers = [segment["pdf_page"] for segment in segment_records]
        records.append(
            {
                "id": block.block_id,
                "kind": block.kind,
                "title": title,
                "start_pdf_page": min(page_numbers),
                "end_pdf_page": max(page_numbers),
                "text": full_text,
                "segments": segment_records,
            }
        )
    return records


def derive_block_title(block_id: str, text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return block_id
    first = re.sub(
        rf"^\s*(?:Rule\s+)?{re.escape(block_id)}\s*", "", lines[0]
    ).strip()
    title_lines = [first] if first else []
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            break
        title_lines.append(stripped)
    title = re.sub(r"\s+", " ", " ".join(title_lines)).strip()
    title = re.sub(r"(?<=\w)-\s+(?=\w)", "-", title)
    return title or block_id


def tag_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def column_starts(pdf_page: int) -> tuple[float, float, float, float]:
    return (72.02, 180.02, 309.65, 439.27) if pdf_page % 2 else (
        50.40,
        158.42,
        288.05,
        417.67,
    )


def column_for_x(x: float, starts: Sequence[float]) -> int:
    # Dictionary columns nearly touch. Column 2 can hang about 5 pt left of
    # its header, so assign by the next column start with a 6 pt tolerance.
    thresholds = [starts[index + 1] - 6.0 for index in range(3)]
    if x < thresholds[0]:
        return 1
    if x < thresholds[1]:
        return 2
    if x < thresholds[2]:
        return 3
    return 4


def bbox_lines(page_element: ET.Element, pdf_page: int) -> list[VisualLine]:
    starts = column_starts(pdf_page)
    grouped: dict[tuple[int, float], list[tuple[float, str]]] = {}
    y_values: dict[tuple[int, float], list[float]] = {}

    for line in (element for element in page_element.iter() if tag_name(element) == "line"):
        words = [element for element in line if tag_name(element) == "word"]
        for word in words:
            text = html.unescape("".join(word.itertext())).strip()
            if not text:
                continue
            x = float(word.attrib["xMin"])
            y = float(word.attrib["yMin"])
            if y < 89.0 or y >= 720.0:
                continue
            column = column_for_x(x, starts)
            key = (column, round(y, 1))
            grouped.setdefault(key, []).append((x, text))
            y_values.setdefault(key, []).append(y)

    visual_lines = []
    for (column, rounded_y), words in grouped.items():
        words.sort(key=lambda item: item[0])
        visual_lines.append(
            VisualLine(
                column=column,
                y=min(y_values[(column, rounded_y)]),
                x=words[0][0],
                text=" ".join(word for _, word in words),
            )
        )
    visual_lines.sort(key=lambda line: (line.y, line.column, line.x))
    return visual_lines


def parse_bbox_xml(source: Path) -> list[ET.Element]:
    pdftotext = executable("pdftotext")
    xml_text = run_text(
        [pdftotext, "-bbox-layout", "-enc", "UTF-8", str(source), "-"],
        timeout=240,
    )
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as error:
        raise ReferenceError(f"Cannot parse pdftotext bbox XML: {error}") from error
    page_elements = [element for element in root.iter() if tag_name(element) == "page"]
    if len(page_elements) != EXPECTED_PAGES:
        raise ReferenceError(
            f"Expected {EXPECTED_PAGES} bbox pages, found {len(page_elements)}"
        )
    return page_elements


def join_column(lines: Iterable[VisualLine]) -> str:
    return "\n".join(line.text for line in sorted(lines, key=lambda item: (item.y, item.x))).strip()


def normalize_headword(value: str) -> str:
    value = value.casefold().replace("…", "...")
    return re.sub(r"\s+", " ", value).strip()


def approval_signal(headword: str) -> str:
    without_qualifiers = re.sub(r"\([^)]*\)", "", headword)
    letters = "".join(character for character in without_qualifiers if character.isalpha())
    if not letters:
        return "unknown"
    return "approved" if letters == letters.upper() else "not-approved"


def extract_dictionary_entries(
    page_elements: Sequence[ET.Element], pages: Sequence[Page]
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for pdf_page in range(149, 435):
        lines = bbox_lines(page_elements[pdf_page - 1], pdf_page)
        by_column = {
            column: [line for line in lines if line.column == column]
            for column in range(1, 5)
        }
        first_column = by_column[1]
        starts = column_starts(pdf_page)
        anchors: list[tuple[int, VisualLine, re.Match[str], bool]] = []
        for index, line in enumerate(first_column):
            match = POS_RE.search(line.text)
            if not match or line.x > starts[0] + 10.0:
                continue
            has_previous_wrap = (
                index > 0
                and 0 < line.y - first_column[index - 1].y <= 15.0
                and not POS_RE.search(first_column[index - 1].text)
            )
            wrapped = not line.text[: match.start()].strip() or has_previous_wrap
            anchors.append((index, line, match, wrapped))

        for sequence, (line_index, anchor, match, wrapped) in enumerate(anchors, 1):
            start_y = anchor.y - 5.0
            warning_values: list[str] = []
            headword_prefix = anchor.text[: match.start()].strip()
            if wrapped and line_index > 0:
                previous = first_column[line_index - 1]
                if 0 < anchor.y - previous.y <= 15.0 and not POS_RE.search(previous.text):
                    start_y = previous.y - 5.0
                    current_prefix = anchor.text[: match.start()].strip()
                    headword_prefix = " ".join(
                        part for part in (previous.text.strip(), current_prefix) if part
                    )
                    warning_values.append("wrapped-headword")
                else:
                    warning_values.append("unresolved-headword-wrap")
            next_y = anchors[sequence][1].y - 5.0 if sequence < len(anchors) else 731.0

            columns: dict[int, str] = {}
            selected_by_column: dict[int, list[VisualLine]] = {}
            for column in range(1, 5):
                selected = [
                    line
                    for line in by_column[column]
                    if start_y <= line.y < next_y
                ]
                selected_by_column[column] = selected
                columns[column] = join_column(selected)

            headword = re.sub(r"\s+", " ", headword_prefix).strip()
            if not headword:
                headword = anchor.text[: match.start()].strip() or "<unresolved>"
                warning_values.append("missing-headword")
            pos = match.group(1)
            record_id = f"D-P{pdf_page:03d}-{sequence:03d}"
            all_text = "\n".join(
                f"C{column}: {columns[column]}" for column in range(1, 5) if columns[column]
            )
            records.append(
                {
                    "id": record_id,
                    "headword": headword,
                    "normalized_headword": normalize_headword(headword),
                    "pos": pos,
                    "approval": approval_signal(headword),
                    "pdf_page": pdf_page,
                    "printed_page": pages[pdf_page - 1].printed_page,
                    "column_1": columns[1],
                    "column_2": columns[2],
                    "column_3": columns[3],
                    "column_4": columns[4],
                    "warnings": warning_values,
                    "text": all_text,
                }
            )

    if len(records) != EXPECTED_DICTIONARY_ENTRIES:
        raise ReferenceError(
            f"Expected {EXPECTED_DICTIONARY_ENTRIES} dictionary row anchors, "
            f"found {len(records)}"
        )
    return records


def create_database(
    database: Path,
    pages: Sequence[Page],
    blocks: Sequence[dict[str, object]],
    entries: Sequence[dict[str, object]],
    metadata: dict[str, str],
) -> None:
    database = private_path(database, "database")
    database.parent.mkdir(parents=True, exist_ok=True)
    temporary = database.with_suffix(database.suffix + ".tmp")
    temporary.unlink(missing_ok=True)
    connection = sqlite3.connect(temporary)
    succeeded = False
    try:
        connection.executescript(
            """
            PRAGMA journal_mode = DELETE;
            PRAGMA synchronous = FULL;
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE pages (
                pdf_page INTEGER PRIMARY KEY,
                printed_page TEXT,
                part TEXT NOT NULL,
                text TEXT NOT NULL
            );
            CREATE TABLE blocks (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                start_pdf_page INTEGER NOT NULL,
                end_pdf_page INTEGER NOT NULL,
                text TEXT NOT NULL
            );
            CREATE TABLE block_segments (
                block_id TEXT NOT NULL REFERENCES blocks(id),
                sequence INTEGER NOT NULL,
                pdf_page INTEGER NOT NULL REFERENCES pages(pdf_page),
                printed_page TEXT,
                text TEXT NOT NULL,
                PRIMARY KEY (block_id, sequence)
            );
            CREATE TABLE dictionary_entries (
                id TEXT PRIMARY KEY,
                headword TEXT NOT NULL,
                normalized_headword TEXT NOT NULL,
                pos TEXT NOT NULL,
                approval TEXT NOT NULL,
                pdf_page INTEGER NOT NULL REFERENCES pages(pdf_page),
                printed_page TEXT,
                column_1 TEXT NOT NULL,
                column_2 TEXT NOT NULL,
                column_3 TEXT NOT NULL,
                column_4 TEXT NOT NULL,
                warnings TEXT NOT NULL,
                text TEXT NOT NULL
            );
            CREATE INDEX dictionary_headword_idx
                ON dictionary_entries(normalized_headword, pos);
            CREATE INDEX dictionary_page_idx
                ON dictionary_entries(pdf_page);
            CREATE VIRTUAL TABLE pages_fts USING fts5(
                text,
                content='pages',
                content_rowid='pdf_page',
                tokenize='unicode61 remove_diacritics 2'
            );
            CREATE VIRTUAL TABLE blocks_fts USING fts5(
                id UNINDEXED,
                title,
                text,
                tokenize='unicode61 remove_diacritics 2'
            );
            CREATE VIRTUAL TABLE dictionary_fts USING fts5(
                id UNINDEXED,
                headword,
                pos,
                column_1,
                column_2,
                column_3,
                column_4,
                tokenize='unicode61 remove_diacritics 2'
            );
            """
        )
        connection.executemany(
            "INSERT INTO metadata(key, value) VALUES (?, ?)", sorted(metadata.items())
        )
        connection.executemany(
            "INSERT INTO pages(pdf_page, printed_page, part, text) VALUES (?, ?, ?, ?)",
            [(page.number, page.printed_page, page.part, page.text) for page in pages],
        )
        connection.executemany(
            "INSERT INTO pages_fts(rowid, text) VALUES (?, ?)",
            [(page.number, page.text) for page in pages],
        )
        for block in blocks:
            connection.execute(
                "INSERT INTO blocks(id, kind, title, start_pdf_page, end_pdf_page, text) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    block["id"],
                    block["kind"],
                    block["title"],
                    block["start_pdf_page"],
                    block["end_pdf_page"],
                    block["text"],
                ),
            )
            connection.execute(
                "INSERT INTO blocks_fts(id, title, text) VALUES (?, ?, ?)",
                (block["id"], block["title"], block["text"]),
            )
            segments = cast(list[dict[str, object]], block["segments"])
            for sequence, segment in enumerate(segments, 1):
                connection.execute(
                    "INSERT INTO block_segments"
                    "(block_id, sequence, pdf_page, printed_page, text) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        block["id"],
                        sequence,
                        segment["pdf_page"],
                        segment["printed_page"],
                        segment["text"],
                    ),
                )
        for entry in entries:
            connection.execute(
                "INSERT INTO dictionary_entries"
                "(id, headword, normalized_headword, pos, approval, pdf_page, "
                "printed_page, column_1, column_2, column_3, column_4, warnings, text) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry["id"],
                    entry["headword"],
                    entry["normalized_headword"],
                    entry["pos"],
                    entry["approval"],
                    entry["pdf_page"],
                    entry["printed_page"],
                    entry["column_1"],
                    entry["column_2"],
                    entry["column_3"],
                    entry["column_4"],
                    json.dumps(entry["warnings"], ensure_ascii=False),
                    entry["text"],
                ),
            )
            connection.execute(
                "INSERT INTO dictionary_fts"
                "(id, headword, pos, column_1, column_2, column_3, column_4) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    entry["id"],
                    entry["headword"],
                    entry["pos"],
                    entry["column_1"],
                    entry["column_2"],
                    entry["column_3"],
                    entry["column_4"],
                ),
            )
        connection.commit()
        result = connection.execute("PRAGMA integrity_check").fetchone()
        if not result or result[0] != "ok":
            raise ReferenceError(f"SQLite integrity check failed: {result}")
        succeeded = True
    finally:
        connection.close()
        if not succeeded:
            temporary.unlink(missing_ok=True)
    temporary.replace(database)


def poppler_version() -> str:
    pdftotext = executable("pdftotext")
    result = subprocess.run(
        [pdftotext, "-v"], capture_output=True, text=True, check=False, timeout=10
    )
    output = (result.stderr or result.stdout).splitlines()
    return output[0].strip() if output else "unknown"


def build(args: argparse.Namespace) -> int:
    source = private_path(args.source, "source")
    database = private_path(args.database, "database")
    manifest_path = private_path(args.manifest, "manifest")
    if len({source, database, manifest_path}) != 3:
        raise ReferenceError("Source, database, and manifest paths must be different")
    if not source.is_file():
        raise ReferenceError(f"Source PDF not found: {source}")
    source_hash = sha256_file(source)
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise ReferenceError(
            "Source SHA-256 does not match the reviewed Issue 9 file.\n"
            f"Expected: {EXPECTED_SOURCE_SHA256}\nActual:   {source_hash}"
        )
    if database.exists() and not args.force:
        raise ReferenceError(f"Database already exists: {database}\nUse --force to rebuild it.")

    print("Extracting physical pages...", file=sys.stderr)
    pages, _ = extract_pages(source)
    print("Segmenting Part 1 rules and recommendations...", file=sys.stderr)
    blocks = extract_blocks(pages)
    print("Extracting positioned dictionary rows...", file=sys.stderr)
    page_elements = parse_bbox_xml(source)
    entries = extract_dictionary_entries(page_elements, pages)

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "standard": STANDARD,
        "issue": ISSUE,
        "issue_date": ISSUE_DATE,
        "source_filename": source.name,
        "source_sha256": source_hash,
        "source_bytes": str(source.stat().st_size),
        "physical_pages": str(len(pages)),
        "rules": str(sum(block["kind"] == "rule" for block in blocks)),
        "guidance": str(sum(block["kind"] == "guidance" for block in blocks)),
        "dictionary_entries": str(len(entries)),
        "extractor": "tools/asd_ste100_local.py",
        "extractor_version": SCHEMA_VERSION,
        "poppler": poppler_version(),
        "review_state": "mechanically-extracted-unreviewed",
        "redistribution": "authorized-derivatives",
        "source_pdf_redistribution": "forbidden",
        "permission_basis": "written-authorization-held-offline-by-repository-owner",
    }
    print("Writing private SQLite reference...", file=sys.stderr)
    create_database(database, pages, blocks, entries, metadata)
    database_hash = sha256_file(database)
    manifest = {
        **metadata,
        "database": database.name,
        "database_sha256": database_hash,
        "usage": "python3 tools/asd_ste100_local.py overview",
        "notice": (
            "Staging build for an authorized derivative reference. The source PDF must remain "
            "private; mechanically extracted structure and column assignments can be wrong."
        ),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def publish(args: argparse.Namespace) -> int:
    source = private_path(args.source, "source")
    database = private_path(args.database, "database")
    manifest_path = private_path(args.manifest, "manifest")
    validation_args = argparse.Namespace(
        source=source,
        database=database,
        manifest=manifest_path,
    )
    if doctor(validation_args) != 0:
        raise ReferenceError("Private staging artifacts did not pass validation")
    if (DEFAULT_DATABASE.exists() or DEFAULT_MANIFEST.exists()) and not args.force:
        raise ReferenceError(
            "Published derivative artifacts already exist. Use publish --force to replace them."
        )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ReferenceError("Private manifest root is not an object")
    if not DERIVATIVE_NOTICE.is_file():
        raise ReferenceError(f"Derivative notice not found: {DERIVATIVE_NOTICE}")
    if not PERMISSION_RECORD.is_file():
        raise ReferenceError(f"Permission record not found: {PERMISSION_RECORD}")
    manifest.update(
        {
            "database": DEFAULT_DATABASE.name,
            "publication": "authorized-derivative",
            "permission_record": PERMISSION_RECORD_REFERENCE,
            "permission_record_sha256": sha256_file(PERMISSION_RECORD),
            "source_pdf_included": False,
            "notice": PUBLICATION_NOTICE,
            "notice_file": DERIVATIVE_NOTICE.name,
            "notice_sha256": sha256_file(DERIVATIVE_NOTICE),
        }
    )

    PUBLISHED_ROOT.mkdir(parents=True, exist_ok=True)
    database_temporary = DEFAULT_DATABASE.with_suffix(".sqlite3.tmp")
    manifest_temporary = DEFAULT_MANIFEST.with_suffix(".json.tmp")
    database_temporary.unlink(missing_ok=True)
    manifest_temporary.unlink(missing_ok=True)
    try:
        shutil.copyfile(database, database_temporary)
        if sha256_file(database_temporary) != manifest["database_sha256"]:
            raise ReferenceError("Published database copy failed its SHA-256 check")
        manifest_temporary.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        database_temporary.replace(DEFAULT_DATABASE)
        manifest_temporary.replace(DEFAULT_MANIFEST)
    finally:
        database_temporary.unlink(missing_ok=True)
        manifest_temporary.unlink(missing_ok=True)

    print(f"Published derivative database: {DEFAULT_DATABASE}")
    print(f"Published manifest: {DEFAULT_MANIFEST}")
    print("Source PDF not copied.")
    return 0


def open_database(path: Path) -> sqlite3.Connection:
    path = reference_path(path, "database")
    if not path.is_file():
        raise ReferenceError(
            f"Local reference not found: {path}\n"
            "Build it with: python3 tools/asd_ste100_local.py build"
        )
    connection = sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def metadata(connection: sqlite3.Connection) -> dict[str, str]:
    return dict(connection.execute("SELECT key, value FROM metadata ORDER BY key"))


def print_json(value: object, compact: bool = False) -> None:
    if compact:
        print(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def output_json(args: argparse.Namespace, value: object) -> None:
    print_json(value, compact=getattr(args, "compact_json", False))


def overview(args: argparse.Namespace) -> int:
    with closing(open_database(args.database)) as connection:
        info = metadata(connection)
        if args.json:
            output_json(args, info)
            return 0
        print(f"{info['standard']} Issue {info['issue']} ({info['issue_date']})")
        print(f"Source SHA-256: {info['source_sha256']}")
        print(
            f"Index: {info['rules']} rules; {info['guidance']} recommendations; "
            f"{info['dictionary_entries']} dictionary rows; {info['physical_pages']} pages"
        )
        print(f"State: {info['review_state']}; redistribution: {info['redistribution']}")
        print("Fast path: search -> excerpt ID QUERY -> rule ID --full only if needed")
        print("Dictionary: word TERM -> entry ID -> entry ID --full only if needed")
        print("Fallback: page PDF_PAGE; add --compact-json for minimum machine-readable output")
    return 0


def page_range(row: sqlite3.Row) -> str:
    start = row["start_pdf_page"]
    end = row["end_pdf_page"]
    return str(start) if start == end else f"{start}-{end}"


def list_rules(args: argparse.Namespace) -> int:
    with closing(open_database(args.database)) as connection:
        values: list[object] = ["rule"]
        where = "kind = ?"
        if args.section is not None:
            where += " AND id LIKE ?"
            values.append(f"{args.section}.%")
        rows = connection.execute(
            f"SELECT id, title, start_pdf_page, end_pdf_page FROM blocks "
            f"WHERE {where} ORDER BY CAST(substr(id, 1, instr(id, '.') - 1) AS INTEGER), "
            f"CAST(substr(id, instr(id, '.') + 1) AS INTEGER)",
            values,
        ).fetchall()
        if args.json:
            output_json(args, [dict(row) for row in rows])
            return 0
        for row in rows:
            print(f"{row['id']} | PDF {page_range(row)} | {row['title']}")
    return 0


def get_block(args: argparse.Namespace) -> int:
    requested = args.id.upper()
    if requested.startswith("RULE "):
        requested = requested[5:].strip()
    with closing(open_database(args.database)) as connection:
        row = connection.execute(
            "SELECT * FROM blocks WHERE upper(id) = ?", (requested,)
        ).fetchone()
        if row is None:
            raise ReferenceError(f"Block not found: {args.id}")
        segments = connection.execute(
            "SELECT sequence, pdf_page, printed_page, text FROM block_segments "
            "WHERE block_id = ? ORDER BY sequence",
            (row["id"],),
        ).fetchall()
        if args.json:
            result = dict(row)
            result.pop("text", None)
            if args.full:
                result["segments"] = [dict(segment) for segment in segments]
            output_json(args, result)
            return 0
        print(f"{STANDARD} Issue {ISSUE} | {row['kind']} {row['id']}")
        print(f"PDF {page_range(row)} | {row['title']}")
        if not args.full:
            print(f"Detail: {len(row['text'])} chars. Re-run with --full only if needed.")
            return 0
        for segment in segments:
            label = f" / {segment['printed_page']}" if segment["printed_page"] else ""
            print(f"\n--- PDF {segment['pdf_page']}{label} ---")
            print(segment["text"])
        print("\n[Mechanically extracted; verify ambiguous formatting against the cited PDF page.]")
    return 0


def dictionary_candidates(
    connection: sqlite3.Connection, term: str, pos: str | None, limit: int
) -> list[sqlite3.Row]:
    normalized = normalize_headword(term)
    parameters: list[object] = [normalized]
    where = "normalized_headword = ?"
    if pos:
        where += " AND pos = ?"
        parameters.append(pos)
    parameters.append(limit)
    rows = connection.execute(
        f"SELECT * FROM dictionary_entries WHERE {where} "
        "ORDER BY pdf_page, id LIMIT ?",
        parameters,
    ).fetchall()
    if rows:
        return rows

    tokens = TOKEN_RE.findall(term)
    if not tokens:
        return []
    phrase = '"' + " ".join(token.replace('"', '""') for token in tokens) + '"'
    parameters = [phrase]
    where = "dictionary_fts MATCH ?"
    if pos:
        where += " AND d.pos = ?"
        parameters.append(pos)
    parameters.append(limit)
    return connection.execute(
        "SELECT d.* FROM dictionary_fts f "
        "JOIN dictionary_entries d ON d.id = f.id "
        f"WHERE {where} ORDER BY rank LIMIT ?",
        parameters,
    ).fetchall()


def dictionary_item(row: sqlite3.Row, full: bool) -> dict[str, object]:
    item = dict(row)
    item["warnings"] = json.loads(item["warnings"])
    item.pop("text", None)
    if not full:
        for key in ("column_1", "column_3", "column_4"):
            item.pop(key, None)
    return item


def print_dictionary_rows(rows: Sequence[sqlite3.Row], full: bool) -> None:
    for index, row in enumerate(rows):
        if index:
            print()
        warnings = json.loads(row["warnings"])
        label = f" / {row['printed_page']}" if row["printed_page"] else ""
        print(
            f"{row['id']} | {row['headword']} ({row['pos']}) | "
            f"{row['approval']} | PDF {row['pdf_page']}{label}"
        )
        print("Meaning/alternatives:")
        print(textwrap.indent(row["column_2"] or "[empty]", "  "))
        if warnings:
            print("Warnings: " + ", ".join(warnings))
        if full:
            print("Word/forms/help:")
            print(textwrap.indent(row["column_1"] or "[empty]", "  "))
            print("STE example:")
            print(textwrap.indent(row["column_3"] or "[empty]", "  "))
            print("Non-STE example:")
            print(textwrap.indent(row["column_4"] or "[empty]", "  "))
        else:
            print("Examples omitted. Re-run with --full only if needed.")
    print("\n[Column-aware mechanical extraction; verify ambiguous rows against the cited PDF page.]")


def word(args: argparse.Namespace) -> int:
    with closing(open_database(args.database)) as connection:
        rows = dictionary_candidates(connection, args.term, args.pos, args.limit)
        if not rows:
            raise ReferenceError(
                f"No dictionary candidate found for: {args.term}\n"
                f"Try: python3 tools/asd_ste100_local.py search {json.dumps(args.term)} --scope pages"
            )
        if args.json:
            output_json(args, [dictionary_item(row, args.full) for row in rows])
            return 0
        print_dictionary_rows(rows, args.full)
    return 0


def entry(args: argparse.Namespace) -> int:
    with closing(open_database(args.database)) as connection:
        row = connection.execute(
            "SELECT * FROM dictionary_entries WHERE upper(id) = upper(?)", (args.id,)
        ).fetchone()
        if row is None:
            raise ReferenceError(f"Dictionary entry not found: {args.id}")
        if args.json:
            output_json(args, dictionary_item(row, args.full))
            return 0
        print_dictionary_rows([row], args.full)
    return 0


def excerpt_window(text: str, query: str, context_words: int) -> str | None:
    compact = re.sub(r"\s+", " ", text).strip()
    words = list(TOKEN_RE.finditer(compact))
    required = {token.casefold() for token in TOKEN_RE.findall(query)}
    if not words or not required:
        return None

    counts: dict[str, int] = {}
    left = 0
    best: tuple[int, int] | None = None
    for right, match in enumerate(words):
        token = match.group(0).casefold()
        if token in required:
            counts[token] = counts.get(token, 0) + 1
        while len(counts) == len(required):
            if best is None or right - left < best[1] - best[0]:
                best = (left, right)
            left_token = words[left].group(0).casefold()
            if left_token in required:
                counts[left_token] -= 1
                if counts[left_token] == 0:
                    del counts[left_token]
            left += 1
    if best is None or best[1] - best[0] + 1 > MAX_EXCERPT_MATCH_WORDS:
        return None

    start_word = max(0, best[0] - context_words)
    end_word = min(len(words) - 1, best[1] + context_words)
    excerpt = compact[words[start_word].start() : words[end_word].end()]
    if start_word:
        excerpt = "… " + excerpt
    if end_word < len(words) - 1:
        excerpt += " …"
    return excerpt


def excerpts(args: argparse.Namespace) -> int:
    requested = args.id.upper()
    if requested.startswith("RULE "):
        requested = requested[5:].strip()
    with closing(open_database(args.database)) as connection:
        block = connection.execute(
            "SELECT id, kind, title FROM blocks WHERE upper(id) = ?", (requested,)
        ).fetchone()
        if block is None:
            raise ReferenceError(f"Block not found: {args.id}")
        segments = connection.execute(
            "SELECT sequence, pdf_page, printed_page, text FROM block_segments "
            "WHERE block_id = ? ORDER BY sequence",
            (block["id"],),
        ).fetchall()
        matches = []
        for segment in segments:
            text = excerpt_window(segment["text"], args.query, args.context_words)
            if text is not None:
                matches.append(
                    {
                        "pdf_page": segment["pdf_page"],
                        "printed_page": segment["printed_page"],
                        "text": text,
                    }
                )
            if len(matches) == args.limit:
                break
        if not matches:
            raise ReferenceError(
                f"No excerpt in block {block['id']} for: {args.query}\n"
                f"Try: python3 tools/asd_ste100_local.py search {json.dumps(args.query)} --scope blocks"
            )
        result = {**dict(block), "query": args.query, "excerpts": matches}
        if args.json:
            output_json(args, result)
            return 0
        print(f"{STANDARD} Issue {ISSUE} | {block['kind']} {block['id']} | {block['title']}")
        for item in matches:
            label = f" / {item['printed_page']}" if item["printed_page"] else ""
            print(f"PDF {item['pdf_page']}{label} | {item['text']}")
        print("\n[Bounded mechanical excerpts; use --full only if the surrounding rule is required.]")
    return 0


def fts_query(value: str) -> str:
    tokens = TOKEN_RE.findall(value)
    if not tokens:
        raise ReferenceError("Search query has no indexable tokens")
    return " AND ".join('"' + token.replace('"', '""') + '"' for token in tokens)


def search(args: argparse.Namespace) -> int:
    query = fts_query(args.query)
    output: list[dict[str, object]] = []
    with closing(open_database(args.database)) as connection:
        if args.scope in ("all", "blocks", "rules"):
            remaining = args.limit - len(output)
            rows = connection.execute(
                "SELECT b.id, b.kind, b.title, b.start_pdf_page, b.end_pdf_page, "
                "snippet(blocks_fts, 2, '[', ']', ' … ', 16) AS snippet "
                "FROM blocks_fts JOIN blocks b ON b.id = blocks_fts.id "
                "WHERE blocks_fts MATCH ? ORDER BY rank, b.id LIMIT ?",
                (query, remaining),
            ).fetchall()
            output.extend({"scope": "block", **dict(row)} for row in rows)
        if args.scope in ("all", "dictionary") and len(output) < args.limit:
            remaining = args.limit - len(output)
            rows = connection.execute(
                "SELECT d.id, d.headword, d.pos, d.approval, d.pdf_page, d.printed_page, "
                "snippet(dictionary_fts, 4, '[', ']', ' … ', 14) AS snippet "
                "FROM dictionary_fts JOIN dictionary_entries d ON d.id = dictionary_fts.id "
                "WHERE dictionary_fts MATCH ? ORDER BY rank, d.id LIMIT ?",
                (query, remaining),
            ).fetchall()
            output.extend({"scope": "dictionary", **dict(row)} for row in rows)
        if args.scope in ("all", "pages") and len(output) < args.limit:
            remaining = args.limit - len(output)
            rows = connection.execute(
                "SELECT p.pdf_page, p.printed_page, p.part, "
                "snippet(pages_fts, 0, '[', ']', ' … ', 18) AS snippet "
                "FROM pages_fts JOIN pages p ON p.pdf_page = pages_fts.rowid "
                "WHERE pages_fts MATCH ? ORDER BY rank, p.pdf_page LIMIT ?",
                (query, remaining),
            ).fetchall()
            output.extend({"scope": "page", **dict(row)} for row in rows)
    if args.json:
        output_json(args, output)
        return 0
    if not output:
        print("No matches.")
        return 1
    for item in output:
        if item["scope"] == "block":
            page_text = (
                str(item["start_pdf_page"])
                if item["start_pdf_page"] == item["end_pdf_page"]
                else f"{item['start_pdf_page']}-{item['end_pdf_page']}"
            )
            print(f"BLOCK {item['id']} | PDF {page_text} | {item['title']}")
        elif item["scope"] == "dictionary":
            print(
                f"WORD {item['id']} | {item['headword']} ({item['pos']}) | "
                f"{item['approval']} | PDF {item['pdf_page']}"
            )
        else:
            label = f" / {item['printed_page']}" if item["printed_page"] else ""
            print(f"PAGE PDF {item['pdf_page']}{label} | {item['part']}")
        print("  " + re.sub(r"\s+", " ", str(item["snippet"])).strip())
    return 0


def show_page(args: argparse.Namespace) -> int:
    with closing(open_database(args.database)) as connection:
        row = connection.execute(
            "SELECT * FROM pages WHERE pdf_page = ?", (args.pdf_page,)
        ).fetchone()
        if row is None:
            raise ReferenceError(f"PDF page out of range: {args.pdf_page}")
        if args.json:
            output_json(args, dict(row))
            return 0
        label = f" / {row['printed_page']}" if row["printed_page"] else ""
        print(f"{STANDARD} Issue {ISSUE} | PDF {row['pdf_page']}{label} | {row['part']}")
        print(row["text"])
        print("\n[Raw layout extraction; the authoritative source is the PDF.]")
    return 0


def doctor(args: argparse.Namespace) -> int:
    source = private_path(args.source, "source")
    database = reference_path(args.database, "database")
    manifest_path = reference_path(args.manifest, "manifest")
    failures: list[str] = []
    source_hash: str | None = None
    manifest_data: dict[str, object] = {}

    if source.is_file():
        source_hash = sha256_file(source)
        if source_hash != EXPECTED_SOURCE_SHA256:
            failures.append(f"source SHA-256 mismatch: {source_hash}")
        try:
            executable("pdftotext")
            executable("pdfinfo")
        except ReferenceError as error:
            failures.append(str(error))

    if not manifest_path.is_file():
        failures.append(f"manifest missing: {manifest_path}")
    else:
        try:
            parsed = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(parsed, dict):
                failures.append("manifest root is not an object")
            else:
                manifest_data = parsed
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"manifest error: {error}")

    database_is_published = database.is_relative_to(PUBLISHED_ROOT)
    manifest_is_published = manifest_path.is_relative_to(PUBLISHED_ROOT)
    if database_is_published != manifest_is_published:
        failures.append("database and manifest must both be staging or both be published")
    if database_is_published and manifest_is_published:
        expected_publication = {
            "publication": "authorized-derivative",
            "permission_record": PERMISSION_RECORD_REFERENCE,
            "source_pdf_included": False,
            "notice": PUBLICATION_NOTICE,
            "notice_file": DERIVATIVE_NOTICE.name,
        }
        for key, value in expected_publication.items():
            if manifest_data.get(key) != value:
                failures.append(
                    f"published manifest {key}: expected {value}, "
                    f"got {manifest_data.get(key)}"
                )
        if not DERIVATIVE_NOTICE.is_file():
            failures.append(f"derivative notice missing: {DERIVATIVE_NOTICE}")
        elif manifest_data.get("notice_sha256") != sha256_file(DERIVATIVE_NOTICE):
            failures.append("derivative notice SHA-256 does not match the manifest")
        if not PERMISSION_RECORD.is_file():
            failures.append(f"permission record missing: {PERMISSION_RECORD}")
        elif manifest_data.get("permission_record_sha256") != sha256_file(PERMISSION_RECORD):
            failures.append("permission record SHA-256 does not match the manifest")

    if not database.is_file():
        failures.append(f"database missing: {database}")
    else:
        database_hash = sha256_file(database)
        if manifest_data.get("database_sha256") != database_hash:
            failures.append("database SHA-256 does not match the manifest")
        if manifest_data.get("database") != database.name:
            failures.append("manifest database filename does not match the selected database")
        try:
            with closing(open_database(database)) as connection:
                integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
                if integrity != "ok":
                    failures.append(f"database integrity: {integrity}")
                foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
                if foreign_key_errors:
                    failures.append(f"foreign-key errors: {len(foreign_key_errors)}")

                info = metadata(connection)
                expected_metadata = {
                    "schema_version": SCHEMA_VERSION,
                    "standard": STANDARD,
                    "issue": ISSUE,
                    "issue_date": ISSUE_DATE,
                    "source_sha256": EXPECTED_SOURCE_SHA256,
                    "physical_pages": str(EXPECTED_PAGES),
                    "rules": str(len(EXPECTED_RULE_IDS)),
                    "guidance": str(len(EXPECTED_GUIDANCE_IDS)),
                    "dictionary_entries": str(EXPECTED_DICTIONARY_ENTRIES),
                    "review_state": "mechanically-extracted-unreviewed",
                    "redistribution": "authorized-derivatives",
                    "source_pdf_redistribution": "forbidden",
                    "permission_basis": "written-authorization-held-offline-by-repository-owner",
                }
                for key, value in expected_metadata.items():
                    if info.get(key) != value:
                        failures.append(
                            f"metadata {key}: expected {value}, got {info.get(key)}"
                        )
                    if manifest_data.get(key) != value:
                        failures.append(
                            f"manifest {key}: expected {value}, got {manifest_data.get(key)}"
                        )
                for key, value in info.items():
                    if manifest_data.get(key) != value:
                        failures.append(
                            f"manifest metadata {key} does not match the database"
                        )
                if source_hash is not None and manifest_data.get("source_sha256") != source_hash:
                    failures.append("manifest source SHA-256 does not match the source PDF")

                actual_counts = {
                    "pages": connection.execute("SELECT count(*) FROM pages").fetchone()[0],
                    "rules": connection.execute(
                        "SELECT count(*) FROM blocks WHERE kind = 'rule'"
                    ).fetchone()[0],
                    "guidance": connection.execute(
                        "SELECT count(*) FROM blocks WHERE kind = 'guidance'"
                    ).fetchone()[0],
                    "dictionary": connection.execute(
                        "SELECT count(*) FROM dictionary_entries"
                    ).fetchone()[0],
                    "pages_fts": connection.execute(
                        "SELECT count(*) FROM pages_fts"
                    ).fetchone()[0],
                    "blocks_fts": connection.execute(
                        "SELECT count(*) FROM blocks_fts"
                    ).fetchone()[0],
                    "dictionary_fts": connection.execute(
                        "SELECT count(*) FROM dictionary_fts"
                    ).fetchone()[0],
                }
                expected_counts = {
                    "pages": EXPECTED_PAGES,
                    "rules": len(EXPECTED_RULE_IDS),
                    "guidance": len(EXPECTED_GUIDANCE_IDS),
                    "dictionary": EXPECTED_DICTIONARY_ENTRIES,
                    "pages_fts": EXPECTED_PAGES,
                    "blocks_fts": len(EXPECTED_RULE_IDS) + len(EXPECTED_GUIDANCE_IDS),
                    "dictionary_fts": EXPECTED_DICTIONARY_ENTRIES,
                }
                for key, value in expected_counts.items():
                    if actual_counts[key] != value:
                        failures.append(
                            f"table count {key}: expected {value}, got {actual_counts[key]}"
                        )

                actual_rules = {
                    row[0]
                    for row in connection.execute(
                        "SELECT id FROM blocks WHERE kind = 'rule'"
                    )
                }
                actual_guidance = {
                    row[0]
                    for row in connection.execute(
                        "SELECT id FROM blocks WHERE kind = 'guidance'"
                    )
                }
                if actual_rules != EXPECTED_RULE_IDS:
                    failures.append("rule ID set does not match Issue 9")
                if actual_guidance != EXPECTED_GUIDANCE_IDS:
                    failures.append("guidance ID set does not match Issue 9")
        except (sqlite3.Error, ReferenceError) as error:
            failures.append(f"database error: {error}")

    if failures:
        print("FAIL")
        for failure in failures:
            print("- " + failure)
        return 1
    print("PASS")
    if source_hash is None:
        print(f"- source PDF: not present (expected SHA-256: {EXPECTED_SOURCE_SHA256})")
    else:
        print(f"- source: {source}")
    print(f"- database: {database}")
    print(f"- manifest: {manifest_path}")
    print(f"- source SHA-256: {EXPECTED_SOURCE_SHA256}")
    print(
        f"- rules: {len(EXPECTED_RULE_IDS)}; guidance: {len(EXPECTED_GUIDANCE_IDS)}; "
        f"dictionary rows: {EXPECTED_DICTIONARY_ENTRIES}"
    )
    print("- derivative index and manifest are authenticated; source PDF is not published")
    return 0


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    common.add_argument("--json", action="store_true", help="emit readable JSON")
    common.add_argument(
        "--compact-json",
        action="store_true",
        help="emit deterministic minified JSON for agent context",
    )

    root = argparse.ArgumentParser(
        description="Build, publish, and query an ASD-STE100 Issue 9 derivative reference."
    )
    commands = root.add_subparsers(dest="command", required=True)

    build_parser = commands.add_parser("build", help="build the private local index")
    build_parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    build_parser.add_argument("--database", type=Path, default=PRIVATE_DATABASE)
    build_parser.add_argument("--manifest", type=Path, default=PRIVATE_MANIFEST)
    build_parser.add_argument("--force", action="store_true")
    build_parser.set_defaults(function=build)

    publish_parser = commands.add_parser(
        "publish", help="copy authenticated derivative artifacts into the versioned snapshot"
    )
    publish_parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    publish_parser.add_argument("--database", type=Path, default=PRIVATE_DATABASE)
    publish_parser.add_argument("--manifest", type=Path, default=PRIVATE_MANIFEST)
    publish_parser.add_argument("--force", action="store_true")
    publish_parser.set_defaults(function=publish)

    overview_parser = commands.add_parser("overview", parents=[common], help="show a short index overview")
    overview_parser.set_defaults(function=overview)

    rules_parser = commands.add_parser("rules", parents=[common], help="list compact rule headings")
    rules_parser.add_argument("--section", type=int, choices=range(1, 10))
    rules_parser.set_defaults(function=list_rules)

    rule_parser = commands.add_parser("rule", parents=[common], help="get a rule or GR recommendation")
    rule_parser.add_argument("id")
    rule_parser.add_argument("--full", action="store_true")
    rule_parser.set_defaults(function=get_block)

    word_parser = commands.add_parser("word", parents=[common], help="look up dictionary candidates")
    word_parser.add_argument("term")
    word_parser.add_argument(
        "--pos", choices=("n", "v", "adj", "adv", "pron", "art", "prep", "conj", "prefix")
    )
    word_parser.add_argument("--limit", type=bounded_limit, default=8)
    word_parser.add_argument("--full", action="store_true")
    word_parser.set_defaults(function=word)

    entry_parser = commands.add_parser(
        "entry", parents=[common], help="get one dictionary row by stable ID"
    )
    entry_parser.add_argument("id")
    entry_parser.add_argument("--full", action="store_true")
    entry_parser.set_defaults(function=entry)

    excerpt_parser = commands.add_parser(
        "excerpt", parents=[common], help="get bounded cited excerpts from one rule or GR"
    )
    excerpt_parser.add_argument("id")
    excerpt_parser.add_argument("query")
    excerpt_parser.add_argument("--limit", type=bounded_limit, default=3)
    excerpt_parser.add_argument(
        "--context-words",
        type=bounded_context_words,
        default=24,
        help="words retained on each side of the smallest match window (0-80)",
    )
    excerpt_parser.set_defaults(function=excerpts)

    search_parser = commands.add_parser("search", parents=[common], help="search compact snippets")
    search_parser.add_argument("query")
    search_parser.add_argument(
        "--scope",
        choices=("all", "blocks", "rules", "dictionary", "pages"),
        default="all",
        help="all uses ordered fallback: blocks, dictionary, then pages; rules aliases blocks",
    )
    search_parser.add_argument("--limit", type=bounded_limit, default=8)
    search_parser.set_defaults(function=search)

    page_parser = commands.add_parser("page", parents=[common], help="show one raw extracted PDF page")
    page_parser.add_argument("pdf_page", type=int)
    page_parser.set_defaults(function=show_page)

    doctor_parser = commands.add_parser(
        "doctor", help="authenticate the derivative index and optional local source"
    )
    doctor_parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    doctor_parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    doctor_parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    doctor_parser.set_defaults(function=doctor)
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if getattr(args, "compact_json", False):
        args.json = True
    try:
        return args.function(args)
    except (ReferenceError, sqlite3.Error, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
