from database.DB_connect import DBConnect
from model.edge import Edge
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
    def getAllNodes(store_id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders o 
                    where o.store_id  = %s"""

        cursor.execute(query,(store_id,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store_id, k,idMapO):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.order_id as oid1, t2.order_id as oid2, sum(t1.quantity+t2.quantity)/DATEDIFF(t2.order_date, t1.order_date) as weight
                    from (select o.order_id, o.order_date,oi.quantity
                    from orders o, order_items oi
                    where o.store_id  = %s and o.order_id = oi.order_id) as t1,
                    (select o.order_id, o.order_date,oi.quantity 
                    from orders o, order_items oi
                    where o.store_id  = %s and o.order_id = oi.order_id) as t2
                    where t1.order_id != t2.order_id and t1.order_date < t2.order_date and DATEDIFF(t2.order_date, t1.order_date)<=%s
                    group by t1.order_id,t2.order_id 
                    order by weight desc"""

        cursor.execute(query,(store_id,store_id,k))

        for row in cursor:
            o1 = idMapO[row["oid1"]]
            o2 = idMapO[row["oid2"]]
            results.append(Edge(o1,o2,row["weight"]))

        cursor.close()
        conn.close()
        return results