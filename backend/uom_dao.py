def get_uoms(connection):
    with connection.cursor() as cursor:
        query = "SELECT uom_id, uom_name FROM gs.uom"
        cursor.execute(query)
        result = cursor.fetchall()
        return [{
            "uom_id": uom_id, 
            "uom_name": uom_name} 
            for uom_id, uom_name in result]

if __name__ == "__main__":
    from sql_connection import get_sql_connection

    connection = get_sql_connection()
    uoms = get_uoms(connection)
    print(uoms)
    connection.close()




# def get_uoms(connection):
#     with connection.cursor() as cursor:
#         query = "SELECT uom_id, uom_name FROM gs.uom"
#         cursor.execute(query)
#         result = cursor.fetchall()
#         response = []
#         for (uom_id, uom_name) in result:
#             response.append({
#                 "uom_id": uom_id,
#                 "uom_name": uom_name
#             })
#         return response

# if __name__ == "__main__":
#     from sql_connection import get_sql_connection

#     connection = get_sql_connection()
#     uoms = get_uoms(connection)
#     #print(get_all_products(connection))
#     print(get_uoms(connection))



