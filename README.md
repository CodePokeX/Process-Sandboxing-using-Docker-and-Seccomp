# 🛡️ Process Sandboxing Tool

A lightweight **sandboxing utility** designed for runtime process isolation using Docker. This tool allows you to **extract a running process by its PID**, encapsulate it in a Docker container, and apply a **custom Seccomp profile** to restrict its system calls—effectively **removing it from the host system** while maintaining controlled execution.

> ⚙️ **Built With:** Python · Docker · Seccomp

---

## 🚀 Features

- ✅ Containerizes a live process by PID
- ✅ Isolates the process from the host system
- ✅ Applies a custom Seccomp profile for syscall filtering
- ✅ Supports custom executables with minimal configuration
- ✅ Simple and extensible Python codebase

---


---

## ⚙️ How It Works

1. Accepts a PID of a running process.
2. Gathers the required file or script associated with that process.
3. If `flagged_file.py` is not found, it needs to be **copied** from `flagged_file.txt`.
4. Launches a Docker container, isolates the process inside it.
5. Applies a **Seccomp profile** to restrict dangerous or unneeded system calls.

---

## 🧑‍💻 How to Use

> ✅ Prerequisite: Ensure Docker is installed and running on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sandboxing-tool.git
cd sandboxing-tool
```

### 2. Ensure flagged_file.py Exists

- If it's not already present, the tool will automatically generate flagged_file.py from flagged_file.txt.

Or create it manually:

```bash
cp flagged_file.txt flagged_file.py
```

### 3. Install psutil

- Make a new python virtual environment and then install psutil

```bash
pip install psutil
```

### 4. Run sandbox_launcher.py

```bash
python sandbox_launcher.py
```

## 🛠️ Custom File Support

- You can sandbox other types of executables by doing the following:

    - Replace flagged_file.py with your desired file.

    - Modify sandbox_launcher.py accordingly to reference the new filename and   update Docker command if needed.

    - Run the tool as usual.

## 🔐 Security

- This project leverages:

    - 🐳 Docker containerization for runtime isolation

    - 🔒 Seccomp syscall filtering for fine-grained control over allowed operations

- To further tighten security, review and customize the seccomp_profile.json according to your specific requirements.


