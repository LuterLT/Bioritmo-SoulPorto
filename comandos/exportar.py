from interfaces.submenu import submenu_exportar
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
        except mysql.connector.Error as erro:
            print("\nERRO: Falha no Banco de Dados, ")
            input("Aperte ENTER para Continuar")
            return
        finally:
            if 'conexao' in locals() and conexao.is_connected:
                cursor.close()
                conexao.close()
