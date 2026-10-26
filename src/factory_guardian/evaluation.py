"""Evidencia reproducible: expectativas declaradas frente a respuestas reales."""
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import sys


def run_sessions(bot, cases):
    """Ejecuta cada entrada y contrasta intención y fragmentos escritos a mano."""
    sessions = []
    for case in cases:
        turns = []
        for case_turn in case["turns"]:
            reply = bot.respond(case_turn["input"])
            missing = [part for part in case_turn["expected_contains"]
                       if part.casefold() not in reply.text.casefold()]
            passed = reply.intent == case_turn["expected_intent"] and not missing
            turns.append({**case_turn, "actual_intent": reply.intent,
                          "actual_text": reply.text, "missing_fragments": missing, "passed": passed})
        sessions.append({"id": case["id"], "purpose": case["purpose"], "turns": turns})
    all_turns = [turn for session in sessions for turn in session["turns"]]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_environment": "google_colab" if "google.colab" in sys.modules else "local",
        "data_scope": "Escenarios y registros ficticios; no son resultados industriales.",
        "context_policy": "Sin estado entre mensajes; cada consulta debe ser completa.",
        "runtime": {"python": platform.python_version(), "platform": platform.system(),
                    "nltk": importlib.metadata.version("nltk")},
        "summary": {"sessions": len(sessions), "turns": len(all_turns),
                    "passed_turns": sum(turn["passed"] for turn in all_turns),
                    "failed_turns": sum(not turn["passed"] for turn in all_turns)},
        "sessions": sessions,
    }


def save_results(result, output_dir):
    """Conserva transcripciones reales en JSON y Markdown legible."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "conversations.json"
    markdown_path = output / "conversations.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = result["summary"]
    lines = ["# Diez conversaciones de prueba de Factory Guardian", "",
             "Escenarios ficticios de evaluación; las respuestas siguientes fueron ejecutadas.",
             f"Entorno: {result['execution_environment']}. Python: {result['runtime']['python']}. "
             f"NLTK: {result['runtime']['nltk']}.",
             f"Sesiones: {summary['sessions']}; mensajes: {summary['turns']}; "
             f"aprobados: {summary['passed_turns']}; fallidos: {summary['failed_turns']}.",
             "Sin memoria entre turnos: los seguimientos contienen la consulta completa.", ""]
    for session in result["sessions"]:
        lines += [f"## {session['id']}: {session['purpose']}", ""]
        for index, turn in enumerate(session["turns"], 1):
            lines += [f"{index}. Usuario: {turn['input']}", "",
                      f"   Bot [{turn['actual_intent']}]: {turn['actual_text']}", "",
                      f"   Esperado: {turn['expected_intent']}; contiene {turn['expected_contains']}. "
                      f"Resultado: {'APROBADO' if turn['passed'] else 'FALLIDO'}.", ""]
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, markdown_path
