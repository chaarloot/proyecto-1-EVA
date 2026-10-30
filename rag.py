# -*- coding: utf-8 -*-
import ollama
from qdrant_client import QdrantClient, models
import config
import db

_ollama = ollama.Client(host=config.OLLAMA_HOST)
_qdrant = QdrantClient(url=config.QDRANT_URL)

def embedding(texto):
    respuesta = _ollama.embed(model=config.EMBEDDING_MODEL, input=texto)
    return list(respuesta.embeddings[0])

def crear_coleccion(reiniciar=False):
    if reiniciar and _qdrant.collection_exists(config.QDRANT_COLLECTION):
        _qdrant.delete_collection(config.QDRANT_COLLECTION)
    if not _qdrant.collection_exists(config.QDRANT_COLLECTION):
        _qdrant.create_collection(
            collection_name=config.QDRANT_COLLECTION,
            vectors_config=models.VectorParams(
                size=config.EMBEDDING_DIM, distance=models.Distance.COSINE),
        )

def indexar_tecnica(tecnica):
    texto_completo = f"{tecnica['titulo']} - {tecnica['categoria']}: {tecnica['descripcion']}"
    _qdrant.upsert(
        collection_name=config.QDRANT_COLLECTION,
        points=[models.PointStruct(
            id=tecnica["id"],
            vector=embedding(texto_completo),
            payload={
                "titulo": tecnica["titulo"],
                "categoria": tecnica["categoria"],
                "descripcion": tecnica["descripcion"]
            },
        )],
    )

def reindexar_todo():
    crear_coleccion(reiniciar=True)
    tecnicas = db.listar_tecnicas()
    for t in tecnicas:
        indexar_tecnica(t)
    return len(tecnicas)

def buscar(consulta, limite=3):
    respuesta = _qdrant.query_points(
        collection_name=config.QDRANT_COLLECTION,
        query=embedding(consulta),
        limit=limite,
    )
    scores = {p.id: p.score for p in respuesta.points}
    tecnicas = db.obtener_tecnicas_por_ids(list(scores))
    for t in tecnicas:
        t["score"] = round(scores[t["id"]], 4)
    return sorted(tecnicas, key=lambda x: x["score"], reverse=True)