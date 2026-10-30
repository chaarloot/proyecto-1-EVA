# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, render_template, request
import agente

app = Flask(__name__)

@app.get("/")
def inicio():
    return render_template("index.html")

@app.post("/api/agente")
def api_agente():
    datos = request.get_json()
    try:
        respuesta = agente.preguntar(datos["conversacion_id"], datos["mensaje"])
    except Exception as error:
        return jsonify({"respuesta": f"Error en el servidor: {error}"}), 500
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "8000")), debug=True)