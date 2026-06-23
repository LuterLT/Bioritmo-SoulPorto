#importar as operações aqui
import mysql.connector
from banco_dados import iniciar_db, abrir_conexao
from interface import exibir_menu


#iniciar o programa
iniciar_db()

while True:
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
        menu = int(input("\nDigite o comando: "))
    except ValueError:
        print("ERROR: Digite apenas números inteiros!")
        continue

    if menu == 0:
        print(f"Caixa Atual: {caixa:.2f}\nEncerrando o Sistema...")
        break

    elif menu == 1:
        print("\n-----Check In-----\n")
    
    elif menu == 2:
        print("\n-----Cadastros/Alterações Cadastrais-----\n")
    
    elif menu == 3:
        print("\n-----Vendas-----\n")

    elif menu == 4:
        print("\n-----Repor Estoque-----\n")
    
    elif menu == 5:
        print("\n-----Consulta-----\n")
    
    elif menu == 6:
        print("\n-----Controle Financeiro-----\n")   
    
    elif menu == 7:
        print("\n-----Exportar Relatórios-----\n")

    else:
        print("ERRO: Operação Inválida")


    # esse bloco de código faz sentido para nosso caso? - Davi
    # sei lá kkkkkkkkkkkkk acho que não na vdd, pq vai ter os submenus né - Madu
    # sim, pensei o mesmo, mas depois das funções nos submenus finalizarem, o usuario vai voltar para o - Davi
    # main.py, que vai levar pro fim do código, onde da a opção de fechar o sistema ou não. faz sentido? - Davi
    # acho que é melhor ele ir saindo até chegar no menu principal - Madu
    # não faz sentido perguntar ao invés de simplesmente ir direto pro menu, pq sair é uma opção do menu - Madu
    # entendi sua lógica, mas ao dar 'return' nos submenus até chegar no menu principal, ele não vai recomeçar o loop while - Davi
    # ele vai continuar da mesma linha, então o sistema não vai dar a opção dele escolher o '0' pra sair do sistema, ele vai continuar o código  - Davi
    # linha por linha, até recomeçar o loop... calma acho que dá pra não usar sim kkkkk - Davi
    # pq no submenu vamos dar a opção de voltar ao menu, e mesmo que ele não recomece o while, ele vai até o final e depois recomeça - Davi
    # tá certo, não precisamos não - Davi
    # kkkkkkkkkkkk concordo que não precisa, fiquei meio confusa mas fé - Madu
    # em minha defesa, estava pensando no codigo do prof, que "não tem" submenus ksks - Davi
    # no main finalizou então não? - Davi
    # acredito que sim hein - Madu
    # testa ai o código então ;-; - Davi
    # tenho que criar outro negocinho lá no mysql né? - Madu
    # pior que vai, pq ele vai ler o iniciar_banco de todo modo - Davi
    # antes muda a senha pra qual vc usa, não esquece isso - Davi
    # deixei a nossa senha pasrão mesmo... minha dúvida é, meu sistema do petshop tá lá no servidor local - Madu
    # aí vai criar outro database no mesmo coisinho, né? - Madu
    # na mesma conexao vc diz? eu acho que não - se vc tiver com a conexao aberta sim, vai criar na mesma conexao, se vc abrir
    # outra conexao, com nome "projeto final uaua" acho que vai abrir nessa segunda - ACHO - Davi
    # mas aí não tem que mudar na hora da conexão aqui? - Madu
    # não, pq aqui usamos o login "root", se vc criar a conexao com o user root, que vem por padrão, não precisa mudar aqui - Davi
    # é mais questão de qual das duas conexoes vc está aberta agr, se não me engano
    # basicamente, o root aq no vscode vai abrir o banco que tiver aberto no momento no workbench? slk mt tecnologia - Madu
    # isso isso, até onde me lembro é isso - Davi
    # testa pra ver se vai desse modo - Davi
    # agora? - Madu
    # se vc estiver disposta, ou manda o código zipado que eu testo - Davi
    # tome-lhe o zip no grupo - Madu
    # vou encerrar a conexão do live share, blz? - Host(Madu)

    
    