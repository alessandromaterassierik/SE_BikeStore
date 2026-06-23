from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def load_categories():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.category_name  from category c """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def load_products(cat, start, end):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """with prod as (select p.id, p.product_name as name, count(*) as tot
                    from product p 
                    join category c on c.id = p.category_id 
                    join order_item oi on oi.product_id = p.id 
                    join `order` o on o.id = oi.order_id 
                    where category_name = %s and
                    o.order_date  between %s and %s
                    group by p.id)
                    
                    select distinct p1.id as id1, p2.id as id2, p1.tot as tot1, p2.tot as tot2, p1.name as name1, p2.name as name2 
                    from prod p1, prod p2
                    where p1.id > p2.id 
                    group by p1.id, p2.id"""

        cursor.execute(query,(cat, start,end,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
