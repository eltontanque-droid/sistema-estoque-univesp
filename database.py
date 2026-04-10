import sqlite3

conn = sqlite3.connect("estoque.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    minimo INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")
dir
