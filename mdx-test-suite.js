#!/usr/bin/env node

import { compile } from '@mdx-js/mdx'
import { readFileSync, writeFileSync, statSync } from 'fs'
import { resolve, relative, basename, dirname } from 'path'
import glob from 'fast-glob'
import chalk from 'chalk'
import os from 'os'
import crypto from 'crypto'

// Cool ASCII art banner
const banner = `
${chalk.cyan('╔═══════════════════════════════════════════════════════════════╗')}
${chalk.cyan('║')}  ${chalk.bold.magenta('███╗   ███╗██████╗ ██╗  ██╗')}    ${chalk.bold.yellow('████████╗███████╗███████╗████████╗')}  ${chalk.cyan('║')}
${chalk.cyan('║')}  ${chalk.bold.magenta('████╗ ████║██╔══██╗╚██╗██╔╝')}    ${chalk.bold.yellow('╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝')}  ${chalk.cyan('║')}
${chalk.cyan('║')}  ${chalk.bold.magenta('██╔████╔██║██║  ██║ ╚███╔╝')}     ${chalk.bold.yellow('   ██║   █████╗  ███████╗   ██║')}     ${chalk.cyan('║')}
${chalk.cyan('║')}  ${chalk.bold.magenta('██║╚██╔╝██║██║  ██║ ██╔██╗')}     ${chalk.bold.yellow('   ██║   ██╔══╝  ╚════██║   ██║')}     ${chalk.cyan('║')}
${chalk.cyan('║')}  ${chalk.bold.magenta('██║ ╚═╝ ██║██████╔╝██╔╝ ██╗')}    ${chalk.bold.yellow('   ██║   ███████╗███████║   ██║')}     ${chalk.cyan('║')}
${chalk.cyan('║')}  ${chalk.bold.magenta('╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝')}    ${chalk.bold.yellow('   ╚═╝   ╚══════╝╚══════╝   ╚═╝')}     ${chalk.cyan('║')}
${chalk.cyan('╚═══════════════════════════════════════════════════════════════╝')}
                    ${chalk.gray('🚀 Ultra Verbose Edition™ 🚀')}
`

// Fun loading messages
const loadingMessages = [
  '🔍 Scanning for markdown files...',
  '🧪 Preparing test environment...',
  '☕ Brewing some coffee...',
  '🎯 Targeting files for validation...',
  '🔬 Initializing MDX compiler...',
  '🌈 Adding some color to your terminal...',
  '🎨 Painting the output pretty...',
  '🚦 Starting validation engines...',
  '⚡ Charging up the processors...',
  '🎪 Welcome to the MDX circus!'
]

// Fun facts to display during processing
const funFacts = [
  '💡 Did you know? MDX combines Markdown with JSX!',
  '🎓 Fun fact: MDX was created by the unified collective',
  '🌟 Pro tip: You can import React components in MDX files',
  '🔥 Hot take: MDX is the future of documentation',
  '🦄 Magic fact: MDX supports frontmatter out of the box',
  '🎯 Tip: Use .mdx extension for better editor support',
  '⚡ Speed tip: MDX compiles to highly optimized JavaScript',
  '🌈 Fun: MDX stands for Markdown eXtended',
  '🚀 Fact: MDX v2 is significantly faster than v1',
  '🎨 Design tip: MDX allows for dynamic documentation'
]

// Get a random item from array
const getRandom = (arr) => arr[Math.floor(Math.random() * arr.length)]

// Progress bar creator
const createProgressBar = (current, total, width = 30) => {
  const percentage = Math.round((current / total) * 100)
  const filled = Math.round((current / total) * width)
  const empty = width - filled
  const bar = chalk.green('█').repeat(filled) + chalk.gray('░').repeat(empty)
  return `${bar} ${percentage}%`
}

// Simple test: can the file compile as MDX?
async function testFile(filepath, vlog) {
  try {
    vlog(`📄 Opening file: ${chalk.blue(basename(filepath))}`)
    const content = readFileSync(filepath, 'utf-8')
    vlog(`📏 File metrics:`)
    vlog(`   • Size: ${chalk.yellow(content.length.toLocaleString())} characters`)
    vlog(`   • Lines: ${chalk.yellow(content.split('\n').length.toLocaleString())}`)
    vlog(`   • Hash: ${chalk.gray(crypto.createHash('md5').update(content).digest('hex').substring(0, 8))}`)
    
    vlog(`🔧 Compiling with MDX engine...`)
    await compile(content, {
      format: 'mdx',
      development: false
    })
    
    vlog(`✅ ${chalk.green('Compilation successful!')} File is valid MDX 🎉`)
    return { file: filepath, valid: true }
  } catch (error) {
    vlog(`❌ ${chalk.red('Compilation failed!')} 😱`)
    vlog(`🐛 Error details:`)
    vlog(`   • Type: ${chalk.red(error.constructor.name)}`)
    vlog(`   • Message: ${chalk.yellow(error.message)}`)
    if (error.position) {
      vlog(`   • Location: Line ${chalk.cyan(error.position.start?.line)}, Column ${chalk.cyan(error.position.start?.column)}`)
    }
    
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
  const input = args.find(arg => !arg.startsWith('--') && arg !== '-v')
  const outputFile = args.find(arg => arg.startsWith('--output='))?.split('=')[1] || 'mdx-test-report.json'
  const verbose = args.includes('--verbose') || args.includes('-v')
  
  // Start time for total execution
  const totalStartTime = Date.now()
  
  // Verbose logging helper with emojis
  const vlog = (...args) => {
    if (verbose) {
      console.log(chalk.gray('[VERBOSE]'), ...args)
    }
  }
  
  // Show banner in verbose mode
  if (verbose) {
    console.log(banner)
    console.log(chalk.gray('═'.repeat(67)))
    
    // System information
    console.log(chalk.bold.cyan('\n🖥️  System Information:'))
    console.log(`   • ${chalk.yellow('OS:')} ${os.type()} ${os.release()} (${os.platform()})`)
    console.log(`   • ${chalk.yellow('CPU:')} ${os.cpus()[0].model}`)
    console.log(`   • ${chalk.yellow('Cores:')} ${os.cpus().length}`)
    console.log(`   • ${chalk.yellow('Memory:')} ${Math.round(os.totalmem() / 1024 / 1024 / 1024)}GB total, ${Math.round(os.freemem() / 1024 / 1024 / 1024)}GB free`)
    console.log(`   • ${chalk.yellow('Node:')} ${process.version}`)
    console.log(`   • ${chalk.yellow('V8:')} ${process.versions.v8}`)
    console.log(`   • ${chalk.yellow('User:')} ${os.userInfo().username}`)
    console.log(`   • ${chalk.yellow('PID:')} ${process.pid}`)
    console.log(`   • ${chalk.yellow('CWD:')} ${process.cwd()}`)
    
    console.log(chalk.gray('═'.repeat(67)))
  }
  
  vlog(`\n🚀 ${chalk.bold('MDX Test Suite initialized!')}`)
  vlog(`📅 Started at: ${chalk.cyan(new Date().toLocaleString())}`)
  vlog(`🎲 Session ID: ${chalk.gray(crypto.randomBytes(6).toString('hex'))}`)
  vlog(`📝 Arguments received: ${chalk.yellow(JSON.stringify(args))}`)
  vlog(`🎯 Input target: ${chalk.blue(input || 'none')}`)
  vlog(`💾 Output file: ${chalk.green(outputFile)}`)
  vlog(`🔊 Verbose mode: ${verbose ? chalk.green('ACTIVATED 📢') : chalk.gray('disabled 🔇')}`)
  
  if (!input || input === '--help' || input === '-h') {
    vlog('ℹ️  Help requested or no input provided')
    console.log(`
${chalk.bold('MDX Test Suite')} ${chalk.gray('- Ultra Verbose Edition™')}

${chalk.italic('Simple MDX validation: tests if markdown files can be compiled as MDX.')}

${chalk.yellow('Usage:')}
  node mdx-test-suite.js <file-or-directory> [options]

${chalk.yellow('Options:')}
  --output=<file>  Specify output file for JSON report (default: mdx-test-report.json)
  --verbose, -v    Enable ultra verbose logging with emojis! 🎉

${chalk.yellow('Examples:')}
  node mdx-test-suite.js docs/                    # Test all .md/.mdx files in docs/
  node mdx-test-suite.js docs/guide/intro.md      # Test a single file
  node mdx-test-suite.js "docs/**/*.mdx"          # Test using glob pattern
  node mdx-test-suite.js docs/ --output=test.json # Custom output file
  node mdx-test-suite.js docs/ --verbose          # Run with verbose logging 🚀

${chalk.gray('Made with ❤️  by your friendly neighborhood developers')}
`)
    vlog('👋 Exiting gracefully with code 0')
    process.exit(0)
  }

  // Show random loading message
  if (verbose) {
    console.log(chalk.dim(`\n${getRandom(loadingMessages)}`))
    await new Promise(resolve => setTimeout(resolve, 500)) // Dramatic pause
  }
  
  // Determine what files to test
  let files = []
  vlog(`\n🔍 ${chalk.bold('Starting file discovery phase...')}`)
  
  try {
    vlog('📊 Analyzing input path...')
    const stats = statSync(input)
    vlog('📈 File statistics retrieved:')
    vlog(`   • Type: ${stats.isDirectory() ? '📁 Directory' : '📄 File'}`)
    vlog(`   • Size: ${chalk.yellow(stats.size.toLocaleString())} bytes`)
    vlog(`   • Created: ${chalk.gray(stats.birthtime.toLocaleString())}`)
    vlog(`   • Modified: ${chalk.gray(stats.mtime.toLocaleString())}`)
    vlog(`   • Permissions: ${chalk.gray(stats.mode.toString(8))}`)
    
    if (stats.isDirectory()) {
      vlog(`\n🗂️  ${chalk.bold('Directory mode activated!')}`)
      vlog('🔎 Search parameters:')
      vlog(`   • Patterns: ${chalk.green('["**/*.md", "**/*.mdx"]')}`)
      vlog(`   • Base directory: ${chalk.blue(input)}`)
      vlog(`   • Exclusions: ${chalk.red('["node_modules/**", ".git/**"]')}`)
      
      // Show searching animation
      if (verbose) {
        process.stdout.write('   🔄 Searching')
        const searchInterval = setInterval(() => process.stdout.write('.'), 100)
        
        files = await glob(['**/*.md', '**/*.mdx'], {
          cwd: input,
          absolute: true,
          ignore: ['node_modules/**', '.git/**']
        })
        
        clearInterval(searchInterval)
        console.log(' Done! ✅')
      } else {
        files = await glob(['**/*.md', '**/*.mdx'], {
          cwd: input,
          absolute: true,
          ignore: ['node_modules/**', '.git/**']
        })
      }
      
      vlog(`\n📊 ${chalk.bold('Search Results:')}`)
      vlog(`   • Total files found: ${chalk.green(files.length)}`)
      vlog(`   • Search completed in: ${chalk.yellow(Date.now() - totalStartTime + 'ms')}`)
      
      if (verbose && files.length > 0) {
        console.log(chalk.gray('\n📋 File list:'))
        files.forEach((file, i) => {
          const icon = file.endsWith('.mdx') ? '🎨' : '📝'
          console.log(chalk.gray(`   ${icon} [${(i + 1).toString().padStart(3, '0')}] ${relative(process.cwd(), file)}`))
        })
      }
    } else if (stats.isFile()) {
      vlog('📄 Single file mode detected')
      files = [resolve(input)]
      vlog(`   • Absolute path: ${chalk.blue(files[0])}`)
      vlog(`   • Extension: ${chalk.yellow(files[0].split('.').pop())}`)
    }
  } catch (err) {
    vlog(`\n⚠️  ${chalk.yellow('Primary detection failed, falling back to glob mode')}`)
    vlog(`🔧 Error was: ${chalk.red(err.message)}`)
    vlog('🌟 Attempting glob pattern interpretation...')
    
    files = await glob(input, {
      absolute: true,
      ignore: ['node_modules/**', '.git/**']
    })
    
    vlog(`✨ Glob search complete! Found ${chalk.green(files.length)} files`)
  }

  if (files.length === 0) {
    vlog('😱 No files found! This is not good...')
    console.error(chalk.red.bold(`\n❌ No files found matching: ${input}`))
    console.error(chalk.gray('💡 Tip: Check your path and try again!'))
    process.exit(1)
  }

  // Pre-test summary
  console.log(chalk.blue.bold(`\n🎯 Testing ${files.length} file(s)...\n`))
  
  if (verbose) {
    console.log(chalk.gray('═'.repeat(67)))
    console.log(chalk.cyan('🏁 Starting validation marathon! Let\'s go! 🏃‍♂️💨'))
    console.log(chalk.gray('═'.repeat(67)))
  }

  // Test all files
  const results = []
  let lastFunFactIndex = 0
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    
    if (verbose) {
      // Show fun fact every 5 files
      if (i > 0 && i % 5 === 0) {
        console.log(chalk.dim(`\n${funFacts[lastFunFactIndex % funFacts.length]}\n`))
        lastFunFactIndex++
      }
      
      console.log(chalk.gray(`\n${'─'.repeat(67)}`))
      console.log(`📦 ${chalk.bold(`Processing file ${i + 1} of ${files.length}`)} ${createProgressBar(i + 1, files.length)}`)
      console.log(chalk.gray(`${'─'.repeat(67)}`))
      vlog('🏷️  File details:')
      vlog(`   • Full path: ${chalk.blue(file)}`)
      vlog(`   • Basename: ${chalk.yellow(basename(file))}`)
      vlog(`   • Directory: ${chalk.gray(dirname(file))}`)
      vlog(`   • Relative: ${chalk.green(relative(process.cwd(), file))}`)
      vlog(`   • Extension: ${chalk.magenta(file.split('.').pop())}`)
    }
    
    process.stdout.write(`${chalk.gray(`[${(i + 1).toString().padStart(3, '0')}/${files.length}]`)} Testing ${chalk.cyan(basename(file))}... `)
    
    const fileStartTime = Date.now()
    vlog(`\n⏱️  Starting test at: ${new Date().toLocaleTimeString()}`)
    
    const result = await testFile(file, vlog)
    const testDuration = Date.now() - fileStartTime
    
    vlog(`⏱️  Test duration: ${chalk.yellow(testDuration + 'ms')}`)
    
    results.push(result)
    
    if (result.valid) {
      console.log(chalk.green('✅ PASS'))
      vlog('🎉 File validation: ' + chalk.green.bold('SUCCESS'))
    } else {
      console.log(chalk.red('❌ FAIL'))
      vlog('💥 File validation: ' + chalk.red.bold('FAILED'))
    }
    
    if (verbose) {
      vlog(`💾 Memory usage: ${JSON.stringify({
        heapUsed: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + 'MB',
        heapTotal: Math.round(process.memoryUsage().heapTotal / 1024 / 1024) + 'MB',
        rss: Math.round(process.memoryUsage().rss / 1024 / 1024) + 'MB'
      })}`)
      vlog(`📊 Progress: ${chalk.green(results.filter(r => r.valid).length)} passed, ${chalk.red(results.filter(r => !r.valid).length)} failed`)
    }
  }

  // Calculate summary
  const validCount = results.filter(r => r.valid).length
  const invalidCount = results.filter(r => !r.valid).length
  const successRate = ((validCount / files.length) * 100).toFixed(2)
  
  if (verbose) {
    console.log(chalk.gray(`\n${'═'.repeat(67)}`))
    console.log(chalk.bold.cyan('📊 FINAL RESULTS'))
    console.log(chalk.gray(`${'═'.repeat(67)}`))
  } else {
    console.log(chalk.bold('\n--- Summary ---'))
  }
  
  // Display fancy summary
  if (verbose) {
    console.log(`\n   ${chalk.green('✅ Passed:')} ${validCount} file${validCount !== 1 ? 's' : ''}`)
    console.log(`   ${chalk.red('❌ Failed:')} ${invalidCount} file${invalidCount !== 1 ? 's' : ''}`)
    console.log(`   ${chalk.blue('📁 Total:')} ${files.length} file${files.length !== 1 ? 's' : ''}`)
    console.log(`   ${chalk.yellow('📈 Success Rate:')} ${successRate}%`)
    console.log(`   ${chalk.magenta('⏱️  Total Time:')} ${((Date.now() - totalStartTime) / 1000).toFixed(2)}s`)
    
    // ASCII success/fail meter
    const meterWidth = 50
    const successBlocks = Math.round((validCount / files.length) * meterWidth)
    const failBlocks = meterWidth - successBlocks
    console.log(`\n   ${chalk.bold('Success Meter:')}`)
    console.log(`   [${chalk.green('█'.repeat(successBlocks))}${chalk.red('█'.repeat(failBlocks))}]`)
    
    // Grade the results
    let grade, gradeColor, gradeEmoji
    if (successRate >= 95) {
      grade = 'A+'; gradeColor = chalk.green; gradeEmoji = '🌟'
    } else if (successRate >= 90) {
      grade = 'A'; gradeColor = chalk.green; gradeEmoji = '⭐'
    } else if (successRate >= 80) {
      grade = 'B'; gradeColor = chalk.yellow; gradeEmoji = '👍'
    } else if (successRate >= 70) {
      grade = 'C'; gradeColor = chalk.yellow; gradeEmoji = '🤔'
    } else if (successRate >= 60) {
      grade = 'D'; gradeColor = chalk.red; gradeEmoji = '😬'
    } else {
      grade = 'F'; gradeColor = chalk.red; gradeEmoji = '💀'
    }
    
    console.log(`\n   ${chalk.bold('Grade:')} ${gradeColor.bold(grade)} ${gradeEmoji}`)
    
  } else {
    console.log(chalk.green(`✓ Valid: ${validCount}`))
    console.log(chalk.red(`✗ Invalid: ${invalidCount}`))
    console.log(chalk.blue(`Total: ${files.length}`))
  }

  if (invalidCount > 0) {
    console.log(chalk.bold(`\n${verbose ? '🚨 Failed Files Report 🚨' : '--- Failed Files ---'}`))
    results.filter(r => !r.valid).forEach((result, idx) => {
      console.log(chalk.red(`\n${verbose ? '❌' : '✗'} ${relative(process.cwd(), result.file)}`))
      console.log(`  ${verbose ? '💬' : ''} Error: ${result.error}`)
      if (result.line) {
        console.log(`  ${verbose ? '📍' : ''} Location: Line ${result.line}, Column ${result.column}`)
      }
      if (verbose) {
        console.log(chalk.gray(`  💡 Tip: Check for JSX syntax errors or unclosed tags`))
      }
    })
  }

  // Create report
  vlog(`\n📝 ${chalk.bold('Generating test report...')}`)
  const report = {
    timestamp: new Date().toISOString(),
    duration: Date.now() - totalStartTime + 'ms',
    environment: verbose ? {
      node: process.version,
      platform: os.platform(),
      arch: os.arch(),
      cpus: os.cpus().length,
      memory: Math.round(os.totalmem() / 1024 / 1024 / 1024) + 'GB'
    } : undefined,
    summary: {
      total: files.length,
      valid: validCount,
      invalid: invalidCount,
      successRate: parseFloat(successRate)
    },
    results: results.map(r => ({
      file: relative(process.cwd(), r.file),
      valid: r.valid,
      error: r.error || null,
      location: r.line ? { line: r.line, column: r.column } : null
    }))
  }
  
  if (verbose) {
    vlog('📄 Report preview:')
    vlog(chalk.gray(JSON.stringify(report, null, 2).substring(0, 500) + '...'))
    vlog(`📏 Report size: ${chalk.yellow(JSON.stringify(report).length.toLocaleString())} bytes`)
  }

  // Write report with style
  vlog(`\n💾 ${chalk.bold('Saving report to disk...')}`)
  writeFileSync(outputFile, JSON.stringify(report, null, 2))
  
  console.log(chalk.dim(`\n📋 Report saved to: ${outputFile}`))
  
  if (verbose) {
    console.log(chalk.gray(`\n${'═'.repeat(67)}`))
    console.log(chalk.bold.cyan('🎬 TEST SUITE COMPLETE!'))
    console.log(chalk.gray(`${'═'.repeat(67)}`))
    
    // Fun exit messages based on results
    if (successRate === '100.00') {
      console.log(chalk.green.bold('\n🎉 PERFECT SCORE! You\'re an MDX wizard! 🧙‍♂️✨'))
    } else if (successRate >= '90') {
      console.log(chalk.green('\n👏 Great job! Your MDX files are looking good!'))
    } else if (successRate >= '70') {
      console.log(chalk.yellow('\n💪 Not bad! A few files need attention.'))
    } else {
      console.log(chalk.red('\n😅 Looks like there\'s some work to do!'))
    }
    
    console.log(chalk.gray(`\n👋 Thanks for using MDX Test Suite!`))
    console.log(chalk.gray(`⭐ Star us on GitHub: https://github.com/your-repo/mdx-test-suite`))
  }

  // Exit with appropriate code
  const exitCode = invalidCount > 0 ? 1 : 0
  vlog(`\n🚪 Exiting with code: ${exitCode === 0 ? chalk.green(exitCode) : chalk.red(exitCode)}`)
  process.exit(exitCode)
}

// Main execution with enhanced error handling
const startTime = Date.now()
main().catch(error => {
  console.error(chalk.red.bold('\n💥 FATAL ERROR 💥'))
  console.error(chalk.red('Error:'), error.message)
  
  if (process.argv.includes('--verbose') || process.argv.includes('-v')) {
    console.log(chalk.gray('\n🔍 Error Details:'))
    console.log(chalk.gray('   • Type:'), error.constructor.name)
    console.log(chalk.gray('   • Stack trace:'))
    console.log(chalk.gray(error.stack.split('\n').map(line => '     ' + line).join('\n')))
    console.log(chalk.gray(`   • Occurred after: ${Date.now() - startTime}ms`))
    console.log(chalk.gray('\n💡 Tip: Check your Node.js version and dependencies'))
  }
  
  console.log(chalk.red('\n😵 Test suite crashed! Exiting...'))
  process.exit(1)
}) 