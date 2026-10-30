
# PSYAGENT — IA para Apoyo Emocional (RAG + Botón de Freno)

Este repositorio contiene la simulación completa de **PSYAGENT**, una arquitectura diseñada para apoyo emocional que resuelve los problemas de alucinación y falta de límites de los LLMs comerciales mediante:

1. **Botón de Freno (Módulo de Seguridad):** Un algoritmo en código tradicional que analiza los mensajes en segundo plano. Si detecta ideación suicida o autolesión, bloquea al agente e imprime el protocolo de emergencia.
2. **Biblioteca de Psicología (RAG + Embeddings):** Base de datos vectorial (Qdrant) cargada con técnicas de Terapia Cognitivo-Conductual (TCC). El agente consulta la base de datos para no inventarse teorías.
3. **Agente Empático (Gemma3 + Ollama):** Formatea las técnicas validadas en respuestas cálidas, cercanas y comprensivas.

## Instrucciones de Ejecución

1. Iniciar Ollama en tu máquina y descargar los modelos:
   ```bash
   ollama pull paraphrase-multilingual
   ollama pull gemma3
   ```
