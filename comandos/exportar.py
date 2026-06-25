from interfaces.submenu import submenu_exportar
import datetime
import mysql.connector
from banco_dados import abrir_conexao


def export_vendas():
    escolha = submenu_exportar
    if escolha == 3: #Escolheu Voltar
        print("\nVoltando...")
        return 
    if escolha == 2: #Escolheu Imprimir Todos
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT vendas.horario, prodserv.nome vendas.qtde, vendas.subtotal
                FROM vendas
                INNER JOIN prodserv IN vendas.id_prodserv = prodserv.id
                ORDER BY vendas.id DESC
            """)
            vendas = cursor.fetchall()

            if not vendas:
                print("\nERRO: Não foi Registrado Nenhuma Vendas Até o Momento")
                input("Aperte ENTER para Continuar")
                return
            
            cursor.execute("""
                SELECT SUM(subtotal)
                FROM vendas
            """)
            faturamento_total = cursor.fetchone()[0]

            mes_atual = datetime.datetime.now().strftime("%m").strip()
            dia_atual = datetime.datetime.now().strftime("%d").strip()
            faturamento_mensal = sum(venda[3] for venda in vendas if venda[0].split("/")[1] ==  mes_atual)
            faturamento_diario = sum(venda[3] for venda in vendas if venda[0].split("/")[2] ==  dia_atual)
        except mysql.connector.Error as erro:
            print(f"\nArquivo: exportar - Linha: 39\nERRO: Falha no Banco de Dados, {erro}")
            input("Aperte ENTER para Continuar")
            return
        finally:
            if 'conexao' in locals() and conexao.is_connected:
                cursor.close()
                conexao.close()

        nome_arquivo = f"relatorio-vendas_{datetime.datetime.now().strftime("%y%m%d_%H-%M-%S")}.txt"
        
        with open(f"relatorios/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
            arquivo.write("=================================================\n")
            arquivo.write("                RELATÓRIO DE VENDAS                ")
            arquivo.write("\n-------------------------------------------------\n\n")
            arquivo.write(f"Faturamento de Hoje = R$ {faturamento_diario:.2f} ----------- Faturamento Mensal: {faturamento_mensal}\n")

            for venda in vendas:
                linha = f"DATA: {venda[0]} | ITEM: {venda[1]} | QUANTIDADE: {venda[2]} | SUBTOTAL: {venda[3]:.2f}\n"
                arquivo.write(linha)
            arquivo.write(f"\n____FATURAMENTO TOTAL:_R$_{faturamento_total}___________________________")
            print("----------SUCESSO")