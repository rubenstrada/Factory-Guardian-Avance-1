# Factory Guardian Avance 1

## Introducción

Este reporte presenta el primer avance de Factory Guardian, un asistente orientado a la consulta de información sobre la interacción entre peatones y montacargas. La propuesta surgió de una idea de hackathon. Para esta actividad decidí comenzar por una necesidad concreta del supervisor: recuperar antecedentes y orientaciones mediante preguntas breves.

La entrega utiliza cuatro registros ficticios y una guía demostrativa. Esta aclaración aplica a todos los ejemplos y resultados del documento; no son observaciones de una planta ni procedimientos aprobados. La visión general del proyecto contempla otras capacidades, pero aquí desarrollo únicamente un chatbot de consultas por reglas.

Documento y repositorio se entregan juntos: el documento explica el problema, la metodología y las decisiones; GitHub conserva el código, el notebook, la documentación técnica y la evidencia completa de ejecución.

## 1. Selecciona un problema real que pueda beneficiarse mediante el uso de inteligencia artificial y justifica su pertinencia.

El problema que seleccioné es la dificultad de recuperar antecedentes y orientaciones cuando la información sobre interacciones entre peatones y montacargas está dispersa. Para un supervisor, localizar lo registrado en una zona y revisar el estado de un evento son tareas diferentes de detectar un peligro. Mi propuesta comienza por facilitar esa consulta, sin asumir que el asistente puede evaluar por sí mismo la seguridad del lugar.

La pertinencia del contexto se relaciona con los riesgos de interacción entre peatones y vehículos industriales, descritos por OSHA al abordar el tránsito en el trabajo (Occupational Safety and Health Administration, s. f.). No cuento con mediciones de tiempos de consulta de una empresa; por eso planteo el beneficio como una posibilidad que habría que validar, no como una reducción de incidentes ya conseguida.

Decidí separar la idea completa del alcance de este avance. Antes de conectar cámaras o generar alertas, necesitaba definir qué preguntas tendría sentido responder y con qué información. Un chatbot por reglas permite concretar esa primera relación entre necesidad, consulta y respuesta, además de atender lo solicitado en la actividad.

## 2. Define los siguientes elementos de la solución:

### Problema

Recuperar información de una base de conocimiento sin revisar manualmente todos sus registros. La consulta debe distinguir entre una zona, un evento identificado y una guía, porque cada uno requiere información diferente para responder.

### Objetivo general

Desarrollar un chatbot funcional en español, basado en reglas y tokenización con NLTK, que permita consultar eventos por zona, recuperar su estado por identificador y encontrar una guía asociada. El resultado esperado es una respuesta vinculada con los datos disponibles o una orientación cuando la pregunta no puede resolverse.

### Usuarios objetivo

Supervisores y personal de seguridad industrial que necesitan recuperar antecedentes. Para esta primera versión representé sus posibles consultas mediante casos de prueba; la evaluación no incluyó participantes de una planta.

### Alcance

El prototipo consulta información de solo lectura. Reconoce preguntas previstas, solicita reformular cuando falta una zona o un identificador y explica sus límites. Cada mensaje se procesa de manera independiente. Cámaras, alertas, registro de nuevos eventos y modelos de lenguaje quedan fuera de este avance.

### Beneficios esperados

Facilitar el acceso a los registros y orientar preguntas incompletas. La utilidad consiste en recuperar información, no en declarar que un área es segura. Para medir el beneficio real sería necesario comparar la consulta con el proceso habitual de los usuarios.

## 3. Diseña la arquitectura conceptual inicial del asistente inteligente. Incluye, como mínimo:

### Usuario

Es quien tiene una necesidad de información y la expresa mediante una pregunta. El flujo parte de esa necesidad, no de una pantalla particular: la consulta puede escribirse en el notebook o en la terminal.

### Chatbot

Interpreta la solicitud mediante reglas, identifica qué información necesita y prepara la respuesta. Separé esta responsabilidad de la interfaz para que el mismo comportamiento se utilice desde distintos puntos de entrada. La organización por responsabilidades también evita concentrar toda la lógica en un archivo principal, dificultad que ya había encontrado en un backend anterior.

### Base de conocimiento

Conserva zonas, eventos y una guía. Cada evento tiene un identificador, zona, estado y descripción. Mantener los datos separados de las respuestas permite consultar su contenido: si cambia la cantidad de registros, debe cambiar el conteo sin reescribir una frase fija.

### Flujo conversacional

La pregunta se normaliza y divide en unidades de texto. Después se identifica la intención y se revisa si incluye los datos necesarios. Una consulta válida recupera información de la base; una incompleta solicita una pregunta completa. Si el tema queda fuera del alcance, se comunica esa limitación.

Por ejemplo, una consulta de eventos necesita una zona, mientras que la consulta de estado requiere un identificador. Esta diferencia explica por qué no basta con reconocer una palabra: también hay que verificar qué dato permite responder. El chatbot no conserva una conversación anterior para completar la siguiente pregunta.

La arquitectura mantiene cuatro componentes relacionados: el usuario plantea la consulta, el chatbot la interpreta, la base aporta la información y el flujo determina cómo responder o pedir una reformulación. Las funciones y archivos que materializan esta organización se explican en la guía técnica del repositorio.

## 4. Diseña un conjunto de intenciones conversacionales y sus respuestas asociadas. Asegúrate de que las intenciones correspondan con el problema, los usuarios y el alcance previamente definidos.

Organicé las intenciones alrededor de lo que el usuario necesita hacer. Las tres consultas principales son eventos por zona, estado por identificador y guía por zona. Saludo, ayuda y despedida permiten orientar la interacción; las respuestas de alcance y de consulta no reconocida atienden solicitudes que no se pueden resolver.

| Intención | Ejemplo de consulta | Respuesta o comportamiento |
|---|---|---|
| Saludo | Hola | Presenta al asistente y ofrece ayuda. |
| Ayuda | Necesito ayuda | Explica las consultas disponibles con ejemplos. |
| Alcance | ¿Puedes enviar alertas? | Aclara qué funciones incluye esta versión. |
| Eventos por zona | Eventos en Cruce C | Devuelve el número de registros de la zona. |
| Estado de un evento | Estado NM-001 | Recupera el estado del identificador indicado. |
| Guía por zona | Guía de Cruce C | Presenta la guía disponible para esa zona. |
| Despedida | Adiós | Cierra la interacción. |
| Consulta no reconocida | ¿Qué clima hará mañana? | Sugiere pedir ayuda y reformular la pregunta. |

Una pregunta útil tiene prioridad sobre el saludo que la acompaña. Si alguien escribe «Hola, eventos en Cruce C», lo importante es responder la consulta, no detenerse en la bienvenida. También distingo una consulta incompleta de una consulta válida sin resultados: pedir una zona no es lo mismo que informar que esa zona tiene cero registros.

En una consulta de guía, la ausencia de información debe comunicarse. No tendría sentido completar una orientación de seguridad con una respuesta inventada. Estas decisiones delimitan el comportamiento esperado y sirven como criterios para las pruebas.

## 5. Implementa un chatbot basado en reglas utilizando Python 3.10 o superior y NLTK. Utiliza Google Colab para el desarrollo y conserva el código fuente en GitHub.

La implementación sigue una secuencia: recibir el texto, normalizarlo, tokenizarlo, aplicar reglas y recuperar la información necesaria. Python permite organizar esas tareas en funciones y una clase de chatbot; NLTK interviene mediante `wordpunct_tokenize`, que divide el texto en unidades utilizables por las reglas (NLTK Project, s. f.).

La normalización reduce diferencias de escritura, como mayúsculas y tildes. Después, las reglas buscan expresiones previstas y los datos de la consulta. Esta elección corresponde a una primera versión con intenciones delimitadas; no requiere entrenar un modelo ni permite afirmar que el chatbot comprende cualquier forma de preguntar.

El código mantiene separados el comportamiento del bot, la base JSON y las formas de ejecutarlo. Así, el notebook y la terminal llaman a la misma solución, en lugar de mantener dos versiones distintas. Las pruebas se encuentran aparte para contrastar el comportamiento con resultados esperados.

### Código fuente

El siguiente fragmento de la implementación muestra la relación entre la consulta y la base:

```python
count = sum(item["zone"] == zone for item in self.knowledge["events"])
noun = "registro disponible" if count == 1 else "registros disponibles"
return Reply("consultar_eventos", f"{zone} tiene {count} {noun}.")
```

El número se obtiene de los registros asociados con la zona. La respuesta no contiene una cifra fija que aparente consultar información. Este fragmento pertenece a una rama que previamente revisa si se reconoció la zona; el archivo completo, las reglas y los comandos de ejecución están en GitHub.

El notebook se entrega en formato `.ipynb`, compatible con Google Colab (Google, s. f.). La evidencia disponible corresponde a ejecución local. El repositorio [Factory Guardian Avance 1](https://github.com/rubenstrada/Factory-Guardian-Avance-1) conserva la implementación, el notebook y las instrucciones para repetir las comprobaciones.

## 6. Realiza pruebas funcionales mediante, al menos, diez conversaciones distintas. Verifica el comportamiento del chatbot ante las intenciones definidas y conserva evidencias de ejecución.

Las pruebas contrastan las intenciones y elementos de respuesta con expectativas definidas. Se revisaron consultas correctas, información faltante, registros inexistentes, diferencias de escritura y solicitudes fuera del alcance. Cada conversación incluye dos mensajes de usuario procesados de manera independiente. El resumen relaciona cada situación con el comportamiento observado.

| Caso | Situación comprobada | Resultado observado |
|---|---|---|
| C01 | Saludo y solicitud de ayuda | Presentación y ejemplos de consulta. |
| C02 | Cruce C y Andén A | Cuatro registros y cero registros, respectivamente. |
| C03 | Saludo con consulta en mayúsculas y Pasillo B | Prioriza la consulta; devuelve cuatro y cero registros. |
| C04 | Estados de NM-001 y NM-003 | Abierto y Cerrado, respectivamente. |
| C05 | NM-999 inexistente y NM-002 | Informa la ausencia; recupera En revisión. |
| C06 | Eventos sin zona y pregunta completa | Pide reformular; después devuelve cuatro registros. |
| C07 | Estado sin ID y consulta de NM-004 | Solicita identificador; después recupera Abierto. |
| C08 | Guías de Cruce C y Andén A | Presenta G-01; comunica que no hay guía para Andén A. |
| C09 | Cámaras, alertas y registro de eventos | Explica el alcance sin ejecutar esas operaciones. |
| C10 | Consulta del clima y despedida | Orienta la reformulación y cierra la interacción. |

El registro de ejecución conserva veinte mensajes aprobados y ninguno fallido. La suite automatizada también registra 26 pruebas aprobadas, entre ellas la ejecución del notebook desde un directorio vacío. Las transcripciones completas, expectativas y salidas están en GitHub; aquí presento su propósito y un ejemplo del comportamiento observado.

## 7. Analiza los resultados obtenidos e identifica las principales limitaciones de esta primera versión, así como posibles mejoras para las siguientes etapas del proyecto.

Los resultados muestran que el prototipo responde conforme a los casos definidos. La consulta de Cruce C devuelve cuatro registros y la de Andén A devuelve cero porque recuperan contenidos distintos de la misma base. Esa diferencia comprueba la consulta; no permite comparar el riesgo de ambas zonas, porque el conjunto no mide exposición, frecuencia ni condiciones reales de operación.

Las conversaciones incompletas muestran otro aspecto importante. El asistente solicita la información necesaria antes de responder, pero el siguiente mensaje debe contener la pregunta completa. Esto simplifica el flujo y evita depender de un contexto implícito, aunque resulta menos cómodo que una conversación con memoria. La limitación debe considerarse al evaluar la experiencia de uso.

El resultado de veinte mensajes aprobados no equivale a una exactitud general del 100 %. Se verificaron ejemplos conocidos, no una muestra representativa del lenguaje de los usuarios. Una expresión no prevista puede quedar sin reconocer; preguntas con varias intenciones o negaciones complejas pueden coincidir con reglas sin representar correctamente lo solicitado.

También es necesario separar un estado registrado de una conclusión operativa. Que NM-003 aparezca como Cerrado indica lo que contiene la base; el chatbot no verificó que una condición de seguridad se haya resuelto. La información y las guías necesitarían responsables de actualización y validación antes de utilizarse en una planta.

La siguiente mejora que priorizaría es probar consultas de usuarios y revisar cuáles no se reconocen. Con esa evidencia tendría sentido ampliar las reglas o incorporar técnicas posteriores de procesamiento del lenguaje. La memoria conversacional podría añadirse si las pruebas muestran dificultades frecuentes para reformular. Las cámaras y alertas corresponden a etapas distintas, con datos y validaciones propias.

## Conclusiones

Mi conclusión es que la primera tarea de Factory Guardian no era incorporar todas las capacidades de la idea original, sino precisar una necesidad que pudiera atender y comprobar. El chatbot permite relacionar una pregunta con datos disponibles y reconocer cuándo falta información. Ese recorrido aporta una base concreta para las siguientes etapas.

Mantengo la distinción entre recuperar información y decidir sobre una situación de seguridad. Las pruebas permiten revisar el funcionamiento de las reglas; la utilidad para el usuario todavía requiere evaluarse en su contexto. Antes de ampliar el proyecto, revisaría si las consultas propuestas corresponden con lo que el supervisor realmente necesita y cómo mantiene actualizados sus antecedentes.

## Uso de herramientas

La idea de Factory Guardian y el alcance que buscaba desarrollar partieron de mí. Primero planteé la necesidad del usuario y después acoté esta entrega a consultas sobre eventos, estados y una guía. Mi experiencia con un backend anterior, donde había concentrado demasiada lógica en `app.py`, influyó en la preferencia por una organización separada por responsabilidades.

Utilicé Codex para discutir alternativas, concretar las especificaciones en código y apoyar la revisión, la preparación del notebook y la documentación. También asistió en la ejecución de las pruebas, cuyos resultados y entorno quedan registrados en el repositorio. El trabajo se fue ajustando al alcance y a la forma de presentación que fui indicando.

Mi responsabilidad sobre la entrega incluye comprender por qué cada consulta necesita determinados datos, de dónde sale la respuesta y qué límites tienen sus resultados. La nota metodológica ampliada de GitHub explica este proceso; el código y las evidencias permiten contrastar la explicación del documento con la implementación.

## Referencias

Google. (s. f.). *Colaboratory frequently asked questions*. Recuperado el 25 de octubre de 2026, de https://research.google.com/colaboratory/faq.html

NLTK Project. (s. f.). *nltk.tokenize package*. Recuperado el 25 de octubre de 2026, de https://www.nltk.org/api/nltk.tokenize.html

Occupational Safety and Health Administration. (s. f.). *Powered industrial trucks eTool: Understanding the workplace—Pedestrian traffic*. U.S. Department of Labor. Recuperado el 25 de octubre de 2026, de https://www.osha.gov/etools/powered-industrial-trucks/workplace/pedestrian-traffic
