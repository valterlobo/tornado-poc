import aiomysql


class MysqlWrapper:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self._pool = None
 
    async def pool(self):
        if not self._pool:
            self._pool = await aiomysql.create_pool(
                host=self.host, port=self.port, user=self.user,
                password=self.password, db=self.db
            )
        return self._pool
 
    async def close(self):
        if not self._pool:
            return
        self._pool.close()
        await self._pool.wait_closed()
 

 
def mysql_context(wrapper):
    def _mysql_context(func):
        async def __mysql_context(*args, **kwargs):
            pool = await wrapper.pool()
            async with pool.acquire() as conn:
                await conn.set_charset('utf8')
                r = await func(conn=conn, *args, **kwargs)
                await conn.commit()
            return r
        return __mysql_context
    return _mysql_context
 
 

 
 
async def close_pool():
    await mysql.close()
    print('Close mysql pool')
 
"""
mysql = MysqlWrapper(host='localhost', port=3306, user='root',
    password='root', db='mercaoferta'
)
 
 
@mysql_context(mysql)
async def mysql_test(conn=None):
    async with conn.cursor(DictCursor) as cur:
        await cur.execute('SELECT id, name, price, stock, attr FROM products')
        print(cur.rowcount)
        print(await cur.fetchone())
        print(await cur.fetchall())

loop = asyncio.get_event_loop()
loop.run_until_complete(mysql_test())
loop.run_until_complete(close_pool())
loop.close()
"""