import psycopg2 as pg
from db import config

material_id_dict = dict()
product_id_dict = dict()

def function(product_type_id, material_type_id, result_count, w:float, h:float):
    try:
        break_material = material_id_dict[material_type_id]
        coefficient_product = product_id_dict[product_type_id]
        if result_count <= 0:
            return -1
        elif w <= 0:
            return -1
        elif h <= 0:
            return -1
    except Exception:
        return -1

    print(type(break_material), type(coefficient_product))
    print(break_material, coefficient_product)

    params_mult = w * h

    need_material_count = params_mult * coefficient_product

    break_count = need_material_count * break_material

    need_material_count += break_count

    all_materials_count = need_material_count * result_count
    return int(all_materials_count)

def get_all_materials_id(connect):
    query = """
    select *
    from material_type
    """

    cursor = connect.cursor()
    cursor.execute(query)

    materials = []
    for el in cursor.fetchall():
        materials.append([el[0].strip(), el[1].strip()])

    return materials

def get_all_products_id(connect):
    query = """
    select *
    from product_type
    """

    cursor = connect.cursor()
    cursor.execute(query)

    products = []
    for el in cursor.fetchall():
        print("el:", el)
        products.append([el[0].strip(), str(el[1])])

    return products

def main():
    connect = pg.connect(
        host = config.host,
        user = config.user,
        password = config.password,
        database = config.db_name
    )

    products = get_all_products_id(connect)
    materials = get_all_materials_id(connect)

    for el in products:
        print("ID: '" + "\t'Коэффициент продукции: ".join(el))
        product_id_dict[el[0]] = float(el[1])
    print("Введите требуемый id продукции:")
    p_id = input("~: ")


    for el in materials:
        print("ID: '"+"' %Брака: ".join(el))
        material_id_dict[el[0]] = float(el[1][:-1])

    print("Введите требуемый id материала:")
    m_id = input("~: ")


    print("Введите требуемое количество продукции")
    try:
        count = int(input("~: "))
    except Exception:
        count = -1

    print("Введите требуемое Ширину и Высоту продукции")
    try:
        w = float(input("Параметр продукции 1: "))
        h = float(input("Параметр продукции 2: "))
    except Exception:
        w, h = -1, -1

    print(function(p_id, m_id, count, w, h))

main()
