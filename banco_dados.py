import mysql.connector

def abrir_conexao():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="soul_code",
        database="bioritmo"
    )
    return conexao

def iniciar_db():
    try:
        conexao = abrir_conexao()
        cursor = conexao.cursor()

        #prodservi = Tabela de Produtos e Serviços
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prodserv(
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                categoria VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                qtde INT NOT NULL,
                ativo INT DEFAULT 1
            )
        """)
        #tabela que contém os planos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planos(
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                qtde_aulas INT NOT NULL,
                ativo INT DEFAULT 1
            )
        """)
        #tabela que contém os alunos
        #atributo aulas_disp = quantidade de aulas disponíveis para o aluno realizar
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aluno(
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                peso DECIMAL(10, 2),
                altura DECIMAL(10, 2),
                aulas_disp INT NOT NULL,
                ativo INT DEFAULT 1,
                id_plano INT NOT NULL,
                FOREIGN KEY (id_plano) REFERENCES planos (id)
            )
        """)
        #histórico de vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas(
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_prodserv INT NOT NULL,
                horario DATETIME NOT NULL,
                qtde INT NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (id_prodserv) REFERENCES prodserv (id)
            )
        """)
        #Tabela de Checkin do Usuário Dentro da Academia
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkin(
                id INT PRIMARY KEY AUTO_INCREMENT,
                id_aluno INT NOT NULL,
                horario DATETIME NOT NULL,
                FOREIGN KEY (id_aluno) REFERENCES aluno (id)
            )
        """)

        #criação dos valores padrão
        cursor.execute("SELECT COUNT(*) FROM prodserv")
        if cursor.fetchone()[0] == 0: #verificar se não tem nem UMA linha na tabela prodserv
            prodserv_iniciais = [
                ("Aula Avulsa", "Serviços", 50, 1),
                ("Água Proteica", "Bebidas", 12.99, 50),
                ("Barrinha de Cereal", "Alimentos", 15.75, 40),
                ("Lacinho para Cabelo", "Equipamentos", 3.50, 30),
                
                ("Lipoaspiração", "Serviços", 200, 1)
            ]

            cursor.executemany("""
                INSERT INTO prodserv (nome, categoria, preco, qtde)
                VALUES (%s, %s, %s, %s)
            """, prodserv_iniciais)
            conexao.commit()

        cursor.execute("SELECT COUNT(*) FROM planos")
        if cursor.fetchone()[0] == 0:
            planos_iniciais = [
                ("Experimental", 0, 1),
                ("Bronze", 49.99, 5),
                ("Prata", 84.99, 10),
                ("Ouro", 99.99, 15),
                ("Diamante", 114.99, 20)
            ]
            cursor.executemany("""
                INSERT INTO planos (nome, preco, qtde_aulas)
                VALUES (%s, %s, %s)
            """, planos_iniciais)

        cursor.execute("SELECT COUNT(*) FROM aluno")
        if cursor.fetchone()[0] == 0: #verificar se não tem nem UMA linha na tabela aluno
            alunos_iniciais = [
                ("Davi Hiluany", "davi.hiluany@gmail.com", 78.15, 1.75, 1, 1),
                ("Gabriella Iglesias", "gabriella.iglesias@gmail.com", 67.00, 1.68, 1, 1),
                ("Madu Zinevicius", "madu.zinevicius@gmail.com", 59.87, 1.65, 1, 1),
                ("João Pedro de França", "joao.defranca@gmail.com", 69.67, 1.69, 1, 1),
                ("Lucas Imparato", "lucas.imparato@gmail.com", 75.78, 1.71, 1, 1),
            ]

            cursor.executemany("""
                INSERT INTO aluno (nome, email, peso, altura, aulas_disp, id_plano)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, alunos_iniciais)
        conexao.commit()


    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO (banco_dados): {erro}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
