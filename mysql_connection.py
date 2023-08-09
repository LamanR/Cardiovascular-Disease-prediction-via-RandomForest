
## SEALED ##
# 
#: Imports
import mysql.connector

def reConnect(user, password, host, db):
	global cnx
	global mycursor
	#: Create the connection
	cnx = mysql.connector.connect(user = user, password = password, host=host, database =db)
	cnx.autocommit = True
	#: Create the cursor
	mycursor = cnx.cursor()


# method: rowToDict
# Transforms the sql result row to dictionary
# @row, tuple: The input value tuple
# @names, list: The list of names
# @return, dict: The dictionary
# @completed
def rowToDict( row: tuple, names: list ) -> dict:
	#: Declare variables
	output = {}
	index = 0
	#: Loop for each
	for n in names:
		#: Read the value
		output[n] = row[index]
		index += 1
	#: Return the output
	return output

# method: dbExecute
# Executes a statement
# @sql, str: The execution statement
# @params, tuple: Arguments
# @completed 
def dbExecute( sql: str ):
	mycursor.execute( sql )

# method: dbInsert
# Executes an insert statement
# @sql, str: The execution statement
# @params, tuple: Arguments
# @return, int: The row id
# @completed 
def dbInsert( sql: str, params) -> int:
	mycursor.execute( sql, params )
	return int(mycursor.lastrowid)

# method: dbSelect
# Executes a statement for selecting
# @sql, str: The execution statement
# @params, tuple: Arguments
# @return: Output
# @completed
def dbSelect( sql: str ):
    
	mycursor.execute( sql )
	myresult = mycursor.fetchall()
	

	return myresult, [i[0] for i in mycursor.description]
























