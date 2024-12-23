import pandas as pd
import psycopg2 as pg

from config import *
def partnersImport(tableName: str, database):
    # Заполнение
    print("excel\\" + tableName + ".xlsx")
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')
    print(df)
    query = "INSERT INTO partners VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cursor = database.cursor()
    for stroka in df.itertuples():
        print(stroka)
        print(stroka._1)
        partnerType = stroka._1
        partnerName = stroka._2
        partnerDirector = stroka.Директор
        partnerMail = stroka._4
        partnerPhone = stroka._5
        partnerAddress = stroka._6
        partnerINN = stroka.ИНН
        partnerRate = stroka.Рейтинг

        values = (partnerType,
                  partnerName,
                  partnerDirector,
                  partnerMail,
                  partnerPhone,
                  partnerAddress,
                  partnerINN,
                  partnerRate)

        cursor.execute(query, values)

    cursor.close()

    database.commit()

def productTypeImport(tableName: str, database):
    # Заполнение
    query = "INSERT INTO productType VALUES (%s, %s)"
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        productTypeName = r._1
        productIndex = r._2

        values = (productTypeName,
                  productIndex,)

        cursor.execute(query, values)

    cursor.close()
    database.commit()

def productsImport(tableName: str, database):
    # Заполнение
    query = "INSERT INTO products VALUES (%s, %s, %s, %s)"
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        productTypeNameFk = r._1
        productName = r._2
        productArticle = r.Артикул
        productMinCost = r._4

        values = (productTypeNameFk,
                  productName,
                  productArticle,
                  productMinCost)

        cursor.execute(query, values)

    cursor.close()
    database.commit()


def partnerProductsImport(tableName: str, database):
    # Заполнение
    query = "INSERT INTO history VALUES (%s, %s, %s, %s)"
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        productNameFk = r.Продукция
        partnerNameFk = r._2
        historyProductsCount = r._3
        historySaleDate = r._4

        values = (productNameFk,
                  partnerNameFk,
                  historyProductsCount,
                  historySaleDate)

        cursor.execute(query, values)

    cursor.close()
    database.commit()

def materialTypeImport(tableName: str, database):
    # Заполнение
    query = "INSERT INTO materialType VALUES (%s, %s)"
    df = pd.read_excel("../excel/" + tableName, engine='openpyxl')    # cursor = database.cursor()
    cursor = database.cursor()
    for r in df.itertuples():
        print(r)
        materialTypeName = r._1
        materialBreakPercent = r._2

        values = (materialTypeName,
                  materialBreakPercent)

        cursor.execute(query, values)

    cursor.close()
    database.commit()


def insertTable():
    # Вызов всех файлов для импорта
    database = pg.connect(database=dbName,
                          user=user,
                          password=password,
                          host=host,
                          port=port)

    partnersImport("Partners_import.xlsx", database)
    productTypeImport("Product_type_import.xlsx", database)
    productsImport("Products_import.xlsx", database)
    partnerProductsImport("Partner_products_import.xlsx", database)
    materialTypeImport("Material_type_import.xlsx", database)

# Вызов работы функции
insertTable()