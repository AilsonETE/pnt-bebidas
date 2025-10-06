import sqlite3


def init_db():
    
    conn = sqlite3.connect("database.db")
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

init_db()

