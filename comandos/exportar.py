import datetime
import mysql.connector
from banco_dados import abrir_conexao
from interfaces.funcontinuar import exibir_submenu

#======================================================================================================
def export_vendas_geral():#==================================================VENDAS GERAL==============
#======================================================================================================    
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT vendas.horario, prodserv.nome, vendas.qtde, vendas.subtotal
            FROM vendas
            INNER JOIN prodserv ON vendas.id_prodserv = prodserv.id
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

        hoje = datetime.datetime.now()
        mes_atual = hoje.month
        dia_atual = hoje.day
        hoje_formatado = hoje.strftime("%d/%m/%y")
        faturamento_mensal = sum(venda[3] for venda in vendas if venda[0].month ==  mes_atual)
        faturamento_diario = sum(venda[3] for venda in vendas if venda[0].day ==  dia_atual)
    except mysql.connector.Error as erro:
        print(f"\nArquivo: exportar - Linha: 38\nERRO: Falha no Banco de Dados, {erro}")
        input("Aperte ENTER para Continuar")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected:
            cursor.close()
            conexao.close()

    nome_arquivo = f"relatorio-vendas-geral_{datetime.datetime.now().strftime("%y%m%d_%H-%M-%S")}.txt"
    
    with open(f"relatorios/vendas/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
        arquivo.write("==========================================================================\n")
        arquivo.write("                         RELATÓRIO DE VENDAS GERAL                        \n")
        arquivo.write("--------------------------------------------------------------------------\n")
        arquivo.write(f"Data de Hoje: {hoje_formatado}\n")
        arquivo.write(f"Faturamento de Hoje = R$ {faturamento_diario:.2f} ----------- Faturamento Mensal: {faturamento_mensal}\n")

        for venda in vendas:
            linha = f"- DATA: {venda[0]} | ITEM: {venda[1]} | QUANTIDADE: {venda[2]} | SUBTOTAL: {venda[3]:.2f}\n"
            arquivo.write(linha)
        arquivo.write(f"\n___________________________FATURAMENTO TOTAL:_R$_{faturamento_total}___________________________")
    print("\nSUCESSO: Relatório Exportado para a Pasta 'vendas' Dentro da Pasta 'relatorios'")


#======================================================================================================
def export_vendas_qtde():#=================================================VENDAS QTDE=================
#======================================================================================================
    continuar = 1
    while True:
        if continuar == 2:
            return
        elif continuar == 0:
            continuar = exibir_submenu("'Inserir Quantidade de Vendas a ser Impressa'")
            continue
        try: 
            qtde_export = int(input("Digite a Quantidade de Vendas Mais Recentes a Serem Exibidas: "))
            if qtde_export <= 0:
                print("\nERRO: Você não Pode Exportar uma Quantidade Nula ou Negativa")
                continuar = 0
                continue
        except ValueError:
            print("\nERRO: Você Deve Digitar APENAS Números")
            continuar = 0
            continue
        break

    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT vendas.horario, prodserv.nome, vendas.qtde, vendas.subtotal
            FROM vendas
            INNER JOIN prodserv ON vendas.id_prodserv = prodserv.id
            ORDER BY vendas.id DESC
            LIMIT %s
        """, (qtde_export,))
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

        hoje = datetime.datetime.now()
        mes_atual = hoje.month
        dia_atual = hoje.day
        hoje_formatado = hoje.strftime("%d/%m/%y")
        faturamento_mensal = sum(venda[3] for venda in vendas if venda[0].month ==  mes_atual)
        faturamento_diario = sum(venda[3] for venda in vendas if venda[0].day ==  dia_atual)
    except mysql.connector.Error as erro:
        print(f"\nArquivo: exportar - Linha: 113\nERRO: Falha no Banco de Dados, {erro}")
        input("Aperte ENTER para Continuar")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected:
            cursor.close()
            conexao.close()

    nome_arquivo = f"relatorio-vendas-quantitativo_{datetime.datetime.now().strftime("%y%m%d_%H-%M-%S")}.txt"
    
    with open(f"relatorios/vendas/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
        arquivo.write("==========================================================================\n")
        arquivo.write("                      RELATÓRIO DE VENDAS QUANTITATIVO                    \n")
        arquivo.write("--------------------------------------------------------------------------\n")
        arquivo.write(f"Data de Hoje: {hoje_formatado}\n")
        arquivo.write(f"Faturamento de Hoje = R$ {faturamento_diario:.2f} ----------- Faturamento Mensal: {faturamento_mensal}\n")

        for venda in vendas:
            linha = f"- DATA: {venda[0]} | ITEM: {venda[1]} | QUANTIDADE: {venda[2]} | SUBTOTAL: {venda[3]:.2f}\n"
            arquivo.write(linha)
        arquivo.write(f"\n___________________________FATURAMENTO TOTAL:_R$_{faturamento_total}___________________________")
    print("\nSUCESSO: Relatório Exportado para a Pasta 'vendas' Dentro da Pasta 'relatorios'")



#======================================================================================================
def export_chekin_geral():#===============================================CHECKIN GERAL================
#======================================================================================================
    '''
    função responsavel por exportar .txt com informações de todos os check-in, incluindo data e demais infos
    '''
    # junção de infos
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT aluno.nome, checkin.horario
            FROM checkin
            INNER JOIN aluno ON checkin.id_aluno = aluno.id
            ORDER BY checkin.horario DESC
        """)
        checkins = cursor.fetchall()

        if not checkins:
            print("\nERRO: Não foi registrado nenhuma check-in até o momento")
            input("Aperte ENTER para retornar")
            return
        
        cursor.execute("""
            SELECT COUNT(*)
            FROM checkin
        """)
        qtde_checkins = cursor.fetchone()[0]

        hoje = datetime.datetime.now()
        ano_atual = hoje.year
        mes_atual = hoje.month
        dia_atual = hoje.day
        hoje_formatado = hoje.strftime("%d/%m/%y")
        checkin_mensal = sum(1 for checkin in checkins if checkin[1].month ==  mes_atual and checkin[1].year == ano_atual) + 1
        checkin_diario = sum(1 for checkin in checkins if checkin[1].day ==  dia_atual and checkin[1].month ==  mes_atual and checkin[1].year == ano_atual) + 1

    except mysql.connector.Error as erro:
        print(f"\nArquivo: exportar, função: export_checkin_geral() \nERRO: Falha no Banco de Dados: {erro}")
        input("Aperte ENTER para Continuar")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected:
            cursor.close()
            conexao.close()

    # criação do arquivo .txt e e exportação de infos de fato
    nome_arquivo = f"relatorio-checkin-geral_{datetime.datetime.now().strftime("%y%m%d_%H-%M-%S")}.txt"

    with open(f"relatorios/checkins/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
        arquivo.write("==========================================================================\n")
        arquivo.write("                      RELATÓRIO DE CHECK-IN GERAL                         \n")
        arquivo.write("==========================================================================\n")
        arquivo.write(f"Data de hoje: {hoje_formatado}\n")
        arquivo.write(f"Check-ins de hoje: {checkin_diario} ----------- Check-ins do mês: {checkin_mensal}\n")

        for checkin in checkins:
            linha = f"- DATA: {checkin[1]} | ALUNO: {checkin[0]}\n"
            arquivo.write(linha)
        arquivo.write(f"\n-------------QUANTIDADE DE CHECK-INS TOTAIS: {qtde_checkins}--------------")
    print("\nSUCESSO: Relatório Exportado para a Pasta 'checkins' Dentro da Pasta 'relatorios'")



    
#======================================================================================================
def export_checkin_qtde():#================================================CHECKIN QTDE================
#======================================================================================================
    '''
    função responsavel por exportar .txt com informações de todos os check-in, incluindo data e demais infos
    '''    
    continuar = 1
    while True:
        if continuar == 2:
            return
        elif continuar == 0:
            continuar = exibir_submenu("'Inserir Quantidade de Checkins a ser Impressa'")
            continue
        try: 
            qtde_export = int(input("Digite a Quantidade de Chekins Mais Recentes a Serem Exibidas: "))
            if qtde_export <= 0:
                print("\nERRO: Você não Pode Exportar uma Quantidade Nula ou Negativa")
                continuar = 0
                continue
        except ValueError:
            print("\nERRO: Você Deve Digitar APENAS Números")
            continuar = 0
            continue
        break
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT checkin.horario, aluno.nome
            FROM checkin
            INNER JOIN aluno ON checkin.id_aluno = aluno.id
            ORDER BY checkin.id DESC
            LIMIT %s
        """, (qtde_export,))
        checkins = cursor.fetchall()

        if not checkins:
            print("\nERRO: Não foi Registrado Nenhum CheckIn Até o Momento")
            input("Aperte ENTER para Continuar")
            return
        
        checkins_totais = len(checkins)

        hoje = datetime.datetime.now()
        ano_atual = hoje.year
        mes_atual = hoje.month
        dia_atual = hoje.day
        hoje_formatado = hoje.strftime("%d/%m/%y")
        checkin_mensal = sum(1 for checkin in checkins if checkin[0].month ==  mes_atual and checkin[0].year == ano_atual) + 1
        checkin_diario = sum(1 for checkin in checkins if checkin[0].day ==  dia_atual and checkin[0].month ==  mes_atual and checkin[0].year == ano_atual) + 1
    except mysql.connector.Error as erro:
        print(f"\nArquivo: exportar - Linha: 255\nERRO: Falha no Banco de Dados, {erro}")
        input("Aperte ENTER para Continuar")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected:
            cursor.close()
            conexao.close()

    nome_arquivo = f"relatorio-checkins-quantitativo_{datetime.datetime.now().strftime("%y%m%d_%H-%M-%S")}.txt"
    
    with open(f"relatorios/checkins/{nome_arquivo}", "w", encoding="utf-8") as arquivo:
        arquivo.write("==========================================================================\n")
        arquivo.write("                    RELATÓRIO DE CHECK-IN QUANTITATIVO                    \n")
        arquivo.write("--------------------------------------------------------------------------\n")
        arquivo.write(f"Data de Hoje: {hoje_formatado}\n")
        arquivo.write(f"Checkins de Hoje = R$ {checkin_diario:.2f} ----------- Checkins Mensal: {checkin_mensal}\n")
        for checkin in checkins:
            linha = f"- DATA: {checkin[0]} | ALUNO: '{checkin[1]}'\n"
            arquivo.write(linha)
        arquivo.write(f"\n___________________________QUANTIDADE TOTAL DE CHECK-INS: {checkins_totais}___________________________")
    print("\nSUCESSO: Relatório Exportado para a Pasta 'checkins' Dentro da Pasta 'relatorios'")