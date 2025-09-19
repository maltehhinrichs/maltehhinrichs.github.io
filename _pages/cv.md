---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script src="{{ '/assets/js/cv-download.js' | relative_url }}"></script>

<div id="cv-download" style="margin-bottom: 2rem;">
    <button 
        @click="downloadCV" 
        :disabled="isDownloading"
        style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; background-color: #dc2626; color: white; border: none; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s ease; text-decoration: none;"
        :style="{ backgroundColor: isDownloading ? '#7f1d1d' : '#dc2626', opacity: isDownloading ? '0.7' : '1' }"
        onmouseover="this.style.backgroundColor='#b91c1c'"
        onmouseout="this.style.backgroundColor=this.disabled ? '#7f1d1d' : '#dc2626'"
    >
        <div v-if="isDownloading" style="width: 16px; height: 16px; border: 2px solid transparent; border-top: 2px solid currentColor; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <svg v-else style="width: 16px; height: 16px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        {{ isDownloading ? 'Preparing Download...' : 'Download CV (PDF)' }}
    </button>
</div>

<style>
@keyframes spin { to { transform: rotate(360deg); } }
</style>

<script>
// Initialize the download button with your Mega URL
document.addEventListener('DOMContentLoaded', function() {
    const megaUrl = 'https://mega.nz/file/ARkGlTKT#SvqaXqEUQEEQjxBoeaI1fmUhFg0CeIID4sl91Xh3fXM';
    initCVDownload(megaUrl);
});
</script>

## Education

**PhD in Economics**  
Queen's University Belfast, UK (October 2023--present)  
Dissertation title: *Renewable Energy in the Industrial Revolution*  
Supervisors: Alan Fernihough and Christopher Colvin

**MSc Economics**  
University of Mannheim, Germany (September 2020--August 2022)  
Grade: 1.6 (1.0=excellent, 4.0=pass)  
Thesis: *Engines of Growth? The Role of the Steam Engine for Long-Run Economic Development in Germany*

**Visiting Student**  
NHH Norwegian School of Economics, Norway (February--June 2021)

**BSc Economics**  
University of Mannheim, Germany (September 2017--August 2020)  
Grade: 1.3 (1.0=excellent, 4.0=pass)  
Thesis: *The Long-Term Effects of Colonialism on Income Inequality*

**Visiting Student**  
Hong Kong University of Science and Technology, Hong Kong (August--December 2019)

## Academic Affiliations

Research Student, Centre for Economics, Policy and History (October 2023--present)

## Working Papers and Works in Progress

"Leapfrogging or path dependence? Water mills and long-run growth in the Scottish Industrial Revolution"

"Water mills and human capital accumulation in industrialising Prussia"

## Teaching Experience

### Queen's University Belfast
ECO1013 -- Principles of Economics, Graduate Teaching Assistant (September 2024--present)

### University of Mannheim
Macroeconomics A, Graduate Teaching Assistant (February--August 2020)

Principles of Economics, Undergraduate Teaching Assistant (September--December 2018)

## Honours and Awards

**Graduated in top 20% of MSc Economics cohort**, University of Mannheim (2022)

**Graduated in top 10% of BSc Economics cohort**, University of Mannheim (2020)

**Dean's List**, Hong Kong University of Science and Technology (2019)

## Research Grants and Funding

**EHES Conference Travel and Accommodation Grant** (July 2025)

**EHS Young Scholar Conference Bursary** (January 2025)

**CEPH Studentship**, Irish Higher Education Authority North-South Research Programme, full funding for PhD studies (October 2023)

**PROMOS Scholarship**, German Academic Exchange Service (DAAD), full funding for semester at HKUST (June 2019)

## Professional Membership

Economic History Society (UK)

European Historical Economics Society

Irish Economic Association

## Academic Presentations

### 2025
**European Historical Economics Society Conference**, University of Hohenheim (September 2025)

**CEPH PhD Workshop in Quantitative Economic History**, Queen's University Belfast (June 2025)

**QBS PGR Conference**, Queen's University Belfast (June 2025)

**Economic History Society Conference**, University of Strathclyde (April 2025)

**QUCEH PhD Discussion Group**, Queen's University Belfast (February 2025)

### 2024
**EHS Residential Training**, University of Warwick (November 2024)

**QUCEH Seminar Series**, Queen's University Belfast (April 2024)

**QUCEH PhD Discussion Group**, Queen's University Belfast (March 2024)

## Professional Development

**Participant**, Graduate Teaching Assistant Workshops, The Economics Network (January 2025)

**Participant**, Weekend Workshop for Teaching Assistants, University of Mannheim (September 2018)

## Industry Experience

**KPMG AG Wirtschaftsprüfungsgesellschaft**  
Junior Consultant, Global Transfer Pricing (April--September 2023)

## Technical Skills

**Software:** R, Stata, Matlab, Quarto, LaTeX, QGIS

**Languages:** German (native), English (fluent), Spanish (intermediate), Latin (reading)
