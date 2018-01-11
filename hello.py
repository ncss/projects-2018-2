from tornado.ncss import Server

def index_handler(request):
  request.write('Hello, World!')

def page_not_found(response, url):
#pls put a big scary skull here, frontenders
    response.write('''
!!!404 TERROR!!!
This page was not found
''')

server = Server()
server.register(r'/', index_handler)
server.set_default_handler(page_not_found)
server.run()
