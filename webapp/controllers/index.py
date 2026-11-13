import web

render = web.template.render("webapp/views", base="template")

class Index:
    
    def __init__(self) -> None:
        pass
    
    def GET(self):
        return render.index() # type: ignore
    
    def POST(self):
        pass