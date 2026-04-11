from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123456"


def conectar():
    return sqlite3.connect("estoque.db")

@app.route("/")
def index():
    if not session.get("logado"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == "admin" and senha == "1234":
            session["logado"] = True
            return redirect("/")
        else:
            return "Login inválido"

    return render_template("login.html")

@app.route("/produtos")
def produtos():
    if not session.get("logado"):
        return redirect("/login")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    return render_template("produtos.html", produtos=dados)

@app.route("/add", methods=["GET", "POST"])
def add():
    if not session.get("logado"):
        return redirect("/login")
    if request.method == "POST":
        nome = request.form["nome"]
        quantidade = int(request.form["quantidade"])
        minimo = int(request.form["minimo"])

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, minimo) VALUES (?, ?, ?)",
            (nome, quantidade, minimo)
        )
        conn.commit()
        conn.close()

        return redirect("/produtos")

    return render_template("add.html")

@app.route("/entrada/<int:id>")
def entrada(id):
    if not session.get("logado"):
        return redirect("/login")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET quantidade = quantidade + 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/produtos")

@app.route("/saida/<int:id>")
def saida(id):
    if not session.get("logado"):
        return redirect("/login")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET quantidade = quantidade - 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/produtos")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
