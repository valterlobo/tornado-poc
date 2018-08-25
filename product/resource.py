import decimal
import json

import tornado.web
from repository import ProductReposistory


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))


class StoryHandler(tornado.web.RequestHandler):
    async def get(self, story_id):
        self.write("this is story %s" % story_id)


class ProductHandler(tornado.web.RequestHandler):

    async def get(self, prod_id):
        product_reposistory = ProductReposistory()
        # prod = product_reposistory.getAll()
        resp = product_reposistory.getByID(prod_id)
        del product_reposistory
        # json_str = json.JSONEncoder.default(self, o)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        if resp is not None:
            self.write(resp['name'])
        else:
            self.write("NOT FOUND")
        self.finish()


class DecimalJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)


class ProductAsyncHandler(tornado.web.RequestHandler):

    async def get(self, prod_id):
        product_reposistory = ProductReposistory()
        # prod = product_reposistory.getAll()
        resp = await product_reposistory.getAsyncByID(prod_id)
        print(resp)
        # del productReposistory
        # json_str = json.JSONEncoder.default(self, o)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        if resp is not None:
            self.write(json.dumps(resp, cls=DecimalJSONEncoder))
        else:
            self.write("NOT FOUND")
        self.finish()
