import psycopg2

import checkInputInfo
from db import config
from partner import Partner


class Database():
    def __init__(self):
        self.connection = self.connectDatabase()

    def connectDatabase(self):
        try:
            connection = psycopg2.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.dbName
            )
            print("Соединение с базой данных установлено")
            return connection
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def takePartnerInfo(self):
        if not self.connection:
            return "Нет соединения с базой данных"
        try:
            cursor = self.connection.cursor()
            query = '''
            SELECT partnertype, partnername, partnerdirector, partnermail, partnerphone, partneraddress, partnerinn, partnerrate
            FROM partners
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                return "Данные отсутствуют"

            partners = [
                {
                    "type": row[0],
                    "name": row[1],
                    "director": row[2],
                    "email": row[3],
                    "phone": row[4],
                    "urAddr": row[5],
                    "inn": row[6],
                    "rate": row[7]
                }
                for row in rows
            ]
            return partners
        except Exception as e:
            print(f"Ошибка выполнения запроса takePartnerInfo: {e}")
            return "Ошибка получения данных"

    def saleSum(self, partnername: str):
        if not self.connection:
            return "Нет соединения с базой данных"
        try:
            cursor = self.connection.cursor()
            query = '''
            SELECT SUM(historyproductscount)
            FROM history
            WHERE partnernamefk = %s
            '''
            cursor.execute(query, (partnername,))
            result = cursor.fetchone()
            cursor.close()

            if result is None or result[0] is None:
                return {"procent": 0}

            return {"procent": result[0]}
        except Exception as e:
            print(f"Ошибка выполнения запроса saleSum: {e}")
            return "Ошибка получения данных"

    # добавление нового партнера в базу данных
    def addPartner(self, infoFromUser: dict):
        if not self.connection:
            return "Нет соединения с базой данных"
        try:
            if not checkInputInfo.checkInputInfo(infoFromUser):
                return False
            try:
                cursor = self.connection.cursor()
                query = '''
                INSERT INTO partners (partnertype, partnername, partnerdirector, partnermail, partnerphone, partneraddress, partnerinn, partnerrate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (infoFromUser["type"], infoFromUser["name"], infoFromUser["director"], infoFromUser["mail"], infoFromUser["phone"], infoFromUser["address"], infoFromUser["inn"], infoFromUser["rate"]))
                self.connection.commit()
                cursor.close()
                return True
            except Exception as e:
                print(f"Ошибка выполнения запроса addPartner: {e}")
                return False
        except Exception as e:
            print(f"Ошибка выполнения запроса addPartner: {e}")
            return False

    def getPartnerByName(self, partnername: str):
        if not self.connection:
            print("Нет соединения с базой данных.")
            return None
        try:
            # Инструмент для работы с запросами
            cursor = self.connection.cursor()

            # Запрос
            query = '''
                SELECT partnertype, partnername, partnerdirector, partnermail,
                       partnerphone, partneraddress, partnerinn, partnerrate 
                FROM partners
                WHERE partnername = %s;
                '''

            # Исполнение запроса
            cursor.execute(query, (partnername,))

            # Перебор выходных кортежей функцией python
            row = cursor.fetchone()

            # Отключение инструмента
            cursor.close()

            # Возврат информации про партнера
            if row:
                return {
                    "type": row[0],
                    "name": row[1],
                    "director": row[2],
                    "mail": row[3],
                    "phone": row[4],
                    "address": row[5],
                    "inn": str(row[6]),
                    "rate": str(row[7])
                }
            else:
                print(f"Партнер с именем '{partnername}' не найден.")
                return None
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def updatePartner(self, latestPartnerInfo: dict):
        if not self.connection:
            return "Нет соединения с базой данных"
        try:
            if not checkInputInfo.checkInputInfo(latestPartnerInfo):
                return False
            cursor = self.connection.cursor()
            query = f'''
            UPDATE partners
            SET
            partnertype = '{latestPartnerInfo["type"]}',
            partnername = '{latestPartnerInfo["name"]}',
            partnerdirector = '{latestPartnerInfo["director"]}',
            partnermail = '{latestPartnerInfo["mail"]}',
            partnerphone = '{latestPartnerInfo["phone"]}',
            partneraddress = '{latestPartnerInfo["address"]}',
            partnerinn = '{latestPartnerInfo["inn"]}',
            partnerrate = {latestPartnerInfo["rate"]}
            WHERE partnername = '{Partner.getName()}';
            '''

            cursor.execute(query, (latestPartnerInfo["type"], latestPartnerInfo["name"], latestPartnerInfo["director"], latestPartnerInfo["mail"], latestPartnerInfo["phone"], latestPartnerInfo["address"], latestPartnerInfo["inn"], latestPartnerInfo["rate"]))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Ошибка выполнения запроса updatePartner: {e}")
            return False

    def getHistory(self, partnername: str):
        if not self.connection:
            print("Нет соединения с базой данных.")
            return []

        try:
            cursor = self.connection.cursor()

            # запрос
            query = """
                SELECT 
                    p.productname AS productname,
                    pr.partnername AS partnername,
                    h.historyproductscount AS quantity,
                    h.historysaledate AS saledate
                FROM 
                    history h
                JOIN 
                    products p ON h.productnamefk = p.productname
                JOIN 
                    partners pr ON h.partnernamefk = pr.partnername
                WHERE 
                    pr.partnername = %s;
            """

            cursor.execute(query, (partnername,))

            # словарь с результатом запроса
            history = [
                {
                    "productname": row[0].strip(),
                    "partnername": row[1].strip(),
                    "quantity": row[2],
                    "saleDate": row[3]
                }
                # перебор результатов запроса
                for row in cursor.fetchall()
            ]

            cursor.close()
            return history
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

#     def debug_getHistory(self, partnername: str):
#         if not self.connection:
#             print("Нет соединения с базой данных.")
#             return []
#
#         try:
#             cursor = self.connection.cursor()
#
#             # Печать SQL-запроса перед его выполнением
#             query = """
#                 SELECT
#                     p.productname AS productname,
#                     pr.partnername AS partnername,
#                     h.historyproductscount AS quantity,
#                     h.historysaledate AS saledate
#                 FROM
#                     history h
#                 JOIN
#                     products p ON h.productnamefk = p.productname
#                 JOIN
#                     partners pr ON h.partnernamefk = pr.partnername
#                 WHERE
#                     pr.partnername = %s;
#             """
#             print(f"Выполняемый запрос: {query} с партнером {partnername}")
#
#             cursor.execute(query, (partnername,))
#
#             # Получение и вывод результатов запроса
#             history = [
#                 {
#                     "productname": row[0].strip(),
#                     "partnername": row[1].strip(),
#                     "quantity": row[2],
#                     "saleDate": row[3]
#                 }
#                 for row in cursor.fetchall()
#             ]
#
#             print(f"Результаты запроса: {history}")
#
#             cursor.close()
#             return history
#         except Exception as e:
#             print(f"Ошибка выполнения запроса: {e}")
#             return []
#
# db = Database()
# history = db.debug_getHistory('Стройсервис')