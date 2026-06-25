def exibir_submenu(texto): #===========================================MENU CONTINUIDADE
    '''
    Função vai exibir o menu de confirmação se o usuário deseja continuar ou voltar. Ela recebe um texto para ser exibido na opção 1.
    Retorna 0 caso algo tenha dado de errado na digitação.
    
    Importante: antes do While, a variavel que vai receber esse resultado deve ser inicilizar com 1 e deve ter comandos Ifs para tratar o resultado retornado.
    '''
    print("\n------------ Continuar? --------------")
    print(f"[1] - Continuar na Opção {texto}")
    print("[2] - Voltar")
    try:
        comando = int(input("Digite um dos numeros acima: "))
    except ValueError:
        print("\n! ERRO: Tipo de Dado Inserido Inválido !\nRetornando...")
        return 0
    if comando == 1:
        return 1
    elif comando == 2:
        print("\nVoltando...") 
        return 2
    else:
        print("\n! ERRO: Comando Inexistente !\nRetornando...")
        return 0

def exibir_submenuHome(): #===========================================MENU CONTINUIDADE INICIO
    '''
    Função vai exibir o menu de confirmação se o usuário deseja voltar ao Início ou finalizar o programa.
    Retorna 0 caso algo tenha dado de errado na digitação.
    
    Importante: antes do While, a variavel que vai receber esse resultado deve ser inicilizar com 1 e deve ter comandos Ifs para tratar o resultado retornado.
    '''
    print("------------Deseja Voltar ao Início ?--------------")
    print(f"[1] - Voltar ao Início")
    print("[2] - Finalizar Programa")
    try:
        comando = int(input("Digite um dos numeros acima: "))
    except ValueError:
        print("\n! ERRO: Tipo de Dado Inserido Inválido !\nRetornando...")
        return 0
    if comando == 1:
        print("\nVoltando ao Inicio...")
        return 1
    elif comando == 2:
        # print("\nVoltando ao Inicio...") 
        return 2
    else:
        print("\n! ERRO: Comando Inexistente !\nRetornando...")
        return 0       