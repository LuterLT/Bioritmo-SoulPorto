from banco_dados import abrir_conexao
import mysql.connector

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













