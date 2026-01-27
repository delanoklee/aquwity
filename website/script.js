// Auto-detect OS and set download links
(function() {
    // Download URLs - update these with your actual hosting URLs
    const DOWNLOAD_URLS = {
        windows: 'https://github.com/delanoklee/aquwity/releases/download/v1.0.0/acuity-windows-x64.zip',
        mac: null, // macOS build coming soon
        linux: 'https://github.com/delanoklee/aquwity/releases/download/v1.0.0/acuity-linux-x64.tar.gz'
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
        if (DOWNLOAD_URLS[detectedOS]) {
            window.location.href = DOWNLOAD_URLS[detectedOS];
        } else {
            alert('macOS build coming soon! Please check back later or download for Windows/Linux.');
        }
    };

    // Set platform links
    document.getElementById('download-windows').href = DOWNLOAD_URLS.windows;
    document.getElementById('download-mac').href = DOWNLOAD_URLS.mac || '#';
    document.getElementById('download-linux').href = DOWNLOAD_URLS.linux;

    // Add click handlers for platform links to prevent default if no URL
    document.getElementById('download-mac').addEventListener('click', function(e) {
        if (!DOWNLOAD_URLS.mac) {
            e.preventDefault();
            alert('macOS build coming soon! Please check back later.');
        }
    });
})();
