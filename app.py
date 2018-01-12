from tornado.ncss import Server, ncssbook_log

def home_page_handler(request):
    request.write(open("style_guide/index.html").read())

def charity_profile_handler(request, charity_profile_id):
    request.write("Here is the profile for charity " + charity_profile_id + ".")

def create_charity_profile_handler(request):
    pass
    """Wanting to do something here but not sure what yet."""

def post_create_profile_handler(request, charity_name, charity_logo):
    request.write("You have added a Charity with this name " + charity_name + " and logo " + charity_logo)

def feed_handler(request):
    request.write("Welcome to your feed!")

def swipe_screen_handler(request, charity_profile_id, swipe_direction):
    request.write("You swiped " + swipe_direction + " for the Charity " + charity_profile_id)

def about_handler(request):
    request.write("This is the 'About' page")

def user_profile_handler(request, user_profile_id, user_profile_name):
    request.write("Here is " + user_profile_id + " aka " + user_profile_name)

def default_handler(request, method):
    request.write("Hello")
    """Redirects all invalid urls to this"""

"""def next_charity_handler(request, )"""
""" Sends user to new page and sends info to data base"""

server = Server()
server.register(r"/", home_page_handler)
server.register(r"/charity_profile/(\d+)/?", charity_profile_handler)
server.register(r"/create_charity_profile/?", create_charity_profile_handler)
server.register(r"/post_create_profile/(.+)/(.+)/?", post_create_profile_handler)
server.register(r"/swipe/(\d+)/(left|right)/?", swipe_screen_handler)
server.register(r"/feed/?", feed_handler)
server.register(r"/about/?", about_handler)
server.register(r"/user_profile/(\d+)/(.+)/?", user_profile_handler)
server.set_default_handler(default_handler)
server.run()
