"""Comportamientos observables; expectativas fijadas antes de implementar."""
import importlib
import importlib.util
import json
from pathlib import Path

import pytest


def make_bot(knowledge_path=None):
    # Permite registrar un RED por capacidad ausente, sin error de colección.
    if importlib.util.find_spec("factory_guardian") is None:
        pytest.fail("Capacidad ausente: todavía no existe FactoryGuardianBot")
    module = importlib.import_module("factory_guardian.bot")
    return module.FactoryGuardianBot(knowledge_path)


@pytest.mark.parametrize("text,intent,fragments", [
    ("Hola", "saludo", ["Factory Guardian", "base de ejemplo"]),
    ("Ayuda", "ayuda", ["eventos", "estado", "guía"]),
    ("¿Cuál es tu alcance?", "alcance", ["solo consultas", "base de ejemplo"]),
    ("¿Cuántos near-miss hay en Cruce C?", "consultar_eventos", ["4 registros", "Cruce C"]),
    ("Estado NM-001", "consultar_estado", ["NM-001", "Abierto"]),
    ("Procedimiento Cruce C", "consultar_procedimiento", ["G-01", "demostrativa", "no sustituye"]),
    ("Adiós", "despedida", ["Hasta luego"]),
    ("¿Qué clima hará mañana?", "no_reconocida", ["No reconozco", "ayuda"]),
])
def test_recognizes_eight_supported_intents(text, intent, fragments):
    reply = make_bot().respond(text)
    assert reply.intent == intent
    assert all(fragment in reply.text for fragment in fragments)


@pytest.mark.parametrize("text", [
    "Hola, ¿CUÁNTOS EVENTOS hay en CRUCE C?",
    "¡BUENOS DÍAS! necesito consultar near-miss del cruce c.",
])
def test_greeting_does_not_hide_the_useful_query(text):
    reply = make_bot().respond(text)
    assert reply.intent == "consultar_eventos"
    assert "4 registros" in reply.text


@pytest.mark.parametrize("text,fragment", [
    ("Eventos en ANDEN A", "Andén A"),
    ("Near-miss en Pasillo B", "Pasillo B"),
])
def test_valid_empty_zone_returns_zero_not_unknown(text, fragment):
    reply = make_bot().respond(text)
    assert reply.intent == "consultar_eventos"
    assert "0 registros" in reply.text and fragment in reply.text


def test_unknown_identifier_is_explicit_not_an_invented_status():
    reply = make_bot().respond("Estado NM-999")
    assert reply.intent == "consultar_estado"
    assert "NM-999" in reply.text and "no existe" in reply.text


@pytest.mark.parametrize("text,intent,fragment", [
    ("¿Cuántos eventos hay?", "consultar_eventos", "consulta completa"),
    ("Eventos en Cruce X", "consultar_eventos", "zona"),
    ("Necesito el estado", "consultar_estado", "ID completo"),
    ("Quiero una guía", "consultar_procedimiento", "consulta completa"),
])
def test_missing_parameters_ask_for_a_complete_reformulation(text, intent, fragment):
    reply = make_bot().respond(text)
    assert reply.intent == intent
    assert fragment in reply.text


def test_partial_followup_does_not_pretend_to_remember_context():
    bot = make_bot()
    bot.respond("Necesito el estado")
    assert bot.respond("el primero").intent == "no_reconocida"
    assert "Abierto" in bot.respond("Estado NM-001").text


def test_count_is_derived_from_supplied_knowledge_not_a_constant(tmp_path):
    knowledge = {
        "notice": "Base ficticia de prueba.",
        "zones": ["Cruce C", "Andén A"],
        "events": [{"id": "NM-101", "zone": "Cruce C", "status": "Cerrado"}],
        "guides": []
    }
    path = tmp_path / "knowledge.json"
    path.write_text(json.dumps(knowledge), encoding="utf-8")
    bot = make_bot(path)
    assert "1 registro" in bot.respond("Eventos en Cruce C").text
    assert "0 registros" in bot.respond("Eventos en Andén A").text
    assert "Cerrado" in bot.respond("Estado NM-101").text


@pytest.mark.parametrize("text", ["", "   ", "...?!"])
def test_empty_or_punctuation_only_input_asks_for_help(text):
    reply = make_bot().respond(text)
    assert reply.intent == "no_reconocida"
    assert "ayuda" in reply.text


def test_procedure_not_available_is_not_fabricated():
    reply = make_bot().respond("Guía para Andén A")
    assert reply.intent == "consultar_procedimiento"
    assert "No hay guía" in reply.text


def test_conversation_suite_has_ten_independent_sessions_and_real_passes():
    bot = make_bot()
    evaluation = importlib.import_module("factory_guardian.evaluation")
    cases = json.loads(Path("tests/conversations.json").read_text(encoding="utf-8"))
    assert len(cases) == 10
    assert len({case["id"] for case in cases}) == 10
    assert all(len(case["turns"]) >= 2 for case in cases)
    result = evaluation.run_sessions(bot, cases)
    assert result["summary"] == {"sessions": 10, "turns": 20, "passed_turns": 20, "failed_turns": 0}
    assert all(turn["actual_text"] for session in result["sessions"] for turn in session["turns"])


def test_conversation_evaluator_exposes_incorrect_expectation():
    bot = make_bot()
    evaluation = importlib.import_module("factory_guardian.evaluation")
    result = evaluation.run_sessions(bot, [{"id": "T", "purpose": "Control negativo", "turns": [
        {"input": "Hola", "expected_intent": "consultar_estado", "expected_contains": ["ZZZ imposible"]}
    ]}])
    assert result["summary"]["failed_turns"] == 1
    assert result["sessions"][0]["turns"][0]["passed"] is False
