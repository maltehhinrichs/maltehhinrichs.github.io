import re
from pathlib import Path

def extract_presentations(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_section = False
    presentations = []

    pat_entry = re.compile(r"^\*\*(.+?)\*\*,\s*(.+?)\s*\((.+?)\)")
    pat_year = re.compile(r"^##\s+(\d{4})")

    for line in lines:
        if line.strip() == "# Academic Presentations":
            in_section = True
            continue
        if in_section and line.startswith("#") and not line.startswith("##"):
            break  # End of section

        if in_section:
            if pat_year.match(line.strip()):
                continue  # skip year headers

            entry_match = pat_entry.match(line.strip())
            if entry_match:
                conference = entry_match.group(1)
                university = entry_match.group(2)
                date = entry_match.group(3)
                presentations.append({
                    "conference": conference,
                    "university": university,
                    "date": date
                })

    return presentations

def format_presentations_md(presentations):
    out = []
    for p in presentations:
        out.append(
            f"- **{p['conference']}**\n"
            f"  - {p['university']}\n"
            f"  - {p['date']}\n"
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

"""

    presentations = extract_presentations(str(cv_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write(format_presentations_md(presentations))
