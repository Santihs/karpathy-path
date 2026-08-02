// Validates 04-Quiz-Bank/<repo>/*.md files against yanki's real parser
// (not a reimplementation) plus emptiness checks yanki won't fail on itself
// (it silently inserts a placeholder for a blank front/back instead of erroring).
import { readdir, readFile } from 'node:fs/promises'
import path from 'node:path'
import * as yaml from 'js-yaml'
import { getNoteFromMarkdown } from 'yanki'

const dir = process.argv[2]
if (!dir) {
	console.error('Usage: node validate-quiz-bank.mjs <dir>')
	process.exit(1)
}

const ALLOWED_MODELS = new Set(['Yanki - Basic'])

function splitFrontmatter(raw) {
	const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
	if (!match) return { frontmatter: null, body: raw }
	return { frontmatter: match[1], body: match[2] }
}

async function validateFile(filePath) {
	const errors = []
	const raw = await readFile(filePath, 'utf8')
	const { frontmatter, body } = splitFrontmatter(raw)

	if (frontmatter === null) {
		errors.push('missing frontmatter block')
		return errors
	}

	let parsed
	try {
		parsed = yaml.load(frontmatter)
	} catch (err) {
		errors.push(`frontmatter is not valid YAML: ${err.message}`)
		parsed = null
	}

	if (parsed) {
		const tags = parsed.tags
		if (!Array.isArray(tags) || tags.length === 0) {
			errors.push('frontmatter missing tags array')
		} else if (!tags.some((t) => String(t).startsWith('repo-'))) {
			errors.push('tags array missing a repo-* tag')
		}
	}

	const parts = body.trim().split(/\n---\n/)
	if (parts.length !== 2) {
		errors.push(
			`expected exactly one "---" separator splitting front/back, found ${parts.length - 1}`,
		)
	} else {
		const [front, back] = parts
		if (front.trim().length === 0) errors.push('front (question) is empty')
		if (back.trim().length === 0) errors.push('back (answer) is empty')
	}

	try {
		const note = await getNoteFromMarkdown(raw)
		if (!ALLOWED_MODELS.has(note.modelName)) {
			errors.push(
				`inferred as note type "${note.modelName}", expected one of: ${[...ALLOWED_MODELS].join(', ')} (check for stray ~~strikethrough~~ or trailing _emphasis_ triggering a different type)`,
			)
		}
	} catch (err) {
		errors.push(`yanki parser threw: ${err.message}`)
	}

	return errors
}

const files = (await readdir(dir)).filter((f) => f.endsWith('.md'))
if (files.length === 0) {
	console.error(`No .md files found in ${dir}`)
	process.exit(1)
}

let failCount = 0
for (const file of files) {
	const filePath = path.join(dir, file)
	const errors = await validateFile(filePath)
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
