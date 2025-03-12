import psycopg2 as pg
from db import config

def create_table(connect):
    # Запрос на создание таблиц в базе данных
    # Создаются таблицы: partners (партнеры), product_type (типы продуктов),
    # products (продукты), history (история продаж), material_type (типы материалов)
    query =f'''
        create table partners(
        partner_type nchar(10) not null,
        partner_name nchar(50) primary key not null,
        partner_director nchar(70) not null,
        partner_mail nchar(100) not null,
        partner_phone nchar(13) not null,
        partner_address nchar(200) not null,
        partner_inn nchar(10) not null,
        partner_rate int not null
        );
    
        create table product_type(
        product_type_name nchar(50) primary key not null,
        product_index real not null
        );
    
        create table products(
        product_type_name_fk nchar(50) not null,
        FOREIGN KEY (product_type_name_fk) REFERENCES product_type(product_type_name),
        product_name nchar(250) primary key not null,
        product_article bigint not null,
        product_min_cost real not null
        );
    
        create table history(
        product_name_fk nchar(250) not null,
        FOREIGN KEY (product_Name_fk) REFERENCES products (product_name),
        partner_name_fk nchar(50) not null,
        FOREIGN KEY (partner_name_fk) REFERENCES partners (partner_name),
        history_products_count bigint not null,
        history_sale_date date not null,
        primary key (product_name_fk, partner_name_fk)
        );
    
        create table material_type(
        material_type_name nchar(30) primary key not null,
        material_break_percent nchar(7) not null
        );
    '''

    # Выполнение запроса и закрытие соединения
    cur = connect.cursor()
    cur.execute(query)
    connect.commit()
    connect.close()

def start_create():
    # Установка соединения с базой данных PostgreSQL
    connect = pg.connect(
        host = config.host,
        user = config.user,
        password = config.password,
        database = config.db_name
    )
    create_table(connect)

start_create()