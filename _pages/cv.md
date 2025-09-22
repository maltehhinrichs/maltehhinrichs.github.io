---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

The most up-to-date version of my CV is available for download here:

<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script src="{{ '/assets/js/cv-download.js' | relative_url }}"></script>

<style>
@keyframes spin { to { transform: rotate(360deg); } }
</style>

<div id="cv-download" style="margin-bottom: 2rem;"></div>

<script>
window.onload = function() {
    const megaUrl = 'https://mega.nz/file/ARkGlTKT#SvqaXqEUQEEQjxBoeaI1fmUhFg0CeIID4sl91Xh3fXM';
    initCVDownload(megaUrl);
};
</script>
