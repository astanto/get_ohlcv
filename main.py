import subprocess

# List your script filenames in the order you want them to run
scripts = ["1h.py", "15m.py", "5m.py"]

for script in scripts:
    print(f"\n🚀 Running {script}...")
    subprocess.run(["python", script])
