import time
from textcolors import TextColors

# object class definition
class GODObject:
	objectID = 0
	title = ''
	payload = ''
	dataType = ''
	createDate = '00000000000000'
	lastModified = '00000000000000'
	parents = []
	children = []

	def loadObject(self,cursor,id):
		sql = 'SELECT * FROM objects WHERE objectID='+str(id)+' LIMIT 1'
		cursor.execute(sql)
		data = cursor.fetchone()
		self.objectID = data[0]
		self.title = data[1]
		self.payload = data[2]
		self.dataType = data[3]
		self.createDate = data[4]
		self.lastModified = data[5]
		return 1


	def saveObject(self,cursor):
		self.lastModified = time.strftime('%Y%m%d%H%M%S')
		if (self.objectID > 0):
			# we are updating, not inserting
			sql = "UPDATE objects SET title='"+self.title+"',payload='"+self.payload+"',dataType='"+self.dataType+"',createDate='"
			sql += self.createDate+"',lastModified='"+self.lastModified+"' WHERE objectID="+str(self.objectID)+" LIMIT 1;"
		else:
			# we are inserting a new record
			self.createDate = self.lastModified
			sql = "INSERT INTO objects (title,payload,dataType,createDate,lastModified) VALUES ('"
			sql += self.title+"','"+self.payload+"','"+self.dataType+"','"+self.createDate+"','"+self.lastModified+"');"

		cursor.execute(sql)
		#print sql
		return 1

	def showObject(self, cursor):
		self.parents = []
		self.children = []

		print "=========================================================="
		# insert code here to show parents
		self.loadParents(cursor)
		print TextColors.GREEN+"[Parent Nodes]"
		for p in self.parents:
			print TextColors.GREEN+"\t["+p[0]+"] "+TextColors.BOLD+p[1]+TextColors.RESET
		print
		print TextColors.RED+"["+TextColors.BOLD+TextColors.BLACK+str(self.objectID)+TextColors.RESET+TextColors.RED+"] "+TextColors.BOLD+self.title
		print TextColors.RESET+TextColors.RED+"---------------------------------------------------"+TextColors.RESET
		print self.payload
		print 
		print TextColors.BOLD+TextColors.BLACK+"Created: "+self.createDate+" / Last Modified: "+self.lastModified+TextColors.RESET
		print
		print TextColors.BLUE+"[Child Nodes]"+TextColors.RESET

		# insert code here to show child nodes
		counter = 0
		self.loadChildren(cursor)
		for c in self.children:
			print TextColors.CYAN+"\t["+c[0]+"]\t"+TextColors.BOLD+TextColors.WHITE+c[1]+TextColors.RESET+": "+c[2]
		print "=========================================================="

	def loadParents(self, cursor):
		sql = "SELECT objects.* FROM objects JOIN links ON objects.objectID=links.parentID WHERE links.childID="+str(self.objectID)+" LIMIT 10"
		data = cursor.execute(sql)
		for row in data:
			self.parents.append((str(row[0]),row[1]))
 
	def loadChildren(self, cursor):		
		sql = "SELECT objects.* FROM objects JOIN links ON objects.objectID=links.childID WHERE links.parentID="+str(self.objectID)+" ORDER BY title ASC LIMIT 50"
		data = cursor.execute(sql)
		for row in data:
			self.children.append((str(row[0]),row[1],row[2]))
