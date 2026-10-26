"""Consultas deterministas con NLTK y una base de conocimiento ficticia.

Cada mensaje es independiente. No se registran eventos ni se envían alertas.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import re
import unicodedata

from nltk.tokenize import wordpunct_tokenize


@dataclass(frozen=True)
class Reply:
    """Intención identificada y respuesta que puede mostrar cualquier interfaz."""
    intent: str
    text: str


def normalize(text: str) -> str:
    """Ignora mayúsculas y acentos sin descargar modelos de lenguaje."""
    return "".join(
        char for char in unicodedata.normalize("NFD", text.casefold())
        if unicodedata.category(char) != "Mn"
    )


def tokenize(text: str) -> tuple[str, ...]:
    """La tokenización NLTK produce las unidades usadas por las reglas."""
    return tuple(token for token in wordpunct_tokenize(normalize(text)) if token.isalnum())


def load_knowledge(path=None) -> dict:
    """Carga JSON local; la ausencia de una fuente no se disimula con datos inventados."""
    source = Path(path) if path is not None else Path(__file__).with_name("knowledge.json")
    return json.loads(source.read_text(encoding="utf-8"))


class FactoryGuardianBot:
    """Chatbot de solo consultas con ocho intenciones y reglas ordenadas."""

    def __init__(self, knowledge_path=None):
        self.knowledge = load_knowledge(knowledge_path)

    def _zone(self, tokens):
        words = " " + " ".join(tokens) + " "
        return next((zone for zone in self.knowledge["zones"]
                     if " " + " ".join(tokenize(zone)) + " " in words), None)

    def _ask_zone(self):
        return ("Escribe la consulta completa con una zona válida: "
                + ", ".join(self.knowledge["zones"])
                + ". La zona está ausente o no se reconoce. No conservo contexto entre mensajes.")

    def respond(self, text: str) -> Reply:
        """Resuelve primero las consultas útiles; después ayuda, cierre y saludo."""
        tokens = tokenize(text)
        words = set(tokens)
        zone = self._zone(tokens)
        identifier = re.search(r"\bnm\s*-?\s*(\d{3})\b", normalize(text))

        if words & {"alcance", "camara", "camaras", "llm", "alerta", "alertas",
                    "registrar", "guardar", "detectar"}:
            return Reply("alcance", "Este avance ofrece solo consultas sobre una base de ejemplo. "
                         "No conecto cámaras, no envío alertas, no registro eventos y no uso un LLM. "
                         "No sustituyo la revisión humana.")

        if identifier or words & {"estado", "estatus"}:
            if identifier is None:
                return Reply("consultar_estado", "Indica el ID completo en la consulta, por ejemplo: "
                             "¿Cuál es el estado de NM-001? No conservo contexto entre mensajes.")
            event_id = "NM-" + identifier.group(1)
            event = next((item for item in self.knowledge["events"] if item["id"] == event_id), None)
            if event is None:
                return Reply("consultar_estado", f"El ID {event_id} no existe en la base de conocimiento.")
            return Reply("consultar_estado", f"{event_id}: {event['status']}. Zona: {event['zone']}.")

        if words & {"procedimiento", "procedimientos", "guia", "guias"}:
            if zone is None:
                return Reply("consultar_procedimiento", self._ask_zone())
            guide = next((item for item in self.knowledge["guides"] if item["zone"] == zone), None)
            if guide is None:
                return Reply("consultar_procedimiento", f"No hay guía demostrativa para {zone}. "
                             "Consulta el procedimiento aprobado con el responsable de seguridad.")
            return Reply("consultar_procedimiento", guide["text"])

        if words & {"evento", "eventos", "incidente", "incidentes", "near", "miss", "cuantos", "cuantas"}:
            if zone is None:
                return Reply("consultar_eventos", self._ask_zone())
            count = sum(item["zone"] == zone for item in self.knowledge["events"])
            noun = "registro disponible" if count == 1 else "registros disponibles"
            return Reply("consultar_eventos", f"{zone} tiene {count} {noun}.")

        if words & {"ayuda", "opciones", "consultas"}:
            return Reply("ayuda", "Puedo consultar eventos por zona, el estado de un ID y una guía demostrativa. "
                         "Ejemplos: 'Eventos en Cruce C', 'Estado NM-001', 'Guía de Cruce C'. "
                         "Envía cada consulta completa.")
        if words & {"adios", "hasta", "salir", "chau"}:
            return Reply("despedida", "Hasta luego. Las consultas de esta demostración no sustituyen la revisión humana.")
        if words & {"hola", "buenos", "buenas", "saludos"}:
            return Reply("saludo", "Hola, soy Factory Guardian. Consulto una base de ejemplo por reglas. "
                         "Escribe 'ayuda' para conocer las consultas disponibles.")
        return Reply("no_reconocida", "No reconozco esa consulta. Escribe 'ayuda' y reformula la pregunta completa "
                     "con la zona o el ID correspondiente.")
