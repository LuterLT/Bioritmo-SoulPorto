from comandos.consultas import consulta_geral, consulta_alunos, consulta_produtos, consulta_planos
from comandos.cadastro import cad_aluno, cad_produtos, cad_planos
from comandos.alterarCad import alt_cad_aluno, alt_cad_produtos, alt_cad_plano 
from comandos.estoque import repor_est, repor_est_lote, red_est
from comandos.financeiro import exibir_nf, promocao_produto, promocao_plano, alt_preco_prodserv, alt_preco_plano
from comandos.atv_inat import aluno_atv_inat, prodserv__atv_inat, plano_atv_inat
from comandos.exportar import export_vendas_geral, export_vendas_qtde, export_chekin_geral, export_checkin_qtde
from interfaces.funcontinuar import exibir_submenu
from interfaces.interface import exibir_users, exibir_prod, exibir_planos

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
                    print("\n1 - Cadastro de Alunos\n2 - Cadastro de Produtos/Serviços\n3 - Cadastro de Planos\n0 - Voltar")
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
                    print("\n- Cadastro de Produtos / Serviços -\n")
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
                    print("\n- Alterar Cadastro de Produtos/Serviços -\n")
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
            print("\n1 - Repor Estoque de 1 item\n2 - Repor Estoque em Lote\n3 - Reduzir Estoque\n0 - Voltar")
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
            continuar = 1
            while True:
                if continuar == 2:
                    break
                elif continuar == 0:
                    continuar = exibir_submenu("'Repor Estoque em Lote'")
                    continue
                try:
                    qtde_rep = int(input("\nQual a quantidade recebida para CADA produto do lote? "))
                except:
                    print("\nERRO: A quantidade deve ser um número inteiro!")
                    continuar = 0
                    continue
                if qtde_rep <= 0:
                    print("ERRO: A quantidade deve ser um número maior que 0!")
                    continuar = 0
                    continue
                print("\nProdutos Disponíveis:\n")
                exibir_prod()
                entrada_ids = input("\nDigite os [IDs] dos produtos separados por vírgula: ")
                try:
                    lista_ids = [int(numero.strip()) for numero in entrada_ids.split(',')]
                except:
                    print("\nERRO: Os [IDs] devem ser em números inteiros!")
                    continuar = 0
                    continue
                repor_est_lote(qtde_rep, *lista_ids)
                continuar = 0
                continue
        elif comando == 3:
            print("\n- Reduzir Estoque -\n")
            red_est()
        else:
            print("ERRO: Operação Inválida")
            continue

        

def submenu_consulta(): #===============================================EXIBE SUBMENU DE ESTOQUE===
    ''' 
    Essa def mostra as opções que o usuário terá para fazer uma buscar
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'escolher consulta'")

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
            continuar = exibir_submenu("'escolhendo tipo de consulta'")

def submenu_listar():
    ''' 
    Essa def mostra as opções que o usuário terá para serem listadas
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'escolher listagem'")

        print("Qual tipo de listagem desejado?\n",
            " [1] - Listagem geral\n",
            " [2] - Listagem de alunos\n",
            " [3] - Listagem de produtos/serviços\n",
            " [4] - Listagem de planos\n",
            " [0] - Sair de listagem\n",)
        
        try:
            listar = int(input("\nListagem desejada: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            return

        if listar == 0:
            return
        elif listar == 1:
            print("\nListagem geral\n")
            exibir_users()
            exibir_prod()
            exibir_planos()
        elif listar == 2:
            exibir_users()
        elif listar == 3:
            exibir_prod()
        elif listar == 4:
            exibir_planos()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = exibir_submenu("'escolher tipo de listagem'")


def submenu_atv_inat():
    '''
    Essa def mostrará os tipos de cadastro (alunos, prods/serv e planos) para ativar/desativar
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'ativar/desativar cadastro'")
        
        print("Qual cadastro deseja ativar/desativar?\n",
            " [1] - Aluno\n",
            " [2] - Produtos / Serviços\n",
            " [3] - Planos\n",
            " [0] - Sair do submenu\n"
        )

        try:
            listar = int(input("\nCadastro a ser ativado/desativado: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            input("Aperte ENTER para Continuar")
            continue

        if listar == 0:
            return
        elif listar == 1:
            pass
            aluno_atv_inat()
        elif listar == 2:
            pass
            prodserv__atv_inat()
        elif listar == 3:
            pass
            plano_atv_inat()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = exibir_submenu("'Ativar/desativar Cadastro'")


def submenu_exportar():
    '''
    Essa def mostra o submenu com as opções de export
    '''
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'exportar relatório'")

        print(" ----- Lista de Comandos ----- \n",
            "Qual relatório desejado?\n",
            " [1] - Vendas - Geral\n",
            " [2] - Vendas - Quantidade Específica\n",
            " [3] - Check-in - Geral\n",
            " [4] - Check-in - Quantidade Específica\n",
            " [0] - Sair de 'Exportar Relatório'\n",
            " ----------------------------- \n"
        )

        try:
            opc = int(input("Relatório a ser exportado: "))
        except ValueError:
            print("\nERRO: O ID deve ser preenchido apenas com números inteiros")
            input("Aperte ENTER para Continuar")
            continue

        if opc == 0:
            return
        elif opc == 1:
            export_vendas_geral()
        elif opc == 2:
            export_vendas_qtde()
        elif opc == 3:
            export_chekin_geral()
        elif opc == 4:
            export_checkin_qtde()
        else:
            print("Opção inválida, selecione uma opção válida")
            continuar = exibir_submenu("'exportar relatório'")


def submenu_financ():
    '''
    Essa def mostra as opções do submenu de finanças, como NF e painel BI, além de permitir a alteração de preço
    de produtos, serviços e planos
    '''
    while True:
        try:
            print("\n1 - Alteração de Preços\n2 - Aplicar Promoções\n3 - Exibir Nota Fiscal\n4 - Painel B.I\n0 - Voltar")
            comando = int(input("\nQual opção deseja acessar? "))
        except ValueError:
            print("ERRO: Digite apenas números inteiros!")
            continue
        
        if comando == 0: #====================ENCERRA O SUBMENU=======================
            break
        elif comando == 1: #====================ALTERAR PREÇO=======================
            try:
                print("\n1 - Alterar Preço de Produto/Serviço\n2 - Alterar Preço de Plano\n0 - Voltar")
                subcomando = int(input("\nQual opção deseja acessar? "))
            except ValueError:
                print("ERRO: Digite apenas números inteiros!")
                continue

            if subcomando == 0: #==================== opção de voltar
                continue
            elif subcomando == 1: #================= alterar preço de produtos e serviços
                alt_preco_prodserv()
            elif subcomando == 2: #================= alterar preço de planos
                alt_preco_plano()
            else: #==================== nenhuma opção do menu
                print("ERRO: Opção Inválida")
                continue

        elif comando == 2:  # ==================== APLICAR PROMOÇÕES ====================
            try:
                print("\n1 - Aplicar Promoção em Produtos/Serviços")
                print("2 - Aplicar Promoção em Planos")
                print("0 - Voltar")
                subcomando = int(input("\nQual opção deseja acessar? "))
            except ValueError:
                print("ERRO: Digite apenas números inteiros!")
                continue

            if subcomando == 0:
                continue

            elif subcomando == 1:   # Produtos e Serviços

                print("\n--- Aplicar Promoção em Produtos/Serviços ---")
                promocao_produto()

            elif subcomando == 2:   # Planos
                print("\n--- Aplicar Promoção em Planos ---")
                promocao_plano()

            else:
                print("ERRO: Opção inválida!")
            
        elif comando == 3: #====================EXIBIR NOTA FISCAL=======================
            exibir_nf()
            
        elif comando == 4: #====================EXIBIR PAINEL BI=======================
            painel_bi()
        else:
            print("ERRO: Operação Inválida")
            break
