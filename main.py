#importar as operações aqui
import mysql.connector

from banco_dados import iniciar_db, abrir_conexao
from comandos.checkin import checkin
from comandos.carrinho import carrinho_venda
# from comandos.consultas import consulta_imc

# importação dos submenus de cada função
from interfaces.submenu import submenu_cad, submenu_est, submenu_consulta
from interfaces.funcontinuar import exibir_submenuHome
from interfaces.interface import exibir_menu


#iniciar o programa
iniciar_db()

continuar = 1 #-> inicialização base do menu de continuidade
while True:
    if continuar == 2: #-> Se o usuário escolheu sair (parar de continuar)
        print(f"Caixa Atual: {caixa:.2f}\nEncerrando o Sistema...")
        break
    elif continuar == 0: #-> Se o usuário digitou o comando errado no submenu de continuidade
        continuar = exibir_submenuHome()
        continue
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        cursor.execute("SELECT SUM(subtotal) FROM vendas")
        result_caixa = cursor.fetchone()[0]
        caixa = result_caixa if result_caixa is not None else 0.0

    except mysql.connector.Error as erro:
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO (main): {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
    
    exibir_menu()
    try:
        menu = int(input("Digite o comando: "))
    except ValueError:
        print("ERROR: Digite apenas números inteiros!")
        continuar = 0
        continue

    if menu == 0:
        print(f"Caixa Atual: {caixa:.2f}\nEncerrando o Sistema...")
        break

    elif menu == 1:
        checkin() #FINALIZADA
    
    elif menu == 2:
        print("\n-----Cadastros/Alterações Cadastrais-----\n")
        submenu_cad() #FINALIZADA
    
    elif menu == 3:
        print("\n-----Vendas-----\n")
        carrinho_venda() #iniciado

    elif menu == 4:
        print("\n-----Repor Estoque-----\n")
        submenu_est() #em alterações
    
    elif menu == 5:
        print("\n-----Listar Informações-----\n")
        #   submenu_listar()

    elif menu == 6:
        print("\n-----Consulta-----\n")
        submenu_consulta() #em alterações

    elif menu == 7:
        print("\n-----Ativar/Desativar Cadastros-----")
        # submenu_atv_dst()

    elif menu == 8:
        print("\n-----Calcular IMC-----")
        # consulta_imc()
    
    elif menu == 9:
        print("\n-----Controle Financeiro-----\n")   
        #não iniciada
    
    elif menu == 10:
        print("\n-----Exportar Relatórios-----\n")
        #não iniciada

    else:
        print("ERRO: Operação Inválida")
    
    continuar = exibir_submenuHome() #-> Menu de Continuidade
    continue