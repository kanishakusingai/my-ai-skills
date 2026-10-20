# 🧠 My AI Skills Collection

A curated personal collection of custom and high-quality AI coding agent skills.

These skills extend and supercharge AI assistants (such as Antigravity, Kiro, Claude Code, Cursor, Codex, and Copilot) with specialized instructions, playbooks, and architectural guidance.

---

## 📦 Included Skills

| Skill | Category | Description |
|---|---|---|
| **`ui-taste`** | Frontend & UI/UX | Eliminates generic "AI slop". Enforces visual polish, hierarchy, spacing, and modern design standards for web and iOS interfaces. |
| **`ios-design`** | Mobile Design | High-fidelity iOS UI/UX guidance using Apple Human Interface Guidelines, SwiftUI, UIKit, and React Native. |

---

## 🚀 How to Add a New Skill

1. Create a new folder inside `skills/` with your skill name:
   ```text
   skills/
   └── my-new-skill/
       └── SKILL.md
   ```

2. Format your `SKILL.md`:
   ```markdown
   ---
   name: my-new-skill
   description: When and why the AI agent should use this skill.
   ---

   # Instructions
   Write your prompt instructions, rules, and best practices here.
   ```

3. Commit and save:
   ```bash
   git add .
   git commit -m "Add my-new-skill"
   ```

---

## 📥 How to Install Skills from This Collection

To install any skill from this repository into any project or machine:

```bash
npx skills add <path-or-github-url> --skill <skill-name>
```
