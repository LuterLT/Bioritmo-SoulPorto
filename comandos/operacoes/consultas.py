import mysql.connector

from banco_dados import abrir_conexao
from interfaces.funcontinuar import exibir_submenu


def consulta_geral():
    print("\nConsulta geral\n")
    
    termo_busca = input("Buscar por: ").strip().lower()

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela aluno
        cursor.execute("""
            SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = planos.id
            WHERE(
                LOWER(aluno.nome) LIKE %s OR
                LOWER(aluno.email) LIKE %s OR
                CAST(aluno.aulas_disp AS DECIMAL(10,2)) LIKE %s OR
                LOWER(planos.nome) LIKE %s
            ) AND aluno.ativo = 1
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print(f"Nenhum aluno com '{termo_busca}' encontrado.\n")
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
            WHERE planos.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                CAST(preco AS DECIMAL(10,2)) LIKE %s OR
                CAST(qtde_aulas AS DECIMAL(10,2)) LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print(f"Nenhum plano com '{termo_busca}' resultado encontrado.\n")
        else:
            print("\nPlanos:")
            for plano in resultado:
                larg_nome = max(len(plano[1]) for plano in resultado)
                print(f" -> [{plano[0]}] {plano[1]:<{larg_nome}} | Preço: {plano[2]} | Aulas permitidas: {plano[3]}")

        # faz a busca na tabela prodserv
        cursor.execute("""
            SELECT id, nome, categoria, preco, qtde
            FROM prodserv
            WHERE prodserv.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                LOWER(categoria) LIKE %s OR
                CAST(preco AS DECIMAL(10,2)) LIKE %s OR
                CAST(qtde AS DECIMAL(10,2)) LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print(f"Nenhum produto ou serviço com '{termo_busca}' resultado encontrado.\n")
        else:
            print("\nProdutos / Serviços:")
            for prodserv in resultado:
                larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                larg_categ = max(len(prodserv[2]) for prodserv in resultado)
                print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS (consulta geral - linha 89): {erro}")
        continuar = exibir_submenu("'consulta geral'")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def consulta_alunos():
    print("\nConsulta de alunos\n")

    termo_busca = input("Buscar por: ").strip().lower()

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela aluno
        cursor.execute("""
            SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome
            FROM aluno
            INNER JOIN planos ON aluno.id_plano = planos.id
            WHERE aluno.ativo = 1 AND (
                LOWER(aluno.nome) LIKE %s OR
                LOWER(aluno.email) LIKE %s OR
                CAST(aluno.aulas_disp AS DECIMAL(10,2)) LIKE %s OR
                LOWER(planos.nome) LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()

        # cursor.close()
        # conexao.close()
        
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
        print(f"ERRO DE BANCO DE DADOS (consulta aluno - linha 133): {erro}")
        continuar = exibir_submenu("'consulta de alunos'")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()



def consulta_produtos():
    print("\nConsulta de produtos\n")
    
    termo_busca = input("Buscar por: ").strip().lower()

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        
        # faz a busca na tabela prodserv
        cursor.execute("""
            SELECT id, nome, categoria, preco, qtde
            FROM prodserv
            WHERE prodserv.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                LOWER(categoria) LIKE %s OR
                CAST(preco AS DECIMAL(10,2)) LIKE %s OR
                CAST(qtde AS DECIMAL(10,2)) LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

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
        print(f"ERRO DE BANCO DE DADOS (consulta produto - linha 176): {erro}")
        continuar = exibir_submenu("'consulta de produtos / serviços'")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def consulta_planos():
    print("\nConsulta de planos\n")
    
    termo_busca = input("Buscar por: ").strip().lower()

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        # faz a busca na tabela planos
        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE planos.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                CAST(preco AS DECIMAL(10,2)) LIKE %s OR
                CAST(qtde_aulas AS DECIMAL(10,2)) LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

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
        continuar = exibir_submenu("'consulta de planos'")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

