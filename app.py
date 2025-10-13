from flask import Flask, render_template, url_for, redirect, request
import sqlite3
import base64
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


@app.route("/cadastrarcategoria", methods=['GET','POST'])
def cadastrarCategoria():
    if request.method == 'POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        imagem = request.files.get('imagem')              
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        if nome_categoria:
            conn = conexao()
            conn.execute('INSERT INTO categoria (nome, descricao, imagem ) VALUES (?, ?, ?)',
                (nome_categoria, descricao, imagem_base64))            
            conn.commit()
            conn.close()
            return redirect(url_for('listarCategoria'))        
    return render_template('admin/cadastrar_categoria.html')
    
    
@app.route("/editarcategoria")
def editarCategoria():
    return render_template('admin/editar_categoria.html')




app.run(debug=True)