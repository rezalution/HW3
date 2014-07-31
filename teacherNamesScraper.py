import urllib2
from bs4 import BeautifulSoup
from fill_tables import *
import random
import re
import string
import time
import sys, json

def main():

    # Load the data that PHP sent us
    data = ''
    try:
    #data = json.loads(sys.argv[1])
        data = sys.argv[1]
    except:
        print "ERROR"
        sys.exit(1)

    #if the data sent is to testJSON, let's do that, and send it back
    if data == "testJSON":
    	onidArray = []
    	onidArray = sys.argv[2].split(',')
        #result = {sys.argv[2]:sys.argv[3],sys.argv[4]:sys.argv[5]}
       	result = {'onid':[onidArray[0],onidArray[1], onidArray[2]],
       	 'startAvailability':[sys.argv[3],sys.argv[3], sys.argv[3]],
       	 'endAvailability':[sys.argv[4],sys.argv[4], sys.argv[4]] }
        #result = {'status': 'testJSON!'}
        print json.dumps(result)
    	
    elif data == "resetPeopleDatabase":
        result = {'status': 'reloading people database!'}
        print json.dumps(result)
        time.sleep(1)
        refillPeopleDatabase()
    
    else:
        result = {'status': 'not working'}
        print json.dumps(result)


def refillPeopleDatabase():
    #connect to database
    db = sqlite3.connect('catalogue.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor()


    #Delete previous test data
    cursor.execute('''DELETE FROM dept ''')
    cursor.execute('''DELETE FROM person ''')




    #this is where we are sending the converted names
    linkPrepend = "http://directory.oregonstate.edu/?type=search&cn="
    linkPostPend = "&affiliation=employee"

    #need to do this for each letter of alphabet
    for y in range(25):
        #convert to ascii capital letter, starting with A
        letter = chr(y + 65)

        soup = BeautifulSoup(urllib2.urlopen('http://catalog.oregonstate.edu/FacultyList.aspx?id=' + letter).read())
        #grab the table that contains all of the tables of info for each teacher
        myTable = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_dlDegreeList"})


        #get all the spans
        teacherNames = []
        for x in range(len(myTable.findAll("span"))):

            #need to make it start at "00", instead of just calling that "0"
            spacer = ""
            if x < 10:
                spacer = "0"


            #this web page increments where the spacer and str(x) is
            id = "ctl00_ContentPlaceHolder1_dlDegreeList_ctl" + spacer + str(x) +"_Label"+"5"
            name = myTable.find("span", {"id": id})
            dept = myTable.find("span", {"id": "ctl00_ContentPlaceHolder1_dlDegreeList_ctl" + spacer + str(x) +"_Label"+"6" })
            #add name if we got one
            if name:
                #teacherNames.append(name.contents)

                #some pages store it in a font spot, others, just in the span
                if name.font:
                    nameString = str(name.font.contents)
                else:
                    nameString = str(name.contents)

                #remove last two characters that are "']"
                nameString = nameString[2:-2]

                #%2C is how the browser represents a comma
                #some names have a pr
                nameString = nameString.replace(',', "%2C")
                nameString = nameString.replace(" ", "+")
                nameString = nameString.replace("'", "")




                #without department
                soup2 = BeautifulSoup(urllib2.urlopen(linkPrepend + nameString + linkPostPend).read())
                myTable2 = soup2.findAll("dd")


                #we may need department for searching, but we will need it for adding later.
                department = re.sub(r'[^a-zA-Z\, @.]', '', str(dept.contents))
                department = department.split(",") #split on the comma
                #now we have to get the last index, and strip the word "font" off
                department = department[len(department)-1][1:-4] #only the last part was the real department
                #print department

                if len(myTable2) < 1:
                    #this means that we returned more than 1 result, so we will add department info
                    deptString = department.replace(" ", "+")
                    deptString = deptString.replace("'", "")
                    deptString = deptString.replace("/", "+%2F+")
                    deptString = "&osudepartment=" +deptString
                    soup2 = BeautifulSoup(urllib2.urlopen(linkPrepend + nameString + deptString+ linkPostPend).read())
                    myTable2 = soup2.findAll("dd")

                #if it's still broken, just print the link and move on... fix later?
                if len(myTable2) < 1:
                    print linkPrepend + nameString + deptString+ linkPostPend
                    continue


                #alright now we have good data. Let's write that to the db
                splitName = re.sub(r'[^a-zA-Z\, ]', '', str(myTable2[0].contents)) #strip all but the comma
                splitName = splitName.split(",") #split on the comma
                #print splitName[0][1:] #print the first name (the u is not stripped above)
                #print splitName[1][1:] #print last name, starting after space

                if myTable2[len(myTable2)-2].find("a"):
                    email = re.sub(r'[^a-zA-Z\, @.]', '', str(myTable2[len(myTable2)-2].a.contents)) #strip away wrapper
                #print email[1:] #strips the u

                else:
                    email = ""
                #print "No Email"

                onid = re.sub(r'[^a-zA-Z\, @.]', '', str(myTable2[len(myTable2)-1].contents))
                #print onid[1:]

                #add to database
                #look to see if this department exists already. If not, add it
                cursor.execute('''SELECT rowid, name FROM dept WHERE name = ?''', (department,))
                deptTest = cursor.fetchall()
                if len(deptTest) == 0:
                    deptFill(db, department)

                #To avoid duplicate names, we will query the db before setting
                cursor.execute('''SELECT dept_id, firstName, lastName, onid, email FROM person WHERE firstName=? AND lastName=? AND onid=? AND  email= ?''', (splitName[1][1:], splitName[0][1:], onid[1:], email[1:],))
                personTest = cursor.fetchall()

                if len(personTest) == 0: #there are no entries identical to this, add
                    personFill(db, splitName[1][1:], splitName[0][1:], onid[1:], email[1:], department)

    db.close()



#fill dept table
#dept_name is text
def deptFill(db, dept_name):
	try:
		cursor = db.cursor()
		cursor.execute('''INSERT INTO dept(name) VALUES(?)''', (dept_name,))
		db.commit()
	except:
		db.rollback()
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return

#fills person table
#first_name, last_name, p_onid, p_email, p_dept are text
def personFill(db, first_name, last_name, p_onid, p_email, p_dept):
	try:
		cursor = db.cursor()
		cursor.execute('''INSERT INTO person (dept_id) SELECT rowid FROM dept WHERE name = ? ''', (p_dept,))
		db.commit()
		cursor.execute('''UPDATE person SET firstName = ?, lastName = ?, onid = ?, email = ? WHERE rowid = ? ''', (first_name, last_name, p_onid, p_email, cursor.lastrowid,))
		db.commit()
	except:
		db.rollback()
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return


if __name__ == '__main__':
	main()
