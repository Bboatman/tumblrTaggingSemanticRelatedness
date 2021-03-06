''' 
Author: Brooke Boatman
Date: December 2015
Custom classes for tumblr users and tag cluster objects made for simplifying 
and making more readable data manipulations in later learning stages
'''

import collections

class User(object):
	def __init__(self, username):
		self.userId = username
		self.tagDict =  {}
		self.posts = []


	def __str__(self):
		return self.userId + ", Number of Posts: " + str(len(self.posts)) + ", Number of unique tags: " + str(len(self.tagDict.keys())) 


	def addPost(self, tumblrPost):
		''' 
		Update a user object with a tumblr post
		Param: tumblrPost - a single post's dictionary from the pytumblr api client
		'''
		tagList = tumblrPost['tags'] # Duplicate for length counting purposes
		newList = tumblrPost['tags']
					
		for x in range(len(tagList)): # When you're popping things off lists, it gets weird, this prevents that
			tag = tagList[0].encode('utf-8')
			if tag in newList: # Get the list of all tags that have cooccured with the tag we just got, add it to the dict
				if tag not in self.tagDict:
					self.tagDict[tag] = collections.Counter()
				newList.remove(tag)
				for word in newList:
					self.tagDict[tag][word] += 1
				newList.append(tag)
		self.posts.append(str(tumblrPost['id']))		


	def getName(self):
		return self.userId


	def getTags(self):
		return self.tagDict


	def getPosts(self):
		return self.posts

class TagCluster(object):
	""" 
	Cluster object for feature extraction of tag vectors
	"""
	def __init__(self):
		self.memberList = []
		self.rawVector = collections.Counter()
		self.centroid = collections.Counter()


	def __str__(self):
		returnString = ""
		for tag in self.memberList[:-1]:
			returnString += (tag + ", ")
		returnString += self.memberList[-1]
		return returnString


	def wipeMembers(self):
		self.memberList = []
		self.rawVector = collections.Counter()

	def addMember(self, name, tagVector):
		self.memberList.append(name)
		self.rawVector += collections.Counter(tagVector)

	def getMembers(self):
		return self.memberList

	def getCentroid(self):
		return self.centroid

	def setCentroid(self):
		centroidCounter = collections.Counter()
		frac = float(len(self.memberList))
		for tag in self.rawVector:
			centroidCounter[tag] = float(self.rawVector[tag]) / frac
		self.centroid = centroidCounter