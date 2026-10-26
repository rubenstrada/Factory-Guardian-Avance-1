"""Construye un notebook autocontenido con las mismas fuentes y casos.

--execute inicia un kernel nuevo del intérprete actual, ejecuta todas las celdas
y conserva las salidas reales. No abre Google Colab ni publica archivos.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager


def build_notebook(root):
    files = {
        "bot": root / "src" / "factory_guardian" / "bot.py",
        "evaluation": root / "src" / "factory_guardian" / "evaluation.py",
        "knowledge": root / "src" / "factory_guardian" / "knowledge.json",
        "cases": root / "tests" / "conversations.json",
    }
    sources = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
    knowledge_cell = ("import json\nfrom pathlib import Path\n\n"
                      f"knowledge = json.loads({sources['knowledge']!r})\n"
                      "Path('knowledge.json').write_text(json.dumps(knowledge, ensure_ascii=False, indent=2), encoding='utf-8')\n"
                      "print(knowledge['notice'])\n"
                      "print('Registros ficticios:', len(knowledge['events']))")
    cases_cell = (
        f"cases = json.loads({sources['cases']!r})\n"
        "bot = FactoryGuardianBot('knowledge.json')\n"
        "results = run_sessions(bot, cases)\n"
        "save_results(results, 'artifacts')\n"
        "for session in results['sessions']:\n"
        "    print('\\n' + session['id'] + ': ' + session['purpose'])\n"
        "    for turn in session['turns']:\n"
        "        print('Usuario:', turn['input'])\n"
        "        print('Bot [' + turn['actual_intent'] + ']:', turn['actual_text'])\n"
        "        print('Resultado:', 'APROBADO' if turn['passed'] else 'FALLIDO')\n"
        "print('\\nResumen:', results['summary'])\n"
        "print('Entorno real:', results['execution_environment'])\n"
        "assert results['summary']['sessions'] == 10\n"
        "assert results['summary']['failed_turns'] == 0"
    )
    notebook = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_markdown_cell(
            "# Factory Guardian — Avance 1\n\n"
            "Chatbot de consultas por reglas con Python y NLTK. Los cuatro registros y la guía son ficticios. "
            "No conecta cámaras, no usa un LLM, no guarda hallazgos y no envía alertas.\n\n"
            "El notebook es autocontenido: puede abrirse en Google Colab y ejecutarse de arriba abajo, "
            "sin clonar GitHub ni configurar rutas de un equipo. La ejecución conservada en esta entrega "
            "fue local; no es evidencia de ejecución en Colab. Cada mensaje es independiente."
        ),
        nbformat.v4.new_code_cell('%pip install -q "nltk>=3.9,<4"'),
        nbformat.v4.new_markdown_cell("## 1. Base de conocimiento ficticia\n\nAndén A y Pasillo B son zonas válidas sin registros. La guía G-01 no es un procedimiento de planta."),
        nbformat.v4.new_code_cell(knowledge_cell),
        nbformat.v4.new_markdown_cell("## 2. Chatbot\n\nEste código es el mismo módulo `bot.py`. NLTK tokeniza; reglas explícitas consultan el JSON. No se entrena un modelo."),
        nbformat.v4.new_code_cell(sources["bot"]),
        nbformat.v4.new_markdown_cell("## 3. Evaluador\n\nCompara respuestas reales con expectativas escritas previamente; conserva JSON y Markdown."),
        nbformat.v4.new_code_cell(sources["evaluation"]),
        nbformat.v4.new_markdown_cell("## 4. Diez conversaciones distintas\n\nCada sesión tiene dos mensajes de usuario. Los seguimientos vuelven a indicar la zona o el ID porque no hay memoria entre turnos. Aprobar estos casos no demuestra comprensión general del lenguaje ni utilidad industrial."),
        nbformat.v4.new_code_cell(cases_cell),
        nbformat.v4.new_markdown_cell("## 5. Probar otra consulta\n\nModifica la variable `consulta` y ejecuta la celda. Para consultas incompletas el chatbot solicita reformular; no inventa el parámetro faltante."),
        nbformat.v4.new_code_cell("consulta = 'Eventos en Cruce C'\nrespuesta = bot.respond(consulta)\nprint(respuesta.intent, '→', respuesta.text)"),
        nbformat.v4.new_markdown_cell("## Límites\n\nLas reglas reconocen vocabulario acotado; no resuelven referencias como ‘el primero’, negaciones complejas ni varias peticiones simultáneas. Las cifras proceden de cuatro registros de demostración. La visión futura de cámara y LLM requiere otro desarrollo y validación humana."),
    ])
    notebook.metadata.update({
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "factory_guardian": {
            "execution_environment": "not_executed",
            "source_sha256": {name: hashlib.sha256(source.encode("utf-8")).hexdigest()
                              for name, source in sources.items()},
            "colab_execution_verified": False,
        },
    })
    return notebook


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output", type=Path, default=root / "notebooks" / "Factory_Guardian_Avance_1.ipynb")
    parser.add_argument("--work-dir", type=Path, default=root / "artifacts" / "notebook_execution")
    args = parser.parse_args()
    notebook = build_notebook(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.execute:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        manager = KernelManager(kernel_name="python3")
        # El kernel usa el intérprete de este entorno; no modifica kernels globales.
        manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        client = NotebookClient(notebook, km=manager, timeout=180,
                                resources={"metadata": {"path": str(args.work_dir.resolve())}})
        client.execute(cleanup_kc=True)
        results = json.loads((args.work_dir / "artifacts" / "conversations.json").read_text(encoding="utf-8"))
        notebook.metadata["factory_guardian"].update({
            "execution_environment": results["execution_environment"],
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "summary": results["summary"],
        })
        print(json.dumps(results["summary"]))
    nbformat.write(notebook, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
