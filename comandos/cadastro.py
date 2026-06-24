import mysql.connector
import datetime
from banco_dados import abrir_conexao
from interfaces.interface import exibir_planos
from interfaces.funcontinuar import exibir_submenu


def cad_aluno(): #==============================  CADASTRA ALUNOS ===========================
    ''' 
    Essa função permite que o usuário crie o cadastro de um novo aluno
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")
        
        novo_nome = input("\nDigite o nome do novo aluno: ").strip()
        novo_email = input("Digite o e-mail do novo aluno: ").strip()

        novo_peso_str = input("Digite o peso (Kg) do aluno (ou ENTER para deixar vazio): ") or ""
        nova_altura_str = input("Digite a altura (m) do aluno (ou ENTER para deixar vazio): ") or ""
        try:
            novo_peso = float(novo_peso_str) if novo_peso_str else 0.0
            nova_altura = float(nova_altura_str) if nova_altura_str else 0.0
            print("\nPlanos Disponíves:")
            exibir_planos()
            novo_plano = int(input("\nQual plano deseja contratar? "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")

        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT id, preco FROM planos WHERE id = %s", (novo_plano,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print("ERRO: O plano selecionado não existe")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")       
        else:
            try:
                cursor.execute("SELECT qtde_aulas FROM planos WHERE id = %s", (novo_plano,))
                aulas = cursor.fetchone()
                
                cursor.execute("""
                    INSERT INTO aluno (nome, email, peso, altura, id_plano, aulas_disp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (novo_nome, novo_email, novo_peso, nova_altura, novo_plano, aulas[0]))
                
                cursor.execute("""
                    INSERT INTO vendas
                    (horario, id_prodserv, qtde, subtotal)
                    VALUES (%s, %s, 1, %s)
                """, (
                    datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
                    novo_plano,
                    resultado[1]
                ))
                conexao.commit()

                print(f"Aluno {novo_nome} cadastrado com SUCESSO!\n")


            except mysql.connector.Error as erro:
                conexao.rollback()
                print("arquivo cadastro - linha 394")
                print(f"ERRO FALTAL DE CONEXÃO COM O BANCO: {erro}")
                input("Aperte ENTER para continuar")
                break
            finally:
                if 'conexao' in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")


def cad_produtos():
    '''
    Função responsavel por cadastrar um novo produto
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")

        # inputs para receber o nome e categoria do novo produto/serviço
        print(" ----- Cadastrar Produto ou Serviço ----- ")
        novo_nome = input("\nQual o nome do novo produto/serviço?")
        print(
            "1 - Serviços",
            "2 - Equipamentos",
            "3 - Alimentos",
            "4 - Bebidas",
            "5 - Suplementos",
            "6 - Cosméticos",
            "7 - Diversos"
        )
        try:
            nova_categoria = int(input("\nQual categoria esse novo produto/serviço? "))
        except ValueError:
            print("")
        if nova_categoria == 1:
            print("")
        

        # inputs para receber o preço e quantidade do novo produto/serviço
        try:
            novo_preco = float(input("Qual o valor (R$) desse novo produto/serviço?\n"))
            if nova_categoria.lower() == "serviços":
                    nova_qtde = 0
            else:
                nova_qtde = int(input("Qual a quantidade inicial desse novo produto?\n"))
                
        except ValueError:
            print("ERROR: Entrada invalida!")
            return
        
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            
            cursor.execute("""
                INSERT INTO prodserv(nome, categoria, preco, qtde)
                VALUES(%s,%s,%s,%s)
            """, (novo_nome, nova_categoria, novo_preco, nova_qtde))

            conexao.commit()
            print(f"Produto/Serviço {novo_nome} adicionado com sucesso!")
            return
        
        except mysql.connector.Error as erro:
            conexao.rollback()
            print("arquivo cadastro - linha 446")
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")
            
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()




def cad_planos():
    '''
    Função responsavel por cadastrar um novo plano
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Cadastrar Novo Plano'")
            continue
        
        # input para receber o nome do novo plano
        print(" ----- Cadastrar Plano de Aulas ----- \n")
        novo_nome = input("Qual o nome do novo plano?\n")
    
        # inputs para receber o preço e quantidade de aulas do novo plano
        try:
            novo_preco = float(input("Qual o valor desse novo plano?\n"))
            nova_qtde_aulas = int(input("Qual a quantidade de aulas desse novo plano?\n"))
        except ValueError:
            print("ERROR: Entrada inválida!")
            return
        
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            
            cursor.execute("""
                INSERT INTO planos(nome, preco, qtde_aulas)
                VALUES(%s,%s,%s)
            """, (novo_nome, novo_preco, nova_qtde_aulas))

            conexao.commit()
            print(f"Plano {novo_nome} adicionado com sucesso!")
            return
        
        except mysql.connector.Error as erro:
            conexao.rollback()
            print("arquivo cadastro - linha 496")
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
            
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()