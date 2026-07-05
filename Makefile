SHELL := /bin/sh
REPO_ROOT := $(CURDIR)
SKILLS_DIR := $(REPO_ROOT)/skills
CODEX_PLUGIN_VALIDATOR ?= $(HOME)/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py

GLOBAL_CLAUDE_SKILLS := $(HOME)/.claude/skills
GLOBAL_CODEX_SKILLS := $(HOME)/.codex/skills
GLOBAL_OPENCODE_SKILLS := $(HOME)/.config/opencode/skills
GLOBAL_AGENTS_SKILLS := $(HOME)/.agents/skills

.PHONY: help validate validate-json validate-skills validate-codex validate-opencode link unlink

help:
	@printf '%s\n' 'Targets:'
	@printf '%s\n' '  make validate           Run all repository checks'
	@printf '%s\n' '  make validate-json      Validate JSON manifests'
	@printf '%s\n' '  make validate-skills    Validate skill folder names and frontmatter'
	@printf '%s\n' '  make validate-codex     Validate Codex plugin metadata'
	@printf '%s\n' '  make validate-opencode  Validate OpenCode plugin scaffold'
	@printf '%s\n' '  make link               Link canonical skills into local global skill folders'
	@printf '%s\n' '  make unlink             Remove symlinks created by make link'

validate: validate-json validate-skills validate-codex validate-opencode

validate-json:
	@python3 -m json.tool .claude-plugin/plugin.json >/dev/null
	@python3 -m json.tool .codex-plugin/plugin.json >/dev/null
	@printf '%s\n' 'JSON manifests are valid.'

validate-skills:
	@python3 tools/validate_skills.py

validate-codex:
	@if [ -f "$(CODEX_PLUGIN_VALIDATOR)" ]; then \
		if python3 -c 'import yaml' >/dev/null 2>&1; then \
			python3 "$(CODEX_PLUGIN_VALIDATOR)" "$(REPO_ROOT)"; \
		else \
			printf '%s\n' 'Codex plugin validator needs PyYAML. Checked JSON only.'; \
		fi; \
	else \
		printf '%s\n' 'Codex plugin validator not found. Checked JSON only.'; \
	fi

validate-opencode:
	@test -f .opencode/plugins/rudironsoni-skills.ts
	@grep -q 'export const RudiSkillsPlugin' .opencode/plugins/rudironsoni-skills.ts
	@printf '%s\n' 'OpenCode plugin scaffold is present.'

link:
	@mkdir -p "$(GLOBAL_CLAUDE_SKILLS)" "$(GLOBAL_CODEX_SKILLS)" "$(GLOBAL_OPENCODE_SKILLS)" "$(GLOBAL_AGENTS_SKILLS)"
	@for skill in "$(SKILLS_DIR)"/*; do \
		[ -d "$$skill" ] || continue; \
		name=$$(basename "$$skill"); \
		ln -sfn "$$skill" "$(GLOBAL_CLAUDE_SKILLS)/$$name"; \
		ln -sfn "$$skill" "$(GLOBAL_CODEX_SKILLS)/$$name"; \
		ln -sfn "$$skill" "$(GLOBAL_OPENCODE_SKILLS)/$$name"; \
		ln -sfn "$$skill" "$(GLOBAL_AGENTS_SKILLS)/$$name"; \
	done
	@printf '%s\n' 'Linked canonical skills into global skill folders.'

unlink:
	@for target in "$(GLOBAL_CLAUDE_SKILLS)" "$(GLOBAL_CODEX_SKILLS)" "$(GLOBAL_OPENCODE_SKILLS)" "$(GLOBAL_AGENTS_SKILLS)"; do \
		[ -d "$$target" ] || continue; \
		for skill in "$(SKILLS_DIR)"/*; do \
			[ -d "$$skill" ] || continue; \
			name=$$(basename "$$skill"); \
			link="$$target/$$name"; \
			if [ -L "$$link" ] && [ "$$(readlink "$$link")" = "$$skill" ]; then \
				rm "$$link"; \
			fi; \
		done; \
	done
	@printf '%s\n' 'Removed symlinks created by this repo.'
