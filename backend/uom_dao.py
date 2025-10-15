class UOMDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_all_uoms(self):
        with self.connection.cursor() as cursor:
            query = "SELECT uom_id, uom_name FROM gs.uom"
            cursor.execute(query)
            result = cursor.fetchall()
            return [
                {"uom_id": uom_id, "uom_name": uom_name}
                for uom_id, uom_name in result
            ]

# Optional test block
if __name__ == "__main__":
    from sql_connection import get_sql_connection

    connection = get_sql_connection()
    dao = UOMDAO(connection)
    uoms = dao.get_all_uoms()
    print(uoms)
    connection.close()





#--------------------------------
# def get_uoms(connection):
#     with connection.cursor() as cursor:
#         query = "SELECT uom_id, uom_name FROM gs.uom"
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return [{
#             "uom_id": uom_id, 
#             "uom_name": uom_name} 
#             for uom_id, uom_name in result]

# if __name__ == "__main__":
#     from sql_connection import get_sql_connection

#     connection = get_sql_connection()
#     uoms = get_uoms(connection)
#     print(uoms)
#     connection.close()




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



