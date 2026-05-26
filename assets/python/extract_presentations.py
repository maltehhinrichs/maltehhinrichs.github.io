import re
from pathlib import Path

def extract_presentations(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_section = False
    presentations = {}
    current_category = "Presentations"
    
    # Target exact Markdown headings that contain presentations and workshops
    target_sections = ["# Academic Presentations", "# Workshops", "# Professional Development"]

    pat_entry = re.compile(r"^\*\*(.+?)\*\*,\s*(.+?)\s*\\hfill\s*(.+)")

    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            if line.strip() in target_sections:
                in_section = True
                current_category = line.replace("#", "").strip()
            else:
                in_section = False 
            continue

        if in_section:
            if line.startswith("## "):
                current_category = line.replace("##", "").strip()
                if current_category not in presentations:
                    presentations[current_category] = []
                continue

            entry_match = pat_entry.match(line.strip())
            if entry_match:
                conference = entry_match.group(1)
                university = entry_match.group(2)
                date = entry_match.group(3)
                
                if current_category not in presentations:
                    presentations[current_category] = []
                    
                presentations[current_category].append({
                    "conference": conference,
                    "university": university,
                    "date": date
                })

    return presentations

def format_presentations_md(presentations):
    out = []
    for category, pres_list in presentations.items():
        if not pres_list:
            continue
        out.append(f"### {category}\n")
        for p in pres_list:
            # Added <br> tags to strictly enforce line breaks in Jekyll markdown
            out.append(
                f"- **{p['conference']}**<br>\n"
                f"  {p['university']}<br>\n"
                f"  {p['date']}\n"
            )
    return "\n".join(out)

if __name__ == "__main__":
    # Set proper paths for input and output
    script_dir = Path(__file__).parent
    repo_root = script_dir.parents[1]
    cv_path = repo_root / "files" / "cv-latest.md"
    output_path = repo_root / "_pages" / "presentations.md"

    # Set front matter
    front_matter = """---
layout: archive
title: "Presentations"
permalink: /presentations/
author_profile: true
---

## Map

<iframe src="/talkmap/map.html" height="600" width="100%" style="border:none;"></iframe>

## Full List

"""

    presentations = extract_presentations(str(cv_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(format_presentations_md(presentations))
