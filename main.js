const { app, BrowserWindow, screen } = require('electron')

try {
  require('electron-reloader')(module)
} catch {}

function createWindow() {
  const display = screen.getPrimaryDisplay()
  const { width: screenWidth } = display.workAreaSize

  // Window is 50% of screen width, centered at top
  const windowWidth = Math.round(screenWidth * 0.5)
  const windowHeight = 60

  const win = new BrowserWindow({
    width: windowWidth,
    height: windowHeight,
    x: Math.round((screenWidth - windowWidth) / 2),
    y: 0,
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    hasShadow: false,
    resizable: true,
    alwaysOnTop: true,
    webPreferences: {
      contextIsolation: true
    }
  })

  win.loadFile('index.html')
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  app.quit()
})
