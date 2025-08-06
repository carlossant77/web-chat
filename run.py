from flask import Flask, render_template, redirect, request, session
import sqlite3
from controllers.chat import Chat
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

nome_usuario = None

app.secret_key = 'chave_para_usar_flask'

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/telinha')
def tela():
    return render_template ("telinha.html")

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        senha_confirmada = request.form['senha1']

        if senha != senha_confirmada:
            print("erro1")
            return render_template('cadastro.html', erro="As senhas não coincidem")

        conexao = sqlite3.connect('models/banco.db')
        cursor = conexao.cursor()

        cursor.execute('SELECT nome FROM tb_clientes WHERE nome = ?', (nome,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            conexao.close()
            print("erro2")
            return render_template('cadastro.html', erro="O nome de usuário já está em uso!")
        
        with sqlite3.connect('models/banco.db') as conexao:
            cursor = conexao.cursor()

        sql = 'INSERT INTO tb_clientes (nome, senha) VALUES (?, ?)'
        cursor.execute(sql, (nome, senha))

        conexao.commit()
        conexao.close()

        return render_template ('index.html')       

    return render_template('cadastro.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conexao = sqlite3.connect('models/banco.db')
        cursor = conexao.cursor()

        sql = "SELECT * from tb_clientes WHERE nome=? AND senha=?"
        cursor.execute(sql, (nome, senha))

        login_usuario = cursor.fetchone()

        if login_usuario:
            print("login efetuado com sucesso")
            session['nome_usuario'] = login_usuario[1]
            print(session['nome_usuario'])  
            return redirect('/chat')
        else:
            print("erro3")
            return render_template("login.html", erro="Não há uma conta com esses dados em nosso sistema.")        
        
    return render_template("login.html")
@app.route('/chat', methods=['POST', 'GET'])
def enviar():
    chat_obj = Chat()

    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        chat_obj.mensagem = mensagem
        chat_obj.enviar_mensagem()  

        socketio.emit('atualizar_lista')

        return redirect('/chat')

    mensagens = chat_obj.consultar_mensagem()
    return render_template('chat.html', mensagens=mensagens)


# app.run(host='127.0.0.1', port=80, debug=True)
# socketio.run(app, host='127.0.0.1', port=80, debug=True)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=80, debug=True)
