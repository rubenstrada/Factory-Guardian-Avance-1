# Factory Guardian — Avance 1

Chatbot de consultas en Python 3.10+ que utiliza NLTK para tokenizar mensajes y reglas para identificar la consulta. Trabaja con cuatro registros ficticios sobre interacción entre peatones y montacargas y con una guía demostrativa.

Planteé Factory Guardian a partir de una idea de hackathon. Para este avance decidí concentrarme en un chatbot de consultas, de acuerdo con la consigna, y organizar el código para poder explicar cómo pasa de un mensaje a una respuesta.

## Consultas disponibles

| Intención | Función |
|---|---|
| `saludo` | Inicia la interacción. |
| `ayuda` | Explica las consultas disponibles. |
| `alcance` | Describe qué hace el prototipo. |
| `consultar_eventos` | Consulta los registros de una zona. |
| `consultar_estado` | Busca el estado de un registro por su ID. |
| `consultar_procedimiento` | Presenta la guía demostrativa. |
| `despedida` | Cierra la interacción. |
| `no_reconocida` | Orienta cuando el mensaje no corresponde a una consulta admitida. |

Las consultas son de solo lectura. Si falta información, el chatbot solicita una pregunta completa; cada mensaje se interpreta por separado.

## Ejecutar

Desde la raíz del repositorio:

```powershell
python -m pip install -e ".[dev]"
python -m factory_guardian.cli
```

NLTK se utiliza para tokenizar el texto sin descargar modelos ni conectarse a servicios externos.

## Usar desde Python

```python
from factory_guardian.bot import FactoryGuardianBot

bot = FactoryGuardianBot()
reply = bot.respond("ayuda")
print(reply.intent)
print(reply.text)
```

`respond` devuelve un objeto `Reply` con la intención identificada y el texto de respuesta.

## Notebook y comprobaciones

El notebook [Factory_Guardian_Avance_1.ipynb](notebooks/Factory_Guardian_Avance_1.ipynb) permite recorrer el prototipo y sus ejemplos. Se entrega para abrirlo en Google Colab; la comprobación del notebook se realiza localmente y se distingue de una ejecución en esa plataforma.

Para ejecutar las diez conversaciones y las pruebas:

```powershell
python scripts/run_conversations.py
python -m pytest --junitxml=artifacts/test_results.xml
```

Las conversaciones comparan las respuestas con expectativas de intención y contenido. Cada sesión incluye al menos dos mensajes de usuario y registra el entorno utilizado. Las salidas se conservan en [conversations.md](artifacts/conversations.md) y [conversations.json](artifacts/conversations.json).

Para reconstruir y ejecutar el notebook localmente:

```powershell
python scripts/build_notebook.py --execute
```

## Organización

- `src/factory_guardian/`: chatbot, normalización del texto y carga del conocimiento.
- `src/factory_guardian/knowledge.json`: registros ficticios y guía demostrativa.
- `scripts/`: ejecución de conversaciones y preparación del notebook.
- `notebooks/`: recorrido del prototipo.
- `tests/`: comprobaciones del comportamiento.
- `docs/`: [reporte del avance](docs/reporte.md), [decisiones](docs/decisiones.md) y [uso de IA](docs/uso_de_ia.md).
- `artifacts/`: resultados de las comprobaciones.

## Límites

Los registros y la guía son ficticios y sirven para demostrar el funcionamiento del chatbot. Las respuestas no sustituyen procedimientos de una planta real ni permiten evaluar una situación de seguridad.

El avance utiliza reglas y no aprende de las conversaciones. La visión por computadora, los modelos de lenguaje, RAG y las alertas quedan como posibilidades de evolución; no forman parte de esta implementación.

Desarrollé esta entrega con asistencia de Codex en el código, las pruebas y la documentación. En la [nota de uso de IA](docs/uso_de_ia.md) explico cómo relacioné ese apoyo con las decisiones del proyecto.
