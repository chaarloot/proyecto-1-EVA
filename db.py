# -*- coding: utf-8 -*-
import pymysql
import config

def conectar(con_db=True):
    return pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB if con_db else None,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def crear_esquema():
    with conectar(con_db=False) as conn, conn.cursor() as cur:
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tecnicas (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                titulo      VARCHAR(150) NOT NULL,
                categoria   VARCHAR(80)  NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)

def listar_tecnicas():
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM tecnicas")
        return cur.fetchall()

def obtener_tecnicas_por_ids(ids):
    if not ids:
        return []
    marcadores = ", ".join(["%s"] * len(ids))
    with conectar() as conn, conn.cursor() as cur:
        cur.execute(f"SELECT * FROM tecnicas WHERE id IN ({marcadores})", ids)
        return cur.fetchall()

def crear_tecnica(datos):
    sql = "INSERT INTO tecnicas (titulo, categoria, descripcion) VALUES (%s, %s, %s)"
    with conectar() as conn, conn.cursor() as cur:
        cur.execute(sql, (datos["titulo"], datos["categoria"], datos["descripcion"]))
        return cur.lastrowid