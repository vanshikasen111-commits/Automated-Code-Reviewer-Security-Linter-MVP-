const { spawn } = require('child_process');
const path = require('path');
const os = require('os');
const fs = require('fs');

// Detect Python executable path (user install or system PATH)
const winUserPy = path.join(os.homedir(), 'AppData', 'Local', 'Programs', 'Python', 'Python311', 'python.exe');
const pythonCmd = fs.existsSync(winUserPy) ? winUserPy : 'python';

const args = process.argv.slice(2);
const targetArgs = args.length > 0 ? args : ['main.py', 'example_test.py'];

const child = spawn(pythonCmd, targetArgs, {
  stdio: 'inherit',
  shell: false
});

child.on('exit', (code) => {
  process.exit(code !== null ? code : 0);
});

child.on('error', (err) => {
  console.error('Failed to start Python process:', err);
  process.exit(1);
});

