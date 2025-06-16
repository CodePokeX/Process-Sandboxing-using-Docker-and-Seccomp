import subprocess
import time
import sys
import os


sys.path.append("testfolder")  
from sandbox import sandbox_process  # type: ignore

def run_python_file():
    """Run the Python file and capture the PID."""
    proc = subprocess.Popen(
        ["python3", "flagged_file.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    time.sleep(2)


    pid = proc.pid
    print(f" Captured PID: {pid}")

    return proc, pid

def compile_and_run_c_file():
    
    subprocess.run(["gcc", "flagged_file.c"])

    proc = subprocess.Popen(
        ["./a.out"],  
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(2)
    pid = proc.pid
    print(f"Captured PID: {pid}")

    return proc, pid

def launch_and_monitor():
    print(" Launching flagged process...")


    if os.path.exists("flagged_file.py"):
        
        proc, pid = run_python_file()
        # proc, pid = compile_and_run_c_file()

    else:
        print("Neither flagged_file.py nor flagged_file.c found!")
        return


    sandbox_process(pid)


    try:
        proc.wait()
    except KeyboardInterrupt:
        print(" Terminating process...")
        proc.terminate()

if __name__ == "__main__":
    launch_and_monitor()