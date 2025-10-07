# generate_map.py
# Description: Generates a map of presentation locations from presentations.md.
#
# Instructions:
# 1. Make sure this script is in the root of your GitHub Pages repository.
# 2. Ensure your presentation list is in a file named `presentations.md`.
# 3. Run `pip install geopy python-frontmatter`.
# 4. Run `python generate_map.py` from your terminal.
# 5. Add the generated map to your page using the iframe code provided after running.
#

import os
import time
import re
import frontmatter
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

# --- Configuration ---
INPUT_FILE = os.path.join("_pages", "presentations.md")     # The markdown file with your presentation list
OUTPUT_FOLDER = "talkmap"       # The folder to save map files in
JS_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "org-locations.js")
GEOCODE_TIMEOUT = 10            # Timeout in seconds for geocoding requests

import re

def parse_presentations(file_path):
    print("-> Parsing presentations.md...")
    presentations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

            raw_lines = [line.rstrip() for line in post.content.splitlines() if line.strip()]

            i = 0
            while i < len(raw_lines):
                line = raw_lines[i]

                # Look for a new entry starting with "- **"
                if line.startswith("- **"):
                    event = re.sub(r"\*\*(.*?)\*\*", r"\1", line.lstrip("- ").strip())
                    if i+2 < len(raw_lines):
                        venue = raw_lines[i+1].strip()
                        date = raw_lines[i+2].strip()
                        presentations.append({
                            "event": event,
                            "venue": venue,
                            "date": date
                        })
                        i += 3
                        continue
                i += 1

        print(f"   Success: Found {len(presentations)} presentations.")
        print("   Preview of parsed entries:")
        for p in presentations:
            print(f"     {p['event']} @ {p['venue']} ({p['date']})")

        return presentations

    except FileNotFoundError:
        print(f"   Error: {file_path} not found. Please check the file name and location.")
        return None

def geocode_locations(presentations):
    """Geocodes the 'venue' for each presentation using Nominatim."""
    print("\n-> Geocoding locations (this may take a moment)...")
    geocoder = Nominatim(user_agent="academic_pages_map_generator")
    geocoded_locations = {}

    for p in presentations:
        venue = p['venue']
        description = f"{p['event']}<br>{p['venue']}<br>{p['date']}"
        # Escape quotes to prevent breaking the JavaScript string
        description = description.replace('"', '&quot;')

        print(f"   Geocoding: {venue}")
        try:
            # Add a 1-second delay between requests to respect Nominatim's usage policy
            time.sleep(1) 
            location_data = geocoder.geocode(venue, timeout=GEOCODE_TIMEOUT)

            if location_data:
                geocoded_locations[description] = (location_data.latitude, location_data.longitude)
                print(f"     -> Success: Found at ({location_data.latitude:.4f}, {location_data.longitude:.4f})")
            else:
                print(f"     -> Failed: Could not find coordinates for '{venue}'.")

        except GeocoderTimedOut:
            print(f"     -> Error: Geocoder timed out on '{venue}'.")
        except Exception as e:
            print(f"     -> Error: An unexpected error occurred for '{venue}': {e}")
    
    print(f"\n   Success: Geocoded {len(geocoded_locations)} out of {len(presentations)} locations.")
    return geocoded_locations

def create_js_file(locations):
    """Creates the org-locations.js file from the geocoded dictionary."""
    print("\n-> Generating JavaScript map data file...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    js_content = "var addressPoints = [\n"
    for description, (lat, lon) in locations.items():
        js_content += f'  ["{description}", {lat}, {lon}],\n'
    
    if js_content.endswith(',\n'):
        js_content = js_content[:-2] + '\n' # Remove the last comma
    js_content += "];"

    with open(JS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"   Success: Map data written to {JS_OUTPUT_FILE}")

def main():
    """Main function to run the script."""
    presentations = parse_presentations(INPUT_FILE)
    if not presentations:
        return

    geocoded = geocode_locations(presentations)
    if not geocoded:
        print("\nNo locations were geocoded. Cannot generate map.")
        return

    create_js_file(geocoded)

    print("\n---")
    print("✅ All done!")
    print("\nNext steps:")
    print("1. Ensure you have a 'map.html' file inside the 'talkmap' folder.")
    print(f"2. Add the following code to '{INPUT_FILE}' where you want the map:")
    print('\n<iframe src="/talkmap/map.html" height="600" width="100%" style="border:none;"></iframe>\n')

if __name__ == "__main__":
    main()
