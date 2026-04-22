import fs from 'node:fs/promises'
import path from 'node:path'
import { createRequire } from 'node:module'

const require = createRequire(import.meta.url)
const rceditModule = require('rcedit')
const rcedit = rceditModule.rcedit || rceditModule.default || rceditModule

export default async function afterPack(context) {
  if (context.electronPlatformName !== 'win32') {
    return
  }

  const projectRoot = process.cwd()
  const iconPath = path.join(projectRoot, 'build', 'icon.ico')
  const exePath = path.join(context.appOutDir, `${context.packager.appInfo.productFilename}.exe`)

  await fs.access(iconPath)
  await fs.access(exePath)

  await rcedit(exePath, { icon: iconPath })

  console.log(`[afterPack] applied ${path.relative(projectRoot, iconPath)} to ${path.relative(projectRoot, exePath)}`)
}
