from interfaces.funcontinuar import exibir_submenu
from interfaces.interface import exibir_prod
from banco_dados import abrir_conexao
from interfaces.funcontinuar import exibir_submenu

import mysql.connector
import datetime

def carrinho_venda():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'carrinho de compra'")
        
        carrinho = []

        exibir_prod()
        try:
            id_venda = int(input("\nDigite o código do produto / serviço (ou -1 pra concluir compra ou -2 pra cancelar a compra):\n"))
        except ValueError:
            print("ERROR: ID invalido!")
            continuar = exibir_submenu(f"carrinho de compra ''")
            continue

        if id_venda == -1:
            break
        elif id_venda == -2:
            print("Compra cancelada")
            carrinho = []
            return

        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, preco, qtde FROM prodserv WHERE id = %s AND ativo = 1", (id_venda,))

        resultado = cursor.fetchone()

        cursor.close()
        conexao.close()

        if not resultado:
            print("ERROR: Id invalido! Esse livro não existe no sistema!")
            continue
            
        nome_prodserv, preco_prodserv, estoque_real = resultado

        try:
            qtd = int(input(f"Quantos do '{nome_prodserv}' você deseja adicionar ao carinho? Estoque disponivel: {estoque_real} \n"))
        except ValueError:
            print("ERROR: Quantidade invalido!")
            continue

        qtd_no_carrinho = sum(prodserv['qtd'] for prodserv in carrinho if prodserv['id'] == id_venda)
        estoque_disponivel = estoque_real - qtd_no_carrinho

        if qtd <= 0:
            print("ERRO: Quantidade invalida!")
        elif qtd > estoque_disponivel:
            print(f"Estoque insuficiente, vocês já tem {qtd_no_carrinho} no carrinho, o estoque total é {estoque_real}.")
        else:
            carrinho.append({
                "id": id_venda,
                "nome": nome_prodserv,
                "preco": preco_prodserv,
                "qtd": qtd,
                "subtotal": qtd * preco_prodserv,
            })

            print(f"-> {qtd} x '{nome_prodserv}' adicionado ao carrinho, cada um com valor de {preco_prodserv}.")
    
    if len(carrinho) > 0:
        total_compra = sum(item['subtotal'] for item in carrinho)
        print(f" ===== Fechamento do caixa ===== \n"
              f"Total a pagar: R$ {total_compra:.2f}") # precisa arrumar
        confirmar = input("Confirmar compra e pagamento? *(S/N)").lower().strip()


        if confirmar == 's':
            conexao = abrir_conexao()
            cursor = conexao.cursor()

#             try:
#                 for item in carrinho:
#                     cursor.execute("""
#                         UPDATE prodserv
#                         SET qtde = qtde - %s
#                         WHERE id = %s
#                     """, (item['qtd'], item['id']))
                
#                     cursor.execute("""
#                         INSERT INTO vendas (horario, id_livro, preco_uni, qtd, valor)
#                         VALUES (%s, %s, %s, %s, %s)
#                     """, (
#                         datetime.datetime.now().strftime("%y/%m/%d - %H:%M:%S"),
#                         item['id'],
#                         item['preco'],
#                         item['qtd'],
#                         item['subtotal']
#                         )
#                     )
#                 conexao.commit()
#                 print("Venda concluida com sucesso! >:D ")

#             except mysql.connector.Error as erro:
#                 conexao.rollback()
#                 print("\nERROR FATAL no banco de dados: Transação cancelada!",
#                         f"Motivo técnico: {erro}",
#                         "O estoque restaurado e nenhuma nota fiscal corrompida gerada.")
            

#             finally:
#                 if 'conexao' in locals() and conexao.is_connected():
#                     cursor.close()
#                     conexao.close()

#         else:
#             print("Venda não finalizada!")