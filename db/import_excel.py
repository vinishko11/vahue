import pandas as pd
import psycopg2 as pg
from db import config

def partners_import(tableName: str, connect):
    # Импорт данных о партнерах из Excel файла в БД
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')

    query = "INSERT INTO partners VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cursor = connect.cursor()

    for r in df.itertuples():
        partner_type = r._1
        partner_name = r._2
        partner_director = r.Директор
        partner_mail = r._4
        partner_phone = r._5
        partner_address = r._6
        partner_inn = r.ИНН
        partner_rate = r.Рейтинг

        values = (partner_type,
                  partner_name,
                  partner_director,
                  partner_mail,
                  partner_phone,
                  partner_address,
                  partner_inn,
                  partner_rate)

        cursor.execute(query, values)

    cursor.close()
    connect.commit()

def product_type_import(tableName: str, connect):
    # Импорт типов продуктов из Excel файла в БД
    query = "INSERT INTO product_type VALUES (%s, %s)"

    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')

    cursor = connect.cursor()

    for r in df.itertuples():
        product_type_name = r._1
        product_index = r._2

        values = (product_type_name,
                  product_index)

        cursor.execute(query, values)

    cursor.close()
    connect.commit()

def products_import(tableName: str, connect):
    # Импорт данных о продуктах из Excel файла в БД
    query = "INSERT INTO products VALUES (%s, %s, %s, %s)"

    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')

    cursor = connect.cursor()

    for r in df.itertuples():
        product_type_name_fk = r._1
        product_name = r._2
        product_article = r.Артикул
        product_min_cost = r._4

        values = (product_type_name_fk,
                  product_name,
                  product_article,
                  product_min_cost)

        cursor.execute(query, values)

    cursor.close()
    connect.commit()


def partner_products_import(tableName: str, connect):
    # Импорт истории продаж партнеров из Excel файла в БД
    query = "INSERT INTO history VALUES (%s, %s, %s, %s)"

    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')

    cursor = connect.cursor()

    for r in df.itertuples():
        product_name_fk = r.Продукция
        partner_name_fk = r._2
        history_products_count = r._3
        history_sale_date = r._4

        values = (product_name_fk,
                  partner_name_fk,
                  history_products_count,
                  history_sale_date)

        cursor.execute(query, values)

    cursor.close()
    connect.commit()

def material_type_import(tableName: str, connect):
    # Импорт типов материалов из Excel файла в БД
    query = "INSERT INTO material_type VALUES (%s, %s)"

    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')

    cursor = connect.cursor()

    for r in df.itertuples():
        material_type_name = r._1
        material_break_percent = r._2

        values = (material_type_name,
                  material_break_percent)

        cursor.execute(query, values)

    cursor.close()
    connect.commit()


def insert_table():
    # Основная функция импорта - подключается к БД и 
    # последовательно импортирует данные из всех Excel файлов
    connect = pg.connect(host = config.host,
                            user = config.user,
                            password = config.password,
                            database = config.db_name,
                            port = config.port)

    partners_import("Partners_import.xlsx", connect)
    product_type_import("Product_type_import.xlsx", connect)
    products_import("Products_import.xlsx", connect)
    partner_products_import("Partner_products_import.xlsx", connect)
    material_type_import("Material_type_import.xlsx", connect)

insert_table()