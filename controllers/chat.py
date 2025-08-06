from controllers.sql import Banco 
from flask import session

class Chat:
    def __init__(self, mensagem = None):
        self.mensagem = mensagem
        self.banco = Banco()        

    def enviar_mensagem(self):
        usuario = session.get("nome_usuario")
        try:
            dados = {
                'mensagem': f"{usuario}: {self.mensagem}",
            }

            self.banco.inserir('tb_chat', dados)
            print("Chat.py | Enviar Mensagem | Enviado com sucesso")
        except:
            print("Chat.py | Enviar Mensagem | Erro ao enviar")
            
    def consultar_mensagem(self):
        try:
            dados = self.banco.consultar('tb_chat')
            print("Chat.py | Consultar Mensagem | Consultado com sucesso")
            return dados
        except:
            print("Chat.py | Consultar Mensagem | Erro ao consultar")