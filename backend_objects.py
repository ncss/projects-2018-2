from tornado.ncss import Server, ncssbook_log
import re
import datetime, time
import sqlite3, os
import db
import random
import hashlib
from db import call_query



numCharities = 0
numUsers = 0

class Charity:

    def __init__(self, charityName, story = '', websiteURL = '', logoURL = '', _id=None, tags=[]):
        self._name = charityName
        self._story = story
        self._websiteURL = websiteURL
        self._logo = logoURL
        self._id = _id
        self._tags = tags

    def __str__(self):
        return "CHARITY OBJECT:( id:{} name:'{}' story[:10]:'{}' websiteURL:'{}' logoURL:'{}' )".format(self._id, self._name, self._story, self._websiteURL, self._logo)
        
    def editProfile(self, charityName, story, websiteURL):
        self._name = charityName
        self._story = story
        self._websiteURL = websiteURL
        ###

    def updateLogo(self, logoURL):
        if logoURL is '' or logoURL is None:
            # Sourced from Creative Commons 
            self._logo = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Default_profile_picture_%28male%29_on_Facebook.jpg/480px-Default_profile_picture_%28male%29_on_Facebook.jpg'
        else:
            self._logo = logoURL
            return True

    def getInfo(self):
        
        info = call_query('SELECT * FROM charities WHERE ? = name', (charity,))
        
        #name = info[]
        #story = info[]
        #webURL = info[]

        return (name, story, webURL, logoURL,)

    @staticmethod
    def get(ID):
        results = call_query('''SELECT name,story,charity_website_url,image_src
        FROM charity
        WHERE id = ?
        ''',(ID,))
        results = results[0]
        c = Charity(results[0],results[1],results[2],results[3], ID)
        return c

    def update(self):
        if self._id is None:
            raise NameError("Charity's _id is None. Charity must have an ID (referring to the relevant database charity entry) in order to have it's database values updated. If this is a new Charity, use Charity.save()")
        #The None's in the query are due to columns in the charity table that exisit for future post-MVP stuff, and aren't in the charity object. (category and admin_id)
        call_query("UPDATE charity SET name= ?, category= ?, story= ?, charity_website_url= ?, image_src= ?, admin_id=? WHERE id=?", (self._name, None, self._story, self._websiteURL, self._logo, None, self._id))

    def save(self):
        '''
        Inserts the given data into the charity table of the database as a new value.
        '''
        data = call_query("""
            SELECT MAX(id)
            FROM charity;
        """,'')
        newcharityid = data[0][0] + 1
        call_query("""
            INSERT INTO charity(id,name,category,story,charity_website_url,image_src,admin_id)
            VALUES (?, ?, '', ?, ?, ?, '');
            """, (newcharityid, self._name, self._story, self._websiteURL, self._logo,))
        self._id = newcharityid


    def post(self, title, content):
        _upload(title, content)
        ###

    def _upload(self, title, content):
        ''' something goes here'''
        some_variable = Post(title, content, self._name)

    def followers(self):
        data = call_query("""
                SELECT user_id FROM charity_followers WHERE ? = charity_id
                """,(self._id,))
        users = []
        for row in data:
            users.append(User.get(row[0]))

        return users

class User:

    def __init__(self, username, password, fname, sname, email, _id=None):
        self._username = username
        self._password = password
        self._fname = fname
        self._sname = sname
        self._email = email
        #self._formerUsernames = []
        #self._charity = charID
        self._id = _id
        #self._blocked = []

    def __str__(self):
        return "USER OBJECT:( id:{} username:'{}' password:{} self._fname:'{}' self._sname:'{}' self._email:'{}' )".format(self._id, self._username, self._password, self._fname, self._sname, self._email)
        
    def addFriend(self, userID): #NOT MVP
        '''
        This function adds a friend to the person's friend list
        Firstly checking whether it is currently in the friends list
        before making its decision on whether to add the friend.
        '''
        result = call_query("SELECT 1 FROM friends WHERE (user_id1 = ?) AND (user_id2 = ?);",(self._id, userID,))
        if len(result) < 1:
            call_query("INSERT INTO friends VALUES (?,?);",(self._id, userID,))

    def removeFriend(self, userID): #NOT MVP
        
        result = call_query("DELETE FROM friends WHERE (user_id1 = ?) AND (user_id2 = ?)", (self._id, userID,))

    def isFriend(self, userID):
        
        friend = call_query('SELECT 10 FROM friends WHERE (user_id1 = ?) AND (user_id2 = ?)', (self._id, userID))
        print(friend)
        if len(friend) > 0:
            return True
        else:
            return False

    def friends(self):
        '''
        This function returns a list of all the user's friends.
        No arguments are passsed to this function.
        '''
        result = call_query("SELECT user_id2 FROM friends WHERE (user_id1 = ?);", (self._id, ))
        user_friends = [User.get(row[0]) for row in result]
        return user_friends


    def controlsCharity(self, charity: int):

        char = call_query('SELECT user FROM charities WHERE ? = user', (self._username,))
        
        if int(charity) in char:
            return True
        else:
            return False    

    def follow(self, charity: int):
        '''
        This function adds the ID of the user and the id of the charity that the user has chosen to follow into the charity_followers table.
        Pass the ID of the charity, not the charity object.
        '''
        result = call_query("SELECT 1 FROM charity_followers WHERE (charity_id = ?) AND (user_id = ?);",(charity, self._id))
        if len(result) < 1:
            call_query("INSERT INTO charity_followers VALUES (?,?);",(charity, self._id))
        
    def unfollow(self, charID: int):
        '''
        Database
        '''
        result = call_query("DELETE FROM charity_followers WHERE (charity_id = ?) AND (user_id = ?)", (charID, self._id,))

    def isFollowing(self, charID):

        charity = call_query('SELECT 10 FROM charity_followers WHERE (charity_id = ?) AND (user_id = ?)', (charID, self._id,))
        if len(charity) > 0:
            return True
        else:
            return False

    def following(self):
        '''
        This function returns the number of charities that are being followed by the user.
        No arguments are passed to this function."
        '''
        result = call_query("SELECT charity_id FROM charity_followers WHERE user_id = ?;",(self._id,))
        charities = [Charity.get(row[0]) for row in result]
        return charities
            
            

    def hasDonated(self, charity: int): #NOT MVP
        '''
        if user has donated to charity:
        return True
        else:
        return False
        '''
        pass

    def friendsDonated(self, charity: int): #NOT MVP
        '''
        '''
        #call_query()
        pass

    def blockUser(self, username: str): #NOT MVP
        '''
        block
        '''
        pass

    def update(self):
        if self._id is None:
            raise NameError("user's id is None. User must have an ID (referring to the relevant database User entry) in order to have it's database values updated. If this is a new User, use User.save()")
        call_query("UPDATE users SET username= ?, pword= ?, fname= ?, sname= ?, email= ? WHERE id = ?;", (self._username, self._password, self._fname, self._sname, self._email, self._id))
        
    @staticmethod
    def get(ID):
        results = call_query('''SELECT username,pword,fname,sname,email
        FROM users
        WHERE id = ?
        ''',(ID,))
        if not results:
            return None
        results = results[0]
        c = User(results[0],results[1],results[2],results[3],results[4], ID)
        return c

    def save(self):
        data = call_query("""
            SELECT MAX(id)
            FROM users;
        """,'')
        newid = data[0][0] + 1
        call_query("""
            INSERT INTO users(id,username,pword,fname,sname,email)
            VALUES (?, ?, ?, '', '', ?);""", (newid, self._username, hashlib.sha256(self._password.encode()).hexdigest(), self._email,))
        self._id = newid

    def getCharityFriends(self, charID):
        c = Charity.get(charID)
        people = c.followers()
        return [x for x in people if self.isFriend(x._id)]

    @staticmethod
    def login(username, password):
        '''
        Takes two strings and compares the hashed password with the database,
        returning the object
         of that user.
        '''
        h = hashlib.sha256()
        h.update(password.encode())
        data = call_query("""SELECT id FROM users WHERE username = ? and pword = ?

            """,(username, h.hexdigest()))
        
        if len(data):
            return User.get(data[0][0])
        else:
            return None





class Post:

    def __init__(self, charityID, postType: str, timestamp, contentText: str, contentImage: str, contentEventTime, contentEventLocation: str, dbID=None):
        '''
        Creates a new Post object
        timestamp should be a datetime object (use "datetime.datetime.fromtimestamp(time.time()) to get the current time as a datetime object)
        Event Time should also be a datetime object - use datetime.datetime(year, month, day, hour, minute, second)
        Currently, postType should be "event" as that is the only supported event type
        '''
        self._id = dbID
        self._charityID = charityID
        self._postType = postType
        self._timestamp = timestamp
        self._contentText = contentText
        self._contentImage = contentImage
        self._contentEventTime = contentEventTime
        self._contentEventLocation = contentEventLocation

    def __str__(self):
        return "POST OBJECT:( id:{} charityID:{} postType:{} timestamp:{} contentText[:10]:{} contentImage:{} contentEventTime:{} contentEventLocation:{}".format(self._id, self._charityID, self._postType, self._timestamp, self._contentText, self._contentImage, self._contentEventTime, self._contentEventLocation)

    @staticmethod
    def getID(ID):
        '''
        Get's a post object from given ID
        '''
        results = call_query("SELECT charity_id, post_type, timestamp, content_text, content_image, content_event_time, content_event_location FROM posts WHERE id = ?", (ID,))
        if len(results) == 0:
            raise IndexError('No charity exisits in the database with ID: ' + str(ID))
        else:
            results = results[0]
        return Post(results[0], results[1], dbTimeFormatToDatetime(results[2]), results[3], results[4], dbTimeFormatToDatetime(results[5]), results[6], ID)


    @staticmethod
    def getCharityPosts(charityID):
        '''
        Get's a post object based on the ID from the owning charitiy's ID
        '''
        results = call_query("SELECT charity_id, post_type, timestamp, content_text, content_image, content_event_time, content_event_location, id FROM posts WHERE charity_id = ?", (charityID,))
        return [Post(result[0], result[1], dbTimeFormatToDatetime(result[2]), result[3], result[4], dbTimeFormatToDatetime(result[5]), result[6], result[7]) for result in results]

    @staticmethod
    def getAllPosts():
        '''
        Get's a post object based on the ID from the owning charitiy's ID
        '''
        results = call_query("SELECT charity_id, post_type, timestamp, content_text, content_image, content_event_time, content_event_location, id FROM posts;")
        return sorted([Post(result[0], result[1], dbTimeFormatToDatetime(result[2]), result[3], result[4], dbTimeFormatToDatetime(result[5]), result[6], result[7]) for result in results], key=(lambda post : post._timestamp), reverse=True)

    def update(self):
        '''
        Pushes any changes made to the post object into the database
        '''
        if self._id is None:
            raise NameError("Post's _id is None. Post must have an ID (referring to the relevant database Post entry) in order to have it's database values updated. If this is a new Post, use Post.save();")
        call_query("UPDATE posts SET post_type = ?, timestamp = ?, content_text = ?, content_image = ?, content_event_time = ?, content_event_location = ? WHERE id = ?;", (self._postType, datetimeToDBTimeFormat(self._timestamp), self._contentText, self._contentImage, datetimeToDBTimeFormat(self._contentEventTime), self._contentEventLocation, self._id))


    def save(self):
        '''
        Puts a new post object into the database
        Generates a new ID and puts it into self._dbID
        '''
        newpostid = call_query("SELECT MAX(id) FROM posts;")[0]
        newpostid = newpostid[0]+1 if newpostid[0] is not None else 0
        call_query("INSERT INTO posts(id, charity_id, post_type, timestamp, content_text, content_image, content_event_time, content_event_location) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (newpostid, self._charityID, self._postType, datetimeToDBTimeFormat(self._timestamp), self._contentText, self._contentImage, datetimeToDBTimeFormat(self._contentEventTime), self._contentEventLocation))
        self._id = newpostid

    def delete(self):
        '''
        Deletes a charity from the database
        '''
        call_query("DELETE FROM posts WHERE id = ?", (self._id,))
        self._id = None

def getTime(timeToUse=None) -> tuple:
    if timeToUse is None:
        ts = time.time()
    else:
        ts = timeToUse

    '''
    This block finds the appropriate suffix based on the digits in the number
    '''
    
    date = datetime.datetime.fromtimestamp(ts).strftime('%d:%m')
    formattedDate = date.split(":")
    if formattedDate[0].endswith("1") and not formattedDate[0].startswith("1"):
        formattedDate[0] += 'st'
    elif formattedDate[0].endswith("2") and not formattedDate[0].startswith("1"):
        formattedDate[0] += 'nd'
    elif formattedDate[0].endswith("3") and not formattedDate[0].startswith("1"):
        formattedDate[0] += 'rd'
    else:
        formattedDate[0] += 'th'

    '''
    This section determines the month that matches the appropriate number
    '''
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if int(formattedDate[1])-1 not in range(12):
        raise SyntaxError("Something went drastically wrong with the datetime module")
    else:
        formattedDate[1] = months[int(formattedDate[1])-1]
    
    date = ' '.join(formattedDate)

    clock = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')

    '''
    This block is used to add the AM/PM suffix to the end of the time
    '''

    formattedClock = clock.split(":")
    if int(formattedClock[0]) == 12:
        clock = ':'.join(formattedClock) + ' pm'
    elif int(formattedClock[0]) == 24 or int(formattedClock[0]) == 0:
        formattedClock[0] = '12'
        clock = ':'.join(formattedClock) + ' am'
    elif int(formattedClock[0]) > 12:
        formattedClock[0] = str(int(formattedClock[0])%12)
        clock = ':'.join(formattedClock) + ' pm'
    elif int(formattedClock[0]) < 12:
        clock = ':'.join(formattedClock) + ' am'
    return (date, clock,)

def datetimeToDBTimeFormat(datetimeObject):
    '''
    Converts a datetime.datetime object into a simple form to be sent into a database.
    Ignores microseconds.
    '''
    return "{},{},{},{},{},{}".format(datetimeObject.year, datetimeObject.month, datetimeObject.day, datetimeObject.hour, datetimeObject.minute, datetimeObject.second)

def dbTimeFormatToDatetime(dbTimeFormat):
    '''
    Converts a compact str representation of the time back into a datetime.datetime object
    Expects formatting given by datetimeToDBTimeFormat (i.e. "year,month,day,hour,minute,second")
    '''
    timeSplit = dbTimeFormat.split(",")
    return datetime.datetime(int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]), int(timeSplit[3]), int(timeSplit[4]), int(timeSplit[5]))

def getRandomCharity():
    #print(charities)
    numCharities = db.call_query('SELECT MAX(id) FROM charity', '')[0][0]
    #print(numCharities)
    num = random.randint(0, numCharities)
    x = Charity.get(num)

    if not x:
        raise SyntaxError("HUGE PROBLEMS WITH READING DATABASE")
    else:
        return x

'''
def loadDatabase():
    array = db.call_query('SELECT * FROM charity', '')
    for id, name, cat, bio, website, img, admin in array:
        charity = Charity(name, bio, website)
        charities.append(charity)
'''

def createUser(username, password, fname, sname, email):
    user = User(username, password, fname, sname, email)
    user.save()

def createCharity(name, story, website, logo):
    charity = Charity(name, story, website, logo)
    charity.save()




if __name__ == "__main__":
    print('== Getting Charity object (id=2)')
    c = Charity.get(2)
    print(c)
    assert c._name == "Snail Helpline"
    assert c._id == 2
    print('== Updating Charity information')
    c._websiteURL = "http://www.blah.com/"
    c.update()
    c = Charity.get(2)
    assert c._websiteURL == "http://www.blah.com/"
    c._websiteURL = "https://hotspicyme.me"
    c.update()
    print('== Getting User object (id=1)')
    u = User.get(1)
    print(u)
    print('== User following Charity ==')
    print(u.isFollowing(c._id))
    u.follow(c._id)
    print(u.isFollowing(c._id))

    assert len(c.followers()) >= 0
    assert len(u.following()) >= 0
    result = call_query("SELECT 1 FROM charity_followers WHERE (charity_id = ?) AND (user_id = ?);",(2, 1))
    print(result)
    assert len(result) > 0

    u.unfollow(c._id)
    print(u.isFollowing(c._id))
    assert len(c.followers()) >= 0
    assert len(u.following()) >= 0
    print('== User befriending User')
    print(u.isFriend(3))
    u.addFriend(3)
    print('==Returning list of friends==')
    print(u.friends())
    assert u.friends()[0]._id == 3
    print(u.isFriend(3))
    u.removeFriend(3)
    print(u.isFriend(3))
    print('==Returning list of friends==')
    print(u.friends())
    print('== Getting random charity')
    r =  getRandomCharity()
    print(r._name)

    print('== Creating new Charity')
    c = Charity('bob')
    print('Saving object:', c._id)
    c.save()
    print('Saving object:', c._id)

    print('== Creating new User')
    c = User('John','trident','','','')
    print('Saving object:', c._id)
    c.save()
    print('Saving object:', c._id)
    c = User.get(c._id)
    assert c._password == 'fb2b9bb163acf7e3ad50dd8d950b56ba0065d96aedb36ffcaa87dc44b9000f2a'

    print('== Testing login')
    assert User.login('foo', 'trident')._id == 0
    assert User.login('foo', 'satgsweg') == None

    print('== Updating User')
    #Get and update User
    u = User.get(3)
    assert u._username == "percy"
    u._fname = "Mr Snail"
    u.update()
    u = User.get(3)
    assert u._fname == "Mr Snail"
    u._fname = None
    u.update()

    #Post tests
    print('==Getting Charity 4\'s posts')
    posts = Post.getCharityPosts(4)
    assert len(posts) == 2
    testPost = posts[0]
    assert testPost._id == 2
    assert testPost._contentImage == "https://www.oxfam.org.au/wp-content/uploads/2016/11/81588scr-1-700x450.jpg"
    testPost._contentEventLocation = "Test Location"
    testPost.update()
    testPost = Post.getID(2)
    assert testPost._contentEventLocation == "Test Location"
    testPost._contentEventLocation = "Greater Sydney Area (Hawkesbury-Harbour)"
    testPost.update()
    newPost = Post(4, 'event', datetime.datetime.fromtimestamp(time.time()), "Test Post Creation", "http://testsite.com/static/testImage.jpg", datetime.datetime(2018, 1, 1, 3, 0, 0), 'Test Location')
    newPost.save()
    newPost = Post.getID(4)
    assert newPost._contentEventLocation == 'Test Location'
    newPost.delete()

    print('== Testing Charity Friends ==')
    u = User.get(0)
    print(u.getCharityFriends(0))
    u.addFriend(1)
    u1 = User.get(1)
    u1.follow(0)
    print(u.getCharityFriends(0))
    assert len(u.getCharityFriends(0)) > 0
    u1.unfollow(0)
    print(u.getCharityFriends(0))
    assert len(u.getCharityFriends(0)) == 0

'''
def validateURL(url):
regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.I)
if re.match(regex, url) is not None:
    return True
return False
'''
