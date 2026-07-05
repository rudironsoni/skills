#!/usr/bin/env python3
from pathlib import Path
import re
import sys

SKILLS_ROOT = Path("skills")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    errors: list[str] = []

    if not SKILLS_ROOT.is_dir():
        errors.append("skills/ directory is missing")
    else:
        validate_skill_tree(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Skill folders are valid.")
    return 0


def validate_skill_tree(errors: list[str]) -> None:
    for skill in sorted(SKILLS_ROOT.iterdir()):
        if skill.name.startswith("."):
            continue
        if not skill.is_dir():
            errors.append(f"{skill} must be a directory")
            continue
        validate_skill(skill, errors)


def validate_skill(skill: Path, errors: list[str]) -> None:
    if not NAME_RE.fullmatch(skill.name):
        errors.append(f"{skill} must use lowercase hyphen-case")

    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill} is missing SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{skill_md} must start with YAML frontmatter")
        return

    frontmatter_end = text.find("\n---", 4)
    if frontmatter_end == -1:
        errors.append(f"{skill_md} frontmatter is not closed")
        return

    frontmatter = parse_frontmatter(text[4:frontmatter_end])

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name != skill.name:
        errors.append(f"{skill_md} frontmatter name must be {skill.name!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_md} frontmatter description must be non-empty")


def parse_frontmatter(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []

    def flush_block() -> None:
        nonlocal current_key, block_lines
        if current_key is not None:
            values[current_key] = "\n".join(line.strip() for line in block_lines).strip()
        current_key = None
        block_lines = []

    for line in text.splitlines():
        if current_key is not None:
            if line.startswith((" ", "\t")) or not line.strip():
                block_lines.append(line)
                continue
            flush_block()

        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value in {">", ">-", "|", "|-"}:
            current_key = key
            block_lines = []
        else:
            values[key] = value.strip("'\"")

    flush_block()
    return values


if __name__ == "__main__":
    raise SystemExit(main())
