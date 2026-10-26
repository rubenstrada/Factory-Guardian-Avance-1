# Factory Guardian Avance 1

## Introducción

Planteé Factory Guardian a partir de una idea de hackathon relacionada con la interacción entre peatones y montacargas. Para este avance delimité la propuesta a un chatbot de consultas por reglas. Busco comprender el recorrido entre una pregunta, su intención y los datos recuperados.

La implementación utiliza Python y NLTK, una base JSON ficticia y respuestas determinadas por reglas. Los ejemplos permiten comprobar el recorrido de una consulta; no representan hallazgos de una planta. Factory Guardian conserva como visión futura la relación entre observaciones visuales, antecedentes y explicaciones para el supervisor. Aquí desarrollo únicamente su componente de consultas.

## 1. Selecciona un problema real que pueda beneficiarse mediante el uso de inteligencia artificial y justifica su pertinencia.

El problema que seleccioné es la dificultad de recuperar antecedentes sobre interacciones entre peatones y montacargas cuando los registros y las orientaciones están dispersos. El supervisor necesita localizar eventos de una zona, revisar su estado y encontrar la guía relacionada. OSHA reconoce riesgos de lesiones por esa interacción y aborda la organización del tránsito en el trabajo (Occupational Safety and Health Administration, s. f.).

No dispongo de información de una planta ni de mediciones sobre sus tiempos de consulta. Por eso utilizo una situación demostrativa, sin atribuirle resultados industriales. El asistente permite explorar una interfaz de lenguaje natural para recuperar información; no determina si un cruce es seguro ni sustituye una evaluación profesional.

## 2. Define los siguientes elementos de la solución:

### Problema

Recuperar registros y orientaciones sin revisar manualmente toda la base. Esta versión interpreta preguntas breves, las vincula con datos disponibles y solicita información cuando falta una zona o un identificador.

### Objetivo general

Desarrollar un chatbot basado en reglas que identifique consultas en español y devuelva información de una base demostrativa sobre eventos, estados y una guía asociada con una zona.

### Usuarios objetivo

Los usuarios objetivo son supervisores y personal de seguridad industrial que necesitan consultar antecedentes. Las pruebas representan sus consultas mediante guiones conocidos; no se afirma que hayan participado usuarios de una planta en esta evaluación.

### Alcance

Delimité las funciones a consultas de solo lectura. Hay cuatro registros ficticios en Cruce C y una guía demostrativa G-01. Andén A y Pasillo B permiten comprobar consultas sin registros. No se conectan cámaras, no se envían alertas, no se modifican estados y no se registran eventos. Tampoco se utiliza un modelo de lenguaje ni un dashboard.

### Beneficios esperados

Espero facilitar consultas y hacer visible la relación entre pregunta, intención y respuesta. Estos beneficios requieren evaluarse con usuarios y datos reales; todavía no se han medido en una empresa.

## 3. Diseña la arquitectura conceptual inicial del asistente inteligente. Incluye, como mínimo:

### Usuario

La persona escribe una consulta completa mediante la terminal, el notebook o una llamada desde Python. Puede solicitar ayuda si desconoce la forma de preguntar.

### Chatbot

La clase `FactoryGuardianBot` recibe texto mediante `respond` y devuelve un objeto `Reply` con `intent` y `text`. Las funciones de normalización, tokenización y carga del conocimiento están separadas de la clase para facilitar su revisión.

### Base de conocimiento

El archivo `knowledge.json` contiene zonas, eventos y una guía. Cada evento tiene ID, zona, estado y descripción. Los estados de ejemplo son Abierto, En revisión y Cerrado. El chatbot cuenta los registros consultados en el JSON; el número cuatro no está escrito como una respuesta fija.

### Flujo conversacional

El recorrido es mensaje del usuario, normalización, tokenización con NLTK, evaluación de reglas, consulta del JSON y respuesta. Una consulta útil tiene prioridad sobre un saludo que la acompañe. Si falta información, el bot solicita reformular la pregunta completa. Cada mensaje se interpreta por separado: después de preguntar «¿Cuántos eventos hay?», escribir únicamente «Cruce C» no completa una conversación anterior.

## 4. Diseña un conjunto de intenciones conversacionales y sus respuestas asociadas. Asegúrate de que las intenciones correspondan con el problema, los usuarios y el alcance previamente definidos.

El conjunto permite consultar información, iniciar y cerrar la interacción, pedir ayuda y responder a solicitudes no reconocidas.

| Intención | Ejemplo de mensaje | Comportamiento asociado |
|---|---|---|
| `saludo` | Hola | Presenta Factory Guardian y ofrece ayuda. |
| `ayuda` | Necesito ayuda | Muestra consultas y ejemplos admitidos. |
| `alcance` | ¿Puedes enviar alertas? | Explica los límites de esta demostración. |
| `consultar_eventos` | Eventos en Cruce C | Cuenta los registros de esa zona. |
| `consultar_estado` | Estado NM-001 | Recupera el estado del identificador. |
| `consultar_procedimiento` | Guía de Cruce C | Presenta G-01 como guía ficticia. |
| `despedida` | Adiós | Cierra la interacción. |
| `no_reconocida` | ¿Qué clima hará mañana? | Solicita reformular y recomienda ayuda. |

Distingo una zona sin registros de un identificador inexistente: ninguna situación debe producir información inventada. La guía mantiene una advertencia explícita sobre su carácter demostrativo. Una petición para registrar un evento conduce a la explicación del alcance, porque las operaciones de escritura quedaron fuera de esta versión.

## 5. Implementa un chatbot basado en reglas utilizando Python 3.10 o superior y NLTK. Utiliza Google Colab para el desarrollo y conserva el código fuente en GitHub.

La implementación utiliza Python 3.10 o superior. NLTK interviene en el procesamiento del texto mediante `wordpunct_tokenize`, herramienta de tokenización documentada por el proyecto (NLTK Project, s. f.). Este fragmento pertenece a `bot.py`:

```python
def tokenize(text: str) -> tuple[str, ...]:
    return tuple(
        token for token in wordpunct_tokenize(normalize(text))
        if token.isalnum()
    )
```

La normalización permite comparar mensajes sin depender de mayúsculas o tildes. La tokenización produce unidades que utilizan las reglas; no supone comprensión general ni aprendizaje a partir de conversaciones. Los identificadores se reconocen por un patrón y las respuestas recuperan datos de la base local.

El notebook es compatible con Google Colab, servicio de notebooks que admite archivos `.ipynb` y permite cargarlos desde GitHub o desde un archivo (Google, s. f.). La evidencia de esta entrega corresponde a ejecución local. El código completo se conserva en el repositorio privado [Factory Guardian Avance 1](https://github.com/rubenstrada/Factory-Guardian-Avance-1), junto con el notebook, las pruebas y sus resultados.

## 6. Realiza pruebas funcionales mediante, al menos, diez conversaciones distintas. Verifica el comportamiento del chatbot ante las intenciones definidas y conserva evidencias de ejecución.

El conjunto funcional contiene diez conversaciones separadas con dos mensajes de usuario en cada una. Las expectativas incluyen la intención y elementos concretos del texto. El registro de ejecución muestra 20 mensajes aprobados y ninguno fallido; la suite automatizada registra 26 pruebas aprobadas. Esto comprueba los casos definidos, sin estimar desempeño industrial.

| Conversación | Mensajes incluidos | Comprobación principal |
|---|---|---|
| C01 | «Hola»; «Necesito ayuda» | Presentación y orientación. |
| C02 | Consulta de Cruce C; consulta de Andén A | Cuatro registros frente a zona sin registros. |
| C03 | Saludo con consulta en mayúsculas; consulta de Pasillo B | Prioridad y normalización. |
| C04 | Estado de NM-001; estado de NM-003 | Estados Abierto y Cerrado. |
| C05 | Estado de NM-999; estado de NM-002 | ID inexistente y consulta válida independiente. |
| C06 | Eventos sin zona; pregunta completa sobre Cruce C | Solicitud de reformulación. |
| C07 | Estado sin ID; consulta de NM-004 | Identificador obligatorio. |
| C08 | Guía de Cruce C; guía de Andén A | Guía disponible y ausencia de guía. |
| C09 | Conectar cámaras y alertas; registrar un evento | Límites y ausencia de escritura. |
| C10 | Consulta del clima; despedida | Mensaje no reconocido y cierre. |

Los archivos `artifacts/conversations.md` y `artifacts/conversations.json` conservan las transcripciones, las expectativas, la salida obtenida y el entorno. `artifacts/test_results.xml` permite revisar las comprobaciones automatizadas. Estos archivos complementan el notebook y permiten contrastar lo que el reporte describe con el comportamiento ejecutado.

## 7. Analiza los resultados obtenidos e identifica las principales limitaciones de esta primera versión, así como posibles mejoras para las siguientes etapas del proyecto.

La interpretación debe centrarse en si cada consulta recupera el dato esperado y mantiene los límites definidos. Obtener cuatro registros en Cruce C únicamente describe el contenido ficticio del JSON; no mide la frecuencia de incidentes. Del mismo modo, devolver «Cerrado» para NM-003 no certifica que una condición real esté resuelta.

La principal limitación es la dependencia de reglas y vocabulario previsto. Una expresión distinta puede no reconocerse; una pregunta ambigua puede coincidir con una regla sin reflejar la intención de la persona. Además, el bot no conserva contexto y la base no se actualiza durante las consultas. Las conversaciones de prueba cubren casos definidos, no todo el lenguaje posible.

Para una siguiente etapa considero ampliar ejemplos con usuarios y revisar solicitudes no reconocidas. Incorporar información real requeriría una fuente autorizada, responsables de actualización y validación de las guías. Otras capacidades exigirían decisiones nuevas; no las presento como funciones ya construidas.

## Conclusiones

Este avance convierte una parte de Factory Guardian en un prototipo acotado que permite relacionar consultas, reglas y datos. Mi decisión fue concentrarme en un recorrido que pudiera explicar antes de ampliar la idea del hackathon. El aprendizaje central es que definir qué puede responder un asistente también exige decidir qué debe pedir, qué información desconoce y qué acciones quedan fuera de su alcance.

## Uso de herramientas

Utilicé Codex para apoyar la escritura y revisión del código, ejecutar las pruebas, preparar el notebook y redactar la documentación. Mi participación consistió en proponer Factory Guardian, delimitar el avance y revisar su relación con la consigna. Asumo la responsabilidad de comprender las reglas, explicar sus resultados y reconocer los límites de esta demostración.

## Referencias

Google. (s. f.). *Colaboratory frequently asked questions*. Recuperado el 25 de octubre de 2026, de https://research.google.com/colaboratory/faq.html

NLTK Project. (s. f.). *nltk.tokenize package*. Recuperado el 25 de octubre de 2026, de https://www.nltk.org/api/nltk.tokenize.html

Occupational Safety and Health Administration. (s. f.). *Powered industrial trucks eTool: Understanding the workplace—Pedestrian traffic*. U.S. Department of Labor. Recuperado el 25 de octubre de 2026, de https://www.osha.gov/etools/powered-industrial-trucks/workplace/pedestrian-traffic
