#!/usr/bin/env python3
"""
Simple script to extract university locations from presentations.md and create a map
"""

import re
import os
import json
import requests
import time
from urllib.parse import quote

# Set the default timeout, in seconds
TIMEOUT = 10

def extract_universities_from_md(file_path):
    """Extract university names and dates from presentations.md"""
    universities = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find lines with university information (lines that contain "University" or "Queen's")
    lines = content.split('\n')
    current_event = None
    current_date = None
    
    for line in lines.strip():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('---'):
            continue
            
        # Check if this is an event line (starts with **)
        if line.startswith('- **') and line.endswith('**'):
            current_event = line[4:-2]  # Remove - ** and **
            continue
            
        # Check if this contains a university
        if any(keyword in line for keyword in ['University', "Queen's", 'Institute']):
            university = line.strip('- ').strip()
            universities.append({
                'event': current_event,
                'university': university,
                'date': current_date
            })
            continue
            
        # Check if this looks like a date
        if re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', line):
            current_date = line.strip('- ').strip()
    
    return universities

def search_university_location(university_name):
    """Search for university location using web search and then geocode"""
    try:
        # Search for the university to get more context
        search_query = f"{university_name} university location address"
        print(f"  Searching web for: {search_query}")
        
        # Use a simple web search approach
        # This would be replaced with actual web search API
        # For now, let's use a more intelligent parsing approach
        
        # Try to extract location clues from the university name itself
        location_clues = []
        
        # Common patterns in university names
        patterns = [
            r'University of ([A-Za-z\s]+)',  # "University of Location"
            r'([A-Za-z\s]+) University',     # "Location University"
            r"([A-Za-z\s']+) University",    # "Location's University"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, university_name)
            if match:
                potential_location = match.group(1).strip()
                if potential_location and len(potential_location) > 2:
                    location_clues.append(potential_location)
        
        # Add the full name as a clue
        location_clues.append(university_name)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_clues = []
        for clue in location_clues:
            if clue not in seen:
                seen.add(clue)
                unique_clues.append(clue)
        
        return unique_clues
        
    except Exception as ex:
        print(f"  ✗ Web search error: {ex}")
        return [university_name]

def geocode_with_nominatim(location_query):
    """Geocode a location using Nominatim"""
    try:
        # Use Nominatim REST API directly
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': location_query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'presentations-map/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        
        results = response.json()
        if results:
            result = results[0]
            return {
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'address': result.get('display_name', location_query)
            }
        
        return None
        
    except Exception as ex:
        print(f"    Geocoding error for '{location_query}': {ex}")
        return None

def geocode_universities(universities):
    """Geocode university locations using web search + geocoding"""
    location_dict = {}
    
    for item in universities:
        university = item['university']
        event = item['event']
        date = item['date']
        
        print(f"Geocoding: {university}")
        
        # Get location clues from web search
        location_clues = search_university_location(university)
        
        geocoded = False
        for clue in location_clues:
            print(f"  Trying to geocode: {clue}")
            
            # Try multiple variations of the location clue
            search_variations = [
                clue,
                f"{clue} university",
                f"{clue}, UK" if not any(country in clue.lower() for country in ['germany', 'france', 'spain', 'italy']) else clue,
                f"{clue}, Germany" if 'hohenheim' in clue.lower() or 'stuttgart' in clue.lower() else None,
            ]
            
            # Remove None values
            search_variations = [v for v in search_variations if v]
            
            for variation in search_variations:
                result = geocode_with_nominatim(variation)
                if result:
                    description = f"{event}<br/>{university}"
                    if date:
                        description += f"<br/>{date}"
                    
                    location_dict[description] = type('obj', (object,), {
                        'latitude': result['latitude'],
                        'longitude': result['longitude'],
                        'address': result['address']
                    })()
                    
                    print(f"  ✓ Found: {result['address']}")
                    geocoded = True
                    break
                
                # Be nice to the API
                time.sleep(1)
            
            if geocoded:
                break
        
        if not geocoded:
            print(f"  ✗ Could not geocode: {university}")
            print(f"    Tried: {', '.join(location_clues)}")
        
        # Be nice to the API between universities
        time.sleep(1)
    
    return location_dict

def create_js_file(location_dict, output_dir="talkmap"):
    """Create the JavaScript file with location data"""
    os.makedirs(output_dir, exist_ok=True)
    
    js_content = "var addressPoints = [\n"
    
    for description, location in location_dict.items():
        js_content += f'  [\n    "{description}",\n    {location.latitude},\n    {location.longitude}\n  ],\n'
    
    js_content = js_content.rstrip(',\n') + '\n];'
    
    js_file_path = os.path.join(output_dir, "org-locations.js")
    with open(js_file_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✓ Created {js_file_path}")

def create_html_file(output_dir="talkmap"):
    """Create the HTML map file"""
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Presentation Locations</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.Default.css" />
    <script src="org-locations.js"></script>
    <style>
        #map { height: 600px; width: 100%; }
        body { margin: 0; padding: 10px; font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <div id="map"></div>
    <p style="margin-top: 10px; font-size: 12px; color: #666;">
        Click markers to see presentation details. Clustered markers can be clicked to zoom in.
    </p>
    <script type="text/javascript">
        var map = L.map('map').setView([54.5, -2.0], 5); // Center on UK/Ireland
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        var markers = L.markerClusterGroup({
            showCoverageOnHover: false,
            maxClusterRadius: 80
        });
        
        for (var i = 0; i < addressPoints.length; i++) {
            var a = addressPoints[i];
            var title = a[0];
            var marker = L.marker(new L.LatLng(a[1], a[2]), { title: title });
            marker.bindPopup(title);
            markers.addLayer(marker);
        }
        
        map.addLayer(markers);
        
        // Fit map to show all markers
        if (addressPoints.length > 0) {
            map.fitBounds(markers.getBounds(), {padding: [20, 20]});
        }
    </script>
</body>
</html>'''
    
    html_file_path = os.path.join(output_dir, "map.html")
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Created {html_file_path}")

def main():
    presentations_file = "presentations.md"
    
    if not os.path.exists(presentations_file):
        print(f"Error: {presentations_file} not found!")
        print("Make sure you run this script from the directory containing presentations.md")
        return
    
    print("Extracting universities from presentations.md...")
    universities = extract_universities_from_md(presentations_file)
    
    if not universities:
        print("No universities found in presentations.md")
        return
    
    print(f"Found {len(universities)} universities:")
    for item in universities:
        print(f"  - {item['university']} ({item['event']})")
    
    print("\nGeocoding locations using web search...")
    print("Note: This may take a while as we respect API rate limits")
    location_dict = geocode_universities(universities)
    
    if not location_dict:
        print("No locations were successfully geocoded")
        return
    
    print(f"\nSuccessfully geocoded {len(location_dict)} locations")
    
    print("\nGenerating map files...")
    create_js_file(location_dict)
    create_html_file()
    
    print("\n✓ Map generated successfully!")
    print("Files created:")
    print("  - talkmap/org-locations.js")
    print("  - talkmap/map.html")
    print("\nYou can now add the map to your presentations page with:")
    print('<iframe src="/talkmap/map.html" height="700" width="100%" style="border:none;"></iframe>')
    print("\nNote: Install required package with: pip install requests")

if __name__ == "__main__":
    main()
