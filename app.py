from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin")
def dashboard():
    return render_template('admin/dashboard.html')

@app.route("/listarcategoria")
def listarCategoria():
    return render_template('admin/listar_categoria.html')




app.run(debug=True)