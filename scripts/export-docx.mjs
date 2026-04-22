import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

import MarkdownIt from 'markdown-it'
import HTMLtoDOCX from 'html-to-docx'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const workspaceRoot = path.resolve(__dirname, '..')
const inputPath = path.resolve(workspaceRoot, 'docs', '前端详细设计方案.md')
const outputPath = path.resolve(workspaceRoot, 'docs', '前端详细设计方案.docx')

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: false
})

const wrapHtml = (bodyHtml) => {
  const css = `
    body { font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; line-height: 1.45; }
    h1 { font-size: 24px; }
    h2 { font-size: 18px; margin-top: 18px; }
    h3 { font-size: 14px; margin-top: 14px; }
    p, li { font-size: 11pt; }
    code { font-family: Consolas, "Courier New", monospace; }
    pre { font-family: Consolas, "Courier New", monospace; font-size: 10pt; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #d0d7de; padding: 6px 8px; }
  `.trim()

  return `<!doctype html><html><head><meta charset="utf-8" /><style>${css}</style></head><body>${bodyHtml}</body></html>`
}

const main = async () => {
  const markdown = await fs.readFile(inputPath, 'utf8')
  const htmlBody = md.render(markdown)
  const html = wrapHtml(htmlBody)

  const docxBuffer = await HTMLtoDOCX(html, undefined, {
    table: { row: { cantSplit: true } },
    footer: false,
    pageNumber: false
  })

  await fs.writeFile(outputPath, docxBuffer)
  process.stdout.write(`DOCX generated: ${outputPath}\n`)
}

main().catch((err) => {
  console.error(err)
  process.exitCode = 1
})
