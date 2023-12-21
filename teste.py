# import sqlite3

# # Conectar ao banco de dados SQLite (será criado se não existir)
# conn = sqlite3.connect('commissions.db')

# # Criar uma tabela para armazenar os dados de comissões
# # conn.execute('''
# #     CREATE TABLE IF NOT EXISTS users_commissions (
# #         id INTEGER PRIMARY KEY,
# #         user_id VARCHAR(25),
# #         comm_id INTEGER,
# #         repetitions INTEGER CHECK (repetitions >= 0 AND repetitions <= 9),
# #         blocked INTEGER CHECK (blocked IN (0, 1))
# #     )
# # ''')

# def readCommissionData(user_id):
#     try:
#         cursor = conn.execute('SELECT * FROM users_commissions WHERE user_id = ?', (user_id,))
#         rows = cursor.fetchall()

#         if rows:
#             return '\n'.join([f"Comissão {row[0]} para o usuário {row[1]}: commission_id={row[2]}, occurrence={row[3]}, blocked={bool(row[4])}" for row in rows])
#         else:
#             generateCommissionData(user_id)
#             return readCommissionData(user_id)  # Chama novamente para obter os dados recém-gerados
#     except Exception as e:
#         return f"Erro ao ler dados de comissões do banco de dados: {e}"

# def generateCommissionData(user_id):
#     default_values = (0, 0)  # comm_id, repetitions, blocked

#     for i in range(1, 230):
#         conn.execute('INSERT INTO users_commissions (user_id, commission_id, occurrence, blocked) VALUES (?, ?, ?, ?)', (user_id, i, *default_values))
#         conn.commit()

# # Exemplo de uso
# user_id = 241297877966520320
# result = readCommissionData(user_id)
# print(result.encode('utf-8').decode('latin-1'))

# # Fechar a conexão quando não precisar mais
# conn.close()

# import sqlite3

# # Conecte-se ao banco de dados SQLite
# conn = sqlite3.connect('commissions.db')
# cursor = conn.cursor()

# # Execute a consulta SQL
# cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")

# # Obtenha os resultados
# tables = cursor.fetchall()

# # Imprima as tabelas e suas definições
# for table in tables:
#     print(f"Tabela: {table[0]}")
#     print(f"Definição: {table[1]}\n")

# # Feche a conexão
# conn.close()

# import csv
# import sqlite3

# # Conectar ao banco de dados SQLite
# conn = sqlite3.connect('commissions.db')
# cursor = conn.cursor()

# # Abrir o arquivo CSV
# with open('db\\comms_list-teste.csv', newline='', encoding='utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file)
    
#     # Pular o cabeçalho
#     # next(csv_reader, None)
    
#     for row in csv_reader:
#         # Inserir na tabela commissions
#         frequency = int(row[2])
#         country = int(row[3])
#         cursor.execute("INSERT INTO commissions (frequency, blocked, country) VALUES (?, 0, ?)", (frequency, country))
        
#         # Obter o ID da comissão recém-inserida
#         commission_id = cursor.lastrowid
        
#         # Inserir na tabela commissions_languages
#         commission_name = row[1]
#         cursor.execute("INSERT INTO commissions_languages (commission_id, language_id, commission_name, description) VALUES (?, 2, ?, '')", (commission_id, commission_name))

# # Commit e fechar a conexão
# conn.commit()
# conn.close()

# import sqlite3

# # Conectar ao banco de dados SQLite
# conn = sqlite3.connect('commissions.db')
# cursor = conn.cursor()

# # Definir a consulta SQL
# sql_query = """
#     SELECT c.id, cl.commission_name, c.frequency, c.blocked, "Sumeru" AS country, cl.description
#     FROM commissions AS c
#     LEFT JOIN (SELECT * FROM commissions_languages WHERE language_id = 2) AS cl ON c.id = cl.commission_id
#     WHERE c.country = 4
# """

# # Executar a consulta SQL
# cursor.execute(sql_query)

# # Obter os resultados
# results = cursor.fetchall()

# # Imprimir o cabeçalho
# header = [description[0] for description in cursor.description]
# print(header)

# # Imprimir os resultados
# for row in results:
#     print(row)

# # Fechar a conexão
# conn.close()


# from db_controller import database_controller

# controller = database_controller()

# print(controller.readCommissionData(241297877966520320).encode('utf-8').decode('latin-1'))

# import pandas as pd
# import sqlite3

# # Ler os dados do arquivo Excel, começando da célula B3
# excel_file = 'Genshin_Commissions_Cycle_tracking_Legacy.xlsx'
# sheet_name = 'Fontaine Cycle'
# df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None, skiprows=2)

# # Conectar ao banco de dados SQLite
# db_file = 'commissions.db'
# conn = sqlite3.connect(db_file)
# cursor = conn.cursor()

# # Iterar sobre as linhas do DataFrame e inserir os dados no banco de dados
# for index, row in df.iterrows():
#     if pd.isna(row[1]):
#         continue
#     commission_id = int(row[1]) if not pd.isna(row[1]) else None  # Índice da coluna "No."
#     commission_name = str(row[3]) if not pd.isna(row[3]) else None  # Índice da coluna "Nome em Português"
#     description = str(row[6]) if not pd.isna(row[6]) else ''  # Índice da coluna "Remark"

#     # Inserir dados na tabela commissions_languages
#     cursor.execute("""
#         INSERT INTO commissions_languages (commission_id, language_id, commission_name, description)
#         VALUES (?, 1, ?, ?)
#     """, (commission_id, commission_name, description))

# # Commit e fechar a conexão
# conn.commit()
# conn.close()

