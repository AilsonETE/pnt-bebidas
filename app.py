from flask import Flask, render_template, url_for, redirect, request
from flask_bcrypt import Bcrypt
import sqlite3
import base64
app = Flask(__name__)
bcrypt = Bcrypt(app)

def conexao():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

"""def usuario_inicial(username, password):    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    conn = conexao()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuario (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        print(f"Usuário '{username}' criado com sucesso.")
    except sqlite3.IntegrityError:
        print(f"Usuário '{username}' já existe.")
    conn.close()
usuario_inicial("admin", "senha123") """

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
        ativo = request.form.get('ativo')
        imagem = request.files.get('imagem')              
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        if nome_categoria:
            conn = conexao()
            conn.execute('INSERT INTO categoria (nome, descricao, ativo, imagem ) VALUES (?, ?, ?, ?)',
                (nome_categoria, descricao, ativo, imagem_base64))            
            conn.commit()
            conn.close()
            return redirect(url_for('listarCategoria'))        
    return render_template('admin/cadastrar_categoria.html')
    
    
@app.route("/editarcategoria/<int:id>", methods=['GET','POST'])
def editarCategoria(id):
    conn = conexao()
    categoria = conn.execute('select * from categoria where id=?', (id,)).fetchone()
    if request.method == 'POST':
        nome_categoria = request.form.get('nome_categoria')
        descricao = request.form.get('descricao')
        ativo = request.form.get('ativo')
        imagem = request.files.get('imagem')              
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        if nome_categoria:
            conn = conexao()
            if imagem:
                conn.execute('UPDATE categoria SET nome=?, descricao=?, ativo=?, imagem=? WHERE id=?',   
                (nome_categoria, descricao, ativo, imagem_base64, id,))           
            else:
                conn.execute('UPDATE categoria SET nome=?, descricao=?, ativo=? WHERE id=?',   
                (nome_categoria, descricao, ativo, id,)) 

            conn.commit()
            conn.close()
            return redirect(url_for('listarCategoria'))

    return render_template('admin/editar_categoria.html',
                            categoria=categoria )

# Rota para excluir categoria
@app.route("/excluir_categoria/<int:id>", methods=['GET', 'POST'])
def excluirCategoria(id):
    conn = conexao()
    categoria = conn.execute('SELECT * FROM categoria WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        conn.execute('DELETE FROM categoria WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listarCategoria'))    
    conn.close()
    return render_template('admin/excluir_categoria.html', categoria = categoria )

@app.route("/login")
def login():
    
    return render_template('admin/login.html')

@app.route("/listarusuario")
def listarUsuario():
    conn = conexao()
    usuario = conn.execute('select * from usuario')
    return render_template('admin/listar_usuario.html',
                           usuario = usuario )


@app.route("/cadastrarusuario", methods=['GET','POST'])
def cadastrarUsuario():
    if request.method == 'POST':
        nome = request.form.get('nome')        
        senha = request.form.get('senha')                  
        senha_cript = bcrypt.generate_password_hash(senha).decode('utf-8')
        
        if nome:
            conn = conexao()
            conn.execute('INSERT INTO usuario (nome, senha ) VALUES (?, ?)',
                (nome, senha_cript))            
            conn.commit()
            conn.close()
            return redirect(url_for('listarUsuario'))        
    return render_template('admin/cadastrar_usuario.html')


@app.route("/editarusuario/<int:id>", methods=['GET','POST'])
def editarUsuario(id):
    conn = conexao()
    usuario = conn.execute('select * from usuario where id=?', (id,)).fetchone()
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        senha_cript = bcrypt.generate_password_hash(senha).decode('utf-8')
        
        if nome:            
            conn.execute('UPDATE usuario SET nome=?, senha=? WHERE id=?',   
                (nome,  senha_cript, id,))   
            
            conn.commit()
            conn.close()
            return redirect(url_for('listarUsuario'))
    return render_template('admin/editar_usuario.html',
                            usuario=usuario )


@app.route("/excluir_usuario/<int:id>", methods=['GET', 'POST'])
def excluirUsuario(id):
    conn = conexao()
    usuario = conn.execute('SELECT * FROM usuario WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        conn.execute('DELETE FROM usuario WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listarUsuario'))    
    conn.close()
    return render_template('admin/excluir_usuario.html', usuario = usuario )

app.run(debug=True)