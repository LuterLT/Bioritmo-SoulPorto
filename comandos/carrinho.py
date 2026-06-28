from interfaces.funcontinuar import exibir_submenu
from interfaces.interface import exibir_prod
from banco_dados import abrir_conexao

import mysql.connector
import datetime

def carrinho_venda():
    carrinho = []
    continuar = 1

    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'carrinho de compra'")
            continue

        while True:
            if continuar == 2:
                break
            elif continuar == 0:
                continuar = exibir_submenu("'carrinho de compra'")
                continue
            exibir_prod()
            #exibe carrinho
            print("--- Carrinho ---")
            if len(carrinho) == 0:
                print("Carrinho vazio até o momento")
            for item in carrinho:
                print(f"-> [{item['id']}] {item['nome']} x {item['qtde']} | Categoria: {item['categoria']} | Valor Unitário: R${item['preco']} | Subtotal: R${item['subtotal']} ")

            try:
                print("\n1 - Adicionar ao carrinho\n2 - FINALIZAR compra\n3 - CANCELAR compra e VOLTAR")
                opcao = int(input("\nQual opção deseja acessar? "))
            except ValueError:
                print("ERRO: Opção inválida")
                continue
            if opcao == 2:
                break
            elif opcao == 3:
                print("Compra CANCELADA\nVoltando...\n")
                carrinho = []
                return
            elif opcao == 1:
                try:
                    id_venda = int(input("\nDigite o [ID] do Produto/Serviço: \n"))
                except ValueError:
                    print("ERRO: Formato Inválido! O [ID] deve ser um número inteiro")
                    continuar = 0
                    continue

                conexao = abrir_conexao()
                cursor = conexao.cursor()

                cursor.execute("SELECT nome, categoria, preco, qtde FROM prodserv WHERE id = %s AND ativo = 1", (id_venda,))
                resultado = cursor.fetchone()

                if not resultado:
                    print("ERRO: ID invalido! Produto/Serviço não existe ou está desativado")
                    continuar = 0
                    continue
                    
                nome_prodserv, categ_prodserv, preco_prodserv, estoque_real = resultado

                try:
                    if categ_prodserv.lower() != "serviços":
                        print(f"Estoque disponível de '{nome_prodserv}': {estoque_real}")
                        qtd = int(input(f"Quantas unidades você deseja adicionar ao carinho? "))
                    else:
                        qtd = 1
                except ValueError:
                    print("ERROR: Quantidade Inválida! A quantidade deve ser um número inteiro")
                    continue

                qtd_no_carrinho = sum(prodserv['qtde'] for prodserv in carrinho if prodserv['id'] == id_venda)
                estoque_disponivel = estoque_real - qtd_no_carrinho

                if qtd <= 0:
                    print("\nERRO: Quantidade invalida!")
                    input("Aperte ENTER para Continuar")
                    continue
                elif qtd > estoque_disponivel:
                    print("\nERRO: Estoque Insuficiente")
                    print(f"Temos no estoque {estoque_disponivel} unidades e você já tem {qtd_no_carrinho} no carrinho")
                    input("Aperte ENTER para Continuar")
                    continue
                else:
                    carrinho.append({
                        "id": id_venda,
                        "nome": nome_prodserv,
                        "categoria": categ_prodserv,
                        "preco": preco_prodserv,
                        "qtde": qtd,
                        "subtotal": qtd * preco_prodserv,
                    })

                    print(f"\n-> {nome_prodserv} x {qtd} adicionado ao carrinho!\n")
                    continue

        if len(carrinho) > 0:
            total_compra = sum(item['subtotal'] for item in carrinho)
            print(f"\n ===== Fechamento do caixa ===== \n"
                f"Total a pagar: R$ {total_compra:.2f}")
            print(f"Produtos no carrinho: ")
            for item in carrinho:
                print(f"-> [{item['id']}] {item['nome']} x {item['qtde']} | Categoria: {item['categoria']} | Valor Unitário: R${item['preco']} | Subtotal: R${item['subtotal']} ")
            confirmar = input("\nConfirmar pagamento e registrar venda (s/n)?\n").lower().strip()

            if confirmar == "s":
                conexao = abrir_conexao()
                cursor = conexao.cursor()

                try:
                    for item in carrinho:
                        if item['categoria'].lower() != "serviços":
                            cursor.execute("""
                                UPDATE prodserv
                                SET qtde = qtde - %s
                                WHERE id = %s
                            """, (item['qtde'], item['id']))
                            
                        cursor.execute("""
                            INSERT INTO vendas (id_prodserv, horario, qtde, subtotal)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            item['id'],
                            datetime.datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
                            item['qtde'],
                            item['subtotal']
                            )
                        )
                    conexao.commit()
                    print("Venda concluida com sucesso! >:D \n")
                    carrinho = []

                except mysql.connector.Error as erro:
                    conexao.rollback()
                    print("\nERROR FATAL no banco de dados: Transação cancelada!",
                            f"Motivo técnico: {erro}",
                            "Estoque restaurado e nenhuma nota fiscal corrompida gerada.")

                finally:
                    if 'conexao' in locals() and conexao.is_connected():
                        cursor.close()
                        conexao.close()

            else: #se colocar "n" no confirmar
                print("\nVenda não finalizada!\n")
        else:
            print("\nERRO: Não é Possível Finalizar uma Compra sem Itens no Carrinho")
            input("Aperte ENTER para Continuar")
