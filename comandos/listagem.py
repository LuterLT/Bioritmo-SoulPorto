from banco_dados import abrir_conexao
from interfaces.interface import exibir_users, exibir_prod, exibir_planos


def listagem_geral():
    print("\nListagem geral\n")
    listagem_alunos()
    listagem_planos()
    listagem_produtos()


def listagem_alunos():
    exibir_users()


def listagem_produtos():
    exibir_prod()


def listagem_planos():
    exibir_planos()
