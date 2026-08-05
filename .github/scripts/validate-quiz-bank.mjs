// CLI wrapper — validation logic lives in validate-quiz-bank-lib.mjs (tested by validate-quiz-bank.test.mjs)
import { readdir, readFile } from 'node:fs/promises'
import path from 'node:path'
import { validateFile } from './validate-quiz-bank-lib.mjs'

const dir = process.argv[2]
if (!dir) {
	console.error('Usage: node validate-quiz-bank.mjs <dir>')
	process.exit(1)
}

const files = (await readdir(dir)).filter((f) => f.endsWith('.md'))
if (files.length === 0) {
	console.error(`No .md files found in ${dir}`)
	process.exit(1)
}

let failCount = 0
for (const file of files) {
	const filePath = path.join(dir, file)
	const raw = await readFile(filePath, 'utf8')
	const errors = await validateFile(raw)
	if (errors.length > 0) {
		failCount++
		console.error(`\n✗ ${file}`)
		for (const e of errors) console.error(`  - ${e}`)
	}
}

console.log(`\n${files.length - failCount}/${files.length} cards valid.`)
if (failCount > 0) {
	console.error(`${failCount} card(s) failed validation.`)
	process.exit(1)
}
