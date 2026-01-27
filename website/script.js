// Auto-detect OS and set download links
(function() {
    // Download URLs - update these with your actual hosting URLs
    const DOWNLOAD_URLS = {
        windows: 'https://github.com/delanoklee/acuity/releases/latest/download/acuity-windows-x64.zip',
        mac: 'https://github.com/delanoklee/acuity/releases/latest/download/acuity-macos-x64.dmg',
        linux: 'https://github.com/delanoklee/acuity/releases/latest/download/acuity-linux-x64.tar.gz'
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

    // Add click handlers for platform links to prevent default if no URL
    document.querySelectorAll('.platform-link').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href.includes('yourusername')) {
                e.preventDefault();
                alert('Download not yet available. Please build the app using the build scripts first!');
            }
        });
    });

    // Same for primary button
    if (DOWNLOAD_URLS[detectedOS].includes('yourusername')) {
        primaryDownloadBtn.onclick = function(e) {
            e.preventDefault();
            alert('Download not yet available. Please build the app using the build scripts first!\n\nTo build:\n1. Run the appropriate build script from build_scripts/\n2. Upload the generated file to GitHub Releases or your hosting\n3. Update the URLs in script.js');
        };
    }
})();
