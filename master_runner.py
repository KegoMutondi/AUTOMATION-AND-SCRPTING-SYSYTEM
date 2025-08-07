import subprocess

scripts = [
    "log.py",
    "file_organizer.py",
    "file_organizer_gui.py",
    "run_organizer.py"
]

for script in scripts:
    print(f"\n🔄 Running {script}...\n")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Failed to run {script}")
