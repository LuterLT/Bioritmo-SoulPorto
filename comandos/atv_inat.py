import mysql.connector
from banco_dados import abrir_conexao
from interfaces.funcontinuar import exibir_submenu

def aluno_atv_inat(): 
    '''
    essa def altera o estado dos alunos entre inativo e ativo
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativar / desativar aluno'")

        print("\nAtivar ou desativar aluno?\n",
            " [1] - Ativar aluno\n",
            " [2] - Inativar aluno\n",
            " [0] - Sair de ativar / desativar aluno\n",)
        
        try:
            opc = int(input("Opção desejada: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = 0

        if opc == 0:
            return
        elif opc == 1:
            aluno_atv()
        elif opc == 2:
            aluno_inat()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = 0


def aluno_atv():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativando / inativando aluno'")
            return

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela alunos inativos
            cursor.execute("""
                SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome, aluno.peso, aluno.altura
                FROM aluno
                INNER JOIN planos ON aluno.id_plano = planos.id
                WHERE aluno.ativo = 0
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum aluno inativo.")
                continuar = 0
                continue
            else:
                print("\nAluno inativos:")
                for aluno in resultado:
                    larg_nome = max(len(aluno[1]) for aluno in resultado)
                    larg_email = max(len(aluno[2]) for aluno in resultado)
                    larg_pln = max(len(aluno[4]) for aluno in resultado)
                    peso_aluno = "-" if not aluno[5] else aluno[5]
                    altura_aluno = "-" if not aluno[6] else aluno[6]
                    print(f" -> [{aluno[0]:<{2}}] {aluno[1]:<{larg_nome}} | Email: {aluno[2]:<{larg_email}} | Plano: {aluno[4]:<{larg_pln}} | Aulas Disponiveis: {aluno[3]:<3} | Peso: {peso_aluno:<5} | Altura: {altura_aluno:<5}")
                print("\n")

            ids_validos = [prodserv[0] for prodserv in resultado]

            try:
                id_aluno = int(input("Digite ID do produto serviço a ser ativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for prodserv in resultado:
                if prodserv[0] == id_aluno:
                    nome_aluno = prodserv[1]
                    break

            if id_aluno not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE aluno SET ativo = 1 WHERE id = %s", (id_aluno,))
            conexao.commit()
            print(f"Aluno '{nome_aluno}' ativado com sucesso!")
            continuar = 0

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def aluno_inat():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativando / inativando aluno'")
            return

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela alunos inativos
            cursor.execute("""
                SELECT aluno.id,  aluno.nome, aluno.email, aluno.aulas_disp, planos.nome, aluno.peso, aluno.altura
                FROM aluno
                INNER JOIN planos ON aluno.id_plano = planos.id
                WHERE aluno.ativo = 1
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum aluno ativo.")
                continuar = 0
                continue
            else:
                print("\nAluno ativos:")
                for aluno in resultado:
                    larg_nome = max(len(aluno[1]) for aluno in resultado)
                    larg_email = max(len(aluno[2]) for aluno in resultado)
                    larg_pln = max(len(aluno[4]) for aluno in resultado)
                    peso_aluno = "-" if not aluno[5] else aluno[5]
                    altura_aluno = "-" if not aluno[6] else aluno[6]
                    print(f" -> [{aluno[0]:<{2}}] {aluno[1]:<{larg_nome}} | Email: {aluno[2]:<{larg_email}} | Plano: {aluno[4]:<{larg_pln}} | Aulas Disponiveis: {aluno[3]:<3} | Peso: {peso_aluno:<5} | Altura: {altura_aluno:<5}")
                print("\n")

            ids_validos = [prodserv[0] for prodserv in resultado]

            try:
                id_aluno = int(input("Digite ID do produto serviço a ser ativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for prodserv in resultado:
                if prodserv[0] == id_aluno:
                    nome_aluno = prodserv[1]
                    break

            if id_aluno not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE aluno SET ativo = 0 WHERE id = %s", (id_aluno,))
            conexao.commit()
            print(f"Aluno '{nome_aluno}' inativado com sucesso!")
            continuar = 0

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()




def prodserv__atv_inat():
    '''
    essa def altera o estado dos produtos / serviços entre inativo e ativo
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativar / desativar produto / serviço'")

        print("\nAtivar ou desativar produto / serviço?\n",
            " [1] - Ativar produto / serviço\n",
            " [2] - Inativar produto / serviço\n",
            " [0] - Sair de ativar / desativar produto / serviço\n",)
        
        try:
            opc = int(input("Opção desejada: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = 0

        if opc == 0:
            return
        elif opc == 1:
            prodserv_atv()
        elif opc == 2:
            prodserv_inat()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = 0


def prodserv_atv():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativando / inativando produtos / serviços'")
            return

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela plprodserv inativos
            cursor.execute("""
                SELECT id, nome, categoria, preco, qtde
                FROM prodserv
                WHERE ativo = 0
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum produtos / serviços inativo.")
                continuar = 0
                continue
            else:
                print("\nProdutos / Serviços inativos:")
                for prodserv in resultado:
                    larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                    larg_categ = max(len(prodserv[2]) for prodserv in resultado)
                    print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]:<6} | Quantidade em estoque: {prodserv[4]}")
                print("\n")

            ids_validos = [prodserv[0] for prodserv in resultado]

            try:
                id_prodserv = int(input("Digite ID do produto serviço a ser ativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for prodserv in resultado:
                if prodserv[0] == id_prodserv:
                    nome_prodserv = prodserv[1]
                    break

            if id_prodserv not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE prodserv SET ativo = 1 WHERE id = %s", (id_prodserv,))
            conexao.commit()
            print(f"Produto / Serviço '{nome_prodserv}' ativado com sucesso!")
            continuar = 0

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def prodserv_inat():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativando / inativando produtos / serviços'")
            return

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            # faz a busca na tabela prodserv ativos
            cursor.execute("""
                SELECT id, nome, categoria, preco, qtde
                FROM prodserv
                WHERE ativo = 1
            """)

            resultado = cursor.fetchall()
            
            if len(resultado) == 0:
                print("Nenhum produtos / serviços ativo.")
                continuar = 0
                continue
            else:
                print("\nProdutos / Serviços ativos:")
                for prodserv in resultado:
                    larg_nome = max(len(prodserv[1]) for prodserv in resultado)
                    larg_categ = max(len(prodserv[2]) for prodserv in resultado)
                    print(f" -> [{prodserv[0]}] {prodserv[1]:<{larg_nome}} | Categoria: {prodserv[2]:<{larg_categ}} | Preço: {prodserv[3]:<6} | Quantidade em estoque: {prodserv[4]}")
                print("\n")

            ids_validos = [prodserv[0] for prodserv in resultado]

            try:
                id_prodserv = int(input("Digite ID do produto serviço a ser inativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for prodserv in resultado:
                if prodserv[0] == id_prodserv:
                    nome_prodserv = prodserv[1]
                    break

            if id_prodserv not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE prodserv SET ativo = 0 WHERE id = %s", (id_prodserv,))
            conexao.commit()
            print(f"Produto / Serviço '{nome_prodserv}' inativado com sucesso!")
            continuar = 0

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


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
            " [0] - Sair de ativar / desativar planos\n",)
        
        try:
            opc = int(input("Opção desejada: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = 0

        if opc == 0:
            return
        elif opc == 1:
            plano_atv()
        elif opc == 2:
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
            continuar = exibir_submenu("'ativando / inativando planos'")
            return

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
            
            ids_validos = [plano[0] for plano in resultado]
            
            try:
                id_plano = int(input("Digite ID do plano a ser ativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for plano in resultado:
                if plano[0] == id_plano:
                    nome_plano = plano[1]
                    break
            
            if id_plano not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE planos SET ativo = 1 WHERE id = %s", (id_plano,))
            conexao.commit()
            print(f"Plano '{nome_plano}' ativado com sucesso!")
            continuar = 0

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
            continuar = exibir_submenu("'ativando / inativando planos'")
            return

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
            
            ids_validos = [plano[0] for plano in resultado]
            
            try:
                id_plano = int(input("Digite ID do plano a ser inativado: "))
            except ValueError:
                print("Digite apenas números inteiros!")
                continuar = 0
                continue

            for plano in resultado:
                if plano[0] == id_plano:
                    nome_plano = plano[1]
                    break
            
            if id_plano not in ids_validos:
                print("ERRO: Id invalido!")
                print(resultado[0])
                continuar = 0
                continue

            cursor.execute("UPDATE planos SET ativo = 0 WHERE id = %s", (id_plano,))
            conexao.commit()
            print(f"Plano '{nome_plano}' inativado com sucesso!")
            continuar = 0

        except mysql.connector.Error as erro:
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()