from tornado.ncss import Server, ncssbook_log

def charity_profile_handler(request, profile_id):
	request.write("Here is the profile for charity " + profile_id + ".")
	
def create_profile_handler(request):
	pass
	"""Wanting to do something here but not sure what yet."""
def post_create_profile_handler(request, charity_name, charity_logo):
	request.write("You have added a Charity with this name " + charity_name + " and logo " + charity_logo)
	
def swipe_screen_handler(request, profile_id, swipe_direction):
	request.write("You swiped " + swipe_direction + " for the Charity " + profile_id)
	
"""def next_charity_handler(request, )"""


""" Sends user to new page and sends info to data base"""

server = Server()
server.register(r"/charity_profile/(\d+)/", charity_profile_handler)
server.register(r"/create_profile/", create_profile_handler)
server.register(r"/post_create_profile/(.+)/(.+)", post_create_profile_handler)
server.register(r"/swipe/(\d+)/(left|right)", swipe_screen_handler)
server.run()