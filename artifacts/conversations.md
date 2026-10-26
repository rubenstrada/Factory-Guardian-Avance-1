# Diez conversaciones de prueba de Factory Guardian

Escenarios ficticios de evaluación; las respuestas siguientes fueron ejecutadas.
Entorno: local. Python: 3.12.14. NLTK: 3.10.4.
Sesiones: 10; mensajes: 20; aprobados: 20; fallidos: 0.
Sin memoria entre turnos: los seguimientos contienen la consulta completa.

## C01: Presentación y orientación

1. Usuario: Hola

   Bot [saludo]: Hola, soy Factory Guardian. Consulto una base de ejemplo por reglas. Escribe 'ayuda' para conocer las consultas disponibles.

   Esperado: saludo; contiene ['Factory Guardian', 'base de ejemplo']. Resultado: APROBADO.

2. Usuario: Necesito ayuda

   Bot [ayuda]: Puedo consultar eventos por zona, el estado de un ID y una guía demostrativa. Ejemplos: 'Eventos en Cruce C', 'Estado NM-001', 'Guía de Cruce C'. Envía cada consulta completa.

   Esperado: ayuda; contiene ['eventos', 'estado', 'guía']. Resultado: APROBADO.

## C02: Contrastar una zona con registros y una zona vacía

1. Usuario: ¿Cuántos near-miss hay en el Cruce C?

   Bot [consultar_eventos]: Cruce C tiene 4 registros disponibles.

   Esperado: consultar_eventos; contiene ['4 registros', 'Cruce C']. Resultado: APROBADO.

2. Usuario: ¿Cuántos eventos hay en Andén A?

   Bot [consultar_eventos]: Andén A tiene 0 registros disponibles.

   Esperado: consultar_eventos; contiene ['0 registros', 'Andén A']. Resultado: APROBADO.

## C03: Prioridad de consulta útil y normalización

1. Usuario: Hola, ¿CUÁNTOS EVENTOS hay en CRUCE C?

   Bot [consultar_eventos]: Cruce C tiene 4 registros disponibles.

   Esperado: consultar_eventos; contiene ['4 registros', 'Cruce C']. Resultado: APROBADO.

2. Usuario: Muéstrame eventos en PASILLO B.

   Bot [consultar_eventos]: Pasillo B tiene 0 registros disponibles.

   Esperado: consultar_eventos; contiene ['0 registros', 'Pasillo B']. Resultado: APROBADO.

## C04: Estados de dos identificadores existentes

1. Usuario: ¿Cuál es el estado de NM-001?

   Bot [consultar_estado]: NM-001: Abierto. Zona: Cruce C.

   Esperado: consultar_estado; contiene ['NM-001', 'Abierto']. Resultado: APROBADO.

2. Usuario: Consulta estado de NM-003

   Bot [consultar_estado]: NM-003: Cerrado. Zona: Cruce C.

   Esperado: consultar_estado; contiene ['NM-003', 'Cerrado']. Resultado: APROBADO.

## C05: Identificador inexistente y reformulación completa

1. Usuario: Estado de NM-999

   Bot [consultar_estado]: El ID NM-999 no existe en la base de conocimiento.

   Esperado: consultar_estado; contiene ['NM-999', 'no existe']. Resultado: APROBADO.

2. Usuario: Estado NM-002

   Bot [consultar_estado]: NM-002: En revisión. Zona: Cruce C.

   Esperado: consultar_estado; contiene ['NM-002', 'En revisión']. Resultado: APROBADO.

## C06: Consulta de eventos sin zona

1. Usuario: ¿Cuántos eventos hay?

   Bot [consultar_eventos]: Escribe la consulta completa con una zona válida: Cruce C, Andén A, Pasillo B. La zona está ausente o no se reconoce. No conservo contexto entre mensajes.

   Esperado: consultar_eventos; contiene ['consulta completa', 'zona', 'Cruce C']. Resultado: APROBADO.

2. Usuario: ¿Cuántos eventos hay en Cruce C?

   Bot [consultar_eventos]: Cruce C tiene 4 registros disponibles.

   Esperado: consultar_eventos; contiene ['4 registros', 'Cruce C']. Resultado: APROBADO.

## C07: Consulta de estado sin identificador

1. Usuario: Necesito saber el estado

   Bot [consultar_estado]: Indica el ID completo en la consulta, por ejemplo: ¿Cuál es el estado de NM-001? No conservo contexto entre mensajes.

   Esperado: consultar_estado; contiene ['ID completo', 'NM-001']. Resultado: APROBADO.

2. Usuario: ¿Cuál es el estado de NM-004?

   Bot [consultar_estado]: NM-004: Abierto. Zona: Cruce C.

   Esperado: consultar_estado; contiene ['NM-004', 'Abierto']. Resultado: APROBADO.

## C08: Guía disponible y zona sin guía

1. Usuario: Consulta el procedimiento del Cruce C

   Bot [consultar_procedimiento]: Guía demostrativa G-01, ficticia: consultar la señalización y la segregación del cruce en el procedimiento aprobado de la planta y solicitar revisión al responsable de seguridad. Esta guía no sustituye un procedimiento real ni una evaluación profesional.

   Esperado: consultar_procedimiento; contiene ['G-01', 'demostrativa', 'no sustituye']. Resultado: APROBADO.

2. Usuario: ¿Tienes una guía para Andén A?

   Bot [consultar_procedimiento]: No hay guía demostrativa para Andén A. Consulta el procedimiento aprobado con el responsable de seguridad.

   Esperado: consultar_procedimiento; contiene ['No hay guía', 'Andén A']. Resultado: APROBADO.

## C09: Límites de cámaras, alertas y registro

1. Usuario: ¿Puedes conectar una cámara y enviar alertas?

   Bot [alcance]: Este avance ofrece solo consultas sobre una base de ejemplo. No conecto cámaras, no envío alertas, no registro eventos y no uso un LLM. No sustituyo la revisión humana.

   Esperado: alcance; contiene ['solo consultas', 'No conecto cámaras', 'no envío alertas']. Resultado: APROBADO.

2. Usuario: Quiero registrar un nuevo evento

   Bot [alcance]: Este avance ofrece solo consultas sobre una base de ejemplo. No conecto cámaras, no envío alertas, no registro eventos y no uso un LLM. No sustituyo la revisión humana.

   Esperado: alcance; contiene ['no registro', 'base de ejemplo']. Resultado: APROBADO.

## C10: Solicitud fuera del dominio y cierre

1. Usuario: ¿Qué clima hará mañana?

   Bot [no_reconocida]: No reconozco esa consulta. Escribe 'ayuda' y reformula la pregunta completa con la zona o el ID correspondiente.

   Esperado: no_reconocida; contiene ['No reconozco', 'ayuda']. Resultado: APROBADO.

2. Usuario: Adiós

   Bot [despedida]: Hasta luego. Las consultas de esta demostración no sustituyen la revisión humana.

   Esperado: despedida; contiene ['Hasta luego']. Resultado: APROBADO.
