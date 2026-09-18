#!/usr/bin/env python3
"""Extract one version's section from CHANGELOG.md for use as a GitHub Release note."""

import pathlib
import re
import sys

CHANGELOG = "CHANGELOG.md"
# Releases are separated by a horizontal rule sitting just above the next heading.
# It is CHANGELOG layout, not release-note content, so it is trimmed off.
HORIZONTAL_RULE = re.compile(r"^-{3,}\s*$")


def extract(changelog: str, version: str) -> str:
    """Return the body of the `# <version>` H1 section, exclusive of its heading.

    Release headings are H1, the same level as the document title, so the heading
    is matched exactly rather than by prefix. Collection stops at the next H1,
    which means a version listed more than once yields its first (topmost) entry.
    """
    body: list[str] = []
    collecting = False
    for line in changelog.splitlines():
        stripped = line.rstrip()
        if collecting:
            if stripped.startswith("# "):  # next release heading -> done
                break
            body.append(line)
        elif stripped == f"# {version}":
            collecting = True
    if not collecting:
        raise SystemExit(f"::error::CHANGELOG.md has no '# {version}' section")
    while body and (not body[-1].strip() or HORIZONTAL_RULE.match(body[-1])):
        body.pop()
    text = "\n".join(body).strip("\n")
    if not text:
        raise SystemExit(f"::error::CHANGELOG.md section '# {version}' is empty")
    return text


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {sys.argv[0]} <version> <output-file>")
    version, out_path = sys.argv[1], sys.argv[2]
    notes = extract(pathlib.Path(CHANGELOG).read_text(encoding="utf-8"), version)
    pathlib.Path(out_path).write_text(notes + "\n", encoding="utf-8")
    print(
        f"Extracted {len(notes.splitlines())} lines of release notes for {version}:\n"
    )
    print(notes)


if __name__ == "__main__":
    main()
