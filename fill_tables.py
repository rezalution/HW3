import sqlite3
import sys

#db is the the open database file

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

#fills course table
#c_title, c_fisrt_name, c_last_name are text
#c_section is int
def courseFill(db, c_title, c_section, c_first_name, c_last_name):
	try:
		cursor = db.cursor()
		cursor.execute('''INSERT INTO course (dept_id, person_id) SELECT dept_id, rowid FROM person WHERE firstName = ? AND lastName = ? ''', (c_first_name, c_last_name,))
		db.commit()
		cursor.execute('''UPDATE course SET title = ?, section = ? WHERE rowid = ?''', (c_title, c_section, cursor.lastrowid,))
		db.commit()
	except:
		db.rollback()
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return

#m_start_time and m_end_time are timestamp
#m_week_day is text
def meetingTimesFill(db, m_start_time, m_end_time, m_week_day):
	try:
		cursor = db.cursor()
		cursor.execute('''INSERT INTO meetingTimes (start_time, end_time, week_day) VALUES (?,?,?)''', (m_start_time, m_end_time, m_week_day,))
		db.commit()
	except:
		db.rollback()
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return

#c_title, m_week_day are text
#c_section is int
#m_start_time, m_end_time are timestamp
#cm_start_date, cm_end_date are date
def courseMeetingTimesFill(db, c_title, c_section, m_start_time, m_end_time, m_week_day, cm_start_date, cm_end_date):
	try:
		cursor = db.cursor()
		cursor.execute('''SELECT rowid FROM course WHERE title = ? AND section = ?''', (c_title, c_section,))
		c_id = cursor.fetchone()
		#convert to int
		c_id = int(c_id[0])
		cursor.execute('''SELECT rowid FROM meetingTimes WHERE start_time = ? AND end_time = ? AND week_day = ?''', (m_start_time, m_end_time, m_week_day,))
		m_id = cursor.fetchone()
		#convert to int
		m_id = int(m_id[0])
		cursor.execute('''INSERT INTO courseMeetingTimes(course_id, meeting_times_id, start_date, end_date) VALUES (?,?,?,?) ''',(c_id, m_id, cm_start_date, cm_end_date,))
		db.commit
	except:
		db.rollback()
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return
