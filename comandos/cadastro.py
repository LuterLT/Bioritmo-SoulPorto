import mysql.connector
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
            continuar = exibir_submenu("Alterando Cadastro dos Alunos")

        exibir_users() #adicionei pra exibir aqui antes do input pra escolher qual
        
        try:
            id_aluno = int(input("\nDigite o [ID] do Aluno que deseja Alterar: "))
        except ValueError:
            print("\n ERRO: O ID Deve Ser Preenchido Apenas com Números Inteiros")
            continuar = exibir_submenu("Alterando Cadastro dos Alunos")
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
                continuar = exibir_submenu("Alterando Cadastro dos Alunos")
                continue
            
            print(f"\nVocê Selecionou o aluno:\n-Nome: '{resultado[1]}'\n-Email: {resultado[2]} \n-Peso: {resultado[3]:.2f} \n-Altura: {resultado[4]:2f}")
            
            #pedir para o usuário digitar os campos
            print("\nPreencha os campos abaixo e APENAS aperte ENTER para aqueles que não deseja alterar")
            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu("Tentando Alterar Cadastro de Produtos")

                novo_nome= input("\nDigite o seu nome completo: ").strip() or resultado[1]
                novo_email= input("Digite o seu email: ").strip() or resultado[2]
                novo_peso_str= input("Digite o seu peso: ").strip()
                try: #------------------------------------------------->alterar esses trys
                    novo_peso = float(novo_peso_str) if novo_peso_str else resultado[3]
                except ValueError:
                    print("\nERRO: O Peso Deve ter um número, alteração cancelada")
                    continuar = exibir_submenu("Tentando Alterar Cadastro dos Alunos")
                    continue
                nova_altura_str= input("Digite a sua altura: ").strip()
                try:
                    nova_altura = float(nova_altura_str) if nova_altura_str else resultado[3]
                except ValueError:
                    print("\nERRO: A Atlura Deve ser em número, alteração cancelada")
                    continuar = exibir_submenu("Tentando Alterar Cadastro dos Alunos")
                    continue
                break
            
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
            print(f"\nSUCESSO: o aluno agora tem os dados: nome: '{novo_nome}' | email: {novo_email} | peso: {novo_peso:.2f} | altura: {nova_altura:.2f}")
            input("Aperte ENTER para Continuar")
        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")
            input("Aperte ENTER para Continuar")
            break
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = exibir_submenu("Alterando Cadastro dos Alunos")


def alt_cad_produtos():
    '''
    Essa função permite que o usuário altere os dados
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("Alterando Cadastro de Produtos")
        try:
            print("Lista de produtos cadastrados:")
            exibir_prod()
            id_produto = int(input("\nDigite o [ID] do Produto que deseja alterar: "))

        except ValueError:
            print("ERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("Alterando Cadastro de Produtos")
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
                continuar = exibir_submenu("Alterando Cadastro de Produtos")
                continue

            print(f"""
Você Selecionou o Produto:
-ID: {produto[0]}
-Nome: {produto[1]}
-Quantidade: {produto[4]}
-Categoria: {produto[2]}
-Preço: R$ {produto[3]:.2f}
""")

            print("\nPreencha os campos abaixo e APENAS aperte ENTER para não alterar")
            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu("Tentando Alter o Cadastro de Produtos")
                # Nome
                novo_nome = input("Digite o novo nome: ").strip() or produto[1]
                # Categoria
                nova_categoria = input("Digite a nova categoria: ").strip() or produto[3]
                # Quantidade e Preço
                nova_qtde_str = input("Digite a nova quantidade: ").strip()
                try:
                    nova_qtde = int(nova_qtde_str) if nova_qtde_str else produto[4]
                except ValueError:
                    print("\nERRO: Não foi possível atribuir um Valor Inteiro a Quantidade")
                if nova_qtde < 0:
                    print("ERRO: A quantidade não pode ser negativa!")
                    input("Aperte ENTER para continuar")
                    continuar = 0
                    continue
                novo_preco_str = input("Digite o novo preço: ").strip()
                try:
                    novo_preco = float(novo_preco_str) if novo_preco_str else produto[3]
                except ValueError:
                    print("\nERRO: Não foi possível atribuir um Valor Inteiro a Quantidade")
                    continuar = 0
                    continue
                if novo_preco < 0:
                    print("ERRO: Preço não pode ser negativo!")
                    input("Aperte ENTER para continuar")
                    continuar = 0
                    continue
                break

            # UPDATE
            cursor.execute("""
                UPDATE prodserv
                SET nome = %s,
                    qtde = %s,
                    categoria = %s,
                    preco = %s
                WHERE id = %s
            """, (
                novo_nome,
                nova_qtde,
                nova_categoria,
                novo_preco,
                id_produto
            ))

            conexao.commit()

            print("\nProduto alterado com sucesso!")


        except mysql.connector.Error as erro:
            print("arquivo cadastro - linha 216")
            print(f"ERRO DE BANCO DE DADOS: {erro}")
            input("Aperte ENTER para continuar")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = exibir_submenu("Alterando Cadastro de Produtos")

def alt_cad_plano(): #============================== ALTERA CADASTRO DE PLANOS ===========================
    ''' 
    Essa função permite que o usuário altere os dados dos planos
    '''
    
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("Alterando cadastro de planos")
            
        try:
            print("\nPlanos cadastrados: ")
            exibir_planos()

            id_plano = int(input("\nDigite o ID do plano que deseja alterar"))
        
        except ValueError:
            print("ERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("Alterando cadastro de planos")
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
                continuar = exibir_submenu("Alterando Cadastro do plano")
                continue
                
            print(f"""
            \nVocê Selecionou o Plano:
            \nID: {plano_atual[0]}
            \nNome: {plano_atual[1]}
            \nPreço: R$ {plano_atual[2]:}
            \nQuantidade de aulas: {plano_atual[3]}
            """)

            print("\nPreencha os campos abaixo e caso não deseje alterar pressione ENTER")

            novo_nome_plano = input("Digite o novo nome: ").strip()
            if novo_nome_plano == "":
                novo_nome_plano = plano_atual[1]

            while True:
                novo_preco_plano = input("Digite o novo preço: ").strip()

                if novo_preco_plano == "":
                    novo_preco_plano = plano_atual[2]
                    break

                try:
                    novo_preco_plano = float(novo_preco_plano.replace(",", "."))
                    
                    if novo_preco_plano < 0:
                        print("ERRO: O preço não pode ser negativo")
                        continue

                    break

                except ValueError:
                    print("ERRO: Digite um preço válido")

            while True:
                nova_qtde_aulas = input("Digite a nova quantidade de aulas do plano: ").strip()

                if nova_qtde_aulas == "":
                    nova_qtde_aulas = plano_atual[3]
                    break
                try:
                    nova_qtde_aulas = int(nova_qtde_aulas)

                    if nova_qtde_aulas < 0:
                        print("ERRO: A quantidade de aulas não pode ser negativa")
                        continue
                    break
                except ValueError:
                    print("ERRO: Digite apenas números inteiros")

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

        except mysql.connector.Error as erro:
            print("arquivo cadastro - linha 332")
            print(f"ERRO FALTAL DE CONEXÃO COM O BANCO: {erro}")
            input("Aperte ENTER para continuar")
            break

        finally:
            if 'conexao' in locals() and conexao.is_connected:
                cursor.close()
                conexao.close()

        continuar = exibir_submenu("Alterando cadastro de planos")
        




def cad_aluno(): #==============================  CADASTRA ALUNOS ===========================
    ''' 
    Essa função permite que o usuário crie o cadastro de um novo aluno
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("Cadastrando Novos Alunos")
        
        novo_nome = input("\nDigite o nome do novo aluno: ").strip()
        novo_email = input("Digite o e-mail do novo aluno: ").strip()

        novo_peso_str = input("Digite o peso do aluno (ou ENTER para deixar vazio): ") or ""
        nova_altura_str = input("Digite a altura do aluno (ou ENTER para deixar vazio): ") or ""
        try:
            novo_peso = float(novo_peso_str) if novo_peso_str else 0.0
            nova_altura = float(nova_altura_str) if nova_altura_str else 0.0
            print("\nPlanos Disponíves:")
            exibir_planos()
            novo_plano = int(input("\nQual plano deseja contratar? "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            continuar = exibir_submenu("Cadastrandos Novos Alunos")

        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM planos WHERE id = %s", (novo_plano,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print("ERRO: O plano selecionado não existe")
            continuar = exibir_submenu("Cadastrando Novos Alunos")       
        else:
            try:
                cursor.execute("SELECT qtde_aulas FROM planos WHERE id = %s", (novo_plano,))
                aulas = cursor.fetchone()
                
                cursor.execute("""
                    INSERT INTO aluno (nome, email, peso, altura, id_plano, aulas_disp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (novo_nome, novo_email, novo_peso, nova_altura, novo_plano, aulas[0]))
                
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
            continuar = exibir_submenu("Cadastrando Novos Alunos")


def cad_produtos():
    '''
    Função responsavel por cadastrar um novo produto
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("Cadastrando Novo Aluno")

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
            novo_preco = float(input("Qual o valor desse novo produto/serviço?\n"))
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
            continuar = exibir_submenu("Cadastrando Novo Plano")
        
        # input para receber o nome do novo plano
        print(" ----- Cadastrar Plano de Aulas ----- \n")
        novo_nome = input("Qual o nome do novo plano?\n")
    
        # inputs para receber o preço e quantidade de aulas do novo plano
        try:
            novo_preco = float(input("Qual o valor desse novo plano?\n"))
            nova_qtde_aulas = int(input("Qual a quantidade de aulas desse novo plano?\n"))
        except ValueError:
            print("ERROR: Entrada invalida!")
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