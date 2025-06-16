# file_types.py

COMMON_FILE_TYPES = {
    '.py': 'python',           # Python scripts
    '.sh': 'bash',             # Bash scripts
    '.pl': 'perl',             # Perl scripts
    '.js': 'nodejs',           # JavaScript (Node.js) scripts
    '.rb': 'ruby',             # Ruby scripts
    '.php': 'php',             # PHP scripts
    '.html': 'html',           # HTML files (though not executable, can be sandboxed)
    '.css': 'css',             # CSS files (non-executable but can be sandboxed)
    '.c': 'c',                 # C source files
    '.cpp': 'cpp',             # C++ source files
    '.h': 'cpp_header',        # C/C++ header files
    '.java': 'java',           # Java source files
    '.go': 'go',               # Go source files
    '.exe': 'binary',          # Windows executables
    '.bin': 'binary',          # Generic binary files
    '.out': 'binary',          # Compiled output (could be binary)
    '.apk': 'apk',             # Android application files
    '.deb': 'deb',             # Debian package files
    '.rpm': 'rpm',             # RPM package files
    '.tar': 'tarball',         # Tarballs (often used in Linux systems)
    '.zip': 'zip',             # Zip archives
    '.gz': 'gzip',             # Gzip archives
    '.tar.gz': 'tarball',      # Tarballs with gzip compression
    '.pdf': 'document',        # PDF files
    '.txt': 'text',            # Text files
    '.log': 'log',             # Log files
}

# Define the install and command templates for each file type
FILE_TYPES = {
    "python": {"install": "RUN apk add --no-cache python3 py3-pip", "cmd": "CMD [\"python3\", \"{script_name}\"]"},
    "bash": {"install": "RUN apk add --no-cache bash", "cmd": "CMD [\"bash\", \"{script_name}\"]"},
    "perl": {"install": "RUN apk add --no-cache perl", "cmd": "CMD [\"perl\", \"{script_name}\"]"},
    "nodejs": {"install": "RUN apk add --no-cache nodejs npm", "cmd": "CMD [\"node\", \"{script_name}\"]"},
    "ruby": {"install": "RUN apk add --no-cache ruby", "cmd": "CMD [\"ruby\", \"{script_name}\"]"},
    "php": {"install": "RUN apk add --no-cache php", "cmd": "CMD [\"php\", \"{script_name}\"]"},
    "html": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'HTML file detected, manually handle this file.'\"]"},
    "css": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'CSS file detected, manually handle this file.'\"]"},
    "c": {"install": "RUN apk add --no-cache gcc", "cmd": "CMD [\"gcc\", \"{script_name}\", \"-o\", \"output\", \"&&\", \"./output\"]"},
    "cpp": {"install": "RUN apk add --no-cache g++", "cmd": "CMD [\"g++\", \"{script_name}\", \"-o\", \"output\", \"&&\", \"./output\"]"},
    "cpp_header": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'C/C++ header file detected, manually handle this file.'\"]"},
    "java": {"install": "RUN apk add --no-cache openjdk11", "cmd": "CMD [\"java\", \"{script_name}\"]"},
    "go": {"install": "RUN apk add --no-cache go", "cmd": "CMD [\"go\", \"run\", \"{script_name}\"]"},
    "binary": {"install": "", "cmd": "CMD [\"./{script_name}\"]"},
    "apk": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'APK file detected, manually handle this file.'\"]"},
    "deb": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Debian package detected, manually handle this file.'\"]"},
    "rpm": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'RPM package detected, manually handle this file.'\"]"},
    "tarball": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Tarball file detected, manually handle this file.'\"]"},
    "zip": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Zip archive detected, manually handle this file.'\"]"},
    "gzip": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Gzip file detected, manually handle this file.'\"]"},
    "document": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Document file detected, manually handle this file.'\"]"},
    "text": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Text file detected, manually handle this file.'\"]"},
    "log": {"install": "", "cmd": "CMD [\"sh\", \"-c\", \"echo 'Log file detected, manually handle this file.'\"]"},
}
