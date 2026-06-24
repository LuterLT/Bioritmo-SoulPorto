from comandos.consultas import consulta_geral, consulta_alunos, consulta_produtos, consulta_planos
from comandos.cadastro import cad_aluno, cad_produtos, cad_planos, alt_cad_aluno, alt_cad_produtos, alt_cad_plano 
from comandos.estoque import repor_est, repor_est_lote


def submenu_cad(): #===============================================EXIBE SUBMENU DE CADASTRO===
    ''' 
    Essa def mostra as opções que o usuário terá para cadastrar ou alterar cadastro
    '''

    while True:
        try:
            print("\n1 - Realizar Novo Cadastro\n2 - Alterar Cadastro Existente\n0 - Voltar")
            comando = int(input("\nQual opção deseja acessar? "))
        except ValueError:
            print("ERRO: Digite apenas números inteiros!")
            continue
            
        #bloco if/elif/else 
        if comando == 0:
            break
        elif comando == 1: #================== REALIZAR NOVO CADASTRO
            while True:
                try:
                    print("\n1 - Cadastro de Alunos\n2 - Cadastro de Produtos\n3 - Cadastro de Planos\n0 - Voltar")
                    subcomando  = int(input("\nQual tipo de cadastro deseja realizar? "))
                except ValueError:
                    print("ERRO: Digite apenas números inteiros!")
                    continue
                if subcomando == 0:
                    break  
                elif subcomando == 1:
                    print("\n- Cadastro de Alunos -\n")
                    cad_aluno()
                elif subcomando == 2:
                    print("\n- Cadastro de Produtos -\n")
                    cad_produtos()
                elif subcomando == 3:
                    print("\n- Cadastro de Planos -\n")
                    cad_planos()
                else:
                    print("ERRO: Operação Inválida")
                    continue
              
        elif comando == 2: #================== ATUALIZAR CADASTRO 
            while True:
                try:
                    print("\n1 - Atualizar Cadastro de Alunos\n2 - Atualizar Cadastro de Produtos\n3 - Atualizar Cadastro de Planos\n0 - Voltar")
                    subcomando  = int(input("\nQual tipo de cadastro deseja atualizar? "))
                except ValueError:
                    print("ERRO: Digite apenas números inteiros!")
                    continue
                if subcomando == 0:
                    break
                elif subcomando == 1:
                    print("\n- Alterar Cadastro de Alunos -\n")
                    alt_cad_aluno()
                elif subcomando == 2:
                    print("\n- Alterar Cadastro de Produtos -\n")
                    alt_cad_produtos()
                elif subcomando == 3:
                    print("\n- Alterar Cadastro de Planos -\n")
                    alt_cad_plano()
        else:
            print("ERRO: Operação Inválida")
            continue


def submenu_est(): #===============================================EXIBE SUBMENU DE ESTOQUE===
    ''' 
    Essa def mostra as opções que o usuário terá para repor estoque (itens individuais ou em lote)
    '''
    
    while True:
        try:
            print("\n1 - Repor Estoque de 1 item\n2 - Repor Estoque em Lote\n0 - Voltar")
            comando = int(input("\nQual opção deseja acessar? "))
        except ValueError:
            print("ERRO: Digite apenas números inteiros!")
            continue

        if comando == 0:
            break
        elif comando == 1:
            print("\n- Repor Estoque de 1 item -\n")
            repor_est()
        elif comando == 2:
            print("\n- Repor Estoque em Lote -\n")
            repor_est_lote()
        else:
            print("ERRO: Operação Inválida")
            continue

        

def submenu_consulta(): #===============================================EXIBE SUBMENU DE ESTOQUE===
    ''' 
    Essa def mostra as opções que o usuário terá para repor estoque (itens individuais ou)
    '''
    print("Qual tipo de consulta desejado?\n",
          " [1] - Consulta geral\n",
          " [2] - Consulta de alunos\n",
          " [3] - Consulta de produtos/serviços\n",
          " [4] - Consulta de planos\n",
          " [0] - Sair de consultas\n",)
    
    try:
        consulta = int(input("Consulta desejada: "))
    except ValueError:
        print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
        return

    if consulta == 0:
        return
    elif consulta == 1:
        consulta_geral()
    elif consulta == 2:
        consulta_alunos()
    elif consulta == 3:
        consulta_produtos()
    elif consulta == 4:
        consulta_planos()
    else:
        print("Opção inválida, selecione uma opção válida")
