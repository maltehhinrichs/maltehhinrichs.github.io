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
        out.append(f"- {p['conference']}\n  {p['university']}\n  {p['date']}\n")
    return "\n".join(out)

if __name__ == "__main__":
    # Look for cv-latest.md in ./files relative to this script
    script_dir = Path(__file__).parent
    cv_path = script_dir.parent / "files" / "cv-latest.md"
    output_path = script_dir.parent / "files" / "presentations.md"

    presentations = extract_presentations(str(cv_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Academic Presentations\n\n")
        f.write(format_presentations_md(presentations))
