import os
import backend_objects
import templater
from tornado.ncss import Server, ncssbook_log

TEMPLATE_DIR = "templates"
aux = 0
def get_template(filename):
    with open(os.path.join(TEMPLATE_DIR, filename)) as f:
        return f.read()

def home_page_handler(request):
    global aux
    request.set_secure_cookie("id", str(aux)) # until we have a login page
    charity = backend_objects.getRandomCharity()
    #charity = backend_objects.Charity("Snail Helpline", "We help snails!!", logoURL = "snail.jpg")
    context = {"charity": charity}
    request.write(templater.render("templates/index.html", context))


def charity_profile_handler(request, charity_profile_id):
    charity = backend_objects.Charity.get(charity_profile_id)
    #charity = backend_objects.Charity("Snail Helpline", "We help snails!!", "https://en.wikipedia.org/wiki/Snail", logoURL = "snail.jpg")
    #request.write("Here is the profile for charity " + charity_profile_id + ".")
    #request.write(get_template("charity.html").format(charity_profile_id = charity_profile_id, charity_name = "charity_name", charity_logo = "charity_logo"))
    context = {"charity": charity, "charity_profile_id": charity_profile_id}
    request.write(templater.render("templates/charity.html", context))


def create_charity_profile_handler(request):
    context = {}
    request.write(templater.render("templates/create_charity_profile.html", context))
    """Wanting to do something here but not sure what yet."""

def post_create_charity_profile_handler(request):
    context = {}
    charity_name = request.get_field('new_name')
    charity_logo_name = request.get_field("logo_name")
    charity_new_bio = request.get_field("new_bio")
    #request.write("You have added a Charity with this name " + charity_name + ". Your logo name is: " + charity_logo_name + ". And your bio is: " + charity_new_bio)
    new_charity = backend_objects.Charity(charity_name,story=charity_new_bio,logoURL=charity_logo_name)
    new_charity.save()
    context['charity'] = new_charity
    request.write(templater.render("templates/post_create_charity_profile.html", context))

def feed_handler(request):
    context = {"Post":backend_objects.Post, "Charity":backend_objects.Charity}
    request.write(templater.render("templates/feed.html", context))

def swipe_screen_handler(request, charity_profile_id, swipe_direction):
    #request.write("You swiped " + swipe_direction + " for the Charity " + charity_profile_id)
    global aux
    request.set_secure_cookie("id", str(aux))
    if swipe_direction == 'right':
        if request.get_secure_cookie("id"):
            cookie = request.get_secure_cookie("id").decode()
            user = backend_objects.User.get(int(cookie))
            user.follow(charity_profile_id)
            #numfollowed = numfollowed + 1
    home_page_handler(request)

def create_user_profile_handler(request):
    context = {}
    request.write(templater.render("templates/user_sign_up.html", context))

def post_create_user_profile_handler(request):
    global aux
    username = request.get_field("username")
    fname = request.get_field("fname")
    sname = request.get_field("sname")
    email = request.get_field("email")
    password = request.get_field("pass")
    cpassword = request.get_field("cpass")
    if password == cpassword: 
        c = backend_objects.User(username, password, fname, sname, email)
        c.save()
        aux = c._id
        request.set_secure_cookie("id", str(aux))
        context = {}
        request.write("You have created a user page with the name: " + str(c._username) + " and id " + str(c._id))
    else:
        request.write("Passwords do not match")

def user_handler(request):
    request.write("Logged|Not logged in.")

def about_handler(request):
    context = {}
    request.write(templater.render("templates/about.html", context))

def user_profile_handler(request, user_profile_id, user_profile_name):
    #request.write("Here is " + user_profile_id + " aka " + user_profile_name)
    user = backend_objects.User.get(0)
    context = {"user": user}
    request.write(templater.render("templates/user.html", context))

def charity_list_handler(request):
    context = {}
    request.write(templater.render("templates/charity_list.html", context))

def default_handler(request, method):
    request.write("Invaild url silly!")
    """Redirects all invalid urls to this"""

"""def next_charity_handler(request, )"""
""" Sends user to new page and sends info to data base"""

# \d+ is any number
# .+ = any letter but preferably a name!!

server = Server()
server.register(r"/?", home_page_handler)
server.register(r"/charity_profile/(\d+)/?", charity_profile_handler)
server.register(r"/create_charity_profile/?", create_charity_profile_handler)
server.register(r"/post_create_charity_profile/?", post_create_charity_profile_handler)
server.register(r"/swipe/(\d+)/(left|right)/?", swipe_screen_handler)
server.register(r"/feed/?", feed_handler)
server.register(r"/about/?", about_handler)
server.register(r"/user_profile/(\d+)/(.+)/?", user_profile_handler)
server.register(r"/create_user_profile/?", create_user_profile_handler)
server.register(r"/post_create_user_profile/?", post_create_user_profile_handler)
server.register(r"/user/?", user_handler)
server.register(r"/charity_list/?", charity_list_handler)
server.set_default_handler(default_handler)
server.run()
