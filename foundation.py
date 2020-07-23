from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Config da base de dados e seu diretório destino.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///objetos.db'
db = SQLAlchemy(app)

#Config das colunas de dados da base de dados.
class ListaObjetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(100), nullable=False)
    Categoria = db.Column(db.String(20), nullable=False)
    Descrição = db.Column(db.Text, nullable=False)
    Local = db.Column(db.String(20), nullable =False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'ListaObjetos' + str(self.id)

#Pagina inicial, onde o usuario irá logar e entrar no sistema.
@app.route('/')
def pagina_inicial():
        return render_template('index.html')

#Pagina onde a pessoa irá cadastrar o objeto achado.
@app.route('/objetos', methods=['GET', 'POST'])
def objetos():
#Função de cadastro do objeto na base de dados para ser listada.
    if request.method == 'POST':
        objeto_Nome = request.form['Nome']
        objeto_Categoria = request.form['Categoria']
        objeto_Descricao = request.form['Descrição']
        objeto_local = request.form['Local']
        novo_objeto = ListaObjetos(Nome=objeto_Nome, Categoria=objeto_Categoria, Descrição=objeto_Descricao, Local=objeto_local)
        db.session.add(novo_objeto)
        db.session.commit()
        return redirect('/objetos')
    else:
        todos_objetos = ListaObjetos.query.order_by(ListaObjetos.data_criacao).all()
        return render_template('objetos.html', objetos=todos_objetos)

#Função de deletar objetos da lista de objetos dentro da base de dados
@app.route('/objetos/deletar/<int:id>')
def deletar(id):
    objeto = ListaObjetos.query.get_or_404(id)
    db.session.delete(objeto)
    db.session.commit()
    return redirect('/objetos')

#Página onde o usuário irá editar os dados dos objetos cadastrados.
#E Função de edição de dados do objeto cadastrado.
@app.route('/objetos/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    objeto = ListaObjetos.query.get_or_404(id)
    if request.method == 'POST':
        objeto.Nome = request.form['Nome']
        objeto.Categoria = request.form['Categoria']
        objeto.Descrição = request.form['Descrição']
        objeto.Local = request.form['Local']
        db.session.commit()
        return redirect('/objetos')
    else:
        return render_template('editar.html', objeto=objeto)

#Execução da aplicação web
if __name__ == '__main__':
     app.run(threaded=True, port=5000, debug=True)
