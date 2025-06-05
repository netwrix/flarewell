#!/usr/bin/env node

import { compile } from '@mdx-js/mdx'
import { readFileSync, writeFileSync, statSync } from 'fs'
import { resolve, relative, basename } from 'path'
import glob from 'fast-glob'

// Simple test: can the file compile as MDX?
async function testFile(filepath) {
  try {
    const content = readFileSync(filepath, 'utf-8')
    await compile(content, {
      format: 'mdx',
      development: false
    })
    return { file: filepath, valid: true }
  } catch (error) {
    return {
      file: filepath,
      valid: false,
      error: error.message,
      line: error.position?.start?.line || null,
      column: error.position?.start?.column || null
    }
  }
}

async function main() {
  const args = process.argv.slice(2)
  const input = args.find(arg => !arg.startsWith('--'))
  const outputFile = args.find(arg => arg.startsWith('--output='))?.split('=')[1] || 'mdx-test-report.json'
  
  if (!input || input === '--help' || input === '-h') {
    console.log(`
MDX Test Suite

Tests if markdown files can be compiled as MDX.

Usage:
  node mdx-test-suite.js <directory> [options]

Options:
  --output=<file>  Specify output file for JSON report (default: mdx-test-report.json)
  --help, -h       Show this help message

Examples:
  node mdx-test-suite.js docs/
  node mdx-test-suite.js docs/ --output=test.json
`)
    process.exit(0)
  }

  // Find all markdown files in directory and subdirectories
  let files = []
  
  try {
    const stats = statSync(input)
    
    if (stats.isDirectory()) {
      files = await glob(['**/*.md', '**/*.mdx'], {
        cwd: input,
        absolute: true,
        ignore: ['node_modules/**', '.git/**']
      })
    } else if (stats.isFile()) {
      files = [resolve(input)]
    }
  } catch (err) {
    // Try as glob pattern
    files = await glob(input, {
      absolute: true,
      ignore: ['node_modules/**', '.git/**']
    })
  }

  if (files.length === 0) {
    console.error(`No files found in: ${input}`)
    process.exit(1)
  }

  console.log(`Testing ${files.length} file(s)...\n`)

  // Test all files
  const results = []
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    process.stdout.write(`[${i + 1}/${files.length}] Testing ${basename(file)}... `)
    
    const result = await testFile(file)
    results.push(result)
    
    if (result.valid) {
      console.log('PASS')
    } else {
      console.log('FAIL')
    }
  }

  // Calculate summary
  const validCount = results.filter(r => r.valid).length
  const invalidCount = results.filter(r => !r.valid).length
  
  console.log('\n--- Summary ---')
  console.log(`Valid: ${validCount}`)
  console.log(`Invalid: ${invalidCount}`)
  console.log(`Total: ${files.length}`)

  if (invalidCount > 0) {
    console.log('\n--- Failed Files ---')
    results.filter(r => !r.valid).forEach(result => {
      console.log(`\n${relative(process.cwd(), result.file)}`)
      console.log(`  Error: ${result.error}`)
      if (result.line) {
        console.log(`  Location: Line ${result.line}, Column ${result.column}`)
      }
    })
  }

  // Create report
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      total: files.length,
      valid: validCount,
      invalid: invalidCount
    },
    results: results.map(r => ({
      file: relative(process.cwd(), r.file),
      valid: r.valid,
      error: r.error || null,
      location: r.line ? { line: r.line, column: r.column } : null
    }))
  }

  // Write report
  writeFileSync(outputFile, JSON.stringify(report, null, 2))
  console.log(`\nReport saved to: ${outputFile}`)

  // Exit with appropriate code
  process.exit(invalidCount > 0 ? 1 : 0)
}

// Run the test suite
main().catch(error => {
  console.error('Error:', error.message)
  process.exit(1)
}) 