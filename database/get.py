import aiosqlite

async def get_user(tg_id):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row
        cursor=await db.execute('''SELECT * FROM users WHERE tg_id = ?''',(tg_id,))
        user=await cursor.fetchone()

        if user is None:
            return None
        return dict(user)

async def get_orders(user_id):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row
        cursor=await db.execute('''SELECT orders.id,products.name,orders.amount,
        orders.price
         FROM orders
         JOIN products
         ON orders.product_id = products.id
         WHERE orders.user_id = ?
         ORDER BY orders.id DESC''',(user_id,))
        orders=await cursor.fetchall()
        return [dict(order) for order in orders]


async def get_more_than_two(tg_id):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''SELECT product_id,COUNT(*) as total
        FROM orders
        JOIN users
        ON orders.user_id = users.id
        WHERE users.id = ?
        GROUP BY product_id
        HAVING COUNT(*) > 2
        ORDER BY total DESC''',(tg_id,))
        users=await cursor.fetchall()
        return users
async def get_products():
    async with aiosqlite.connect("shopbot.db") as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM products "



        )

        products = await cursor.fetchall()

        return [dict(product) for product in products]

async def get_product_by_id(product_id):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row
        cursor=await db.execute('''SELECT * FROM products 
        WHERE id = ?''',(product_id,))
        product=await cursor.fetchone()
        if product is None:
            return None
        return dict(product)

async def get_product_by_name(name):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row
        cursor=await db.execute('''SELECT * FROM products 
        WHERE name = ?''',(name,))
        product=await cursor.fetchone()
        if product is None:
            return None
        return dict(product)




async def get_order(user_id):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row

        cursor=await db.execute('''SELECT * FROM orders 
        WHERE user_id = ?''',(user_id,))
        order=await cursor.fetchone()
        if order is None:
            return None
        return dict(order)



async def get_cart(user_id):
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row

        cursor=await db.execute('''SELECT 
         cart.id,
         cart.user_id,
         cart.product_id,
         cart.quantity,
         products.name,
         products.price,
         products.price * cart.quantity AS total
         FROM cart
         JOIN products ON cart.product_id=products.id
         WHERE cart.user_id = ?''',(user_id,))
        cart=await cursor.fetchall()
        if not cart:
            return None
        result = []
        for row in cart:
            result.append(dict(row))
        return result

async def get_statistics():
    async with aiosqlite.connect('shopbot.db') as db:
        db.row_factory=aiosqlite.Row
        cursor=await db.execute('''SELECT COUNT(users.id) AS users,
        COUNT(products.id) AS products,
        COUNT(orders.id) AS orders,
        SUM(orders.price*orders.amount) AS total,
        SUM(products.stock) AS stock,
        SUM(orders.amount) AS amount,
        AVG(orders.price*orders.amount) AS average
        FROM orders
        JOIN users
        ON orders.user_id = users.id
        JOIN products
        ON orders.product_id = products.id
        
        ''')
        statistics=await cursor.fetchone()
        result=dict(statistics)
        return result