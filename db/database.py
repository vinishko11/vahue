import psycopg2

from db import config

from CheckInputData import start_check

# Класс для работы с базой данных PostgreSQL
class Database():
    def __init__(self):
        # Инициализация подключения к БД при создании объекта
        self.connection_uri = self.connect_to_db()

    def connect_to_db(self):
        """Установка соединения с базой данных"""
        try:
            connection = psycopg2.connect(host = config.host,
                                          user = config.user,
                                          password = config.password,
                                          database = config.db_name,
                                          port = config.port)
            print('База данных -> Подключена')
            return connection
        except Exception as error:
            print(error)
            return None

    def take_all_partners_info(self):
        # Получение информации о всех партнерах из БД
        try:
            query = '''
            SELECT *
            FROM partners;
            '''
            cursor = self.connection_uri.cursor()
            cursor.execute(query)

            partners_data = []
            for return_row in cursor.fetchall():
                partners_data.append(
                    {
                        'type': return_row[0].strip(),
                        'name': return_row[1].strip(),
                        'dir': return_row[2].strip(),
                        'mail': return_row[3].strip(),
                        'phone': return_row[4].strip(),
                        'addr': return_row[5].strip(),
                        'inn': return_row[6].strip(),
                        'rate': return_row[7]
                    }
                )
            return partners_data
        except Exception as error:
            print(error)
            return []

    def take_count_of_sales(self, partner_name: str):
        # Подсчет общего количества продаж для конкретного партнера
        try:
            query = f'''
            SELECT SUM(history_products_count)
            FROM history
            WHERE partner_name_fk = '{partner_name}';
            '''
            cursor = self.connection_uri.cursor()
            cursor.execute(query)
            count = cursor.fetchone()
            cursor.close()
            if count:
                return count[0]
            return None
        except Exception as error:
            print(error)
            return None

    def take_partner_info(self, partner_name: str):
        # Получение информации о конкретном партнере из БД
        try:
            query = f'''
            SELECT *
            FROM partners
            WHERE partner_name = '{partner_name}';
            '''
            cursor = self.connection_uri.cursor()
            cursor.execute(query)
            partners_data = dict()
            for data in cursor.fetchall():
                partners_data = {
                    'type': data[0].strip(),
                    'name': data[1].strip(),
                    'dir': data[2].strip(),
                    'mail': data[3].strip(),
                    'phone': data[4].strip(),
                    'addr': data[5].strip(),
                    'inn': data[6].strip(),
                    'rate': data[7]
                }
            cursor.close()
            return partners_data
        except Exception as error:
            print(f':: {error}')
            return dict()

    def update_partner(self, partner_data: dict, partner_name: str):
        try:
            if not start_check(partner_data):
                return False

            query = f'''
            UPDATE partners
            SET 
            partner_type = '{partner_data['type']}', 
            partner_name = '{partner_data['name']}', 
            partner_director = '{partner_data['dir']}', 
            partner_mail = '{partner_data['mail']}', 
            partner_phone = '{partner_data['phone']}', 
            partner_address = '{partner_data['addr']}', 
            partner_inn = '{partner_data['inn']}', 
            partner_rate = '{partner_data['rate']}'
            
            WHERE partner_name = '{partner_name}';
            '''

            cursor = self.connection_uri.cursor()
            cursor.execute(query)
            self.connection_uri.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'::^ {error}')
            return False

    def add_new_partner(self, partner_data: dict):
        try:
            if not start_check(partner_data):
                return False

            query = f'''
                INSERT INTO partners
                VALUES (
                '{partner_data['type']}', 
                '{partner_data['name']}', 
                '{partner_data['dir']}', 
                '{partner_data['mail']}', 
                '{partner_data['phone']}', 
                '{partner_data['addr']}', 
                '{partner_data['inn']}', 
                '{partner_data['rate']}');
                '''

            cursor = self.connection_uri.cursor()
            cursor.execute(query)
            self.connection_uri.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f'::^ {error}')
            return False