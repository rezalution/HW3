from datetime import datetime

#this stores the class start and end date/times so we can find events start/end times
class TimeClass:
	def __init__(self, start, end = None):
		self.start = start
		self.end = end
		
	def getEnd(self):
		return self.start
		
	def getStart(self):
		return self.end
