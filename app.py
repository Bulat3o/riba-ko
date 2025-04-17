from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# Модель игрока
class Player(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(50), nullable=False)
   score = db.Column(db.Integer, nullable=False)


# Главная страница со списком игроков
@app.route('/')
def index():
   players = Player.query.order_by(Player.score.desc()).all()
   return render_template('index.html', players=players)


# Страница добавления нового игрока
@app.route('/add', methods=['GET', 'POST'])
def add_player():
   if request.method == 'POST':
       name = request.form['name']
       score = int(request.form['score'])
       new_player = Player(name=name, score=score)
       db.session.add(new_player)
       db.session.commit()
       return redirect(url_for('index'))
   return render_template('add_player.html')


# Страница изменения игрока
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_player(id):
   player = Player.query.get_or_404(id)
   if request.method == 'POST':
       player.name = request.form['name']
       player.score = int(request.form['score'])
       db.session.commit()
       return redirect(url_for('index'))
   return render_template('edit_player.html', player=player)


# Удаление игрока
@app.route('/delete/<int:id>', methods=['POST'])
def delete_player(id):
   player = Player.query.get_or_404(id)
   db.session.delete(player)
   db.session.commit()
   return redirect(url_for('index'))


if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   app.run(debug=True)
