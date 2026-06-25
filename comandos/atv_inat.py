import mysql.connector
from banco_dados import abrir_conexao
from interfaces.funcontinuar import exibir_submenu

def aluno_atv_inat(): 
    '''
    essa def altera o estado dos alunos entre inativo e ativo
    '''
    pass

def prodserv__atv_inat():
    '''
    essa def altera o estado dos produtos / serviços entre inativo e ativo
    '''
    pass

def plano_atv_inat():
    '''
    essa def altera o estado dos planos entre inativo e ativo
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativar / desativar plano'")

        print("\nAtivar ou desativar plano?\n",
            " [1] - Ativar plano\n",
            " [2] - Inativar plano\n",
            " [0] - Sair de consultas\n",)
        
        try:
            consulta = int(input("Consulta desejada: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = 0

        if consulta == 0:
            return
        elif consulta == 1:
            plano_atv()
        elif consulta == 2:
            plano_inat()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = 0


def plano_atv():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativar plano'")
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela planos inativos
            cursor.execute("""
                SELECT id, nome, preco, qtde_aulas
                FROM planos
                WHERE ativo = 0
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum plano inativo.")
                continuar = 0
                continue
            else:
                print("\nPlanos inativos:")
                for plano in resultado:
                    larg_nome = max(len(plano[1]) for plano in resultado)
                    print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]:<6} | Aulas permitidas: {plano[3]}")
                print("\n")
            
            try:
                id_plano = int(input("Digite ID do plano a ser ativado"))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            if id_plano not in resultado[0]:
                print("ERRO: Id invalido!")
                continuar = 0
                continue

            cursor.execute("UPDATE planos SET ativo = 1 WHERE id = %s", (id_plano,))
            conexao.commit()
            print(f"Plano '{resultado[1]}' ativado com sucesso!")

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def plano_inat():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'inativar plano'")
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela planos ativos
            cursor.execute("""
                SELECT id, nome, preco, qtde_aulas
                FROM planos
                WHERE ativo = 1
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum plano ativo.")
                continuar = 0
                continue
            else:
                print("\nPlanos ativos:")
                for plano in resultado:
                    larg_nome = max(len(plano[1]) for plano in resultado)
                    print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]:<6} | Aulas permitidas: {plano[3]}")
                print("\n")
            
            try:
                id_plano = int(input("Digite ID do plano a ser inativado"))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            if id_plano not in resultado[0]:
                print("ERRO: Id invalido!")
                continuar = 0
                continue

            cursor.execute("UPDATE planos SET ativo = 0 WHERE id = %s", (id_plano,))
            conexao.commit()
            print(f"Plano '{resultado[1]}' inativado com sucesso!")

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()