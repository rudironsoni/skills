SHELL := /bin/sh

REPO_ROOT := $(CURDIR)
SKILLS_DIR := $(REPO_ROOT)/skills
GLOBAL_CLAUDE_SKILLS := $(HOME)/.claude/skills
GLOBAL_CODEX_SKILLS := $(HOME)/.codex/skills
GLOBAL_OPENCODE_SKILLS := $(HOME)/.config/opencode/skills
GLOBAL_AGENTS_SKILLS := $(HOME)/.agents/skills

.PHONY: help validate validate-json validate-skills validate-claude list link unlink

help:
	@printf '%s\n' \
		'make validate  Validate manifests, versions, grouped skills, and plugin coverage.' \
		'make list      List canonical skills by capability.' \
		'make link      Link canonical skills into global harness skill folders.' \
		'make unlink    Remove links created by this repository.'

validate: validate-json validate-skills validate-claude

validate-json:
	@python3 -m json.tool .claude-plugin/plugin.json >/dev/null
	@python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
	@python3 -m json.tool .changeset/config.json >/dev/null
	@python3 -m json.tool package.json >/dev/null
	@python3 -m json.tool package-lock.json >/dev/null
	@printf '%s\n' 'JSON manifests are valid.'

validate-skills:
	@python3 tools/validate_skills.py

validate-claude:
	@if command -v claude >/dev/null 2>&1; then \
		claude plugin validate . --strict; \
	else \
		printf '%s\n' 'Claude CLI not found. Skipped native plugin validation.'; \
	fi

list:
	@find "$(SKILLS_DIR)" -mindepth 3 -maxdepth 3 -name SKILL.md -type f -print | \
		sort | while IFS= read -r skill_md; do \
			skill=$$(dirname "$$skill_md"); \
			capability=$$(basename "$$(dirname "$$skill")"); \
			name=$$(basename "$$skill"); \
			printf '%s/%s\n' "$$capability" "$$name"; \
		done

link:
	@mkdir -p "$(GLOBAL_CLAUDE_SKILLS)" "$(GLOBAL_CODEX_SKILLS)" "$(GLOBAL_OPENCODE_SKILLS)" "$(GLOBAL_AGENTS_SKILLS)"
	@find "$(SKILLS_DIR)" -mindepth 3 -maxdepth 3 -name SKILL.md -type f -print | \
		sort | while IFS= read -r skill_md; do \
			skill=$$(dirname "$$skill_md"); \
			name=$$(basename "$$skill"); \
			for target in "$(GLOBAL_CLAUDE_SKILLS)" "$(GLOBAL_CODEX_SKILLS)" "$(GLOBAL_OPENCODE_SKILLS)" "$(GLOBAL_AGENTS_SKILLS)"; do \
				link="$$target/$$name"; \
				if [ -e "$$link" ] && [ ! -L "$$link" ]; then \
					printf '%s\n' "error: $$link exists and is not a symlink" >&2; \
					exit 1; \
				fi; \
				ln -sfn "$$skill" "$$link"; \
			done; \
		done
	@printf '%s\n' 'Linked canonical skills into global skill folders.'

unlink:
	@find "$(SKILLS_DIR)" -mindepth 3 -maxdepth 3 -name SKILL.md -type f -print | \
		sort | while IFS= read -r skill_md; do \
			skill=$$(dirname "$$skill_md"); \
			name=$$(basename "$$skill"); \
			for target in "$(GLOBAL_CLAUDE_SKILLS)" "$(GLOBAL_CODEX_SKILLS)" "$(GLOBAL_OPENCODE_SKILLS)" "$(GLOBAL_AGENTS_SKILLS)"; do \
				link="$$target/$$name"; \
				if [ -L "$$link" ] && [ "$$(readlink "$$link")" = "$$skill" ]; then \
					rm "$$link"; \
				fi; \
			done; \
		done
	@printf '%s\n' 'Removed symlinks created by this repository.'
