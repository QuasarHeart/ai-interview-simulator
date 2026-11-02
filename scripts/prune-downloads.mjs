import fs from 'node:fs/promises'
import path from 'node:path'

const projectRoot = process.cwd()
const installerPath = path.join(projectRoot, 'dist', 'downloads', '伯乐智面-Setup.exe')
const downloadsDir = path.dirname(installerPath)

async function removeIfExists(targetPath) {
  try {
    await fs.unlink(targetPath)
  } catch (error) {
    if (error?.code !== 'ENOENT') {
      throw error
    }
  }
}

async function removeDirIfEmpty(targetDir) {
  try {
    const items = await fs.readdir(targetDir)
    if (items.length === 0) {
      await fs.rmdir(targetDir)
    }
  } catch (error) {
    if (error?.code !== 'ENOENT' && error?.code !== 'ENOTEMPTY') {
      throw error
    }
  }
}

await removeIfExists(installerPath)
await removeDirIfEmpty(downloadsDir)

console.log('[prune] removed dist/downloads/伯乐智面-Setup.exe')
