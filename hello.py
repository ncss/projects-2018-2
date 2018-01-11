from tornado.ncss import Server

def index_handler(request):
  request.write('Hello, World!')

server = Server()
server.register(r'/', index_handler)
server.run()
