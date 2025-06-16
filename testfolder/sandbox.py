import os
import shutil
import psutil # type: ignore
import subprocess
import uuid
import logging
from file_types import COMMON_FILE_TYPES, FILE_TYPES # type: ignore


MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(MAIN_DIR, "sandbox_log.txt")
SECCOMP_PROFILE_PATH = os.path.join(MAIN_DIR, "seccomp_profile.json")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def get_process_info(pid):
    try:
        p = psutil.Process(pid)
        process_info = {
            "exe": p.exe(),
            "args": p.cmdline(),
            "cwd": p.cwd(),
            "status": p.status(),
            "name": p.name(),
            "pid": p.pid,
            "parent_pid": p.ppid(),
            "create_time": p.create_time(),
            "open_files": p.open_files(),
            "connections": p.connections(),
            "threads": p.threads(),
            "memory_percent": p.memory_percent(),
            "cpu_percent": p.cpu_percent(interval=0.1),
        }

        print(f" Process Information for PID {pid}:")
        logger.info(f" Process Information for PID {pid}:")
        for key, value in process_info.items():
            print(f"{key}: {value}")
            logger.info(f"{key}: {value}")

        return process_info

    except psutil.NoSuchProcess:
        print(f" Process with PID {pid} not found.")
        logger.error(f"Process with PID {pid} not found.")
        return None
    except Exception as e:
        print(f" Error retrieving process info: {e}")
        logger.error(f" Error retrieving process info: {e}")
        return None


def determine_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return COMMON_FILE_TYPES.get(file_extension, 'unknown')


def write_dockerfile(script_name, folder, file_type):
    if file_type == 'unknown' or file_type not in FILE_TYPES:
        raise ValueError(f"Unsupported or unknown file type: {file_type}")

    base_image = "alpine:latest"
    install_command = FILE_TYPES[file_type]["install"]
    cmd_command = FILE_TYPES[file_type]["cmd"].format(script_name=os.path.basename(script_name))

    dockerfile_content = f"""
FROM {base_image}
WORKDIR /sandbox
COPY {os.path.basename(script_name)} /sandbox/
RUN chmod +x {os.path.basename(script_name)}

{install_command}

{cmd_command}
"""

    with open(os.path.join(folder, "Dockerfile"), "w") as f:
        f.write(dockerfile_content.strip() + "\n")


def cleanup_files(files_for_cleanup):
    for file_path in files_for_cleanup:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f" Removed file: {file_path}")
                logger.info(f" Removed file: {file_path}")
        except PermissionError:
            print(f" Permission denied when removing file: {file_path}. Skipping...")
            logger.warning(f" Permission denied when removing file: {file_path}. Skipping...")
        except Exception as e:
            print(f" Failed to delete file {file_path}: {e}")
            logger.error(f"Failed to delete file {file_path}: {e}")


def sandbox_process(pid):
    info = get_process_info(pid)
    if not info:
        return

    cwd = info["cwd"]
    args = info["args"]
    exe = info["exe"]

    flagged_files = []
    flagged_file = None
    open_files = []
    copied_files_for_cleanup = []
    original_flagged_files = set()

    sandbox_id = str(uuid.uuid4())[:8]
    sandbox_dir = f"/tmp/sandbox_{sandbox_id}"
    os.makedirs(sandbox_dir, exist_ok=True)

    try:
        open_files = psutil.Process(pid).open_files()
        for file in open_files:
            file_type = determine_file_type(file.path)
            if file_type != 'unknown':
                flagged_files.append(file.path)
                original_flagged_files.add(os.path.abspath(file.path))
                dest_path = os.path.join(sandbox_dir, os.path.basename(file.path))
                shutil.copy2(file.path, dest_path)
                copied_files_for_cleanup.append(dest_path)
                print(f" Copied open file: {file.path}")
                logger.info(f" Copied open file: {file.path}")
    except Exception as e:
        print(f" Error while copying open files: {e}")
        logger.error(f"Error while copying open files: {e}")

    try:
        for arg in args[1:]:
            cleaned_arg = arg.strip(' "\'')
            if cleaned_arg.endswith(tuple(COMMON_FILE_TYPES.keys())):
                possible_path = os.path.join(cwd, cleaned_arg) if not os.path.isabs(cleaned_arg) else cleaned_arg
                print(f" Trying path: {possible_path}")
                logger.info(f" Trying path: {possible_path}")
                if os.path.isfile(possible_path):
                    flagged_file = possible_path
                    print(f" Identified main script from args: {flagged_file}")
                    logger.info(f" Identified main script from args: {flagged_file}")
                    break

        if not flagged_file and exe and os.path.exists(exe) and not exe.startswith(("/usr/", "/bin/", "/lib/")):
            flagged_file = exe
            print(f" Identified executable: {flagged_file}")
            logger.info(f" Identified executable: {flagged_file}")

        if not flagged_file:
            for file in open_files:
                if file.path.startswith(cwd) and os.path.isfile(file.path):
                    flagged_file = file.path
                    print(f" Using fallback from open_files: {flagged_file}")
                    logger.info(f"Using fallback from open_files: {flagged_file}")
                    break
    except Exception as e:
        print(f" Error identifying main file: {e}")
        logger.error(f" Error identifying main file: {e}")

    if flagged_file and flagged_file not in flagged_files:
        try:
            dest_path = os.path.join(sandbox_dir, os.path.basename(flagged_file))
            shutil.copy2(flagged_file, dest_path)
            flagged_files.append(flagged_file)
            copied_files_for_cleanup.append(dest_path)
            original_flagged_files.add(os.path.abspath(flagged_file))
            print(f" Copied main script {flagged_file} to sandbox.")
            logger.info(f"Copied main script {flagged_file} to sandbox.")
        except Exception as e:
            print(f" Error copying main file: {e}")
            logger.error(f" Error copying main file: {e}")
            return

    if not flagged_file:
        print(" Could not determine the main malicious file.")
        logger.error(" Could not determine the main malicious file.")
        return

    file_type = determine_file_type(flagged_file)
    print(f" Detected file type: {file_type}")
    logger.info(f"Detected file type: {file_type}")

    try:
        p = psutil.Process(pid)
        p.terminate()
        p.wait(timeout=3)
        print(f" Terminated process with PID {pid}")
        logger.info(f" Terminated process with PID {pid}")
    except Exception as e:
        print(f" Failed to terminate process: {e}")
        logger.error(f"Failed to terminate process: {e}")

    try:
        write_dockerfile(flagged_file, sandbox_dir, file_type)
        print(" Dockerfile created.")
        logger.info(" Dockerfile created.")
    except Exception as e:
        print(f" Failed to write Dockerfile: {e}")
        logger.error(f"Failed to write Dockerfile: {e}")
        return

    image_name = f"sandbox_image_{sandbox_id}"

    try:
        print(" Building Docker image...")
        logger.info(" Building Docker image...")
        subprocess.run(["docker", "build", "-t", image_name, "."], cwd=sandbox_dir, check=True)
        print(" Docker image built successfully.")
        logger.info(" Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        print(f" Docker build failed: {e}")
        logger.error(f" Docker build failed: {e}")
        return

    try:
        print(" Running container with seccomp profile...")
        logger.info(" Running container with seccomp profile...")
        result = subprocess.run(
            [
                "docker", "run",
                "--rm",
                "--log-driver=syslog",
                "--network", "none",
                "--memory", "256m",
                "--security-opt", f"seccomp={SECCOMP_PROFILE_PATH}",
                image_name
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        print("Container executed successfully.")
        logger.info("Container executed successfully.")
        if result.stdout:
            print(" Output:\n", result.stdout.strip())
            logger.info(f"Output:\n{result.stdout.strip()}")
        if result.stderr:
            print(" Errors:\n", result.stderr.strip())
            logger.warning(f" Errors:\n{result.stderr.strip()}")

        if not result.stdout and not result.stderr:
            print(" No output received — process might be a silent infinite loop.")
            logger.warning(" No output received — process might be a silent infinite loop.")
    except subprocess.TimeoutExpired:
        print("⏱ Docker container timed out.")
        print(" This confirms the script **did start running**, but never exited (likely infinite loop).")
        logger.warning("⏱ Docker container timed out. Likely infinite loop.")
    except Exception as e:
        print(f" Error running container: {e}")
        logger.error(f" Error running container: {e}")

    cleanup_files(copied_files_for_cleanup)
    cleanup_files(original_flagged_files)

    try:
        if os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir)
            print(f" Removed sandbox directory: {sandbox_dir}")
            logger.info(f" Removed sandbox directory: {sandbox_dir}")
    except Exception as e:
        print(f" Failed to remove sandbox directory: {e}")
        logger.error(f" Failed to remove sandbox directory: {e}")