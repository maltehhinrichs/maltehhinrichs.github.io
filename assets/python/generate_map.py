# generate_map.py
import os
import re
import json
import time
import urllib.request
import urllib.parse
import frontmatter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# --- Configuration ---
INPUT_FILE = os.path.join("_pages", "presentations.md")
OUTPUT_FOLDER = "talkmap"
JS_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "org-locations.js")
GEOCODE_TIMEOUT = 10

def get_country_for_uni(venue):
    """
    Queries the open Research Organization Registry (ROR) API 
    to find the country of the most famous institution with this name.
    """
    try:
        query = urllib.parse.quote(venue)
        url = f"https://api.ror.org/organizations?query={query}"
        req = urllib.request.Request(url, headers={'User-Agent': 'AcademicMapGenerator/1.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get('items') and len(data['items']) > 0:
                item = data['items'][0]
                # Check for ROR API v2 schema
                if 'locations' in item and len(item['locations']) > 0:
                    return item['locations'][0].get('geonames_details', {}).get('country_name')
                # Fallback for ROR API v1 schema
                elif 'country' in item and 'country_name' in item['country']:
                    return item['country']['country_name']
    except Exception as e:
        print(f"     -> [Debug] ROR API lookup failed: {e}")
        pass
    return None

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
                if line.startswith("- **"):
                    # Strip the <br> out of the event name to prevent double breaks in JS
                    event = re.sub(r"\*\*(.*?)\*\*", r"\1", line.lstrip("- ").strip()).replace("<br>", "").strip()
                    if i+2 < len(raw_lines):
                        venue = raw_lines[i+1].replace("<br>", "").strip()
                        date = raw_lines[i+2].replace("<br>", "").strip()
                        presentations.append({
                            "event": event,
                            "venue": venue,
                            "date": date
                        })
                        i += 3
                        continue
                i += 1

        print(f"   Success: Found {len(presentations)} presentations.")
        return presentations

    except FileNotFoundError:
        print(f"   Error: {file_path} not found.")
        return None

def geocode_locations(presentations):
    print("\n-> Geocoding locations (this may take a moment)...")
    geocoder = Nominatim(user_agent="academic_cv_map_generator")
    geocoded_locations = {}

    for p in presentations:
        venue = p['venue']
        description = f"{p['event']}<br>{p['venue']}<br>{p['date']}"
        description = description.replace('"', '&quot;')

        print(f"   Geocoding: {venue}")
        
        # 1. Smart Disambiguation: Find the country using ROR
        search_query = venue
        country = get_country_for_uni(venue)
        if country:
            search_query = f"{venue}, {country}"
            print(f"     -> Smart match: Identified as '{search_query}'")

        # 2. Ask Nominatim for coordinates using the enriched search query
        try:
            time.sleep(1) 
            location_data = geocoder.geocode(search_query, timeout=GEOCODE_TIMEOUT)

            if location_data:
                geocoded_locations[description] = (location_data.latitude, location_data.longitude)
                print(f"     -> Success: Found at ({location_data.latitude:.4f}, {location_data.longitude:.4f})")
            else:
                if search_query != venue:
                    time.sleep(1) 
                    location_data = geocoder.geocode(venue, timeout=GEOCODE_TIMEOUT)
                    if location_data:
                        geocoded_locations[description] = (location_data.latitude, location_data.longitude)
                        print(f"     -> Success (Fallback): Found at ({location_data.latitude:.4f}, {location_data.longitude:.4f})")
                        continue
                print(f"     -> Failed: Could not find coordinates for '{venue}'.")

        except GeocoderTimedOut:
            print(f"     -> Error: Geocoder timed out on '{venue}'.")
        except Exception as e:
            print(f"     -> Error: An unexpected error occurred for '{venue}': {e}")
    
    print(f"\n   Success: Geocoded {len(geocoded_locations)} out of {len(presentations)} locations.")
    return geocoded_locations

def create_js_file(locations):
    print("\n-> Generating JavaScript map data file...")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    js_content = "var addressPoints = [\n"
    for description, (lat, lon) in locations.items():
        js_content += f'  ["{description}", {lat}, {lon}],\n'
    
    if js_content.endswith(',\n'):
        js_content = js_content[:-2] + '\n' 
    js_content += "];"

    with open(JS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"   Success: Map data written to {JS_OUTPUT_FILE}")

def main():
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

if __name__ == "__main__":
    main()
