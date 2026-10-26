# Registro de desarrollo y verificación

El asistente Codex realizó estas ejecuciones automatizadas. No se atribuyen al alumno como ejecución manual.

## RED observado, 25 de octubre de 2026

Antes de escribir los módulos del chatbot y el constructor del notebook se ejecutó:

`python -m pytest -q --tb=short --junitxml=artifacts/tdd_red.xml`

Resultado observado: **26 pruebas fallidas, 0 aprobadas**, código de salida 1. Las pruebas del chatbot fallaron explícitamente por la capacidad ausente (`FactoryGuardianBot` todavía no existía). La prueba del notebook falló porque el constructor aún no existía. El XML conserva esa ejecución real; no es una suite final fallida.

## Decisiones de ejecución

- El proyecto es independiente y tiene su propio `.venv`; no se modificaron los entornos de Lumina.
- La primera instalación de dependencias falló por un tiempo de espera al descargar Jedi; el segundo intento con mayor timeout terminó correctamente.
- La interfaz de consultas permanece sin estado. Cada seguimiento debe reformular la consulta completa.
- El notebook contendrá los mismos módulos, conocimiento y casos embebidos. Su ejecución local no constituye evidencia de ejecución en Google Colab.
- El plan general y su seguimiento documental pertenecen al agente coordinador; este registro cubre únicamente código, pruebas y notebook.

## GREEN y notebook verificados

- Primera implementación: 25 pruebas del chatbot aprobadas; después, suite completa de 26 aprobadas.
- Ajuste solicitado de presentación: se actualizaron primero las expectativas del saludo y alcance para usar “base de ejemplo”. La ejecución RED registró 3 fallidas y 22 aprobadas en `tdd_copy_red.xml`; después se acortaron las respuestas sin cambiar reglas ni funciones.
- Verificación final: `python -m pytest -q --tb=short --junitxml=artifacts/test_results.xml` devolvió **26 aprobadas, 0 fallos, 0 errores**.
- `python scripts/run_conversations.py` ejecutó diez sesiones y veinte mensajes: **20 aprobados, 0 fallidos**.
- `python scripts/build_notebook.py --execute` inició un kernel nuevo local y ejecutó las seis celdas de código sin outputs de error. Una prueba de integración también lo ejecutó desde un directorio vacío.
- La comparación mediante `nbformat` confirmó que el notebook incluye exactamente los módulos de chatbot y evaluación del repositorio y reproduce las veinte respuestas del runner. Una comprobación inicial con `json.loads` comparó erróneamente la lista de líneas de la serialización ipynb con un string; se corrigió la comprobación usando `nbformat`, sin modificar el código del producto.
- Python 3.12.14, NLTK 3.10.4. El kernel local mostró un aviso de transporte TCP; la ejecución finalizó correctamente. No se verificó una ejecución en Google Colab.
