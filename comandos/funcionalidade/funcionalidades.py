import mysql.connector
import re

from banco_dados import abrir_conexao
from interfaces.interface import exibir_users
from interfaces.funcontinuar import exibir_submenu

#DEF responsavel pela consulta do imc dos alunos
def consulta_imc():
    """
    Calcula o IMC do usuário.
    """
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Consultar IMC")
            continue
        try:
            conexao = abrir_conexao()
            cursor = conexao.cursor()

            print("\n========= ALUNOS CADASTRADOS =========")
            exibir_users()
            print("\n0 - Continuar sem aluno cadastrado")
            try:
                #Input para inserir o ID do aluno ou pressionar 0 para seguir sem cadastro
                id_aluno = int(input("\nDigite o ID do aluno ou 0 para continuar sem cadastro: "))
            except ValueError:#Segurança caso valor inválido
                print("\nERRO: Digite apenas números inteiros.")
                continuar = 0
                continue

            if id_aluno == 0: #calcular IMC de aluno sem cadastro
                while True:
                    if continuar == 2:
                        break
                    elif continuar == 0:
                        continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                        continue
                    try:
                        peso = float(input("Digite o peso do aluno (kg): ").strip().replace(",", ".")) #converte a vírgula "," em ponto "." para que o código não dê erro
                    except ValueError: #Usuário envia dados não aceitaveis 
                        print("\nERRO: Digite apenas números para o cálculo de IMC")
                        continuar = 0
                        continue

                    #Limitações de peso dos alunos
                    if peso <= 0:
                        print("\nERRO: O peso deve ser maior que zero!")
                        continuar = 0
                        continue
                    if peso > 700:
                        print("\nERRO: O peso não pode ser maior que 700kg")
                        continuar = 0
                        continue

                    try:
                        altura = float(input("Digite a altura do aluno (m): ").strip().replace(",", "."))
                    except ValueError: #Segurança de codigo caso o usuário insira um dado não aceitavel
                        print("\nERRO: Digite apenas números para o cálculo de IMC")
                        continuar = 0
                        continue

                    # verificação altura para que não seja possível dados negativos
                    if altura <= 0:
                        print("\nERRO: A altura deve ser maior que zero")
                        continuar = 0
                        continue
                    #verificação de altura para que não seja maior que 3 metros de altura! 
                    if altura > 3:
                        print("\nERRO: A altura não pode ser maior que 3 metros.")
                        continuar = 0
                        continue
                    break
 
            else: #caso o ID seja diferente de 0
                #busca as informações do aluno no bd para ser apresentado no terminal
                cursor.execute(""" 
                    SELECT nome, peso, altura
                    FROM aluno
                    WHERE id = %s
                    AND ativo = 1
                """, (id_aluno,))

                aluno = cursor.fetchone()
                #caso a pesquisa não corresponda a um resultado do bd
                if not aluno:
                    print("\nERRO: Aluno não encontrado.")
                    continuar = 0
                    continue
                
                nome = aluno[0]
                #if caso o aluno selecionado tenha optado por não inserir peso e altura
                if not aluno[1] or not aluno[2]:
                    print(
                        f"\nAluno selecionado: {nome}."
                        "\nPeso e/ou altura não cadastrados."
                        "\nInforme os dados para continuar o cálculo"
                    )
                    #inserir o peso e altura
                    while True:
                        if continuar == 2:
                            break
                        elif continuar == 0:
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue
                        try:
                            peso = float(input("\nDigite o peso (kg): ").strip().replace(",", "."))#Evitar erro de código por uso de vírgula ","
                        except ValueError: #Segurança caso insira input inválido
                            print("\nERRO: Digite apenas números.")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue

                        if peso <= 0: #evitar valores negativos
                            print("\nERRO: O peso deve ser maior que zero")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue
                        if peso > 700: #Evitar valores superiores a 700Kg
                            print("\nERRO: O peso não pode ser maior que 700 kg.")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue

                        try:
                            altura = float(input("Digite a altura (m): ").strip().replace(",", "."))#Segurança caso utilize vírgula ","
                        except ValueError:#s
                            print("\nERRO: Digite apenas números.")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue

                        if altura <= 0:#Evitar valores negativos
                            print("\nERRO: A altura deve ser maior que zero")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue

                        if altura > 3:#Evitar altura maior que 3 metros
                            print("\nERRO: A altura não pode ser maior que 3 metros.")
                            continuar = exibir_submenu("Digitar Peso e Altura do Aluno")
                            continue
                        break


                else:#Caso o cadastro do aluno ja possua peso e altura
                    peso = float(aluno[1])
                    altura = float(aluno[2])
                    print(f"\nAluno selecionado: {nome}")

        except mysql.connector.Error as erro:
            print(f"\nArquivo-funcionalidade Linha-170\nERRO: Falha no Banco de Dados, {erro}")
            continue
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

        # cálculo IMC
        imc = (peso / (altura ** 2))

        # classificação/resultado
        if imc < 18.5:
            classificacao = "Abaixo do peso"
            dica = (
                "Procure manter uma alimentação equilibrada e, se possível, "
                "consulte um nutricionista para avaliar suas necessidades."
            )

        elif imc < 25:
            classificacao = "Peso normal"
            dica = (
                "Parabéns! Continue mantendo hábitos saudáveis, "
                "alimentação equilibrada e prática regular de exercícios."
            )

        elif imc < 30:
            classificacao = "Sobrepeso"
            dica = (
                "Considere aumentar a prática de atividades físicas e "
                "adotar uma alimentação mais equilibrada."
            )

        elif imc < 35:
            classificacao = "Obesidade Grau I"
            dica = (
                "É recomendável buscar orientação médica e nutricional "
                "para reduzir riscos à saúde."
            )

        elif imc < 40:
            classificacao = "Obesidade Grau II"
            dica = (
                "Procure acompanhamento profissional para desenvolver "
                "um plano seguro de perda de peso."
            )

        else:
            classificacao = "Obesidade Grau III"
            dica = (
                "É importante procurar orientação médica especializada "
                "para avaliação e acompanhamento."
            )

        print("\n======= RESULTADO =======") #devolve o resultado de IMC para o usuário
        print(f"Peso: {peso:.2f} kg")
        print(f"Altura: {altura:.2f} m")
        print(f"IMC: {imc:.2f}")
        print(f"Classificação: {classificacao}")

        print("\nDica:")
        print(dica)

        while True:#Sugerir uma nova consulta
            opcao = input("\nDeseja realizar uma nova consulta? (1 - Sim / 2 - Não): ").strip().lower()

            if opcao == "1":
                break

            elif opcao == "2":
                print("\nRetornando ao menu...")
                return

            else:
                print("ERRO: Digite apenas 1 ou 2")


def validar_email(email):#def responsável pela validação de email (Verifica o formato do email) 
    '''
    Essa função vai receber o email digitar e vai verificar se ela segue o mesmo padrão do regex
    '''
    padrao = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(padrao, email):
        return email
    else:
        return ""