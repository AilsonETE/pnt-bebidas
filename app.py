from flask import Flask, render_template, url_for
import sqlite3
app = Flask(__name__)

def conexao():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin")
def dashboard():
    return render_template('admin/dashboard.html')

@app.route("/listarcategoria")
def listarCategoria():
    conn = conexao()
    categoria = conn.execute('select * from categoria')
    return render_template('admin/listar_categoria.html',
                           categorias = categoria )




app.run(debug=True)