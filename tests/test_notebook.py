"""El constructor debe producir un notebook portable y ejecutable."""
import json
from pathlib import Path
import subprocess
import sys


def test_self_contained_notebook_runs_from_an_empty_directory(tmp_path):
    result = subprocess.run([
        sys.executable, "scripts/build_notebook.py", "--execute",
        "--output", str(tmp_path / "demo.ipynb"), "--work-dir", str(tmp_path / "execution")
    ], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr
    notebook = json.loads((tmp_path / "demo.ipynb").read_text(encoding="utf-8"))
    assert notebook["metadata"]["factory_guardian"]["execution_environment"] == "local"
    artifact = json.loads((tmp_path / "execution" / "artifacts" / "conversations.json").read_text(encoding="utf-8"))
    assert artifact["summary"]["sessions"] == 10
    assert artifact["summary"]["failed_turns"] == 0
    assert all(cell.get("execution_count") is not None for cell in notebook["cells"] if cell["cell_type"] == "code")
