from tornado.ncss import Server, ncssbook_log
import re
import datetime




class Charity:

	def __init__(self, charityName, story = '', websiteURL = '', logoURL = ''):
		self._name = charityName
		self._story = story
		self._websiteURL = websiteURL
		self._logo = logoURL

		
	def editProfile(self, charityName, story, websiteURL):
		self._name = charityName
		self._story = story
		self._websiteURL = websiteURL
	
	def updateLogo(self, logoURL):
		if logoURL is '' or logoURL is None:
			return False
		else:
			self._logo = logoURL
			return True

	def getInfo(self):
		'''
		Database goes here
		'''
		return name, story, webURL
	
	def post(self, title, content):
		_upload(title, content)

	def _upload(self, title, content):
		''' something goes here'''

		
class User:

	def __init__(self, username, password, fname, sname, email):
		self._username = username
		self._password = password
		self._fname = fname
		self._sname = sname
		self._email = email
		self._formerUsernames = []
		self._friends = []
		self._charity = charID

		
	def addFriend(self, username):
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
	
	def removeFriend(self, username):
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

	def isFriend(self, username):
		'''
		This function is mostly used internally.
		It checks that the username parameter is inside the Person's friend list.
		'''
		if username in friends:
			return True
		else:
			return False

	
	def controlsCharity(self, charity):
		if self._charity == charity.lower():
			return True
		else:
			return False	
	def follow(self, charity):
		'''
		Database
		'''
		
	def unfollow(self, charity):
		'''
		Database
		'''
		
	def hasDonated(self, charity):
		'''
		if user has donated to charity:
		return True
		else:
		return False
		'''
	
	def blockUser(self, username):
		'''
		block
		'''
		
	
class Post:
	
	def __init__(self, title, content, user):
		self._title = title
		self._content = content
		self._user = user
		self._uploadTime = getTime()

	def getPostContent(self):
		return self._title, self._content, self._user, self._timestamp

	

def getTime(self):
  	ts = time.time()
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
  
  
 	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  	if int(formattedDate[1])-1 not in range(12):
    	raise SyntaxError
  	else:
    	formattedDate[1] = months[int(formattedDate[1])-1]
  	date = ' '.join(formattedDate)
  
  	clock = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
  
  	formattedClock = clock.split(":")
  	return (date, clock,)

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