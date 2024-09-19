# A PARTE DO GPT FOI RETIRADA POR CONTA DA LICENÇA QUE EXPIROU
# POR CONTA DE ERROS AO SUBIR O BD PARA O GIT A CRIAÇÃO DO BANDO DE DADOS DEVE SER MANUAL
# o banco de dados utilizado deve ter o nome de SGD

import mysql.connector

class Database:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

    def connect(self):
        return mysql.connector.connect(**self.config)

class Usuario:
    def __init__(self, nome, email, senha, departamento):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.departamento = departamento

    def adicionar(self, db):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (nome, email, senha, departamento) VALUES (%s, %s, %s, %s)
        """, (self.nome, self.email, self.senha, self.departamento))
        conn.commit()
        cursor.close()
        conn.close()
        print("Usuário adicionado com sucesso!")

    @staticmethod
    def login(db, email, senha):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT departamento FROM Usuarios WHERE email = %s AND senha = %s
        """, (email, senha))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

class ExercicioDissertativo:
    def __init__(self, tipo_exercicio, descricao, resposta):
        self.tipo_exercicio = tipo_exercicio
        self.descricao = descricao
        self.resposta = resposta

    def adicionar(self, db):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exercicio_dissertativo (tipo_exercicio, descricao, resposta) VALUES (%s, %s, %s)
        """, (self.tipo_exercicio, self.descricao, self.resposta))
        conn.commit()
        cursor.close()
        conn.close()
        print("Exercício dissertativo adicionado com sucesso!")

class ExercicioObjetivo:
    def __init__(self, tipo_exercicio, descricao, resposta, numero_questao):
        self.tipo_exercicio = tipo_exercicio
        self.descricao = descricao
        self.resposta = resposta
        self.numero_questao = numero_questao

    def adicionar(self, db):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Exercicio_objetivo (tipo_exercicio, descricao, resposta, numero_questao) VALUES (%s, %s, %s, %s)
        """, (self.tipo_exercicio, self.descricao, self.resposta, self.numero_questao))
        conn.commit()
        cursor.close()
        conn.close()
        print("Exercício objetivo adicionado com sucesso!")

class ResolverExercicio:
    def __init__(self, db):
        self.db = db

    def resolver_dissertativo(self, id_exercicio, resposta):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Exercicio_dissertativo SET resposta = %s WHERE id = %s
        """, (resposta, id_exercicio))
        conn.commit()
        cursor.close()
        conn.close()
        print("Resposta do exercício dissertativo enviada com sucesso!")

    def resolver_objetivo(self, id_exercicio, resposta):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Exercicio_objetivo SET resposta = %s WHERE id = %s
        """, (resposta, id_exercicio))
        conn.commit()
        cursor.close()
        conn.close()
        print("Resposta do exercício objetivo enviada com sucesso!")

class GerenciadorExercicios:
    def __init__(self, db):
        self.db = db

    def listar_exercicios_dissertativos(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exercicio_dissertativo")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def listar_exercicios_objetivos(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exercicio_objetivo")
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    def listar_exercicio_por_id(self, id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                ed.id AS id_dissertativo, 
                ed.tipo_exercicio AS tipo_dissertativo, 
                ed.descricao AS descricao_dissertativo, 
                ed.resposta AS resposta_dissertativa, 
                eo.id AS id_objetivo, 
                eo.tipo_exercicio AS tipo_objetivo, 
                eo.descricao AS descricao_objetivo, 
                eo.resposta AS resposta_objetiva
            FROM 
                Exercicio_dissertativo ed
            LEFT JOIN 
                Exercicio_objetivo eo ON eo.numero_questao = ed.id
            WHERE 
                ed.id = %s
        """, (id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

def main():
    db = Database('root', 'root', 'localhost', 'sgd')

    gerenciador = GerenciadorExercicios(db)
    resolver = ResolverExercicio(db)

    while True:
        print("\nMenu Inicial")
        print("1. Entrar")
        print("2. Cadastrar")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            # Login do usuário
            email = input("Email: ")
            senha = input("Senha: ")
            departamento = Usuario.login(db, email, senha)

            if departamento:
                departamento = departamento[0]
                print(f"Bem-vindo! Você é do departamento: {departamento}")
                
                while True:
                    print("\nGerenciador de Exercícios")
                    if departamento == "Funcionário":
                        print("1. Adicionar Usuário")
                        print("2. Adicionar Exercício Dissertativo")
                        print("3. Adicionar Exercício Objetivo")
                    print("4. Listar Exercícios Dissertativos")
                    print("5. Listar Exercícios Objetivos")
                    print("6. Listar Exercício por ID")
                    print("7. Resolver Exercício")
                    print("0. Sair")
                    
                    opcao_gestao = input("Escolha uma opção: ")
                    
                    if opcao_gestao == '1':
                        if departamento == "Funcionário":
                            nome = input("Nome: ")
                            email = input("Email: ")
                            senha = input("Senha: ")
                            departamento_usuario = input("Departamento: ")
                            usuario = Usuario(nome, email, senha, departamento_usuario)
                            usuario.adicionar(db)
                        else:
                            print("Apenas funcionários podem adicionar usuários.")
                    
                    elif opcao_gestao == '2':
                        if departamento == "Funcionário":
                            tipo_exercicio = input("Tipo de Exercício: ")
                            descricao = input("Descrição: ")
                            resposta = input("Resposta: ")
                            exercicio = ExercicioDissertativo(tipo_exercicio, descricao, resposta)
                            exercicio.adicionar(db)
                        else:
                            print("Apenas funcionários podem adicionar exercícios dissertativos.")
                    
                    elif opcao_gestao == '3':
                        if departamento == "Funcionário":
                            tipo_exercicio = input("Tipo de Exercício: ")
                            descricao = input("Descrição: ")
                            resposta = input("Resposta (A/B/C/D): ")
                            numero_questao = int(input("Número da Questão (ID do dissertativo): "))
                            exercicio = ExercicioObjetivo(tipo_exercicio, descricao, resposta, numero_questao)
                            exercicio.adicionar(db)
                        else:
                            print("Apenas funcionários podem adicionar exercícios objetivos.")
                    
                    elif opcao_gestao == '4':
                        exercicios = gerenciador.listar_exercicios_dissertativos()
                        for ex in exercicios:
                            print(ex)
                    
                    elif opcao_gestao == '5':
                        exercicios = gerenciador.listar_exercicios_objetivos()
                        for ex in exercicios:
                            print(ex)

                    elif opcao_gestao == '6':
                        id = int(input("Digite o ID do exercício dissertativo: "))
                        exercicios = gerenciador.listar_exercicio_por_id(id)
                        for ex in exercicios:
                            print(ex)

                    elif opcao_gestao == '7':
                        tipo_exercicio = input("Qual tipo de exercício você quer resolver? (dissertativo/objetivo): ").lower()
                        if tipo_exercicio == "dissertativo":
                            id_exercicio = int(input("Digite o ID do exercício dissertativo: "))
                            resposta = input("Digite sua resposta: ")
                            resolver.resolver_dissertativo(id_exercicio, resposta)
                        elif tipo_exercicio == "objetivo":
                            id_exercicio = int(input("Digite o ID do exercício objetivo: "))
                            resposta = input("Digite sua resposta (A/B/C/D): ")
                            resolver.resolver_objetivo(id_exercicio, resposta)
                        else:
                            print("Tipo de exercício inválido.")

                    elif opcao_gestao == '0':
                        print("Saindo...")
                        break
                    
                    else:
                        print("Opção inválida! Tente novamente.")

            else:
                print("Email ou senha incorretos. Tente novamente.")

        elif opcao == '2':
            # Cadastrar um novo usuário
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            departamento_usuario = input("Departamento: ")
            usuario = Usuario(nome, email, senha, departamento_usuario)
            usuario.adicionar(db)

        elif opcao == '3':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
