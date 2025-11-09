from database.DB_connect import DBConnect

from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrdersbyStore(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from orders o where o.store_id=%s"""

        cursor.execute(query, (store.store_id,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o1.order_id AS id1, o2.order_id AS id2, 
                   ((SUM(oi.quantity) + SUM(oi2.quantity)) / DATEDIFF(o2.order_date, o1.order_date)) AS weight
                    FROM 
                        orders o1, orders o2, order_items oi, order_items oi2
                    WHERE 
                        o1.store_id = %s
                        AND o1.store_id = o2.store_id
                        AND oi.order_id = o1.order_id
                        AND oi2.order_id = o2.order_id
                        AND o1.order_date < o2.order_date
                        AND DATEDIFF(o2.order_date, o1.order_date) <= %s
                    GROUP BY 
                        o1.order_id, o2.order_id
                """

        cursor.execute(query, (store.store_id,k))

        for row in cursor:
            results.append((idMap[row["id1"]],idMap[row["id2"]], row["weight"]))

        cursor.close()
        conn.close()
        return results