import mysql.connector
from banco_dados import abrir_conexao
from interfaces.interface import exibir_prod
from interfaces.funcontinuar import exibir_submenu


def repor_est():
    exibir_prod()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Repor Estoque'")
            
        try:
            id_prod = int(input("\nDigite o [ID] do produto que deseja repor estoque: "))
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro!")
            continuar = exibir_submenu("'Repor Estoque'")
            continue
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome, categoria, qtde FROM prodserv WHERE id = %s AND ativo = 1", (id_prod,))
            prod = cursor.fetchone()

            if not prod:
                print("ERRO: O produto buscado não existe ou está inativo!")
                continue
            elif prod[1].lower() == "serviços":
                print("ERRO: Não é possível alterar o estoque de serviços!")
                continue

            print(f"\nEstoque disponível de {prod[0]}: {prod[2]} unidades")
            try:
                qtde_rep = int(input("\nQuantas unidades deseja adicionar no estoque? "))
            except ValueError:
                print("ERRO: A quantidade deve ser um número inteiro")
                continue
            if qtde_rep < 0:
                print("ERRO: A quantidade não pode ser negativa!")
                continue
            
            cursor.execute("UPDATE prodserv SET qtde = qtde + %s WHERE id = %s", (qtde_rep, id_prod))
            conexao.commit()

            print(f"\nEstoque do produto {prod[0]} atualizado para {prod[2] + qtde_rep} com SUCESSO!")
            break
        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

def repor_est_lote():
    print("")



def red_est():
    exibir_prod()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Reduzir Estoque'")
        try:
            id_prod = int(input("\nDigite o [ID] do produto que deseja reduzir estoque: "))
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro!")
            continuar = exibir_submenu("'Reduzir Estoque'")
            continue

        






















