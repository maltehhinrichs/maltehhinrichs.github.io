import re

def extract_presentations(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_section = False
    presentations = []

    year = None
    # Matches: **Conference Name**, University Name (Month Year)
    pat_entry = re.compile(r"^\*\*(.+?)\*\*,\s*(.+?)\s*\((.+?)\)")
    pat_year = re.compile(r"^##\s+(\d{4})")

    for line in lines:
        if line.strip() == "# Academic Presentations":
            in_section = True
            continue
        if in_section and line.startswith("#") and not line.startswith("##"):
            break  # End of section

        if in_section:
            year_match = pat_year.match(line.strip())
            if year_match:
                year = year_match.group(1)
                continue

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
        out.append(f"- {p['conference']}\n  {p['university']}\n  {p['date']}\n")
    return "\n".join(out)

if __name__ == "__main__":
    presentations = extract_presentations("cv-latest.md")
    with open("presentations.md", "w", encoding="utf-8") as f:
        f.write("# Academic Presentations\n\n")
        f.write(format_presentations_md(presentations))
