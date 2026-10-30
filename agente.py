# -*- coding: utf-8 -*-
import ollama
import config
import rag

_ollama = ollama.Client(host=config.OLLAMA_HOST)

# --- MÓDULO DE SEGURIDAD / BOTÓN DE FRENO ---
PALABRAS_RIESGO = [
    "hacerme daño", "suicid", "no quiero vivir", "acabar con todo",
    "quitarme la vida", "autolesi", "matarme"
]

MENSAJE_CRISIS = (
    "⚠️ **PROTOCOLO DE EMERGENCIA ACTIVADO** ⚠️\n\n"
    "Siento mucho que estés pasando por un momento tan duro. Como IA de apoyo emocional, "
    "mi prioridad es tu seguridad y no puedo gestionar situaciones de crisis grave por mí misma.\n\n"
    "Por favor, contacta con profesionales inmediatamente:\n"
    "• **Línea a la conducta suicida:** 024 (Gratuito y 24h)\n"
    "• **Teléfono de la Esperanza:** 717 003 717\n"
    "• **Emergencias:** 112\n\n"
    "No estás solo/a. Por favor acude a urgencias o habla con alguien de tu confianza."
)

PROMPT_TERAPEUTA = """Eres PSYAGENT, una inteligencia artificial de apoyo emocional diseñada para escuchar con empatía \
y ofrecer herramientas basadas en psicología.

Reglas:
1. Sé empático, cálido y comprensivo. Escucha sin juzgar.
2. Usa ÚNICAMENTE las Técnicas de Psicología recuperadas de la base de datos (RESULTADOS RAG).
3. Adapta el consejo o ejercicio práctico al problema expresado.
4. NUNCA inventes teorías psicológicas ni diagnostiques trastornos graves.
"""

_memoria = {}

def obtener_memoria(conversacion_id):
    return _memoria.setdefault(conversacion_id, {"historial": []})

def evaluar_riesgo(mensaje):
    msg_lc = mensaje.lower()
    return any(p in msg_lc for p in PALABRAS_RIESGO)

def preguntar(conversacion_id, mensaje):
    # 1. EVALUACIÓN DEL BOTÓN DE FRENO
    if evaluar_riesgo(mensaje):
        return MENSAJE_CRISIS

    memoria = obtener_memoria(conversacion_id)
    memoria["historial"].append({"role": "user", "content": mensaje})

    # 2. BÚSQUEDA RAG EN LA BIBLIOTECA VECTORIAL
    tecnicas = rag.buscar(mensaje, limite=2)
    contexto_teorico = "\n".join([f"- {t['titulo']}: {t['descripcion']}" for t in tecnicas])

    # 3. GENERACIÓN EMPÁTICA
    mensajes = (
        [{"role": "system", "content": PROMPT_TERAPEUTA}]
        + memoria["historial"][-6:]
        + [{"role": "system", "content": f"TÉCNICAS Y HERRAMIENTAS VALIDADAS (RAG):\n{contexto_teorico}"}]
    )

    respuesta = _ollama.chat(model=config.LLM_MODEL, messages=mensajes).message.content
    respuesta_limpia = (respuesta or "").replace("**", "").strip()

    memoria["historial"].append({"role": "assistant", "content": respuesta_limpia})
    return respuesta_limpia