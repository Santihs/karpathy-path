import assert from 'node:assert/strict'
import { test } from 'node:test'
import { splitFrontmatter, validateFile } from './validate-quiz-bank-lib.mjs'

const validCard = `---
tags:
  - repo-karpathy
  - phase-0
---
What is a vector?

---

An element of a vector space.

Ref: \`02-Topics/foo.md\`
`

test('splitFrontmatter: no frontmatter block returns null', () => {
	const { frontmatter, body } = splitFrontmatter('just some text, no frontmatter')
	assert.equal(frontmatter, null)
	assert.equal(body, 'just some text, no frontmatter')
})

test('splitFrontmatter: parses frontmatter and body separately', () => {
	const { frontmatter, body } = splitFrontmatter(validCard)
	assert.match(frontmatter, /repo-karpathy/)
	assert.match(body, /What is a vector\?/)
})

test('validateFile: valid card produces no errors', async () => {
	const errors = await validateFile(validCard)
	assert.deepEqual(errors, [])
})

test('validateFile: missing frontmatter block', async () => {
	const errors = await validateFile('no frontmatter here\n\n---\n\nback')
	assert.deepEqual(errors, ['missing frontmatter block'])
})

test('validateFile: invalid YAML frontmatter', async () => {
	const raw = `---\ntags: [unclosed\n---\nfront\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.startsWith('frontmatter is not valid YAML')))
})

test('validateFile: missing tags array', async () => {
	const raw = `---\nnoteId: 123\n---\nfront\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.includes('frontmatter missing tags array'))
})

test('validateFile: empty tags array', async () => {
	const raw = `---\ntags: []\n---\nfront\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.includes('frontmatter missing tags array'))
})

test('validateFile: tags present but missing repo-* tag', async () => {
	const raw = `---\ntags: [phase-0]\n---\nfront\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.includes('tags array missing a repo-* tag'))
})

test('validateFile: no "---" separator between front and back', async () => {
	const raw = `---\ntags: [repo-karpathy]\n---\njust one block, no separator\n`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.includes('found 0')))
})

test('validateFile: more than one "---" separator', async () => {
	const raw = `---\ntags: [repo-karpathy]\n---\nfront\n\n---\n\nmiddle\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.includes('found 2')))
})

// NOTE: a truly blank front/back can't reach the "is empty" checks below —
// body.trim() strips the leading/trailing newline the "\n---\n" separator
// regex needs, so it falls into the "found 0 separators" branch instead.
// These two tests document that actual (surprising) behavior rather than
// the intended one; see PR notes for the reachability gap this exposes.
test('validateFile: blank front collapses into a missing-separator error, not "front is empty"', async () => {
	const raw = `---\ntags: [repo-karpathy]\n---\n\n---\n\nback\n`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.includes('found 0')))
	assert.ok(!errors.includes('front (question) is empty'))
})

test('validateFile: blank back collapses into a missing-separator error, not "back is empty"', async () => {
	const raw = `---\ntags: [repo-karpathy]\n---\nfront\n\n---\n\n\n`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.includes('found 0')))
	assert.ok(!errors.includes('back (answer) is empty'))
})

test('validateFile: stray strikethrough triggers wrong note-type error', async () => {
	const raw = `---
tags:
  - repo-karpathy
---
Is ~~this~~ a cloze?

---

No, it just has stray strikethrough.
`
	const errors = await validateFile(raw)
	assert.ok(errors.some((e) => e.includes('inferred as note type')))
})
