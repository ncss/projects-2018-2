from tornado.ncss import Server, ncssbook_log
import re
import datetime, time
import sqlite3, os
import db
import random
from db import call_query



numCharities = 0
numUsers = 0
charities = []
users = []

class Charity:

    def __init__(self, charityName, story = '', websiteURL = '', logoURL = '', _id=None):
        self._name = charityName
        self._story = story
        self._websiteURL = websiteURL
        self._logo = logoURL
        self._id = _id

        
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

    
class User:

    def __init__(self, username, password, fname, sname, email, _id=None):
        self._username = username
        self._password = password
        self._fname = fname
        self._sname = sname
        self._email = email
        #self._formerUsernames = []
        self._friends = []
        self._follows = []
        #self._charity = charID
        self._id = _id
        #self._blocked = []

        
    def addFriend(self, username): #NOT MVP
        '''
        This function adds a friend to the person's friend list
        Firstly checking whether it is currently in the friends list
        before making its decision on whether to add the friend.
        '''
        if not isFriend(username):
            self._friends.append(username)
            return True
        else:
            return False

    def removeFriend(self, username): #NOT MVP
        '''
        This function removes a friend from the person's friends list
        Firstly checking whether it is currently in the friends list
        before making its decision on whether to add the friend.
        '''
        if isFriend(username):
            self._friends.remove(username)
            return True
        else:
            return False

    def isFriend(self, username: str):
        
        friend = call_query('SELECT user FROM friends WHERE ? = user', (self._username,))

        if username in friend:
            return True
        else:
            return False


    def controlsCharity(self, charity: str):

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
        
    def unfollow(self, charity: int):
        '''
        Database
        '''

        if charity not in self._follows:
            return False
        else:
            self._follows.remove(charity)
            return True
        pass

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
            VALUES (?, ?, ?, '', '', ?);""", (newid, self._username, self._password, self._email,))
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

def loadDatabase():
    array = db.call_query('SELECT * FROM charity', '')
    for id, name, cat, bio, website, img, admin in array:
        charity = Charity(name, bio, website)
        charities.append(charity)

def createUser(username, password, email):
    user = User(username, password, '', '', email)
    db.call_insert_users(username, password, email)
    numUsers += 1
    users.append(user)

def createCharity(name, story, website):
    charity = Charity(name, story, website, '')
    db.call_insert_charities(numCharities, name, story, website)
    numCharities += 1
    charities.append(charity)

if __name__ == "__main__":
    print('== Getting Charity object')
    c = Charity.get(2)
    print(c._name)
    assert c._name == "Snail Helpline"
    print(c)
    print(c._id)
    assert c._id == 2
    print('== Getting User object')
    u = User.get(1)
    print('== User following Charity')
    u.follow(c._id)
    result = call_query("SELECT 1 FROM charity_followers WHERE (charity_id = ?) AND (user_id = ?);",(2, 1))
    print(result)
    assert len(result) > 0

    print('== Getting random charity')
    r =  getRandomCharity()
    print(r._name)

    print('== Creating new Charity')
    c = Charity('bob')
    print('Saving object:', c._id)
    c.save()
    print('Saving object:', c._id)

    print('== Creating new User')
    c = User('John','','','','')
    print('Saving object:', c._id)
    c.save()
    print('Saving object:', c._id)

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
