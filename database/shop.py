
import aiosqlite





async def spend_money(user_id):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''SELECT SUM(price * amount) 
        FROM orders
        JOIN products
        ON orders.product_id = products.id
        WHERE user_id = ?''',(user_id,))
        money=await cursor.fetchone()
        if money is None:
            return 0
        return str(money)





async def delete_order(order_id):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''DELETE FROM orders WHERE order_id = ?''',(order_id,))
        await db.commit()


async def update_product(price,stock,name):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''UPDATE products 
        SET price = ?, stock = ?
        WHERE name=?''',(price,stock,name))
        await db.commit()
        return cursor.rowcount>0

async def change_stock(name,stock):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''UPDATE products 
        SET stock = stock + ?
        WHERE name=?  ''',(stock,name,))
        await db.commit()


async def buy_products(user_id):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''SELECT 
    cart.product_id,
    cart.quantity,
    products.name,
    products.price,
    products.stock
     FROM cart
        JOIN products ON cart.product_id=products.id
        WHERE user_id = ?''',(user_id,))
        cart=await cursor.fetchall()
        if not cart:
            return False,"Корзина пустая"
        for product_id, amount, name, price, stock in cart:
            if amount > stock:
                return False,f'{name} слишком мало на складе!'
        for product_id, amount, name, price, stock in cart:
            await db.execute('''UPDATE products SET stock = stock - ? WHERE id = ?''',(amount,product_id))
            await db.execute('''INSERT INTO orders(user_id,product_id,amount,price)VALUES(?,?,?,?)''',(user_id,product_id,amount,price))
        await db.execute('''DELETE FROM cart WHERE user_id = ?''',(user_id,))
        await db.commit()
        return True, "Заказ оформлен"

async def delete_product(name):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''DELETE FROM products 
        WHERE name = ?''',(name,))
        await db.commit()

async def remove_from_cart(user_id,product_id):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''DELETE FROM cart
        WHERE user_id = ? AND product_id = ?''',(user_id,product_id))
        if cursor.rowcount ==0:
            return False
        await db.commit()
        return True
