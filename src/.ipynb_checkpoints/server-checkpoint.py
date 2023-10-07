# Hosted Server

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

class Server:
    def __init__(self):
        pass
    
    def start(self, store):

        async def insert(request):
            #store.insert()
            return JSONResponse({'hello': 'world' + request.path_params[]})
        
        async def delete(request):
            #store.delete()
            return JSONResponse({'hello': 'world'})
        
        async def query(request):
            #store.query()
            return JSONResponse({'hello': 'world'})

        app = Starlette(debug=True, routes=[
            Route('/insert', insert),
            Route('/delete', delete),
            Route('/query', query),
        ])
        
        uvicorn.run(app)

    
    def terminate(self):
        pass