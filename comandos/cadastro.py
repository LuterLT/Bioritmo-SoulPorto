import mysql.connector
import datetime
from banco_dados import abrir_conexao
from interfaces.interface import exibir_planos
from interfaces.funcontinuar import exibir_submenu
from comandos.funcionalidades import validar_email

#cadastro de alunos, produtos e planos...


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
            continue
        
        novo_nome = input("\nDigite o nome do novo aluno: ").strip()
        novo_email = input("Digite o e-mail do novo aluno: ").strip()
        if not validar_email(novo_email):
            print("\nERRO: Email Inválido")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")
            continue

        try:
            novo_peso_str = input("Digite o peso (Kg) do aluno (ou ENTER para deixar vazio): ").replace(",", ".") or ""
            novo_peso = float(novo_peso_str) if novo_peso_str else 0.0
            if novo_peso > 700 or novo_peso < 0:
                print("\nERRO: Peso Inválido")
                continuar = exibir_submenu("'Cadastrar Novo Aluno'")
                continue
        except ValueError:
            print("\nERRO: O Peso Deve ser Preenchido com números")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")
            continue
        try:  
            nova_altura_str = input("Digite a altura (m) do aluno (ou ENTER para deixar vazio): ").replace(",", ".") or ""
            nova_altura = float(nova_altura_str) if nova_altura_str else 0.0
            if nova_altura > 3.0 or nova_altura < 0:
                print("\nERRO: Altura Inválida")
                continuar = exibir_submenu("'Cadastrar Novo Aluno'")
                continue
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")
            continue
        try:
            print("\nPlanos Disponíves:")
            exibir_planos()
            novo_plano = int(input("\nQual plano deseja contratar? "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("'Cadastrar Novo Aluno'")
            continue

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
            continuar = exibir_submenu("'Cadastrar Novo Produto'")

        # inputs para receber o nome e categoria do novo produto/serviço
        print(" ----- Cadastrar Produto ou Serviço ----- ")
        novo_nome = input("\nQual o nome do novo produto/serviço? ")
        print(
            "\n1 - Serviços",
            "\n2 - Equipamentos",
            "\n3 - Alimentos",
            "\n4 - Bebidas",
            "\n5 - Suplementos",
            "\n6 - Cosméticos",
            "\n7 - Diversos"
        )
        try:
            nova_categoria_int = int(input("\nQual categoria esse novo produto/serviço? "))
        except ValueError:
            print("ERRO: Opção deve ser um número inteiro")
            continuar = exibir_submenu("'Cadastrar Novo Produto'")
            continue

        if nova_categoria_int == 1:
            nova_categoria = "Serviços"
        elif nova_categoria_int == 2:
            nova_categoria = "Equipamentos"
        elif nova_categoria_int == 3:
            nova_categoria = "Alimentos"
        elif nova_categoria_int == 4:
            nova_categoria = "Bebidas"
        elif nova_categoria_int == 5:
            nova_categoria = "Suplementos"
        elif nova_categoria_int == 6:
            nova_categoria = "Cosméticos"
        elif nova_categoria_int == 7:
            nova_categoria = "Diversos"
        else:
            print("Opção Inválida")


        # inputs para receber o preço e quantidade do novo produto/serviço
        try:
            novo_preco = float(input("Qual o valor (R$) desse novo produto/serviço? "))

            if nova_categoria_int == 1:
                nova_qtde = 1
            else:
                nova_qtde = int(input("Qual a quantidade inicial desse novo produto? "))
                
        except ValueError:
            print("ERROR: Entrada Inválida, o preço deve ser um número!")
            continuar = exibir_submenu("'Cadastrar Novo Produto / Serviço'")
            continue
        
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            
            cursor.execute("""
                INSERT INTO prodserv(nome, categoria, preco, qtde)
                VALUES(%s,%s,%s,%s)
            """, (novo_nome, nova_categoria, novo_preco, nova_qtde))

            conexao.commit()
            print(f"\nProduto/Serviço {novo_nome} adicionado com sucesso!")
            continuar = exibir_submenu("'Cadastrar Novo Produto / Serviço'")
            continue

        except mysql.connector.Error as erro:
            conexao.rollback()
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
        novo_nome = input("Qual o nome do novo plano? ")
    
        # inputs para receber o preço e quantidade de aulas do novo plano
        try:
            novo_preco = float(input("Qual o valor desse novo plano? "))
        except ValueError:
            print("\nERRO: Entrada inválida, o valor deve ser um número!")
            input("Aperte ENTER para continuar")
            continuar = exibir_submenu("'Cadastrar Novo Plano'")
            continue

        try:
            nova_qtde_aulas = int(input("Qual a quantidade de aulas desse novo plano? "))
        except ValueError:
            print("\nERRO: Entrada inválida, a qtde de aulas deve ser um número inteiro!")
            input("Aperte ENTER para continuar")
            continuar = exibir_submenu("'Cadastrar Novo Plano'")
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            
            cursor.execute("""
                INSERT INTO planos(nome, preco, qtde_aulas)
                VALUES(%s,%s,%s)
            """, (novo_nome, novo_preco, nova_qtde_aulas))

            conexao.commit()
            print(f"\nPlano {novo_nome} adicionado com sucesso!")
            continuar = exibir_submenu("'Cadastrar Novo Plano'")
            continue
        
        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")            
            
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()