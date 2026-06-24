import mysql.connector
import datetime
from banco_dados import abrir_conexao
from interfaces.interface import exibir_planos, exibir_users, exibir_prod
from interfaces.funcontinuar import exibir_submenu




def alt_cad_aluno(): #===============================================ALTERA CADASTRO ALUNO===
    '''
    Essa função vai permitir que o usuário altere os dados 
    '''

    continuar = 1
    while True:
        if continuar == 2: #-> Se o usuário escolheu sair (parar de continuar)
            break
        elif continuar == 0: #-> Se o usuário digitou o comando errado no submenu de continuidade
            continuar = exibir_submenu("'Alterar Cadastro de Alunos'")

        exibir_users() #adicionei pra exibir aqui antes do input pra escolher qual
        
        try:
            id_aluno = int(input("\nDigite o [ID] do Aluno que deseja Alterar: "))
        except ValueError:
            print("\n ERRO: O ID Deve Ser Preenchido Apenas com Números Inteiros")
            continuar = exibir_submenu("'Alterar Cadastro de Alunos'")
            continue
        
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT * 
                FROM aluno 
                WHERE id = %s
            """, (id_aluno,))
            resultado = cursor.fetchone()
            if resultado is None:
                print("\nERRO: O ID Digitado não é equivalente a nenhum cadastrado no Banco de Dados!")
                continuar = exibir_submenu("'Alterar Cadastro de Alunos'")
                continue
            
            
            #pedir para o usuário digitar os campos
            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu(f"de Alterar o Cadastro do Aluno {resultado[1]}")
                    continue
                print(f"\nVocê Selecionou o aluno:\n-Nome: '{resultado[1]}'\n-Email: {resultado[2]} \n-Peso: {resultado[3]:.2f} Kg \n-Altura: {resultado[4]:2f} m")
                print("\nPreencha os campos abaixo e APENAS aperte ENTER para aqueles que não deseja alterar")
                
                novo_nome= input("\nDigite o seu nome completo: ").strip() or resultado[1]
                novo_email= input("Digite o seu email: ").strip() or resultado[2]

                novo_peso_str= input("Digite o seu peso (quilos): ").strip()
                try: 
                    novo_peso = float(novo_peso_str) if novo_peso_str else resultado[3]
                except ValueError:
                    print("\nERRO: O Peso deve ter um número, alteração cancelada")
                    continuar = exibir_submenu(f"de Alterar o Cadastro do Aluno '{resultado[1]}'")
                    continue

                nova_altura_str= input("Digite a sua altura (metros): ").strip()
                try:
                    nova_altura = float(nova_altura_str) if nova_altura_str else resultado[4]
                except ValueError:
                    print("\nERRO: A Altura deve ser em número, alteração cancelada")
                    continuar = exibir_submenu(f"de Alterar o Cadastro do Aluno '{resultado[1]}'")
                    continue
    
            
                cursor.execute("""
                    UPDATE aluno
                    SET
                        nome = %s,
                        email = %s,
                        peso = %s,
                        altura = %s 
                    WHERE id = %s
                """, (novo_nome, novo_email, novo_peso, nova_altura, id_aluno))
                conexao.commit()
                print(f"\nSUCESSO: o aluno agora tem os dados:\n\nNome: '{novo_nome}'\nE-mail: {novo_email}\nPeso: {novo_peso:.2f} Kg\nAltura: {nova_altura:.2f} m")
                input("\nAperte ENTER para Continuar")
                break
        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
            input("Aperte ENTER para Continuar")
            break
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = exibir_submenu("'Alterar Cadastro de Alunos'")
        continue


def alt_cad_produtos():
    '''
    Essa função permite que o usuário altere os dados
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Alterar Cadastro de Produtos'")
        try:
            print("Lista de produtos cadastrados:")
            exibir_prod()
            id_produto = int(input("\nDigite o [ID] do Produto que deseja alterar: "))

        except ValueError:
            print("ERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("'Alterar Cadastro de Produtos'")
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT *
                FROM prodserv
                WHERE id = %s
            """, (id_produto,))
            produto = cursor.fetchone()

            if produto is None:
                print("\nERRO: Produto não encontrado")
                continuar = exibir_submenu("'Alterar Cadastro de Produtos'")
                continue

            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu(f"de Alterar o Produto '{produto[1]}'")
                    continue
                print("\nPreencha os campos abaixo e APENAS aperte ENTER para não alterar")
                print(f"""
    Você Selecionou o Produto:
    -ID: {produto[0]}
    -Nome: {produto[1]}
    -Categoria: {produto[2]}
    -Preço: R$ {produto[3]:.2f}
    """)
                
                # novo nome
                novo_nome = input("Digite o novo nome: ").strip() or produto[1]
                # nova categoria
                nova_categoria = input("Digite a nova categoria: ").strip() or produto[2]
                # novo preço
                novo_preco_str = input("Digite o novo preço (R$): ").strip()

                try:
                    novo_preco = float(novo_preco_str) if novo_preco_str else produto[3]

                    if novo_preco < 0:
                        print("\n ERRO: O preço não pode ser negativo")
                        continuar = exibir_submenu(f"de Alterar o Produto '{produto[1]}'")
                        continue
                    
                except ValueError:

                    print("\nERRO: O preço deve ser um número válido")
                    continuar = exibir_submenu(f"de Alterar o Produto '{produto[1]}'")
                    continue

                # UPDATE
                cursor.execute("""
                    UPDATE prodserv
                    SET nome = %s,
                        categoria = %s,
                        preco = %s
                    WHERE id = %s
                """, (
                    novo_nome,
                    nova_categoria,
                    novo_preco,
                    id_produto
                ))

                conexao.commit()

                print("\nProduto alterado com sucesso!")
                input("Pressione ENTER para continuar")
                break

        except mysql.connector.Error as erro:
            print("arquivo cadastro - linha 216")
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Pressione ENTER para continuar")
            break

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = exibir_submenu("'Alterar Cadastro de Produtos'")
        continue

def alt_cad_plano(): #============================== ALTERA CADASTRO DE PLANOS ===========================
    ''' 
    Essa função permite que o usuário altere os dados dos planos
    '''
    
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Alterar Cadastro de Plano'")
            
        try:
            print("\nPlanos cadastrados: ")
            exibir_planos()
            #input para selecionar o plano que será alterado
            id_plano = int(input("\nDigite o ID do plano que deseja alterar: "))
        
        except ValueError:
            print("ERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("'Alterar Cadastro de Plano'")
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute ("""
                SELECT *
                FROM planos
                WHERE id = %s
            """, (id_plano,))

            plano_atual = cursor.fetchone()

            if  plano_atual is None:
                print("\nERRO: O ID Digitado não é equivalente a nenhum plano no Banco de Dados!")
                continuar = exibir_submenu("'Alterar Cadastro de Plano'")
                continue
                


            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu(f"de Alterar o Plano '{plano_atual[1]}'")
                    continue
                print(f"""
Você Selecionou o Plano:
\n-ID: {plano_atual[0]}
-Nome: {plano_atual[1]}
-Preço: R$ {plano_atual[2]:}
-Quantidade de aulas: {plano_atual[3]}
""")
                print("\nPreencha os campos abaixo e caso não deseje alterar pressione ENTER")
                
                novo_nome_plano = input("Digite o novo nome do plano: ").strip() or plano_atual[1]

                novo_preco_plano_str  = input("Digite o novo preço do plano: ").strip()
                try:
                    novo_preco_plano = float(novo_preco_plano_str) if novo_preco_plano_str else plano_atual[2]
                except ValueError:
                    print("\nERRO: Digite um preço válido")
                    continuar = exibir_submenu(f"de Alterar o Plano '{plano_atual[1]}'")
                    continue
                    
                if novo_preco_plano < 0:
                    print("\nERRO: O preço não pode ser negativo")
                    continuar = exibir_submenu(f"de Alterar o Plano '{plano_atual[1]}'")
                    continue

                nova_qtde_aulas_str = input("Digite a nova quantidade de aulas do plano: ").strip()
                try:
                    nova_qtde_aulas = int(nova_qtde_aulas_str) if nova_qtde_aulas_str else plano_atual[3]
                except ValueError:
                    print("\nERRO: Digite apenas números inteiros")
                    continuar = exibir_submenu(f"de Alterar o Plano '{plano_atual[1]}'")
                    continue

                if nova_qtde_aulas <= 0:
                    print("\nERRO: A quantidade de aulas não pode ser menor que 1")
                    continuar = exibir_submenu(f"de Alterar o Plano '{plano_atual[1]}'")
                    continue

                cursor.execute("""
                    UPDATE planos
                    SET nome = %s,
                        preco = %s,
                        qtde_aulas = %s
                    WHERE id = %s
                """, (
                    novo_nome_plano,
                    novo_preco_plano,
                    nova_qtde_aulas,
                    id_plano
                ))

                conexao.commit()

                print("\nPlano alterado com sucesso!")
                break

        except mysql.connector.Error as erro:
            print("arquivo cadastro - linha 332")
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO: {erro}")
            input("Aperte ENTER para continuar")
            break

        finally:
            if 'conexao' in locals() and conexao.is_connected:
                cursor.close()
                conexao.close()

        continuar = exibir_submenu("'Alterar Cadastro de Plano'")
        continue