#!/usr/bin/python

# Gigantic Object Database - CLI written in Python
#
# build 0.0.1 - 2015.08.09 Asyn

# imports
import sqlite3
import godobject
from textcolors import TextColors

# "Constants"
DBCONNECT = 'god.db'
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1
START_NODE = 1




# connect to the database4
conn = sqlite3.connect(DBCONNECT)
cursor = conn.cursor()


def printHelp():
	print "- GOD command list -"
	print "0# : shorthand for jump"
	print "add : add child to this node"
	print "delete : delete this node"
	print "jump|j # : load object with ID #"
	print "link <parent> # : link this node as <parent> or child(default) to node #"
	print "new : new node without parent or child"
	print "payload : changes the current payload"
	print "quit : quits this application"
	print "search|s <query> : search for <query>"
	print "show : shows the current object"
	print "title : changes current title"
	print "unlink <parent> # : unlink <parent> or child(default) with objectID #"
	print "? : help (this screen)"


def addChild():
	title = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Title of new node: "+TextColors.WHITE));
	payload = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Payload of new node: "+TextColors.WHITE));
	dataType = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Data Type (ENTER for 'basic.text'): "+TextColors.WHITE));
	childObject = godobject.GODObject()
	childObject.title = title
	childObject.payload = payload
	if (dataType == ''):
		childObject.dataType = 'basic.text'
	else:
		childObject.dataType = dataType
	childObject.saveObject(cursor)
	conn.commit()
	sql = "INSERT INTO links VALUES ("+str(currObject.objectID)+","+str(cursor.lastrowid)+")"
	cursor.execute(sql)
	conn.commit()
	currObject.showObject(cursor)
	
def newNode():
	title = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Title of new node: "+TextColors.WHITE));
	payload = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Payload of new node: "+TextColors.WHITE));
	dataType = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Data Type (ENTER for 'basic.text'): "+TextColors.WHITE));
	currObject.objectID=0
	currObject.title = title
	currObject.payload = payload
	if (dataType == ''):
		currObject.dataType = 'basic.text'
	else:
		currObject.dataType = dataType
	try:
		currObject.saveObject(cursor)
		conn.commit()
		currObject.loadObject(cursor,cursor.lastrowid)
	except sqlite3.Error, e:
		print "Error %s: " % e.args[0]
		
	print TextColors.RESET
	currObject.showObject(cursor)


def search(params):
	params = params.lstrip("s ")
	params = params.lstrip("search ")
	sql = "SELECT * FROM objects WHERE (title like '%"+params+"%' OR payload like '%"+params+"%') LIMIT 20"
	data = cursor.execute(sql)
	for row in data:
		print "("+str(row[0])+") "+row[1]+" : "+row[2]


def changeTitle():
	workStr = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Enter title ["+currObject.title+"]: "+TextColors.WHITE))
	currObject.title = workStr
	currObject.saveObject(cursor)
	conn.commit()
	currObject.showObject(cursor)
	print TextColors.RESET

def changePayload():
	workStr = str(raw_input(TextColors.BOLD+TextColors.BLUE+"Enter payload: "+TextColors.WHITE))
	currObject.payload = workStr
	currObject.saveObject(cursor)
	conn.commit()
	currObject.showObject(cursor)
	print TextColors.RESET

def resolveAlias(alias):
	sql = "SELECT payload FROM objects WHERE title='"+alias+"' AND dataType='alias.node' LIMIT 1"
	cursor.execute(sql)
	data = cursor.fetchone()
	currObject.loadObject(cursor,data[0])
	currObject.showObject(cursor)	

# main loop

done = 0
currObject = godobject.GODObject()

while (done < 1): 
	if (currObject.objectID < 1):
		currObject.loadObject(cursor,1)
	#currObject.showObject(cursor)
	# allow for input
	inStr = str(raw_input(TextColors.BOLD+TextColors.BLUE+'Command (? for help): '+TextColors.RESET))
	
	workStr = inStr.split()
	# parse input
	if (workStr[0].lower() == 'quit'):
		done = 1
	elif (inStr[0] == '?'):
		printHelp()
	elif (inStr[0] == '.'):
		resolveAlias(inStr)
	elif (inStr[0] == '0'):
		currObject.loadObject(cursor,int(inStr))
		currObject.showObject(cursor)
	elif (workStr[0].lower() == 'add'):
		addChild()
	elif ((workStr[0].lower() == 'jump')|(workStr[0].lower() == 'j')):
		currObject.loadObject(cursor,int(workStr[1]))
		currObject.showObject(cursor)
	elif (workStr[0].lower() == 'link'):
		if (workStr[1].lower() == 'parent'):
			# linking this object as parent
			sql = "INSERT INTO links VALUES ("+str(currObject.objectID)+","+workStr[2]+")"
		else:
			# linking this object as a child
			sql = "INSERT INTO links VALUES ("+workStr[1]+","+str(currObject.objectID)+")"
		cursor.execute(sql)
		conn.commit()
		currObject.showObject(cursor)
	elif (workStr[0].lower() == 'new'):
		newNode()
	elif (workStr[0].lower() == 'payload'):
		changePayload()
	elif ((workStr[0].lower() == 's')|(workStr[0].lower() == 'search')):
		search(inStr)
	elif (workStr[0].lower() == 'show'):
		currObject.showObject(cursor)
	elif (workStr[0].lower() == 'title'):
		changeTitle()
	elif (workStr[0].lower() == 'unlink'):
		if (workStr[1].lower() == 'parent'):
			sql = "DELETE FROM links WHERE parentID="+workStr[2]+" AND childID="+str(currObject.objectID)
		else:
			sql = "DELETE FROM links WHERE parentID="+str(currObject.objectID)+" AND childID="+workStr[1]
		cursor.execute(sql)
		conn.commit()
	else:
		print TextColors.BOLD+TextColors.RED+"Invalid command, use '?' for help"+TextColors.RESET
conn.close()

