import mysql.connector
from banco_dados import abrir_conexao
from interface import exibir_planos, exibir_users, exibir_prod
from comandos.submenu import exibir_submenu 

id_aluno = int(input("Digite o id do aluno: "))
conexao = abrir_conexao()
cursor = conexao.cursor()
cursor.execute("""
    SELECT * 
    FROM aluno 
    WHERE id = %s
""", (id_aluno,))
resultado = cursor.fetchone()
if resultado is None:
    print("\nERRO: O ID Digitado não é equivalente a nenhum cadastrado no Banco de Dados!")
    continuar = exibir_submenu("Alterando Cadastro dos Alunos")
    #continue

print(f"Você Selecionou o aluno: '{resultado[1]}' | email: {resultado[2]} | peso: {resultado[3]:.2f} | altura: {resultado[4]:2f}")

#pedir para o usuário digitar os campos
print("\nPreencha os campos abaixo e APENAS aperte ENTER para aqueles que não deseja alterar")
novo_nome= input("Digite o seu nome completo: ").strip() or resultado[1]
novo_email= input("Digite o seu email: ").strip() or resultado[2]
novo_peso_str= input("Digite o seu peso: ") or resultado[3]
nova_altura_str= input("Digite a sua altura: ") or resultado[4]


try:
    novo_peso = float(novo_peso_str) if novo_peso_str else resultado[3]
except ValueError:
    print("\nERRO: O Peso Deve ser um números, alteração cancelada")
try:
    nova_altura = float(nova_altura_str) if nova_altura_str else resultado[4]
except ValueError:
    print("\nERRO: A Altura Deve ser em números, alteração cancelada")

cursor.execute("""
                UPDATE aluno
                SET
                    nome = %s,
                    email = %s,
                    peso = %s,
                    altura = %s 
                WHERE id = %s
            """, (novo_nome, novo_email, novo_peso, nova_altura, id_aluno))
conexao.commit()


#========COLAR AQUI ABAIXO
# cursor.execute("SELECT nome, autor, ano, categoria FROM livros WHERE id = %s", (id_produto,))
#     livro = cursor.fetchone()

#     if not livro:
#         print("ERRO: Livro não encontrado")
#         return
#     print(f"\nEditando livro: {livro[0]} ({livro[2]}) | Autor: {livro[1]} | Genero: {livro[3]}")
#     print("(Se não quiser alterar algum elemento, deixe em branco e aperte enter)")

#     novo_nome = input(f"Alterar nome do livro [{livro[0]}]  para: ").strip() or livro[0]
#     novo_autor = input(f"Alterar nome do autor [{livro[1]}] para: ").strip() or livro[1]
#     novo_genero = input(f"Alterar genero de [{livro[3]}] para: ").strip() or livro[3]

#     novo_ano_str = input(f"Alterar ano de publicação [{livro[2]}] para: ").strip()

#     try:
#         novo_ano = int(novo_ano_str) if novo_ano_str else livro[2]
#     except ValueError:
#         print("ERRO: O ANO PRECISA SER NUMERICO, alteração cancelada")
#         return

#     cursor.execute("""
#     UPDATE livros
#     SET nome = %s, autor = %s, ano = %s, genero = %s
#     WHERE id = %s
#     """, (novo_nome, novo_autor, novo_ano, novo_genero, id_produto))