import sys, os, pickle

"""
ImportExistingUser

Iterates through the User directory and parses the line to create an array. Then
appends the list into a userList which is returned at the end.
"""
def ImportExistingUser():
    userList = [] # create a user list

    # check if the users directory exists, if it does then return the list
    if os.path.isdir("Users") == True:
        # iterate files in Users
        for filenames in os.listdir("Users"):
            # return all the lines into an array 
            filepath = os.path.join("Users", filenames)
            file = open(filepath, 'r')
            line = file.readlines()
            no_newlines = list(map(lambda a: a.replace('\n', ''), line))
            
            # return the user list
            userList.append(no_newlines)  
        return userList 
    else: # return the blank list
        return []  

""" 
UserExists

Iterates the userList and checks if the user (from the argument) exists in the user
list.
"""
def UserExists(user, userList):
    # iterate all the users in the userList
    for users in userList:
        # if the user exists then return true
        if user == users[0]:
            return True

    # return false if it doesn't exist
    return False

"""
AddUser 

Define a user and password for the system.
"""
def AddUser(user, password):

    # check if the user is a valid string -> invalid username
    if user == "":
        print("Error: username missing")
        sys.exit(-1)

    # add to list if Users directory wasn't created
    if os.path.isdir("Users") == False:
        os.mkdir("Users")
        f = open("{}.txt".format("Users/"+user), "w")
        f.write("{}\n{}\n".format(user, password))
        f.close()
        print("Success")
        sys.exit(0)

    userList = ImportExistingUser() # import all the users in the directory

    # if user is in userlist, return error
    if UserExists(user, userList):
        print("Error: user exists")
        sys.exit(-1)

    # add user to user's directory
    if (user != "" or user != None) and password != None:
        f = open("{}.txt".format("Users/"+user), "w")
        f.write("{}\n{}\n".format(user, password))
        f.close()
        print("Success")
        sys.exit(0)
    else:
        print("Error: invalid username or password combination")
        sys.exit(-1)

""" 
ValidatePassword

Returns the user and there password.
"""
def ValidatePassword(user, userList):
    # iterate the userlists
    for users in userList:
        # if the password exists then that means the password is validated
        if user == users[0]:
            return users

    # if it returns false that would mean its invalidated
    return None

"""  
Authenticate

Validate the user's password given the user and password.
"""
def Authenticate(user, password): 

    # check if user exists
    userList = ImportExistingUser() # import all the users in the directory

    # check if the user actually exists
    if UserExists(user, userList) == False:
        print("Error: no such user")
        sys.exit(-1)

    # now we know the user exists so we can check for a bad password
    users = ValidatePassword(user, userList)

    # check if the user actually returned something
    if users != None:
        # check the password of the user
        if users[1] == password:
            print("Success")
        else:
            print("Error: bad password")
            sys.exit(-1)
    else: # the user doesn't exist otherwise
        print("Error: no such user")
        sys.exit(-1)

"""  
UpdateUsers

Update the directory of user's information.
"""
def UpdateUsers(userList):
    # iterate the userlist
    for user in userList:
        # for each user's file lets start updating
        f = open("{}.txt".format("Users/"+user[0]), "w")
        # iterate the userlist index and update
        for i in range(len(user)):
            f.write("{}\n".format(user[i]))
        f.close()
    
    # return true just for success
    return True

"""  
SetDomain

Set the domain for the user belongs to.
"""
def SetDomain(user, domain_name):
    
    # check if domain name is an empty string
    if domain_name == '':
        print("Error: missing domain")
        sys.exit(-1)

    # check if the user exists
    userList = ImportExistingUser()

    if UserExists(user, userList) == False:
        print("Error: no such user")
        sys.exit(-1)

    # Check if the domain exists for the user -> if it does update the user lists otherwise dont
    for i in range(len(userList)):
        conditional = (0 <= 2) and (2 < len(userList[i]))
        if conditional == False:
            userList[i].append(domain_name)
        else:
            domains = userList[i][2:]
            if domain_name in domains:
                break
            else:
                userList[i].append(domain_name)

    # Update the user list if needed
    UpdateUsers(userList)    
    print("Success")

"""  
ParseDomains

Get all the domains the user belongs too.
"""
def ParseDomains(userList):
    domains = {} # will contain domains information for users

    # iterate the user list
    for user in userList:
        # get all the domains in the user
        domain_list = user[2:]
        # iterate the domain list you made
        for i in range(len(domain_list)):
            # if the domain doesn't exist make list
            if domain_list[i] not in domains:
                domains[domain_list[i]] = []
                domains[domain_list[i]].append(user[0])
            else: # otherwise just append
                domains[domain_list[i]].append(user[0])
    
    # return the domains dictionary at the end
    return domains

"""  
DomainInfo

Get all the users in that domain.
"""
def DomainInfo(domain_name):

    # check if domain is an empty string
    if domain_name == "":
        print("Error: missing domain")
        sys.exit(-1)

    # import the current userList and parse the domains based on the user list
    userList = ImportExistingUser()
    domains = ParseDomains(userList)

    # check from imported domains if the domain exists, otherwise don't print anything
    if domain_name in domains:
        domains_list = domains[domain_name]
    else:
        domains_list = []
    
    # print the info from the requested domain_name
    for user in domains_list:
        print(user)

"""  
ExtractTypes

Extract all the files in the type.
"""
def ExtractTypes(directory):
    types = [] # store the types into a list
    filenames = next(os.walk(directory), (None, None, []))[2] # get all the files in the directory
    
    # iterate all the files in the directory
    for file in filenames:
        # extract the type so replace the .txt with ""
        type_ext = file.replace(".txt", "")
        types.append(type_ext) # append to the types list

    # return the types at the end
    return types

"""
LoadObjects

Load the objects from the pickle file.
"""
def LoadObjects():
    # Create an ACM list
    objects = []

    # extract the previous ACM from storage
    if os.path.exists('objects.pkl') == True:
        with open('objects.pkl', 'rb') as f:
            objects = pickle.load(f)

    # return acm
    return objects

"""  
SetType

Set the type for the given object and type.
"""
def SetType(objectname, type):
    
    # check if objectname is a empty string or if type is a empty string
    if objectname == "":
        if type == "":
            print("Error: did not provide a valid object name and type")
            sys.exit(-1)
        else:
            print("Error: did not provide a object name")
            sys.exit(-1)

    # check if the type is an empty string
    if type == "":
        print("Error: did not provide a valid type name")
        sys.exit(-1)

    # create types directory, if it doesn't exist then continues
    if os.path.isdir("Type") == False:
        os.mkdir("Type")
    
    # checks now if the type exists or not (each file .txt is the type) -> i.e: music.txt (type = music)
    
    # Extract all the types and the objects created, if it isn't created they will be blank for their respective type
    types = ExtractTypes("Type")
    objects = LoadObjects()

    # if the type doesn't exist create it otherwise just add on too the type
    if type not in types:
        # write to file
        f = open("{}.txt".format("Type/"+type), "w")
        f.write("{}\n".format(objectname))
        f.close()  
    else:
        f = open("{}.txt".format("Type/"+type), "a")
        f.write("{}\n".format(objectname))
        f.close()
    
    # if the objects list isn't created yet, then start adding to it
    if objects == []:
        # write an object list of list
        types = []
        types.append(type)
        objLst = {objectname: types}
        objects.append(objLst)
    else: # otherwise perform an update to the objects list
        for i in range(len(objects)):
            if objectname in objects[i]:
                if type not in objects[i][objectname]:
                    objects[i][objectname].append(type)
            else:
                types = []
                types.append(type)
                objects[i][objectname] = types

    # store the objects into memory
    with open('objects.pkl', 'wb') as f:
        pickle.dump(objects, f)

    # print success
    print("Success")

"""  
FilesInType

Get the list of files in the type.
"""
def FilesInType(filename):

    # get the file from the Type directory
    file = open("Type/{}.txt".format(filename), 'r')
    # break the lines of the file into an array
    line = file.readlines()
    # get rid of any newline escape characters
    files = list(map(lambda a: a.replace('\n', ''), line))

    # return files at the end
    return files

"""  
TypeInfo

Get all the files within the given type.
"""
def TypeInfo(type):
    
    # if the type is empty return an error
    if type == "":
        print("Error: no valid type name given")
        sys.exit(-1)

    # Check if the type exists
    types = ExtractTypes("Type")

    # check if the type is in types list
    if type not in types:
        return []

    # now check for anything in the types file
    files = FilesInType(type)

    # print out all the files
    for file in files:
        print(file)

"""  
LoadACM

Load the Access Control Matrix from memory.
"""
def LoadACM():
    # Create an ACM list
    acm = []

    # extract the previous ACM from storage
    if os.path.exists('acm.pkl') == True:
        with open('acm.pkl', 'rb') as f:
            acm = pickle.load(f)

    # return acm
    return acm

"""  
AddAccess

Add an control list too the access control matrix given operation, domain name and type name.
"""
def AddAccess(operation, domain_name, type_name):

    # check if operation, domain name or type name is an empty string
    if operation == "":
        print("Error: operation is not given")
        sys.exit(-1)
    elif domain_name == "":
        print("Error: domain name is not given")
        sys.exit(-1)
    elif type_name == "":
        print("Error: type name is not given")
        sys.exit(-1)

    # check if the domain exists if it doesn't add the domain
    userList = ImportExistingUser()
    domains = ParseDomains(userList)
    domain_list = []
    if domain_name in domains:
        domain_list.append(domain_name)
    
    # store the list into memory
    with open('domains.pkl', 'wb') as f:
        pickle.dump(domain_list, f)

    # check if the type_name exists, if it doesn't add it
    types = ExtractTypes('Type')
    if type_name not in types:
        types.append(type_name)

    # store the list into memory
    with open('types.pkl', 'wb') as f:
        pickle.dump(types, f)

    # now load the acm from memory or create a new one
    acm = LoadACM()

    # create a control list from the arguments given
    cl = dict({operation: (domain_name, type_name)})
    if cl not in acm:
        acm.append(cl)

    # store the acm into memory
    with open('acm.pkl', 'wb') as f:
        pickle.dump(acm, f)

    # print success on updating acm
    print("Success")

"""  
CanAccess

Check if the user can access an object given the operation and object.
"""
def CanAccess(operation, user, object):

    # check if all the arguments are valid 
    if operation == "":
        print("Error: access denied")
        sys.exit(-1)
    elif user == "":
        print("Error: access denied")
        sys.exit(-1)
    elif object == "":
        print("Error: access denied")
        sys.exit(-1)

    # get the userList
    userList = ImportExistingUser()
    
    # check if the user exists
    if UserExists(user, userList) == False:
        print("Error: access denied")
        sys.exit(-1)

    # import objects 
    objects = LoadObjects()

    # import the Access Control Matrix
    acm = LoadACM()
    
    """ 
    Check if the user can access 
    """

    # create variables to use later
    accessPermission = False
    operationExists = False
    currUser = None
    
    # create an instance of the current user from the userList
    for users in userList:
        if user == users[0]:
            currUser = users
            break

    # if the current user isn't there, then something went wrong
    if currUser == None:
        print("Error: access denied")
        sys.exit(-1)

    # get all the object types given the objectname
    objTypes = None
    for i in range(len(objects)):
        for key in objects[i]:
            if key == object:
                objTypes = objects[i][key]

    # check if the objTypes is null
    if objTypes == None:
        print("Error: access denied")
        sys.exit(-1)

    # now finally check if the user can access the file
    for i in range(len(acm)):
        if operation in acm[i]:
            operationExists = True
            if acm[i][operation][0] in currUser[2:] and acm[i][operation][1] in objTypes:
                accessPermission = True # granted
                break

    # now given the boolean statements from before return the correct message
    if accessPermission == True:
        print("Success")
        sys.exit(0)
    elif operationExists == False:
        print("Error: access denied")
        sys.exit(-1)
    else:
        print("Error: access denied")
        sys.exit(-1)

"""  
Main 

The application starting point.
"""
if __name__ == "__main__":
    
    # iterate through all the possible commands for the API
    if sys.argv[1] == "AddUser": # Add a User
        # check if a valid amount of arguments was given
        if len(sys.argv) != 4:
            print("Error: missing arguments for AddUser")
            sys.exit(-1)
        AddUser(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "Authenticate": # Authenticate a Password
        # check if a valid amount of arguments was given
        if len(sys.argv) != 4:
            print("Error: missing arguments for Authenticate")
            sys.exit(-1)   
        Authenticate(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "SetDomain": # Set a user to a domain
        # check required amount of arguments
        if len(sys.argv) != 4: 
            print("Error: missing arguments for SetDomain")
            sys.exit(-1)
        SetDomain(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "DomainInfo": # Check the info of a domain
        # check the number of arguments
        if len(sys.argv) != 3:
            print("Error: missing arguments for DomainInfo")
            sys.exit(-1)
        DomainInfo(sys.argv[2])
    elif sys.argv[1] == "SetType": # Set the type of an object
        # check the number of arguments given
        if len(sys.argv) != 4:
            print("Error: missing arguments for SetType")
            sys.exit(-1)
        SetType(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "TypeInfo": # Check the info for a specific type
        # check the number of arguments
        if len(sys.argv) != 3:
            print("Error: missing arguments for TypeInfo")
            sys.exit(-1)
        TypeInfo(sys.argv[2])
    elif sys.argv[1] == "AddAccess": # Add a control list to the ACM
        # check the number of arguments given
        if len(sys.argv) != 5:
            print("Error: missing arguments for AddAccess")
            sys.exit(-1)
        AddAccess(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "CanAccess": # Check if a user can access an object
        # check the number of arguments given
        if len(sys.argv) != 5:
            print("Error: missing arguments for CanAccess")
            sys.exit(-1)
        CanAccess(sys.argv[2], sys.argv[3], sys.argv[4])
    else: # If you go through everything, simply return invalid command
        print("Error: invalid command")
        sys.exit(-1)