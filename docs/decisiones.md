# Decisiones del avance

La idea de Factory Guardian surgió de un hackathon. Para desarrollar este avance, preferí convertir una parte pequeña de esa idea en un chatbot que pudiera ejecutar, revisar y explicar.

## Alcance de las consultas

Decidí concentrarme en consultas de solo lectura sobre registros ficticios y una guía demostrativa. El chatbot permite revisar eventos por zona, buscar el estado de un registro y consultar la guía. Así puedo mostrar la relación entre una pregunta y los datos utilizados para responderla.

## Reglas y procesamiento del texto

El prototipo utiliza Python 3.10+ y NLTK para tokenizar los mensajes. Las reglas identifican ocho intenciones: saludo, ayuda, alcance, consulta de eventos, consulta de estado, consulta de procedimiento, despedida y mensaje no reconocido. Este alcance no requiere entrenar un modelo ni utilizar un servicio externo.

Una consulta útil tiene prioridad sobre el saludo que pueda acompañarla. Si falta una zona o un ID necesario, el chatbot pide reformular la pregunta completa. Cada mensaje se interpreta por separado, para que el comportamiento pueda seguirse sin depender de un contexto conversacional implícito.

## Información de ejemplo

El conocimiento contiene cuatro registros ficticios de interacción entre peatones y montacargas, con ID, zona y estado. Los recuentos se obtienen de esos registros. La guía también es demostrativa: permite revisar la respuesta del chatbot sin atribuirle validez como procedimiento de una planta real.

## Organización del proyecto

Quise separar el chatbot de la forma de utilizarlo: la misma clase puede llamarse desde Python, la terminal o el notebook. Esa preferencia viene de una experiencia anterior con un backend de ERP, en el que concentrar demasiada lógica en `app.py` dificultaba localizar responsabilidades. Aquí el conocimiento se conserva en JSON y las comprobaciones tienen sus propios archivos. Esta organización permite localizar qué parte interpreta el mensaje, de dónde obtiene la información y cómo se revisa la respuesta, sin añadir componentes que este avance todavía no necesita.

## Comprobaciones

La revisión combina pruebas del comportamiento y diez conversaciones separadas, con al menos dos mensajes de usuario en cada una. Se contrastan la intención y elementos esperados de la respuesta, y se conserva la salida obtenida junto con el entorno de ejecución. También se revisan consultas incompletas, zonas sin registros, IDs desconocidos, variaciones de mayúsculas y tildes, y saludos que acompañan una consulta.

El notebook está preparado para Google Colab. La comprobación local se identifica como local; una ejecución en Colab requiere su propia evidencia.

## Posibles siguientes etapas

La visión por computadora, los modelos de lenguaje, RAG y las alertas son posibilidades para desarrollar después. En este avance mantuve el trabajo en el chatbot de consultas por reglas, sin presentar esas posibilidades como capacidades implementadas.

El código, las pruebas y la documentación se desarrollaron con asistencia de Codex, como explico en la [nota de uso de IA](uso_de_ia.md).
