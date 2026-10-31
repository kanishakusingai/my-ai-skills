# 🧠 My AI Skills Collection

A clean personal collection of custom AI coding agent skills.

---

## 📂 Skills

```text
skills/
└── amazon-skills/
    ├── amazon-premium-aplus/             # Premium A+ modules, image sizes, JSON shapes, workflow
    │   └── SKILL.md
    ├── amazon-aplus-visual-preferences/  # Seller's A+ and Brand Story visual style preferences
    │   ├── SKILL.md
    │   └── references/
    │       ├── reference-images.txt      # Index of the reference images
    │       └── images/                   # Featured examples + all-aplus/<product>/ full sets
    └── amazon-ad-campaign-designer/      # Sponsored Products campaigns, keywords, bids, negatives
        ├── SKILL.md
        └── scripts/                      # merge_xray.py, check_negatives.py, fill_template.py
```

| Skill | Use it for |
|---|---|
| [amazon-premium-aplus](skills/amazon-skills/amazon-premium-aplus/SKILL.md) | Planning, validating, and submitting Amazon.in Premium A+ content |
| [amazon-aplus-visual-preferences](skills/amazon-skills/amazon-aplus-visual-preferences/SKILL.md) | Designing or reviewing A+ images and Brand Story artwork in the seller's style |
| [amazon-ad-campaign-designer](skills/amazon-skills/amazon-ad-campaign-designer/SKILL.md) | Building Amazon India Sponsored Products campaigns from keyword research |

The ad campaign scripts need Python 3 with `pandas` and `openpyxl`.

---

## 🚀 How to Add Your Own Skill

1. Create a folder inside `skills/` with your skill name:
   ```text
   skills/
   └── my-skill-name/
       └── SKILL.md
   ```

2. Format your `SKILL.md` with:
   ```markdown
   ---
   name: my-skill-name
   description: When and why the AI agent should use this skill.
   ---

   # Instructions
   Write your prompt instructions, rules, and best practices here.
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Add my-skill-name"
   git push
   ```
