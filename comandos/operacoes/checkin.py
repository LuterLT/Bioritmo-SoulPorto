import mysql.connector
import datetime

from interfaces.funcontinuar import exibir_submenu
from banco_dados import abrir_conexao
from interfaces.interface import exibir_users, exibir_checkin


def checkin():
    continuar = 1
    while True:
        if continuar == 2:
            break
        elif continuar == 0:
            continuar = exibir_submenu("'Fazer check-in'")
        
        print("\n-----Check-in-----\n")

        print("\n[1] - Fazer check-in",
              "\n[2] - Listar últimos check-In")
        try:
            opt_checkin = int(input("\nEscolha uma das operações do check-in acima: \n"))
        except ValueError:
            print("ERRO: Digite apenas números inteiros!")
            continuar = exibir_submenu("'Fazer Check-In'")
            continue

        if opt_checkin == 1: # opção que realiza o check-in
            exibir_users()

            try: # pega o id do aluno para realizar o check-in
                id_user = int(input("\nQual id do aluno a fazer check-in?\n"))
            except ValueError:
                print("ERRO: Digite apenas números inteiros!")
                continuar = exibir_submenu("'Fazer check-in'")
                continue
            
            conexao = None
            try:
                conexao = abrir_conexao()
                cursor = conexao.cursor()

                # buscar as aulas disponíveis do aluno informado
                cursor.execute(
                    "SELECT aulas_disp FROM aluno WHERE id = %s AND ativo = 1", (id_user,)
                )
                resultado = cursor.fetchone()

                # verificar se o aluno foi encontrado
                if resultado is None:
                    print(f"\nERRO: Aluno com ID {id_user} não encontrado ou inativo.")
                    continuar = exibir_submenu("'Fazer check-in'")
                    continue

                aulas_disp = resultado[0]

                # verificar se o aluno tem 'aulas_disp'
                if resultado[0] > 0:
                    horario_atual = datetime.datetime.now().strftime("%y/%m/%d - %H:%M:%S")

                    # inserir o registro na tabela 'checkin'
                    cursor.execute(
                        "INSERT INTO checkin (id_aluno, horario) VALUES (%s, %s)",
                        (id_user, horario_atual),
                    )

                    # diminuir as 'aulas_disp' do aluno em -1
                    cursor.execute(
                        "UPDATE aluno SET aulas_disp = aulas_disp - 1 WHERE id = %s",
                        (id_user,),
                    )

                    # confirmar as alterações no banco de dados
                    conexao.commit()
                    print(
                        f"\nCheck-in de realizado com sucesso em {horario_atual}!"
                    )
                    print(f"Aulas restantes para o aluno: {aulas_disp - 1}")

                    continuar = exibir_submenu("'Fazer check-in'")
                    continue

                else:
                    # se o valor for igual a 0, retornar um aviso de erro
                    print(
                        "\nERRO: O aluno não possui aulas disponíveis para realizar o check-in!"
                    )

            except mysql.connector.Error as erro:
                # se algo der errado nas queries, desfaz as alterações não salvas
                if conexao:
                    conexao.rollback()
                print(f"\nERRO: Ocorreu um erro ao realizar o check-in no banco: {erro}")

            finally:
                # garante o fechamento das conexões após operação finalizar
                if conexao and conexao.is_connected():
                    cursor.close()
                    conexao.close()
        
        elif opt_checkin == 2: # opção que lista os check-in
            try:
                limite = int(input("\nListar quantos check-in?\n"))
            except ValueError:
                print("ERRO: Digite apenas números inteiros!")
                continuar = exibir_submenu("'fazer check-in'")
                continue
            if limite <= 0:
                print("Valor inválido, valor mínimo: '1'")
                continuar = exibir_submenu("'fazer check-in'")
                continue
            # exibe uma lista dos últimos check-ins, se limitando a quantidade que usuario delimitou
            exibir_checkin(limite)
            continuar = exibir_submenu("'fazer check-in'")
            continue

        else: # opção invalida
            print("ERRO: Digite apenas opções válidas!")
            continuar = exibir_submenu("'fazer check-in'")
            continue


