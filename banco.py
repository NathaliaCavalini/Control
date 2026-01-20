import sqlite3
import os
import json
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), 'notas.db')


def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  titulo TEXT,
                  conteudo TEXT,
                  cor_fundo TEXT,
                  cor_texto TEXT,
                  fonte TEXT,
                  wallpaper TEXT,
                  senha TEXT,
                  anexos TEXT,
                  checklist TEXT)''')
    conn.commit()
    conn.close()


def salvar_nota(id_nota, titulo, conteudo, cor_fundo, cor_texto, fonte, wallpaper, senha, anexos, checklist):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cor_fundo_str = json.dumps(cor_fundo)
    cor_texto_str = json.dumps(cor_texto)
    anexos_str = json.dumps(anexos)
    checklist_str = json.dumps(checklist)
    senha_hash = hashlib.sha256(senha.encode()).hexdigest() if senha else ""

    if id_nota:
        c.execute("""
            UPDATE notas SET titulo=?, conteudo=?, cor_fundo=?, cor_texto=?, fonte=?, wallpaper=?, senha=?, anexos=?, checklist=?
            WHERE id=?
        """, (titulo, conteudo, cor_fundo_str, cor_texto_str, fonte, wallpaper, senha_hash, anexos_str, checklist_str, id_nota))
    else:
        c.execute("""
            INSERT INTO notas (titulo, conteudo, cor_fundo, cor_texto, fonte, wallpaper, senha, anexos, checklist)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titulo, conteudo, cor_fundo_str, cor_texto_str, fonte, wallpaper, senha_hash, anexos_str, checklist_str))

    conn.commit()
    conn.close()


def listar_notas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, titulo FROM notas ORDER BY id DESC")
    return c.fetchall()


def carregar_nota(id_nota):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM notas WHERE id=?", (id_nota,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'titulo': row[1],
            'conteudo': row[2],
            'cor_fundo': json.loads(row[3]),
            'cor_texto': json.loads(row[4]),
            'fonte': row[5],
            'wallpaper': row[6],
            'senha': row[7],
            'anexos': json.loads(row[8] or '[]'),
            'checklist': json.loads(row[9] or '[]')
        }
    return {}


def deletar_nota(id_nota):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM notas WHERE id=?", (id_nota,))
    conn.commit()
    conn.close()