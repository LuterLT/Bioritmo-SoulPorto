import mysql.connector
from banco_dados import abrir_conexao

def exibir_menu():  #=============================================EXIBIR MENU===========
    print("=========== BIO RITMO SoulPorto ===========\n",
          "1 - Check In\n", #registrar o check-in de um aluno específico
          "2 - Cadastros/Alterações Cadastrais\n", #cadastro e atualização de alunos e/ou produtos
          "3 - Vendas\n", #registrar vendas de produtos/serviços
          "4 - Repor Estoque\n", #repor estoque de produtos (unitário e lote)
          "5 - Consulta\n", #busca alunos, planos e produtos/serviços
          "6 - Controle Financeiro\n", #altera preço de planos/produtos, aplica promoções, exibe NF, painel BI
          "7 - Exportar Relatórios\n", #exporta os relatórios de check-in e de vendas
          "0 - Fechar o Sistema\n"
          )



def exibir_users(): #=============================================EXIBIR USUÁRIOS===========
    '''
    Função feita para exibir na CLI todos os usuários cadastrados Banco e seus dados
    '''
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT aluno.id aluno.nome, aluno.email, planos.nome, aluno.aulas_disp
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = plano.id
            WHERE ativo = 1
        """)
        resultado = cursor.fetchall()
        for user in resultado:
            print(f"-> [{user[0]}] {user[1]} | E-mail: {user[2]} | Plano: {user[3]} | Aulas Disponíveis: {user[4]}")
    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco, {erro}")
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
        
        cursor.execute("""
            SELECT id, nome, qtd, categoria, preco
            FROM prodserv
            WHERE ativo = 1
        """)
        resultado = cursor.fetchall()
        
        for produto in resultado:
            print(f"-> [{produto[0]}] {produto[1]} | Quantidade em Estoque: {produto[2]} | Categoria: {produto[3]} | Preço: R$ {produto[4]:.2f}")
    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco, {erro}")
        input("Aperte ENTER para Continuar")
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

        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE ativo = 1
        """)
        resultado = cursor.fetchall()
        
        for plano in resultado:
            print(f"-> [{plano[0]}] {plano[1]} | Preço: {plano[2]} | Quantidade de Aulas/Mês: {plano[3]}")
    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco, {erro}")
        input("Aperte ENTER para Continuar")
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
            SELECT aluno.nome, checkin.data
            FROM checkin
            INNER JOIN aluno ON checkin.id_aluno = aluno.id
            ORDER BY checkin.data DESC
            LIMIT %s
        """, (limite,))

        resultado = cursor.fetchall()
        for checkin in resultado:
            print(f"-> Data: {checkin[1]} | Nome do Aluno: {checkin[0]}")

    except mysql.connector.Error as erro:
        print(f"\nERRO: Ocorreu um erro no banco, {erro}")
        input("Aperte ENTER para Continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

