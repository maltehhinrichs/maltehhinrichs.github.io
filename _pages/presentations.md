---
layout: archive
title: "Presentations"
permalink: /presentation/
author_profile: true
---

Below is a list of presentations, with locations mapped:

<div id="presentation-map" style="height: 400px; margin-bottom: 2em;"></div>

<ul id="presentation-list">
  <!-- List will be populated by script -->
</ul>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
fetch('{{ "/assets/data/presentations.json" | relative_url }}')
  .then(res => res.json())
  .then(data => {
    const map = L.map('presentation-map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const list = document.getElementById('presentation-list');
    data.forEach(pres => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${pres.name}</strong> (${pres.event})<br>${pres.location}`;
      list.appendChild(li);

      if (pres.lat && pres.lng) {
        L.marker([pres.lat, pres.lng]).addTo(map)
          .bindPopup(`<strong>${pres.name}</strong><br>${pres.location}`);
      }
    });
  });
</script>
