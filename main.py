from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db'
db = SQLAlchemy(app)

# Modelo de dados
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data_nascimento = request.form['data_nascimento']

        nova_pessoa = Pessoa(nome=nome, email=email, data_nascimento=data_nascimento)

        try:
            db.session.add(nova_pessoa)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um erro ao adicionar pessoa'
        
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)
    

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    pessoa = Pessoa.query.get(id)
    if not pessoa:
        return 'Pessoa não encontrada'

    if request.method == 'POST':
        try:
            db.session.delete(pessoa)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um erro ao excluir a pessoa'

    # Método GET: Mostrar a página de confirmação de exclusão
    return render_template('delecao.html', pessoa=pessoa)





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
