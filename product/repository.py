import async_mysql
import database
from aiomysql.cursors import DictCursor


class ProductReposistory(object):
    mariaDB = database.MariaDBData()

    mysql = async_mysql.MysqlWrapper(host='localhost', port=3306, user='root',
                                     password='root', db='mercaoferta'
                                     )

    def __init__(self):
        print('Start :ProductReposistory')
        self.mariaDB.connect_to_db('localhost', 'root', 'root', 'mercaoferta')

    def __del__(self):
        self.mariaDB.disconnect_from_db()

    def getAll(self):
        pass

    def getByID(self, id):
        result = self.mariaDB.get_data(
            "SELECT id, name, price, stock, attr FROM products WHERE id={0}".format(id))
        get = None
        print(type(result))
        if not result:
            get = None
        else:
            get = result[0]
        return get

    @async_mysql.mysql_context(mysql)
    async def getAsyncByID(self, id, conn=None):
        async with conn.cursor(DictCursor) as cur:
            await cur.execute('SELECT id, name, price, stock, attr FROM products WHERE id={0}'.format(id))
            print(cur.rowcount)
            # print(await cur.fetchone())

            result = await cur.fetchone()
            get = None
            print(type(result))
            if not result:
                get = None
            else:
                get = result
            return get
