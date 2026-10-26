# Guía técnica de Factory Guardian

Esta guía explica cómo está organizado el prototipo y cómo repetir sus comprobaciones. El [reporte metodológico](reporte.md) desarrolla el problema y las decisiones; aquí sigo el recorrido entre la entrada del usuario, las reglas y la respuesta.

## Responsabilidades

| Archivo | Responsabilidad |
|---|---|
| [bot.py](../src/factory_guardian/bot.py) | Normaliza y tokeniza el texto, carga el conocimiento y resuelve las consultas. |
| [knowledge.json](../src/factory_guardian/knowledge.json) | Conserva las zonas, los cuatro registros ficticios y la guía demostrativa. |
| [cli.py](../src/factory_guardian/cli.py) | Recibe mensajes en la terminal y muestra la intención y la respuesta. |
| [evaluation.py](../src/factory_guardian/evaluation.py) | Contrasta respuestas con expectativas y guarda los resultados en JSON y Markdown. |
| [run_conversations.py](../scripts/run_conversations.py) | Carga los diez casos, ejecuta el evaluador y guarda las transcripciones. |
| [build_notebook.py](../scripts/build_notebook.py) | Reúne el mismo código, conocimiento y casos en un notebook autocontenido; puede ejecutarlo localmente. |
| [tests](../tests/) | Comprueba las reglas, los recuentos, las entradas incompletas, el evaluador y la ejecución del notebook. |

La terminal y el notebook utilizan la misma lógica del chatbot. La interfaz muestra las respuestas; el módulo `bot.py` decide qué responder. Las consultas leen el conocimiento sin registrar eventos ni modificar el JSON.

## Funciones y resultado de una consulta

Las siguientes funciones y clases están en [bot.py](../src/factory_guardian/bot.py):

| Elemento | Comportamiento |
|---|---|
| `normalize(text)` | Aplica `casefold` y descomposición Unicode NFD, y elimina marcas diacríticas. Permite comparar palabras sin distinguir mayúsculas o tildes. |
| `tokenize(text)` | Normaliza el mensaje, lo divide con `nltk.tokenize.wordpunct_tokenize` y conserva los tokens alfanuméricos en una tupla. |
| `load_knowledge(path=None)` | Lee JSON en UTF-8. Usa la ruta recibida o el archivo `knowledge.json` que acompaña a `bot.py`. |
| `FactoryGuardianBot(knowledge_path=None)` | Carga el conocimiento al construir la instancia y lo conserva en `self.knowledge`. |
| `respond(text)` | Identifica la zona y un posible ID, recorre las reglas en orden y devuelve la primera respuesta aplicable. |
| `Reply` | Es una `dataclass` inmutable con dos campos: `intent` y `text`. Permite que distintas interfaces presenten el mismo resultado. |

NLTK interviene en la tokenización. La clasificación depende de reglas explícitas, sin entrenamiento ni modelos descargables. El ID se extrae mediante una expresión regular sobre el texto normalizado y se convierte al formato `NM-001` para buscarlo en la base.

```python
from factory_guardian.bot import FactoryGuardianBot

bot = FactoryGuardianBot()
reply = bot.respond("Estado NM-001")
print(reply.intent)  # consultar_estado
print(reply.text)    # NM-001: Abierto. Zona: Cruce C.
```

## Base de conocimiento

El archivo [knowledge.json](../src/factory_guardian/knowledge.json) tiene cuatro secciones:

| Clave | Contenido |
|---|---|
| `notice` | Aviso sobre el carácter ficticio de la base. |
| `zones` | Zonas reconocidas: Cruce C, Andén A y Pasillo B. |
| `events` | Registros con `id`, `zone`, `status` y `description`. |
| `guides` | Guías con `id`, `zone` y `text`. |

Los cuatro registros, de `NM-001` a `NM-004`, pertenecen a Cruce C. Andén A y Pasillo B son zonas válidas sin registros. La guía G-01 corresponde a Cruce C y es demostrativa.

El recuento se calcula recorriendo `events` y contando los elementos cuya zona coincide con la consulta. El estado se obtiene buscando el ID en esos registros. La consulta de procedimiento busca una guía de la zona indicada. El número de registros se obtiene de los datos cargados, por lo que puede cambiar si se utiliza otra base con `knowledge_path`.

## Orden de las reglas

`respond` devuelve el resultado de la primera condición que coincide:

| Prioridad | Intención | Condición principal |
|---|---|---|
| 1 | `alcance` | Palabras clave como `alcance`, `camaras`, `llm`, `alertas`, `registrar`, `guardar` o `detectar`, después de normalizar. |
| 2 | `consultar_estado` | Un ID con formato reconocido o las palabras `estado` o `estatus`. |
| 3 | `consultar_procedimiento` | Palabras como `procedimiento` o `guía`; requiere una zona reconocida. |
| 4 | `consultar_eventos` | Palabras como `eventos`, `incidentes`, `near-miss` o `cuántos`; requiere una zona reconocida. |
| 5 | `ayuda` | Palabras como `ayuda`, `opciones` o `consultas`. |
| 6 | `despedida` | Palabras de cierre como `adiós` o `salir`. |
| 7 | `saludo` | Palabras como `hola`, `buenos` o `saludos`. |
| 8 | `no_reconocida` | Ninguna condición anterior coincide. |

Este orden permite responder una consulta que venga acompañada de un saludo. También significa que cada mensaje obtiene una sola intención: las reglas no descomponen varias peticiones simultáneas ni interpretan negaciones complejas.

## Consultas completas y datos ausentes

El chatbot conserva la base de conocimiento, pero no el contexto de las preguntas anteriores. Una consulta de seguimiento debe repetir el tipo de consulta y la zona o el ID. Por ejemplo, después de pedir un estado, `el primero` no identifica un registro; `Estado NM-001` sí proporciona la información necesaria.

| Consulta | Resultado |
|---|---|
| `Eventos en Andén A` | La zona existe y tiene cero registros; devuelve el recuento. |
| `Eventos en Cruce X` | La zona no se reconoce; solicita una consulta completa con una zona válida. |
| `¿Cuántos eventos hay?` | Falta la zona; solicita la misma reformulación. |
| `Estado NM-999` | El ID tiene el formato admitido, pero no existe en la base; lo indica expresamente. |
| `Necesito el estado` | Falta el ID; solicita incluirlo en la pregunta completa. |
| `Guía de Andén A` | La zona es válida, pero no tiene guía; indica que no hay una guía demostrativa disponible. |

Una zona vacía y una zona desconocida no reciben el mismo tratamiento. La primera permite calcular un cero; la segunda necesita aclaración. Las consultas incompletas conservan la intención reconocida, como `consultar_estado`, aunque la respuesta solicite más información.

## Ejemplo del recorrido

Para el mensaje `Hola, ¿CUÁNTOS EVENTOS hay en CRUCE C?`:

1. `normalize` obtiene `hola, ¿cuantos eventos hay en cruce c?`.
2. `tokenize` produce `('hola', 'cuantos', 'eventos', 'hay', 'en', 'cruce', 'c')`.
3. El método auxiliar `_zone` reconoce la secuencia `cruce c` como Cruce C.
4. La regla de eventos coincide antes que la regla de saludo. Se cuentan los cuatro registros de esa zona en `events`.
5. El resultado es `Reply(intent='consultar_eventos', text='Cruce C tiene 4 registros disponibles.')`. La interfaz muestra esos campos.

El saludo acompaña a una consulta completa y no la reemplaza. Este caso aparece en las [expectativas C03](../tests/conversations.json) y en su [transcripción ejecutada](../artifacts/conversations.md#c03-prioridad-de-consulta-útil-y-normalización).

## Ejecución desde la raíz

Se requiere Python 3.10 o posterior. Desde la carpeta que contiene `pyproject.toml`:

```powershell
python -m pip install -e ".[dev]"
python -m factory_guardian.cli
```

También puede enviarse una sola pregunta desde la terminal:

```powershell
python -m factory_guardian.cli --text "Eventos en Cruce C"
```

Para repetir las conversaciones y las pruebas:

```powershell
python scripts/run_conversations.py
python -m pytest -q --junitxml=artifacts/test_results.xml
```

El primer comando lee `tests/conversations.json` y guarda las respuestas en `artifacts/conversations.json` y `artifacts/conversations.md`. Termina con código 0 si todos los mensajes cumplen sus expectativas y con código 1 si alguno falla. El segundo ejecuta las pruebas y actualiza el archivo XML indicado.

Para reconstruir y ejecutar el notebook con el mismo código, conocimiento y casos:

```powershell
python scripts/build_notebook.py --execute
```

El constructor utiliza un kernel del intérprete actual y guarda las salidas en el notebook y en `artifacts/notebook_execution/`. El [notebook entregado](../notebooks/Factory_Guardian_Avance_1.ipynb) es autocontenido y portable para Google Colab. La ejecución conservada en la evidencia fue local.

`pyproject.toml` declara los rangos de dependencias del proyecto. Las versiones utilizadas en la comprobación se conservan en el [resumen de verificación](../artifacts/verification_summary.json).

## Cómo se revisan las respuestas

Las expectativas están en [tests/conversations.json](../tests/conversations.json), separadas de las respuestas obtenidas. Cada mensaje incluye `input`, `expected_intent` y `expected_contains`. La función `run_sessions` de [evaluation.py](../src/factory_guardian/evaluation.py) llama al chatbot y comprueba que coincida la intención y que estén presentes todos los fragmentos esperados, sin distinguir mayúsculas.

El evaluador registra la intención y el texto reales, los fragmentos ausentes y si el mensaje pasó la comprobación. También conserva el entorno de ejecución y las versiones de Python y NLTK. `save_results` escribe la versión estructurada y la transcripción legible.

[test_bot.py](../tests/test_bot.py) comprueba las ocho intenciones, la prioridad de una consulta sobre un saludo, las zonas vacías, los IDs inexistentes, los mensajes incompletos y la falta de memoria entre consultas. También usa una base alternativa para comprobar que el recuento sale de los datos y una expectativa incorrecta para comprobar que el evaluador detecta un fallo. [test_notebook.py](../tests/test_notebook.py) ejecuta el notebook desde un directorio vacío y revisa sus salidas.

## Evidencia disponible

| Recurso | Qué permite revisar |
|---|---|
| [Expectativas de las diez conversaciones](../tests/conversations.json) | Preguntas, intención esperada y fragmentos que debe contener la respuesta. |
| [Diez transcripciones](../artifacts/conversations.md) | Mensajes, respuestas reales y resultado de cada comparación. |
| [Resultados de conversaciones en JSON](../artifacts/conversations.json) | Respuestas, expectativas, entorno y resumen estructurados. |
| [Resultados de pruebas](../artifacts/test_results.xml) | Resultado de la ejecución de pytest. |
| [Resumen de verificación](../artifacts/verification_summary.json) | Entorno, comandos y resultados de pruebas, conversaciones y notebook. |
| [Notebook con salidas](../notebooks/Factory_Guardian_Avance_1.ipynb) | Código, datos y conversaciones en un recorrido ejecutable. |
| [Resultados locales del notebook](../artifacts/notebook_execution/artifacts/conversations.json) | Evaluación producida al ejecutar sus celdas. |
| [Registro de pruebas durante el desarrollo](../artifacts/tdd_log.md) | Fallos previos y comprobaciones posteriores. |

La evidencia conservada registra 26 pruebas aprobadas y diez sesiones con veinte mensajes: veinte cumplieron las expectativas y ninguno falló. Estos resultados describen los casos definidos para el prototipo de reglas. El [uso de IA](uso_de_ia.md) explica la asistencia recibida durante el desarrollo y las comprobaciones.
