import json
import re
import copy

import pythondb.errors as errors
import pythondb.simpleFileManager as files

def createDatabase(name, uniqueFields=[], nonUniqueFields=[], rows=[]):
    # (public)

    db = {
        'name' : name,
        'uniqueFields' : copy.deepcopy(uniqueFields),
        'nonUniqueFields' : copy.deepcopy(nonUniqueFields),
        'rows' : []
    }
    # Add the rows here one by one, to use the inbuilt error checker in appendRow()
    for row in rows:
        appendRow(db, copy.deepcopy(row))
    return db

# File stuff
# ----------

def openDatabase(filename):
    # Open and load the database at filename, return it as an object

    # Read the file

    # This try-except-finally is not needed as of now
    # as the only error which is expected doesn't get caught,
    # but it will make for easier modification in future

    stringData = '{}' # safeguard in case there is a case which slips through
    try:
        stringData = files.read(filename)
    # no except block - let whatever error has occured break out of this function
    # a finally block is needed here to make syntax correct
    finally:
        pass
    
    # Parse the file

    try:
        database = json.loads(stringData)
        return database
    except json.decoder.JSONDecodeError as err:
        raise errors.FileCorrupted from err

def saveDatabase(database, filename=None):
    # Save the database to filename
    # If filename is None, then it will be saved to: [the name of the database] + 'json'

    if filename is None:
        filename = database['name'] + '.json'
    try:
        databaseStr = json.dumps(database)
        files.write(filename, databaseStr)
    except:
        raise

# Get stuff
# ---------

def getDatabaseName(database):
    # (public)
    return database['name']

def fieldPathToDirectoryList(fieldPath):
    # Turn the field path into a list of directions
    # (private)

    return re.split('(?<!\\\)[/]', fieldPath)

def getFieldContents(row, fieldPath=None, directoryList=None):
    # Get the contents of the field at fieldPath in row
    # Pass in either a fieldPath or a directoryList
    # (public)
    try:
        if directoryList is None:
            directoryList = fieldPathToDirectoryList(fieldPath)
        crntDir = row
        for item in directoryList:
            crntDir = crntDir[item]
        return crntDir
    except Exception as err:
        raise errors.InvalidFieldPath from err

def getColumn(database, fieldPath):
    # Get a list of all of the items in the fieldPath column
    # (public)
    if (fieldPath not in database['uniqueFields']) and \
        (fieldPath not in database['nonUniqueFields']):
        raise errors.InvalidFieldPath

    column = []
    for crntRow in database['rows']:
        column.append(getFieldContents(crntRow, fieldPath=fieldPath))
    
    return column

def getRowByUniqueField(database, fieldPath, fieldValue):
    # Find the row which has fieldPath set to fieldValue
    # (public)

    # If the field doesn't exist, exit
    if fieldPath not in database['uniqueFields']:
        raise errors.InvalidFieldPath

    row = None

    for crntRow in database['rows']:
        if getFieldContents(crntRow, fieldPath=fieldPath) == fieldValue:
            row = crntRow
            break
    
    return row

        
def getRowsByField(database, fieldPath, fieldValue):
    # Find all of the fields in which fieldPath is set to fieldValue
    # (public)
    
    # If the field doesn't exist, exit
    if fieldPath not in database['nonUniqueFields']:
        raise errors.InvalidFieldPath

    rows = []
    for crntRow in database['rows']:
        if getFieldContents(crntRow, fieldPath) == fieldValue:
            rows.append(crntRow)
    
    return rows

# Set stuff
# ---------

def setDatabaseName(database, newName):
    # (public)
    database['name'] = newName

def setFieldValue(database, row, fieldPath, fieldValue):
    # (public)
    # set the value of the field at row in database
    if fieldPath in database['uniqueFields']:
        existingValues = getColumn(database, fieldPath)
        if fieldValue in existingValues:
            raise errors.FieldDuplicated
        else:
            # Navigate to the dir containing the field
            directoryList = fieldPathToDirectoryList(fieldPath)
            containingDir = getFieldContents(row, directoryList=directoryList[:-1])
            # Then set the last part (the actual field) to the value
            containingDir[directoryList[-1]] = fieldValue
            
    elif fieldPath in database['nonUniqueFields']:
        directoryList = fieldPathToDirectoryList(fieldPath)
        containingDir = getFieldContents(row, directoryList=directoryList[:-1])
        containingDir[directoryList[-1]] = fieldValue
    else:
        raise errors.InvalidFieldPath

# Add stuff
# ---------

def createRow(database, rowContents):
    # Row contents is in the form:
    # {
    #   fieldPath : value,
    # }
    # eg:
    # {
    #   'username' : 'james',
    #   'password' : 123
    # }
    # Note that this does not add the row to the database, use appendRow() for that
    # (public)

    row = {}
    # Set the keys and values of the row object
    for fieldPath in rowContents:
        # Check if the fieldPath is a valid field
        if fieldPath in database['uniqueFields'] or \
            fieldPath in database['nonUniqueFields']:
            setFieldValue(database, row, fieldPath, rowContents[fieldPath])
        else:
            raise errors.InvalidFieldPath
    
    # Now check if the row has any duplicate unique fields
    if not canAddRow(database, row):
        raise errors.FieldDuplicated
    
    return row

def appendRow(database, row):
    # Append the row to the database
    # (public)
    
    if canAddRow(database, row):
        database['rows'].append(row)
    else:
        raise errors.FieldDuplicated

def insertRow(database, row, index=-1):
    # Insert the row into the database at index
    # If index is unspecified, append it to the end
    # (public)
    
    if canAddRow(database, row):
        database['rows'].insert(index, row)
    else:
        raise errors.FieldDuplicated

# Other
# -----

def canAddRow(database, row):
    # Check whether the values any of the row's unique fields are already in the database
    # (private)

    noDuplicateFields = True
    for fieldPath in database['uniqueFields']:
        column = getColumn(database, fieldPath)
        if getFieldContents(row, fieldPath=fieldPath) in column:
            noDuplicateFields = False
            break
    
    return noDuplicateFields

def removeRow(database, row=None, index=None):
    # If row is specified, remove it from the db
    # If index is specified, remove the row at index
    # (public)

    if row is not None:
        database['rows'].remove(row)
        del row # clear up
    
    elif index is not None:
        del database['rows'][index]
        del row # clear up
    
    else:
        raise errors.NoRowProvided