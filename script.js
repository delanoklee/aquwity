// Auto-detect OS and set download links
(function() {
    // Download URLs - update these with your actual hosting URLs
    const DOWNLOAD_URLS = {
        windows: 'https://github.com/delanoklee/aquwity/releases/latest/download/Acuity.exe',
        mac: 'https://github.com/delanoklee/aquwity/releases/latest/download/acuity-macos-x64.dmg',
        linux: 'https://github.com/delanoklee/aquwity/releases/latest/download/Acuity-x86_64.AppImage'
    };

    // Detect OS
    function detectOS() {
        const platform = navigator.platform.toLowerCase();
        const userAgent = navigator.userAgent.toLowerCase();

        if (platform.includes('win') || userAgent.includes('windows')) {
            return 'windows';
        } else if (platform.includes('mac') || userAgent.includes('mac')) {
            return 'mac';
        } else if (platform.includes('linux') || userAgent.includes('linux')) {
            return 'linux';
        }

        // Default to Windows
        return 'windows';
    }

    // Get OS display name
    function getOSName(os) {
        const names = {
            windows: 'Windows',
            mac: 'macOS',
            linux: 'Linux'
        };
        return names[os] || 'Windows';
    }

    // Initialize
    const detectedOS = detectOS();
    const primaryDownloadBtn = document.getElementById('primary-download');
    const downloadText = document.getElementById('download-text');

    // Set primary download button
    downloadText.textContent = `Download for ${getOSName(detectedOS)}`;
    primaryDownloadBtn.onclick = function() {
        window.location.href = DOWNLOAD_URLS[detectedOS];
    };

    // Set platform links
    document.getElementById('download-windows').href = DOWNLOAD_URLS.windows;
    document.getElementById('download-mac').href = DOWNLOAD_URLS.mac;
    document.getElementById('download-linux').href = DOWNLOAD_URLS.linux;
})();
