import aiosqlite


from database.get import get_product_by_name,get_product_by_id, get_order,get_user


async def create_table_users():
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        username TEXT,
        role TEXT DEFAULT 'user')''')
        await db.commit()
async def create_table_products():
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        stock INTEGER)''')
        await db.commit()

async def create_table_orders():
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        amount INTEGER,
        price INTEGER,
        status TEXT DEFAULT 'created',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id))
        ''')
        await db.commit()


async def create_table_cart():
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS cart(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id),

        UNIQUE(product_id,user_id,tg_id)
        )''')
        await db.commit()
async def create_indexes():
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id)''')
        await db.commit()


async def add_user(username,tg_id):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''INSERT INTO users(username,tg_id) VALUES (?,?)''',(username,tg_id))
        await db.commit()

async def add_admin(tg_id):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''UPDATE users 
        SET role='admin'
        WHERE tg_id=?''',(tg_id,))
        await db.commit()


async def add_product(name,price,stock):
    async with aiosqlite.connect('shopbot.db') as db:
        await db.execute('''INSERT INTO products(name,price,stock) VALUES (?,?,?)''',(name,price,stock))
        await db.commit()

async def add_product_to_cart(user_id,product_id,quantity:int=1):
    async with aiosqlite.connect('shopbot.db') as db:
        cursor=await db.execute('''
        SELECT quantity
        FROM cart
        WHERE user_id=? AND product_id=?''',(user_id,product_id))
        item =await cursor.fetchone()
        if item:
            await db.execute('''UPDATE cart 
            SET quantity=quantity+?
            WHERE user_id=? AND product_id=?''',(quantity,user_id,product_id))
        else:
            await db.execute('''INSERT INTO cart(user_id,product_id,quantity) VALUES (?,?,?)''',(user_id,product_id,quantity))
        await db.commit()




