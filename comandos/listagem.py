from banco_dados import abrir_conexao

import mysql.connector


def listagem_geral():
    print("\nListagem geral\n")

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela aluno
        cursor.execute("""
            SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = planos.id
            WHERE aluno.ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print(f"Nenhum aluno encontrado.\n")
            print("Aperte ENTER para continuar")
        else:
            print("\nAlunos:")
            for aluno in resultado:
                larg_nome = max(len(aluno[1]) for aluno in resultado)
                larg_email = max(len(aluno[2]) for aluno in resultado)
                larg_pln = max(len(aluno[4]) for aluno in resultado)
                print(f" -> [{aluno[0]}] {aluno[1]:<{larg_nome}} | Email: {aluno[2]:<{larg_email}} | Plano: {aluno[4]:<{larg_pln}} | Aulas Disponiveis: {aluno[3]}")

        # faz a busca na tabela planos
        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE planos.ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print(f"Nenhum plano encontrado.\n")
        else:
            print("\nPlanos:")
            for plano in resultado:
                larg_nome = max(len(plano[1]) for plano in resultado)
                print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]} | Aulas permitidas: {plano[3]}")

        # faz a busca na tabela prodserv
        cursor.execute("""
            SELECT id, nome, categoria, preco, qtde
            FROM prodserv
            WHERE prodserv.ativo = 1
        """,)

        resultado = cursor.fetchall()

        if len(resultado) == 0:
            print(f"Nenhum produto / serviço encontrado.\n")
        else:
            print("\nProdutos / Serviços:")
            for prodserv in resultado:
                larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                larg_categ = max(len(prodserv[2]) for prodserv in resultado)
                print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def listagem_alunos():
    print("\nListagem de alunos\n")

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela aluno
        cursor.execute("""
            SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = planos.id
            WHERE aluno.ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("Alunos:\n")
            for aluno in resultado:
                larg_nome = max(len(aluno[1]) for aluno in resultado)
                larg_email = max(len(aluno[2]) for aluno in resultado)
                larg_pln = max(len(aluno[4]) for aluno in resultado)
                print(f" -> [{aluno[0]}] {aluno[1]:<{larg_nome}} | Email: {aluno[2]:<{larg_email}} | Plano: {aluno[4]:<{larg_pln}} | Aulas Disponiveis: {aluno[3]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def listagem_produtos():
    print("\nListagem de produtos\n")
    
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
            print("Produtos / Serviços:\n")
            for prodserv in resultado:
                larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                larg_categ = max(len(prodserv[1]) for prodserv in resultado)
                print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def listagem_planos():
    print("\nListagem de planos\n")
    
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela planos
        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE planos.ativo = 1
        """)

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("Planos:\n")
            for plano in resultado:
                larg_nome = max(len(plano[1]) for plano in resultado)
                print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]} | Aulas permitidas: {plano[3]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS: {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
