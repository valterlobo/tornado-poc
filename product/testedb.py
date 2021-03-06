import asyncio
import aiomysql

loop = asyncio.get_event_loop()


@asyncio.coroutine
def test_example():
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root', db='mercaoferta',
                                       loop=loop)

    cur = yield from conn.cursor()
    yield from cur.execute("SELECT id, name, price, stock, attr FROM products;")
    print(cur.description)
    r = yield from cur.fetchall()
    print(r)
    yield from cur.close()
    conn.close()


loop.run_until_complete(test_example())
