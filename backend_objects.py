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
            raise NameError("user's id is None. User must have an ID (referring to the relevant database User entry) in order to have its database values updated. If this is a new User, use User.save()")
        call_query("UPDATE users SET username= ?, pword= ?, fname= ?, sname= ?, email= ? WHERE id = ?;", (self._username, self._password, self._fname, self._sname, self._email, self._id))

    @staticmethod
    def login(username, password):
        '''
        Takes two strings and compares the hashed password with the database,
        returning the id of that user.
        '''
        h = hashlib.sha256()
        h.update(password.encode())
        data = call_query("""SELECT id FROM users WHERE username = ? and pword = ?

            """,(username, h.hexdigest()))
        
        if len(data):
            return User.get(data[0][0])
        else:
            return None
        
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


class Post:

    def __init__(self, title: str, content: str, user: str):
        self._title = title
        self._content = content
        self._user = user
        self._uploadTime = getTime()

    def getPostContent(self):
        return self._title, self._content, self._user, self._timestamp



def getTime() -> tuple:

    ts = time.time()

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

    print('== Testing login')
    assert User.login('foo', 'trident')._id == 0
    assert User.login('foo', 'satgsweg') == None

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