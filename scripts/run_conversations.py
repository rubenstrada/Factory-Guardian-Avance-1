"""Ejecuta las diez sesiones y conserva evidencia, sin tocar la base ficticia."""
import argparse
import json
from pathlib import Path

from factory_guardian.bot import FactoryGuardianBot
from factory_guardian.evaluation import run_sessions, save_results


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=root / "artifacts")
    args = parser.parse_args()
    cases = json.loads((root / "tests" / "conversations.json").read_text(encoding="utf-8"))
    result = run_sessions(FactoryGuardianBot(), cases)
    paths = save_results(result, args.output_dir)
    print(json.dumps(result["summary"], ensure_ascii=False))
    print("Entorno de ejecución:", result["execution_environment"])
    for path in paths:
        print(path)
    return 0 if result["summary"]["failed_turns"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
