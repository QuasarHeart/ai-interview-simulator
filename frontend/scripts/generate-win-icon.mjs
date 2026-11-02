import fs from 'node:fs/promises'
import path from 'node:path'
import sharp from 'sharp'
import pngToIco from 'png-to-ico'

const projectRoot = process.cwd()
const sourceJpg = path.join(projectRoot, 'src', 'assets', 'images', 'logo.jpg')
const outputDir = path.join(projectRoot, 'build')
const outputIco = path.join(outputDir, 'icon.ico')

const iconSizes = [16, 24, 32, 48, 64, 128, 256]

async function generateIcoFromLogo() {
  await fs.access(sourceJpg)
  await fs.mkdir(outputDir, { recursive: true })

  const pngBuffers = await Promise.all(
    iconSizes.map((size) =>
      sharp(sourceJpg)
        .resize(size, size, { fit: 'cover' })
        .png()
        .toBuffer()
    )
  )

  const icoBuffer = await pngToIco(pngBuffers)
  await fs.writeFile(outputIco, icoBuffer)
  console.log(`[icon] generated ${path.relative(projectRoot, outputIco)} from ${path.relative(projectRoot, sourceJpg)}`)
}

generateIcoFromLogo().catch((error) => {
  console.error('[icon] failed to generate icon.ico:', error)
  process.exit(1)
})
