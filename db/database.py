import psycopg2
from PySide6.scripts.deploy_lib import Config

from db import config

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
