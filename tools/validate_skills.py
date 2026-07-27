#!/usr/bin/env python3

import hashlib
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"
PLUGIN_PATH = REPO_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PACKAGE_PATH = REPO_ROOT / "package.json"
PACKAGE_LOCK_PATH = REPO_ROOT / "package-lock.json"
README_PATH = REPO_ROOT / "README.md"
CHANGESETS_CONFIG_PATH = REPO_ROOT / ".changeset" / "config.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
ALLOWED_RESOURCE_DIRS = {"agents", "assets", "references", "scripts"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}

    end = text.find("\n---", 4)
    if end == -1:
        return {}

    values: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []

    def flush_block() -> None:
        nonlocal current_key, block_lines
        if current_key is not None:
            values[current_key] = "\n".join(line.strip() for line in block_lines).strip()
        current_key = None
        block_lines = []

    for line in text[4:end].splitlines():
        if current_key is not None and (line.startswith((" ", "\t")) or not line.strip()):
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
        else:
            values[key] = value.strip("'\"")

    flush_block()
    return values


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
        return {}

    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
        return {}
    return value


def validate_relative_links(root: Path, errors: list[str]) -> None:
    for markdown_path in sorted(root.rglob("*.md")):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("#", "/", "http://", "https://", "mailto:")):
                continue
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"{markdown_path.relative_to(REPO_ROOT)} has broken link {raw_target!r}"
                )


def main() -> int:
    errors: list[str] = []
    plugin = load_json(PLUGIN_PATH, errors)
    marketplace = load_json(MARKETPLACE_PATH, errors)
    package = load_json(PACKAGE_PATH, errors)
    package_lock = load_json(PACKAGE_LOCK_PATH, errors)
    changesets_config = load_json(CHANGESETS_CONFIG_PATH, errors)
    top_readme = README_PATH.read_text(encoding="utf-8")

    package_version = package.get("version")
    plugin_version = plugin.get("version")
    package_lock_version = package_lock.get("version")
    lock_packages = package_lock.get("packages", {})
    lock_root = lock_packages.get("") if isinstance(lock_packages, dict) else None
    package_lock_root_version = lock_root.get("version") if isinstance(lock_root, dict) else None
    release_versions = {
        "package.json": package_version,
        ".claude-plugin/plugin.json": plugin_version,
        "package-lock.json": package_lock_version,
        'package-lock.json packages[""]': package_lock_root_version,
    }
    for source, version in release_versions.items():
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            errors.append(f"{source} version must use strict semantic versioning")
    if any(version != package_version for version in release_versions.values()):
        errors.append("package, lockfile, and Claude plugin versions must match")

    expected_changelog = [
        "@changesets/changelog-github",
        {"repo": "rudironsoni/skills"},
    ]
    if changesets_config.get("changelog") != expected_changelog:
        errors.append("Changesets must generate changelogs for rudironsoni/skills")
    if changesets_config.get("baseBranch") != "main":
        errors.append("Changesets base branch must be main")
    if changesets_config.get("privatePackages") != {"version": True, "tag": True}:
        errors.append("Changesets must version and tag the private package")

    plugin_name = plugin.get("name")
    marketplace_plugins = marketplace.get("plugins", [])
    if not isinstance(marketplace_plugins, list) or len(marketplace_plugins) != 1:
        errors.append(".claude-plugin/marketplace.json must expose exactly one plugin")
    elif marketplace_plugins[0].get("name") != plugin_name or marketplace_plugins[0].get("source") != "./":
        errors.append("marketplace plugin must reference the repo-wide Claude plugin")

    expected_plugin_paths: set[str] = set()
    seen_names: dict[str, Path] = {}
    shared_prompt_refs: list[Path] = []

    if not SKILLS_ROOT.is_dir():
        errors.append("skills/ directory is missing")
    else:
        for capability in sorted(SKILLS_ROOT.iterdir()):
            if capability.name.startswith("."):
                continue
            if not capability.is_dir():
                errors.append(f"{capability.relative_to(REPO_ROOT)} must be a capability directory")
                continue
            if not NAME_RE.fullmatch(capability.name):
                errors.append(f"{capability.relative_to(REPO_ROOT)} must use lowercase hyphen-case")

            capability_readme_path = capability / "README.md"
            if not capability_readme_path.is_file():
                errors.append(f"{capability.relative_to(REPO_ROOT)} is missing README.md")
                capability_readme = ""
            else:
                capability_readme = capability_readme_path.read_text(encoding="utf-8")

            for entry in sorted(capability.iterdir()):
                if entry.name == "README.md" or entry.name.startswith("."):
                    continue
                if not entry.is_dir():
                    errors.append(f"{entry.relative_to(REPO_ROOT)} must be a skill directory")
                    continue
                if not NAME_RE.fullmatch(entry.name):
                    errors.append(f"{entry.relative_to(REPO_ROOT)} must use lowercase hyphen-case")

                previous = seen_names.get(entry.name)
                if previous is not None:
                    errors.append(
                        f"duplicate skill name {entry.name!r}: "
                        f"{previous.relative_to(REPO_ROOT)} and {entry.relative_to(REPO_ROOT)}"
                    )
                seen_names[entry.name] = entry

                skill_md = entry / "SKILL.md"
                if not skill_md.is_file():
                    errors.append(f"{entry.relative_to(REPO_ROOT)} is missing SKILL.md")
                    continue

                frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                if frontmatter.get("name") != entry.name:
                    errors.append(f"{skill_md.relative_to(REPO_ROOT)} name must be {entry.name!r}")
                if not frontmatter.get("description", "").strip():
                    errors.append(f"{skill_md.relative_to(REPO_ROOT)} needs a non-empty description")

                for child in entry.iterdir():
                    if child.name == "SKILL.md" or child.name.startswith("."):
                        continue
                    if not child.is_dir() or child.name not in ALLOWED_RESOURCE_DIRS:
                        errors.append(
                            f"{child.relative_to(REPO_ROOT)} is not an allowed skill resource directory"
                        )

                relative_skill = skill_md.relative_to(REPO_ROOT).as_posix()
                plugin_path = f"./{skill_md.parent.relative_to(REPO_ROOT).as_posix()}"
                expected_plugin_paths.add(plugin_path)
                if f"({entry.name}/SKILL.md)" not in capability_readme:
                    errors.append(f"{capability_readme_path.relative_to(REPO_ROOT)} must link {entry.name}")
                if f"(./{relative_skill})" not in top_readme:
                    errors.append(f"README.md must link {relative_skill}")

                shared_ref = entry / "references" / "claude-prompting-best-practices.md"
                if shared_ref.is_file():
                    shared_prompt_refs.append(shared_ref)

    declared_plugin_paths = plugin.get("skills")
    if not isinstance(declared_plugin_paths, list) or not all(
        isinstance(path, str) for path in declared_plugin_paths
    ):
        errors.append(".claude-plugin/plugin.json skills must be an array of paths")
    elif set(declared_plugin_paths) != expected_plugin_paths or len(declared_plugin_paths) != len(
        expected_plugin_paths
    ):
        errors.append("Claude plugin skills must list every canonical skill exactly once")

    prompt_hashes = {
        hashlib.md5(path.read_bytes()).hexdigest()  # noqa: S324 - equality check, not security
        for path in shared_prompt_refs
    }
    if len(shared_prompt_refs) != 3 or len(prompt_hashes) != 1:
        errors.append("the three shared Claude prompting references must be byte-identical")

    validate_relative_links(SKILLS_ROOT, errors)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(seen_names)} skills across "
        f"{len({path.parent for path in seen_names.values()})} capabilities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
