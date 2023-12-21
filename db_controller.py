import os
import json
import sqlite3

class database_controller():
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(current_dir, 'commissions.db')
        self.con = sqlite3.connect(database_path)

    def readCommissionList(self, user_id, country_id, language_id):
        self.readCommissionData(user_id)
        try:
            sql_query = """
                SELECT
                    cl.commission_id,
                    cl.commission_name,
                    cl.description,
                    c.frequency AS commission_frequency,
                    uc.occurrence AS commission_occurrence,
                    uc.blocked AS commission_blocked
                FROM
                    commissions_languages AS cl
                    LEFT JOIN commissions c ON cl.commission_id = c.id
                    LEFT JOIN users_commissions uc ON cl.commission_id = uc.commission_id AND uc.user_id = ?
                WHERE
                    cl.commission_id IN (SELECT id FROM commissions WHERE country = ?)
                    AND cl.language_id = ?;
            """
            cursor = self.con.execute(sql_query, (user_id, country_id, language_id,))
            rows = cursor.fetchall()

            if rows:
                return '\n'.join([f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{bool(row[5])}" for row in rows])
            else:
                return "Nenhuma comissão encontrada"  # Chama novamente para obter os dados recém-gerados
        except Exception as e:
            return f"Erro ao ler dados de comissões do banco de dados: {e}"

    # def readCommissionList(self, country_id, language_id):
    #     try:
    #         sql_query = """
    #             SELECT c.id, cl.commission_name, c.frequency, c.blocked, cl.description
    #             FROM commissions AS c
    #             LEFT JOIN (SELECT * FROM commissions_languages WHERE language_id = ?) AS cl ON c.id = cl.commission_id
    #             WHERE c.country = ?
    #         """
    #         cursor = self.con.execute(sql_query, (language_id, country_id,))
    #         rows = cursor.fetchall()

    #         if rows:
    #             return '\t'.join([f"{row[0]}: {row[1]}, {row[2]}, {bool(row[3])}, {row[4]}" for row in rows])
    #         else:
    #             return "Nenhuma comissão encontrada"  # Chama novamente para obter os dados recém-gerados
    #     except Exception as e:
    #         return f"Erro ao ler dados de comissões do banco de dados: {e}"
    
    def readCommissionData(self, user_id):
        try:
            # Obtém a lista de IDs das comissões do usuário
            user_commission_ids = [row[0] for row in self.con.execute('SELECT commission_id FROM users_commissions WHERE user_id = ?', (user_id,)).fetchall()]

            # Obtém a lista de IDs de todas as comissões
            all_commission_ids = [row[0] for row in self.con.execute('SELECT id FROM commissions').fetchall()]

            # Identifica os IDs ausentes
            missing_commission_ids = set(all_commission_ids) - set(user_commission_ids)

            # Preenche os registros ausentes
            if missing_commission_ids:
                self.fillMissingCommissions(user_id, missing_commission_ids)

            return True
        except Exception as e:
            self.log_error(f"Erro ao ler dados de comissões do banco de dados: {e}")
            return False

        
    def fillMissingCommissions(self, user_id, missing_commission_ids):
        try:
            default_values = (0, 0)  # comm_id, repetitions, blocked

            # Insere os registros ausentes na tabela users_commissions
            for commission_id in missing_commission_ids:
                self.con.execute('INSERT INTO users_commissions (user_id, commission_id, occurrence, blocked) VALUES (?, ?, ?, ?)', (user_id, commission_id, *default_values))

            self.con.commit()
        except Exception as e:
            self.log_error(f"Erro ao preencher comissões ausentes para o jogador: {e}")
    
    def resetCommissionData(self, user_id):
        try:
            with self.con:
                self.con.execute('DELETE FROM users_commissions WHERE user_id = ?', (user_id,))
                self.generateCommissionData(user_id)
            return True
        except Exception as e:
            self.log_error(f"Erro ao resetar dados de comissões do jogador: {e}")
            return False

    def generateCommissionData(self, user_id):
        try:
            total_commissions = self.con.execute('SELECT COUNT(id) FROM commissions').fetchone()[0]
            default_values = (0, 0)

            with self.con:
                for i in range(1, total_commissions + 1):
                    self.con.execute('INSERT INTO users_commissions (user_id, commission_id, occurrence, blocked) VALUES (?, ?, ?, ?)', (user_id, i, *default_values))

            return True
        except Exception as e:
            self.log_error(f"Erro ao gerar dados de comissões para o jogador: {e}")
            return False


# # Define a função corretamente
# def readUserData(user_id):
#     # Obtém o diretório do arquivo main.py
#     current_dir = os.path.dirname(os.path.abspath(__file__))

#     # Constrói o caminho para o arquivo data.json dentro do diretório 'db'
#     data_path = os.path.join(current_dir, 'db', 'data.json')

#     while True:
#         try:
#             with open(data_path, 'r') as file:
#                 data = json.load(file)

#                 # Converte o ID do usuário para string, pois os IDs no JSON são strings
#                 user_id_str = str(user_id)

#                 # Verifica se o ID do usuário está no JSON
#                 if user_id_str in data:
#                     # Obtém o valor associado ao ID do usuário
#                     user_data = data[user_id_str]
#                     return (f"Valor associado ao ID {user_id_str}: {user_data}")
#                 else:
#                     generateUserData(data_path, user_id_str)
#                     continue
#         except FileNotFoundError:
#             return (f"Arquivo data.json não encontrado em {data_path}")
#         except Exception as e:
#             return (f"Erro ao ler o arquivo data.json: {e}")

# def generateUserData(data_path, user_id_str):
#     data = {}
#     default_values = {
#         0: 1,
#         1: 0
#     }

#     for i in range(1, 230):
#         data[i] = {k: int(v) for k, v in default_values.items()}

#     formatted_json_str = json.dumps(data, separators=(',', ':'), indent=None)

#     # If you want to save it to a file, uncomment the following lines
#     with open(data_path, 'a') as json_file:
#         json_file.write(formatted_json_str)
