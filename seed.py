# -*- coding: utf-8 -*-
import sys
import db
import rag

BIBLIOTECA_TCC = [
    dict(titulo="Identificación de Distorsiones Cognitivas", categoria="TCC Cognitiva",
            descripcion="Técnica para detectar pensamientos automáticos negativos como el catastrofismo o el pensamiento de todo o nada."),
    dict(titulo="Registro de Pensamientos Disfuncionales", categoria="TCC Cognitiva",
            descripcion="Anotar la situación, la emoción y el pensamiento automático para reestructurarlo por una respuesta racional."),
    dict(titulo="Respiración Diafragmática (4-4-6)", categoria="Ansiedad",
            descripcion="Técnica de respiración profunda para activar el sistema parasimpático y frenar ataques de pánico."),
    dict(titulo="Técnica de Anclaje 5-4-3-2-1", categoria="Ansiedad / Mindfulness",
            descripcion="Ejercicio sensorial para conectar con el presente buscando cosas visibles, audibles y palpables."),
    dict(titulo="Activación Conductual", categoria="Depresión / Estado de Ánimo",
            descripcion="Estrategia para romper el aislamiento dividiendo objetivos diarios en micro-acciones agradables."),
    dict(titulo="Validación Emocional y Escucha Empática", categoria="Apoyo Emocional",
            descripcion="Permitir al usuario desahogarse y validar lo que siente sin juzgar antes de proponer consejos."),
    dict(titulo="Técnica de Resolución de Problemas", categoria="Estrés",
            descripcion="Método estructurado en 5 pasos para analizar problemas agobiantes y tomar decisiones graduales.")
]

if __name__ == "__main__":
    print("1) Inicializando base de datos MySQL...")
    db.crear_esquema()

    if "--si-vacio" in sys.argv and db.listar_tecnicas():
        print("Ya existen datos en el sistema.")
        sys.exit(0)

    print("2) Cargando Biblioteca de Psicología...")
    with db.conectar() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE tecnicas")
    for t in BIBLIOTECA_TCC:
        db.crear_tecnica(t)

    print("3) Generando embeddings e indexando en Qdrant...")
    total = rag.reindexar_todo()
    print(f"Éxito: {total} intervenciones psicológicas listas en PSYAGENT.")