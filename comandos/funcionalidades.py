import re

def consulta_imc():
    """
    Calcula o IMC do usuário.
    """
    while True:

        #peso
        while True:
            try:
                peso = float(
                    input("Digite seu peso (kg): ").strip().replace(",", ".")
                )

                if peso <=0:
                    print("\nERRO: o peso deve ser maior que zero!")
                    continue
                break

            except ValueError:
                print("\nERRO: Digite apenas número para o cálculo de IMC")

        #altura
        while True:
            try:
                altura = float(
                    input("Digite sua altura(m): ").strip().replace(",", ".")
                )

                if altura <= 0:
                    print("\nERRO: A altura deve ser maior que zero")
                    continue

                break
            
            except ValueError:
                print("\nERRO: Digiste apenas números para o cálculo de IMC")

        #cálculo
        imc = peso / (altura ** 2)

        #classificação/resultado
        if imc < 18.5:
            classificacao = "Abaixo do peso"
            dica = ("Procure manter uma alimentação equilibrada e, se possível, consulte um nutricionista para avaliar suas necessidades.")

        elif imc < 25:
            classificacao = "Peso normal"
            dica = ("Parabéns! Continue mantendo hábitos saudáveis, alimentação equilibrada e prática regular de exercícios.")

        elif imc < 30:
            classificacao = "Sobrepeso"
            dica = ("Considere aumentar a prática de atividade físicas e adotar uma alimentação mais equilibrada.")

        elif imc < 35:
            classificacao = "Obesidade Grau I"
            dica = ("É recomendável buscar orientação médica e nutricional para reduzir riscos à saúde.")

        elif imc < 40:
            classificacao = "Obesidade Grau II"
            dica = ("Procure acompanhamento profissional para desenvolver um plano seguro de perda de peso.")

        else:
            classificacao = "Obesidade Grau III"
            dica = ("É importante procurar orientação médica especializada para avaliação e acompanhamento.")

        print("\n=======RESULTADO=======")
        print(f"Peso: {peso:.2f} kg")
        print(f"Altura: {altura:.2f} m")
        print(f"IMC: {imc:.2f}")
        print(f"Classificação: {classificacao}")

        print("\n Dica:")
        print(dica)

        while True:
            opcao = input(
                "\n Deseja realizar uma nova consulta? (s/n)"
            ).strip().lower()

            if opcao == "s":
                print()
                break

            elif opcao == "n":
                print("\nRetornando ao menu...")
                return

            else:
                print("ERRO: Digite apenas s ou n.")


def validar_email(email):
    
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(padrao, email):
        return email
    else:
        return ""