Start Claude Code on Opus from the repo root:

    claude --model claude-opus-5-5

Then paste:

---

You are the senior engineer for this build. Read docs/build/senior-engineer.md first; that is your role. Then read CLAUDE.md and BUILD_BRIEF.md in full, and skim standards/, .claude/, clients/_template/, and lib/docx/SPEC.md.

This repo is a migration of my claude.ai Ethos Assistant project into a Claude Code workspace. You lead the build and direct the app-builder and tester subagents; I make the calls you're not authorized to make.

Before anything else, give me a short readback: what you're building, the phases, how you'll run the builder/tester loop, and anything in the brief that looks wrong, missing, or contradictory. Push back if you see a better approach. Then start Phase 0 and stop at the end of it for my review.
