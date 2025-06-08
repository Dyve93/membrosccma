
import sqlite3

def criar_banco():
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS membros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            nascimento TEXT,
            endereco TEXT,
            funcao TEXT,
            status TEXT,
            user_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_membro(nome, nascimento, endereco, funcao, status, user_id=None):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute('INSERT INTO membros (nome, nascimento, endereco, funcao, status, user_id) VALUES (?, ?, ?, ?, ?, ?)',
              (nome, nascimento, endereco, funcao, status, user_id))
    conn.commit()
    conn.close()

def editar_membro(id_membro, nome, nascimento, endereco, funcao, status):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute('UPDATE membros SET nome=?, nascimento=?, endereco=?, funcao=?, status=? WHERE id=?',
              (nome, nascimento, endereco, funcao, status, id_membro))
    conn.commit()
    conn.close()

def excluir_membro(id_membro):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute('DELETE FROM membros WHERE id=?', (id_membro,))
    conn.commit()
    conn.close()

def buscar_membros(status=None):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    if status:
        c.execute('SELECT * FROM membros WHERE status = ?', (status,))
    else:
        c.execute('SELECT * FROM membros')
    membros = c.fetchall()
    conn.close()
    return membros

def buscar_aniversariantes(mes):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute("SELECT * FROM membros WHERE strftime('%m', nascimento) = ?", (f'{mes:02}',))
    membros = c.fetchall()
    conn.close()
    return membros

def buscar_por_nome(nome):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute("SELECT * FROM membros WHERE nome LIKE ?", (f'%{nome}%',))
    membros = c.fetchall()
    conn.close()
    return membros

def buscar_por_user_id(user_id):
    conn = sqlite3.connect('membros.db')
    c = conn.cursor()
    c.execute("SELECT * FROM membros WHERE user_id = ?", (user_id,))
    membro = c.fetchone()
    conn.close()
    return membro
