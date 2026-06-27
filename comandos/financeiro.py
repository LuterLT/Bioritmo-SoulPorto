import mysql.connector
from banco_dados import abrir_conexao

from interfaces.interface import exibir_prod, exibir_planos
from interfaces.funcontinuar import exibir_submenu

def exibir_nf():
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT vendas.id, vendas.horario, prodserv.nome, vendas.qtde, vendas.subtotal
            FROM vendas
            INNER JOIN prodserv ON vendas.id_prodserv = prodserv.id        
        """)
        historico = cursor.fetchall()

        if len(historico) == 0:
            print("Nenhuma venda efetuada até o momento")
        else:
            for venda in historico:
                print(f"""
Venda: #{venda[0]}  
Data e Horário: {venda[1]}

Produto Vendido: {venda[2]}
                x {venda[3]} unidades

Valor Total da Venda: {venda[4]:.2f}

--------------------------------------------
""")
    except mysql.connector.Error as erro:
        print(f"ERRO: Falha no Banco de Dados, {erro}")
        input("Aperte ENTER para Continuar")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected:
            cursor.close()
            conexao.close()


def promocao_produto():
    """
    Aplica promoção em Produtos/Serviços
    """
    while True:
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            print("\n----- PRODUTOS E SERVIÇOS -----")

            cursor.execute("""
                SELECT id, nome, categoria, preco
                FROM prodserv
                WHERE ativo = 1
            """)

            produtos = cursor.fetchall()

            if not produtos:
                print("\nNenhum produto ou serviço cadastrado.")
                return

            print(f"\n{'ID':<5}{'Nome':<30}{'Categoria':<20}{'Preço'}")
            print("-" * 70)

            for produto in produtos:
                print(
                    f"{produto[0]:<5}"
                    f"{produto[1]:<30}"
                    f"{produto[2]:<20}"
                    f"R$ {float(produto[3]):.2f}"
                )

            print("\n0 - Aplicar promoção em TODOS")

            # Escolha do produto
            while True:
                try:
                    id_produto = int(input("\nDigite o ID do produto/serviço ou 0 para todos: "))
                    break
                except ValueError:
                    print("\nERRO: Digite apenas números inteiros.")

            # Escolha do desconto
            while True:
                try:
                    desconto = float(input("Digite o percentual de desconto (%): ").replace(",", "."))

                    if desconto <= 0:
                        print("\nERRO: O desconto deve ser maior que zero.")
                        continue

                    if desconto > 100:
                        print("\nERRO: O desconto não pode ser maior que 100%.")
                        continue

                    break

                except ValueError:
                    print("\nERRO: Digite apenas números.")

            # PROMOÇÃO EM TODOS
            if id_produto == 0:

                cursor.execute("""
                    SELECT nome, preco
                    FROM prodserv
                    WHERE ativo = 1
                """)

                produtos = cursor.fetchall()

                cursor.execute("""
                    UPDATE prodserv
                    SET preco = preco - (preco * %s / 100)
                    WHERE ativo = 1
                """, (desconto,))

                conexao.commit()

                print(f"\nPromoção de {desconto:.2f}% aplicada!\n")

                print(f"{'Produto':<35}{'Antigo':<15}{'Novo'}")
                print("-" * 65)

                for nome, preco in produtos:
                    novo_preco = float(preco) * (1 - desconto / 100)

                    print(
                        f"{nome:<35}"
                        f"R$ {float(preco):<10.2f}"
                        f"R$ {novo_preco:.2f}"
                    )

            # PROMOÇÃO EM UM PRODUTO
            else:

                cursor.execute("""
                    SELECT nome, preco
                    FROM prodserv
                    WHERE id = %s
                    AND ativo = 1
                """, (id_produto,))

                produto = cursor.fetchone()

                if not produto:
                    print("\nERRO: Produto/Serviço não encontrado.")
                    continue

                nome = produto[0]
                preco_antigo = float(produto[1])
                preco_novo = preco_antigo * (1 - desconto / 100)

                cursor.execute("""
                    UPDATE prodserv
                    SET preco = preco - (preco * %s / 100)
                    WHERE id = %s
                    AND ativo = 1
                """, (desconto, id_produto))

                conexao.commit()

                print("\nPromoção aplicada com sucesso!\n")

                print(f"Produto      : {nome}")
                print(f"Preço antigo : R$ {preco_antigo:.2f}")
                print(f"Desconto     : {desconto:.2f}%")
                print(f"Novo preço   : R$ {preco_novo:.2f}")

            # Perguntar se deseja continuar
            while True:
                resposta = input(
                    "\nDeseja aplicar outra promoção? (1 - Sim / 2 - Não): "
                ).strip()

                if resposta == "1":
                    break

                elif resposta == "2":
                    return

                else:
                    print("ERRO: Digite apenas 1 ou 2.")

        except mysql.connector.Error as erro:
            print(f"\nERRO: Falha no Banco de Dados: {erro}")

            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()

            return

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

def promocao_plano():
    """
    Função responsável por aplicar promoção em planos
    """
    while True:
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            print("\n======= PLANOS =======")

            cursor.execute("""
                SELECT id, nome, preco
                FROM planos
                WHERE ativo = 1
            """)

            planos = cursor.fetchall()

            if not planos:
                print("\nNenhum plano cadastrado.")
                return

            print(f"\n{'ID':<5}{'Nome':<30}{'Preço'}")
            print("-" * 50)

            for plano in planos:
                print(
                    f"{plano[0]:<5}"
                    f"{plano[1]:<30}"
                    f"R$ {float(plano[2]):.2f}"
                )

            print("\n0 - Aplicar promoção em TODOS")

            # Escolha do plano
            while True:
                try:
                    id_plano = int(input("\nDigite o ID do plano ou 0 para todos: "))
                    break
                except ValueError:
                    print("\nERRO: Digite apenas números inteiros.")

            # Escolha do desconto
            while True:
                try:
                    desconto = float(
                        input("Digite o percentual de desconto (%): ").replace(",", ".")
                    )

                    if desconto <= 0:
                        print("\nERRO: O desconto deve ser maior que zero.")
                        continue

                    if desconto > 100:
                        print("\nERRO: O desconto não pode ser maior que 100%.")
                        continue

                    break

                except ValueError:
                    print("\nERRO: Digite apenas números.")

            # PROMOÇÃO EM TODOS
            if id_plano == 0:

                cursor.execute("""
                    SELECT nome, preco
                    FROM planos
                    WHERE ativo = 1
                """)

                planos = cursor.fetchall()

                cursor.execute("""
                    UPDATE planos
                    SET preco = preco - (preco * %s / 100)
                    WHERE ativo = 1
                """, (desconto,))

                conexao.commit()

                print(f"\nPromoção de {desconto:.2f}% aplicada!\n")

                print(f"{'Plano':<35}{'Antigo':<15}{'Novo'}")
                print("-" * 65)

                for nome, preco in planos:
                    novo_preco = float(preco) * (1 - desconto / 100)

                    print(
                        f"{nome:<35}"
                        f"R$ {float(preco):<10.2f}"
                        f"R$ {novo_preco:.2f}"
                    )

            # PROMOÇÃO EM UM PLANO
            else:

                cursor.execute("""
                    SELECT nome, preco
                    FROM planos
                    WHERE id = %s
                    AND ativo = 1
                """, (id_plano,))

                plano = cursor.fetchone()

                if not plano:
                    print("\nERRO: Plano não encontrado.")
                    continue

                nome = plano[0]
                preco_antigo = float(plano[1])
                preco_novo = preco_antigo * (1 - desconto / 100)

                cursor.execute("""
                    UPDATE planos
                    SET preco = preco - (preco * %s / 100)
                    WHERE id = %s
                    AND ativo = 1
                """, (desconto, id_plano))

                conexao.commit()

                print("\nPromoção aplicada com sucesso!\n")

                print(f"Plano        : {nome}")
                print(f"Preço antigo : R$ {preco_antigo:.2f}")
                print(f"Desconto     : {desconto:.2f}%")
                print(f"Novo preço   : R$ {preco_novo:.2f}")

            # Perguntar se deseja continuar
            while True:
                resposta = input(
                    "\nDeseja aplicar outra promoção? (1 - Sim / 2 - Não): "
                ).strip()

                if resposta == "1":
                    break

                elif resposta == "2":
                    return

                else:
                    print("\nERRO: Digite apenas 1 ou 2.")

        except mysql.connector.Error as erro:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()

            print(f"\nERRO no Banco de Dados: {erro}")
            return

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

def alt_preco_prodserv():
    exibir_prod()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Alterar Preço de Produtos/Serviços'")
            continue
            
        try:
            id_prodserv = int(input("\nDigite o [ID] do produto/serviço que deseja alterar o preço: "))
        except ValueError:
            print("ERRO: Formato Inválido! O ID deve ser um número inteiro.")
            continuar == 0
            continue
        
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome, preco FROM prodserv WHERE id = %s AND ativo = 1", (id_prodserv,))
            result = cursor.fetchone()

            if not result:
                print("\nERRO: Produto/serviço não existe ou está desativado")
                continuar = 0
                continue
                
            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu(f"Alterar Preço de '{result[0]}'")
                    continue
                try:
                    novo_preco = float(input(f"\nDigite o novo preço de '{result[0]}': R$ ").replace(",", "."))
                except ValueError:
                    print("ERRO: Formato Inválido! O preço deve ser um número.")
                    continuar = 0
                    continue

                if novo_preco < 0:
                    print("ERRO: O preço não pode ser negativo!")
                    continuar = 0
                    continue
                
                cursor.execute("UPDATE prodserv SET preco = %s WHERE id = %s", (novo_preco, id_prodserv))
                conexao.commit()
                
                print(f"\nO preço de '{result[0]}' foi alterado para R$ {novo_preco:.2f} com SUCESSO!")
                break

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = 0
        continue
    
    
def alt_preco_plano():
    exibir_planos()
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Alterar Preço de Planos'")
            continue
            
        try:
            id_plano = int(input("\nDigite o [ID] do plano que deseja alterar o preço: "))
        except ValueError:
            print("ERRO: Formato Inválido! O ID deve ser um número inteiro.")
            continuar == 0
            continue

        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT nome, preco FROM planos WHERE id = %s AND ativo = 1", (id_plano,))
            result = cursor.fetchone()

            if not result:
                print("\nERRO: Plano não existe ou está desativado")
                continuar = 0
                continue

            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu(f"Alterar Preço de '{result[0]}'")
                    continue
                try:
                    novo_preco = float(input(f"\nDigite o novo preço de '{result[0]}': R$ ").replace(",", "."))
                except ValueError:
                    print("ERRO: Formato Inválido! O preço deve ser um número.")
                    continuar = 0
                    continue

                if novo_preco < 0:
                    print("ERRO: O preço não pode ser negativo!")
                    continuar = 0
                    continue
                
                cursor.execute("UPDATE planos SET preco = %s WHERE id = %s", (novo_preco, id_plano))
                conexao.commit()

                print(f"\nO preço de '{result[0]}' foi alterado para R$ {novo_preco:.2f} com SUCESSO!")
                break

        except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
        continuar = 0
        continue



def painel_bi():
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM vendas")
        if cursor.fetchone()[0] == 0: # ~~~~ALTERAÇÃO NO FETCH PARA VER SE RESOLVE O BUG!~~~~~~
            print("\nNenhuma venda registrada até o momento")
            return
        cursor.execute("SELECT SUM(subtotal) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f"\n-> Histórico de Faturamento Bruto: R${faturamento:.2f}")

        cursor.execute("SELECT AVG(subtotal) FROM vendas")
        ticket_medio = cursor.fetchone()[0]
        print(f"-> Ticket Médio: R${ticket_medio:.2f}")

        cursor.execute("""
            SELECT prodserv.nome, SUM(vendas.qtde)
            FROM vendas
            INNER JOIN prodserv ON vendas.id_prodserv = prodserv.id
            GROUP BY prodserv.nome
            ORDER BY SUM(subtotal) DESC
            LIMIT 1
        """)
        prod_camp, maior_qtde = cursor.fetchone()
        print(f"-> Produto mais vendido: {prod_camp} ({maior_qtde}) unidades vendidas!")

        #ADICIONANDO UNIDADE MENOS VENDIDA CASO NÃO QUEIRA PODE APAGAR 
        cursor.execute("""
            SELECT prodserv.nome, SUM(vendas.qtde)
            FROM vendas
            INNER JOIN prodserv ON vendas.id_prodserv = prodserv.id
            GROUP BY prodserv.nome
            ORDER BY SUM(vendas.qtde) ASC
            LIMIT 1
        """)
        prod_menos, menor_qtde = cursor.fetchone()
        print(f"\n-> Produto menos vendido: {prod_menos} ({menor_qtde}) unidades vendidas!")

        #FIM DO UNIDADE MENOS VENDIDA

    except mysql.connector.Error as erro:
            conexao.rollback()
            print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

