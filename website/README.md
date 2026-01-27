# Acuity Website

Simple static website for downloading Acuity.

## Files

- `index.html` - Main landing page
- `style.css` - Styling
- `script.js` - OS detection and download links

## Deployment

### Quick Deploy to GitHub Pages

1. Push this website folder to GitHub
2. Enable GitHub Pages in repo settings
3. Set source to `main` branch, `/website` folder
4. Access at `https://yourusername.github.io/acuity/`

### Update Download URLs

Before deploying, edit `script.js` and update the download URLs:

```javascript
const DOWNLOAD_URLS = {
    windows: 'your-actual-windows-download-url',
    mac: 'your-actual-macos-download-url',
    linux: 'your-actual-linux-download-url'
};
```

### Local Testing

Just open `index.html` in a browser. No build process needed!

## Hosting Options

- **GitHub Pages**: Free, easy
- **Netlify**: Free, custom domain
- **Vercel**: Free, fast CDN
- **Any static host**: Just upload the files

See `../DEPLOYMENT.md` for detailed instructions.
