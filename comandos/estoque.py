import mysql.connector
from banco_dados import abrir_conexao
from interfaces.interface import exibir_prod
from interfaces.funcontinuar import exibir_submenu


def repor_est():#def responsavel pela reposição de estoque
    exibir_prod()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Repor Estoque'")
            
        try: #inserir o ID do produto e verifica se o valor está em um formato aceitável
            id_prod = int(input("\nDigite o [ID] do produto que deseja repor estoque: "))
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro!")
            continuar = 0
            continue
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome, categoria, qtde FROM prodserv WHERE id = %s AND ativo = 1", (id_prod,))
            prod = cursor.fetchone()

            if not prod:
                print("ERRO: O produto buscado não existe ou está inativo!")
                continuar = 0
                continue
            elif prod[1] == "Serviços":
                print("ERRO: Não é possível alterar o estoque de serviços!")
                continuar = 0
                continue
            print(f"\nEstoque disponível de {prod[0]}: {prod[2]} unidades")
            try: #Reposição do estoque e verificação de valor aceitável para reposição
                qtde_rep = int(input("\nQuantas unidades deseja adicionar no estoque? "))
            except ValueError:
                print("ERRO: A quantidade deve ser um número inteiro")
                continuar = 0
                continue
            if qtde_rep < 0:
                print("ERRO: A quantidade não pode ser negativa!")
                continuar = 0
                continue
            
            cursor.execute("UPDATE prodserv SET qtde = qtde + %s WHERE id = %s", (qtde_rep, id_prod))
            conexao.commit()

            print(f"\nEstoque do produto {prod[0]} atualizado para {prod[2] + qtde_rep} com SUCESSO!")

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = 0
        continue



def repor_est_lote(qtde_rep, *lista_ids):
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        print(f"\nIniciando reposição de +{qtde_rep} unidades para os IDs selecionados no estoque...")
        for id_produto in lista_ids:
            cursor.execute("SELECT nome, categoria FROM prodserv WHERE id = %s", (id_produto,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"- ERRO: Produto com o ID {id_produto} não existe no sistema")
                return
            
            if resultado[1] == "Serviços":
                print("ERRO: Não é possível alterar o estoque de Serviços")
                return

            nome_prod = resultado[0]

            cursor.execute("""
                UPDATE prodserv
                SET qtde = qtde + %s
                WHERE id = %s
            """, (qtde_rep, id_produto))
            print(f"- Foram adicionadas {qtde_rep} unidades do seguinte produto: {nome_prod}")
            conexao.commit()

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()




def red_est(): #Def responsável por reduzir o estoque
    exibir_prod()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Reduzir Estoque'")
            continue
        try: #Input busca o ID do produto / verifica se é um valor válido 
            id_prod = int(input("\nDigite o [ID] do produto que deseja reduzir estoque: "))
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro!")
            continuar = 0
            continue
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            #busca na db
            cursor.execute("SELECT nome, categoria, qtde FROM prodserv WHERE id = %s AND ativo = 1", (id_prod,))
            prod = cursor.fetchone()
            #verifica se existe o produto
            if not prod:
                print("ERRO: O produto buscado não existe ou está inativo!")
                continuar = 0
                continue
            if prod[1] == "Serviços": #verifica se é um serviço (serviço não tem estoque)
                print("ERRO: Não é possível alterar o estoque de serviços!")
                continuar = 0
                continue
            print(f"\nEstoque disponível de {prod[0]}: {prod[2]} unidades") #apresenta o estoque disponível
            try: #input quantas unidades serão retiradas do estoque / verifica se valor é válido
                qtde_red = int(input("\nQuantas unidades deseja retirar do estoque? "))
            except ValueError:
                print("ERRO: A quantidade deve ser um número inteiro")
                continuar = 0
                continue
            if qtde_red > prod[2]:
                print("ERRO: Não é possível retirar mais itens que os disponíveis em estoque!")
                continuar = 0
                continue
            if qtde_red == prod[2]:
                try:# confirmação 
                    conf = int(input("O estoque será zerado. Você tem certeza que deseja fazer isso? (1 - Sim | 2 - Não) "))
                except ValueError:
                    print("ERRO: A entrada deve ser um número. Operação cancelada")
                    continuar = 0
                    continue
                if conf == 1:
                    pass
                elif conf == 2:
                    print("Operação Cancelada")
                    continuar = 0
                    continue
                else:
                    print("ERRO: Opção Inválida. Operação Cancelada.")
                    continuar = 0
                    continue
                
            cursor.execute("UPDATE prodserv SET qtde = qtde - %s WHERE id = %s", (qtde_red, id_prod))
            conexao.commit()

            print(f"\nEstoque do produto '{prod[0]}' atualizado para {prod[2] - qtde_red} com SUCESSO!")


        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = 0
        continue



