const fs = require('fs');
if (!fs.existsSync('docs')) {
  console.error('Docs folder not found');
  process.exit(1);
}
console.log('Build completed');
