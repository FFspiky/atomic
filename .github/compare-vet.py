import pathlib
import subprocess

root = pathlib.Path.cwd()
base = root / ".baseline-vet"
subprocess.run(["git", "worktree", "add", "--detach", str(base),
                "59b8c279e6d576be562e9163b85e871fff9b825a"], check=True)
results = []
for label, cwd in [("original upstream", base), ("patched source", root)]:
    result = subprocess.run(["go", "vet", "./..."], cwd=cwd,
                            text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    print(label, "exit", result.returncode)
    print(result.stdout)
    results.append(result)
original, patched = results
if original.returncode != patched.returncode or original.stdout != patched.stdout:
    raise SystemExit("vet diagnostics differ from the original source")
if patched.returncode:
    print("Raw vet still fails; confirmed identical baseline diagnostics.")
else:
    print("Both vet checks pass.")
