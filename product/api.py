import tornado.ioloop
import tornado.web
from resource import MainHandler
from resource import StoryHandler
from resource import ProductHandler
from resource import ProductAsyncHandler
from tornado.web import url


def make_app():
    app = tornado.web.Application([
        url(r"/", MainHandler),
        url(r"/story/([0-9]+)", StoryHandler, name="story"),
        url(r"/product/([0-9]+)", ProductHandler),
        url(r"/product2/([0-9]+)", ProductAsyncHandler)
    ])

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
