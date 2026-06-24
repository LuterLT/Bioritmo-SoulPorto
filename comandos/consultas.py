# def alt_cad_aluno(): #===============================================ALTERA CADASTRO ALUNO===
#     '''
#     Essa função vai permitir que o usuário altere os dados 
#     '''
    
#     continuar = 1
#     while True:
#         if continuar == 2: #-> Se o usuário escolheu sair (parar de continuar)
#             break
#         elif continuar == 0: #-> Se o usuário digitou o comando errado no submenu de continuidade
#             continuar = exibir_submenu("Alterando Cadastro dos Alunos")

#         exibir_users() #adicionei pra exibir aqui antes do input pra escolher qual
        
#         try:
#             id_aluno


# except ValueError:
#     print("ERRO: O ID deve ser preenchido apenas com números inteiros")
#     continuar = exibir_submenu("Alterando Cadastro de Produtos")
#     continue



import mysql.connector
from banco_dados import abrir_conexao


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
                aluno.aulas_disp LIKE %s OR
                LOWER(planos.nome) LIKE %s
            ) AND aluno.ativo = 1
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nAlunos:")
            for aluno in resultado:
                print(f" -> [{aluno[0]}] {aluno[1]} | Email: {aluno[2]} | Plano: {aluno[4]} | Aulas Disponiveis: {aluno[3]}")

        # faz a busca na tabela planos
        cursor.execute("""
            SELECT id, nome, preco, qtde_aulas
            FROM planos
            WHERE planos.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                preco LIKE %s OR
                qtde_aulas LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nPlanos:")
            for plano in resultado:
                print(f" -> [{plano[0]}] {plano[1]} | Preço: {plano[2]} | Aulas permitidas: {plano[3]}")

        # faz a busca na tabela prodserv
        cursor.execute("""
            SELECT id, nome, categoria, preco, qtde
            FROM prodserv
            WHERE prodserv.ativo = 1 AND (
                LOWER(nome) LIKE %s OR
                LOWER(categoria) LIKE %s OR
                preco LIKE %s OR
                qtde LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("\nProdutos / Serviços:")
            for prodserv in resultado:
                print(f" -> [{prodserv[0]}] {prodserv[1]} | Categoria: {prodserv[2]} | Preço: {prodserv[3]} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS (consulta geral - linha 89): {erro}")
        input("Aperte ENTER para continuar")
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
                aluno.aulas_disp LIKE %s OR
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
                print(f" -> [{aluno[0]}] {aluno[1]} | Email: {aluno[2]} | Plano: {aluno[4]} | Aulas Disponiveis: {aluno[3]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS (consulta aluno - linha 133): {erro}")
        input("Aperte ENTER para continuar")
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
                preco LIKE %s OR
                qtde LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()

        # cursor.close()
        # conexao.close()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("Produtos / Serviços:\n")
            for prodserv in resultado:
                print(f" -> [{prodserv[0]}] {prodserv[1]} | Categoria: {prodserv[2]} | Preço: {prodserv[3]} | Quantidade em estoque: {prodserv[4]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS (consulta produto - linha 176): {erro}")
        input("Aperte ENTER para continuar")
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
                preco LIKE %s OR
                qtde_aulas LIKE %s
            )
        """, (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))

        resultado = cursor.fetchall()

        # cursor.close()
        # conexao.close()
        
        if len(resultado) == 0:
            print("Nenhum resultado encontrado.")
        else:
            print("Planos:\n")
            for plano in resultado:
                print(f" -> [{plano[0]}] {plano[1]} | Preço: {plano[2]} | Aulas permitidas: {plano[3]}")
            print("\n")

    except mysql.connector.Error as erro:
        print(f"ERRO DE BANCO DE DADOS (consulta plano - linhas 217): {erro}")
        input("Aperte ENTER para continuar")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()