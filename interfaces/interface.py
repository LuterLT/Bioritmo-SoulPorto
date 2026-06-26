import mysql.connector
from banco_dados import abrir_conexao


def exibir_menu():  #=============================================EXIBIR MENU===========
    print("=========== BIO RITMO SoulPorto ===========\n",
          "1  - Check In\n", #registrar o check-in de um aluno específico
          "2  - Cadastros/Alterações Cadastrais\n", #cadastro e atualização de alunos e/ou produtos
          "3  - Vendas\n", #registrar vendas de produtos/serviços
          "4  - Alterar Estoque\n", #repor estoque de produtos (unitário e lote)
          "5  - Listar cadastros\n",
          "6  - Consulta\n", #busca alunos, planos e produtos/serviços
          "7  - Ativar/Desativar cadastros\n", #ativa/desativa cadastros
          "8  - Calcular IMC\n", # caucula imc de um aluno
          "9  - Controle Financeiro\n", #altera preço de planos/produtos, aplica promoções, exibe NF, painel BI
          "10 - Exportar Relatórios\n", #exporta os relatórios de check-in e de vendas
          "0  - Fechar o Sistema\n"
          )


def exibir_users(): #=============================================EXIBIR USUÁRIOS===========
    '''
    Função feita para exibir na CLI todos os usuários cadastrados Banco e seus dados
    '''
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela aluno
        cursor.execute("""
            SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome, aluno.peso, aluno.altura
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = planos.id
            WHERE aluno.ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nAlunos:")
            for aluno in resultado:
                larg_nome = max(len(aluno[1]) for aluno in resultado)
                larg_email = max(len(aluno[2]) for aluno in resultado)
                larg_pln = max(len(aluno[4]) for aluno in resultado)
                peso_aluno = "-" if not aluno[5] else aluno[5]
                altura_aluno = "-" if not aluno[6] else aluno[6]
                print(f" -> [{aluno[0]}] {aluno[1]:<{larg_nome}} | Email: {aluno[2]:<{larg_email}} | Plano: {aluno[4]:<{larg_pln}} | Aulas Disponiveis: {aluno[3]:<3} | Peso: {peso_aluno:<5} | Altura: {altura_aluno:<5}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco: {erro}")
        input("Aperte ENTER para Continuar")
    
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def exibir_prod(): #=============================================EXIBIR PRODUTOS===========
    '''
    Essa função serve para exibir na CLI todos os produtos cadastrados no Banco de Dados
    '''
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        
        # faz a busca na tabela prodserv
        cursor.execute("""
            SELECT id, nome, categoria, preco, qtde
            FROM prodserv
            WHERE prodserv.ativo = 1
        """)

        resultado = cursor.fetchall()

        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nProdutos / Serviços:")
            for prodserv in resultado:
                larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                larg_categ = max(len(prodserv[2]) for prodserv in resultado)
                #larg_prc = max(len(plano[2]) for plano in resultado)
                print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]:<6} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def exibir_planos(): #=============================================EXIBIR PLANOS===========
    '''
    Essa função serve para exibir na CLI todos os planos cadastrados no Banco de Dados
    '''
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela planos
        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nPlanos:")
            for plano in resultado:
                larg_nome = max(len(plano[1]) for plano in resultado)
                print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]:<6} | Aulas permitidas: {plano[3]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()



def exibir_checkin(limite): #======================================EXIBIR CHECK-INS RECENTES=
    '''
    Essa função vai exibir os checkins mais recentes e todos os seus dados
    '''
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT aluno.nome, checkin.horario, aluno.id
            FROM checkin
            INNER JOIN aluno ON checkin.id_aluno = aluno.id
            ORDER BY checkin.horario DESC
            LIMIT %s
        """, (limite,))

        resultado = cursor.fetchall()

        if len(resultado) == 0:
            print("\nNenhum Check-In Registrado até o momento")
            input("Aperte ENTER para Continuar")
        else:
            for checkin in resultado:
               print(f"-> Data: {checkin[1]} | Aluno: {checkin[0]} | ID do Aluno: {checkin[2]}")
            input("Aperte ENTER para Continuar")

    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco, {erro}")
        input("Aperte ENTER para Continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()