// CV Download functionality for Academic Pages
function initCVDownload() {
    const { createApp, ref } = Vue;
    
    createApp({
        setup() {
            const isDownloading = ref(false);
            // The direct path to the CV file created by your GitHub Action.
            const cvFilePath = 'files/cv-latest.pdf';

            const downloadCV = () => {
                if (isDownloading.value) return;

                isDownloading.value = true;

                // We keep a short delay to allow the "Preparing Download..." state to show.
                setTimeout(() => {
                    // Trigger the download by simply navigating to the file.
                    window.location.href = cvFilePath;

                    // Reset the button's state after a few seconds,
                    // giving the browser time to process the download.
                    setTimeout(() => {
                        isDownloading.value = false;
                    }, 3000);
                }, 500);
            };

            return {
                isDownloading,
                downloadCV
            };
        },
        // The template is unchanged to keep the button design identical.
        template: `
            <button 
                @click="downloadCV" 
                :disabled="isDownloading"
                style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; background-color: #dc2626; color: white; border: none; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s ease; text-decoration: none;"
                :style="{ backgroundColor: isDownloading ? '#7f1d1d' : '#dc2626', opacity: isDownloading ? '0.7' : '1' }"
                @mouseover="event.target.style.backgroundColor='#b91c1c'"
                @mouseout="event.target.style.backgroundColor=event.target.disabled ? '#7f1d1d' : '#dc2626'"
            >
                <div v-if="isDownloading" style="width: 16px; height: 16px; border: 2px solid transparent; border-top: 2px solid currentColor; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <svg v-else style="width: 16px; height: 16px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                {{ isDownloading ? 'Preparing Download...' : 'Download CV (PDF)' }}
            </button>
        `
    }).mount('#cv-download');
}
