// CV Download functionality for Academic Pages
function initCVDownload(megaUrl) {
    const { createApp, ref } = Vue;
    
    createApp({
        setup() {
            const isDownloading = ref(false);
            const apiEndpoint = 'https://mega.wldbs.workers.dev/api/info';

            const downloadCV = async () => {
                if (isDownloading.value) return;

                isDownloading.value = true;

                try {
                    const formData = new FormData();
                    formData.append('megaurl', megaUrl);

                    const response = await fetch(apiEndpoint, {
                        method: 'POST',
                        body: formData,
                    });

                    const data = await response.json();

                    if (data.ok) {
                        const base64Url = btoa(megaUrl);
                        const directLink = `https://mega.wldbs.workers.dev/download?url=${base64Url}`;
                        
                        setTimeout(() => {
                            window.location.href = directLink;
                            setTimeout(() => {
                                isDownloading.value = false;
                            }, 3000);
                        }, 500);
                    } else {
                        throw new Error(data.error || 'Could not access CV file');
                    }
                } catch (error) {
                    console.error('Download error:', error);
                    alert('Sorry, there was an error downloading the CV. Please try again later.');
                    isDownloading.value = false;
                }
            };

            return {
                isDownloading,
                downloadCV
            };
        }
    }).mount('#cv-download');
}
