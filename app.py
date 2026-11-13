import web

from webapp.controllers.index import Index

urls = (
    "/","Index",
)

app = web.application(urls,globals())

if __name__=="__main__":
    app.run()
