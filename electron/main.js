// electron/main.js
// 1. 新增引入 ipcMain
import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'path'
import fs from 'fs'

const process = global.process
let win = null

function resolveWindowIcon() {
  const iconCandidates = [
    path.join(process.cwd(), 'build/icon.ico'),
    path.join(__dirname, '../src/assets/images/logo.jpg'),
    path.join(process.cwd(), 'src/assets/images/logo.jpg'),
    path.join(process.cwd(), 'public/logo.jpg'),
  ]

  return iconCandidates.find((iconPath) => fs.existsSync(iconPath))
}

function createWindow() {
  const icon = resolveWindowIcon()

  win = new BrowserWindow({
    width: 1200,          
    height: 800,          
    minWidth: 800,        
    minHeight: 600,       
    frame: false, // 隐藏原生边框
    icon,
    
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  })

  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL)
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'))
  }
}

app.whenReady().then(() => {
  app.setAppUserModelId('com.aiinterview.app')
  createWindow()

  // === 新增：监听前端发来的窗口控制信号 ===
  ipcMain.on('window-min', () => {
    if (win) win.minimize()
  })
  
  ipcMain.on('window-max', () => {
    if (win) {
      if (win.isMaximized()) {
        win.unmaximize() // 恢复原状
      } else {
        win.maximize()   // 最大化
      }
    }
  })
  
  ipcMain.on('window-close', () => {
    app.exit(0)
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})