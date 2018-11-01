#NEA Task 1 Sample#
#Author: William Lau#

#Here I have imported several libraries  which will be used
#os and sys are used to check file paths
#datetime is used to validate DOB
#re is used to validate the phone numbers against regular expressions
#time is used to add a delay before exiting

import os,sys,datetime,re,time

def genderFunction():
    #Validating the gender
    genderIn=input("Enter gender: M or F").upper()
    if genderIn == "M" or genderIn == "F":
        return genderIn
    else:
        print("Invalid input")
        return genderFunction()              
    

def usernameFunction(userIn):
    #By checking the existing students, we avoid duplicate IDs. A simple append of # ensures that all IDs are unique
    userOut=userIn
    with open ("students.txt","r") as studentFile: 
        for line in studentFile:
            if userIn in line:
                userOut=userIn+"#"
                for line in studentFile:
                    if userOut in line:
                        userOut=userOut+"#"
            else:
                userOut=userIn
    return userOut

def dobFunction():
    #This checks that the DOB is in a valid format
    try:
        dobRaw=input("Enter their DOB in the DD/MM/YYYY format")
        dobOut=datetime.datetime.strptime(dobRaw, "%d/%m/%Y").date()
        return dobOut
    except:
        print("Please enter a valid DOB")
        return dobFunction()

def phoneFunction():
    #I used www.regexlib.com to find the patterns for UK landlines and mobiles
    ukphone="^((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$"
    ukmobile="^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$"
    phoneNumRaw=input("Enter their phone number")
    #If the inputted number matches either pattern it is valid, otherwise they are asked to re-enter
    if re.match(ukphone,phoneNumRaw) or re.match(ukmobile,phoneNumRaw):
        #print("valid")
        return phoneNumRaw
    else:
        print("Please enter a valid phone number")
        return phoneFunction()
    

def enterStudentDetailsProcedure():
    firstname=input("What is the student's firstname?").title()
    surname=input("What is the student's surname?").title()
    #Check if the DOB is valid
    dob = dobFunction()
    dobString=str(dob)
    address1=input("Enter the first line of the address")
    address2=input("Enter the second line of the address")
    postcode=input("Enter the postcode")
    phoneNum=phoneFunction()
    gender=genderFunction()
    tutorGroup=input("Enter their tutor group")

    #We pass an intial uniqueID to a function which checks if it already exists
    #The uniqueID is generated based on the user's name and DOB. We sliced only two letters
    #as some (Chinese) names are quite short e.g. Bo Li 
    initialUniqueID=(firstname[:2]+surname[:2]+dobString[2:4]+dobString[5:7])
    uniqueID=usernameFunction(initialUniqueID)
    email=(uniqueID+"@TRS.sch.uk")
    print("This is their unique ID",uniqueID,"and this is their email",email)
    
    studentDetails=str('["'+uniqueID+'","'+email+'","'+firstname+'","'+surname+'","'+dobString+'","'+address1+'",\
"'+address2+'","'+postcode+'","'+phoneNum+'","'+gender+'","'+tutorGroup+'"]')

    ##############################################################################################################
    #Check if the file exists, it may not do if you are running this for the first time. The path needs editing###
    ##############################################################################################################
    if not os.path.exists("C:/Users/William/Documents/BCS Cert/students.txt"):####edit this with your own path####
    ##############################################################################################################
        print("Writing new file")
        with open ("students.txt","wt") as newStudentFile:            
            newStudentFile.write(studentDetails)
            print("Written")
    else:
        #After the first time the program is run, we are merely appending a new list on a new line
        #A 2D List could have been implemented instead, however this was the simplest solution
        print("Adding to existing file")
        with open ("students.txt","a") as studentFile:
            studentFile.write("\n"+studentDetails)

def retrieveStudentDetailsProcedure():
    #A boolean flag is created so that invalid usernames are handled with a recursive call back to the procedure
    found=False

    uniqueIdIn=input("Enter a student ID to retrieve their details")

    #We check if the username is in a line and is in an exact match before outputting the student details
    with open ("students.txt","r") as studentFile: 
        for line in studentFile:
            if uniqueIdIn in line:
                studentDetails=eval(line)

                if studentDetails[0]==uniqueIdIn:
                    found=True
                    break
                else:
                    continue
        if found:
            #As studentDetails is a list, I have formatted the output to look more presentable
            print("Username:",studentDetails[0])
            print("Full Name:",studentDetails[2],studentDetails[3])
            print("Form:",studentDetails[10])
            dobOut=studentDetails[4].split("-")
            print("DOB:",dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0])
            print("Gender:",studentDetails[9])
            print("Address:",studentDetails[5],studentDetails[6],studentDetails[7])
            print("Email:",studentDetails[1])
            print("Phone:",studentDetails[8])
        if not found:
            print("User details not found, please check unique ID")
            return retrieveStudentDetailsProcedure()

            
def report1():
    #A table structure is created using the headings for the student details
    print("Username  ","First Name","Surname     ","Form","DOB       ","M/F",\
          "Address 1        ","Address 2   ","Postcode ","Phone")
    
    with open ("students.txt","r") as studentFile:
        for line in studentFile:
            #Each line is read one at a time
            studentDetails=eval(line)

            #Due to datetime formatting, the dob needs reformatting for output
            dobOut=studentDetails[4].split("-")

            #Padding has been created to maintain a table structure
            usernamePad=10-len(studentDetails[0])
            firstnamePad=10-len(studentDetails[2])
            surnamePad=12-len(studentDetails[3])
            add1Pad=17-len(studentDetails[5])
            add2Pad=12-len(studentDetails[6])
            postcodePad=9-len(studentDetails[7])
        
            #Output the data for the table including padding
            print(studentDetails[0]+" "*usernamePad,studentDetails[2]+" "*firstnamePad,studentDetails[3]+" "*surnamePad,\
                  studentDetails[10]+" ",dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0],\
                  studentDetails[9]+" "*2,studentDetails[5]+" "*add1Pad,studentDetails[6]+" "*add2Pad,\
                  studentDetails[7]+" "*postcodePad,studentDetails[8])
                  
def report2():
    #Take a register and output the report
    form=input("Please enter the form you wish to register")
    print("Please use the following codes:\n\
/ -present \n\
N -absent \n\
I -ill \n")
    #Make a list so that a list can be appended within this to create a 2D List
    register=[]
    #Register each student in a given form line by line
    with open ("students.txt","r") as studentFile: 
        for line in studentFile:
            if form in line:
                studentDetails=eval(line)
                dobOut=studentDetails[4].split("-")
                print(studentDetails[2],studentDetails[3],dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0])
                reg=input("Present?")
                #Append the present mark to the student details
                studentDetails.append(reg)
                #Append this to the register list thereby creating a 2D List
                register.append(studentDetails)

    #write the register to a text file with the form and current date            
    now = datetime.datetime.now()
    nowDate=now.strftime("%d-%m-%Y")
    with open (form+"-"+nowDate+".txt","wt") as newRegister:            
        newRegister.write(str(register))
        time.sleep(1)
        print("\nWritten")
        time.sleep(1)
        print("Outputting register \n")

    #Read the register, outputting only the names, DOB and reg mark
    with open (form+"-"+nowDate+".txt","r") as currentRegister:            
        regOut=eval(currentRegister.read())
    present=0
    print("First Name","Surname     ","DOB       ","Present?")
    for count in range(0,len(regOut)):
        firstnamePad=10-len(regOut[count][2])
        surnamePad=12-len(regOut[count][3])
        dobOut=regOut[count][4].split("-")
        
        print(regOut[count][2]+" "*firstnamePad,regOut[count][3]+" "*surnamePad,dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]," "*3,regOut[count][11])
        if regOut[count][11]=="/":
            present=present+1
    print("Attendance percentage",round(present/len(regOut)*100,1),"%")
                           
def report3():
    print("Please ensure all absences are chased up before 12pm")
    form=input("Please enter the form you wish to check for absences")
    
    now = datetime.datetime.now()
    nowDate=now.strftime("%d-%m-%Y")
    
    with open (form+"-"+nowDate+".txt","r") as currentRegister:            
        regOut=eval(currentRegister.read())
    print("\nFirst Name","Surname     ","DOB       ","Present?","Phone")
    for count in range(0,len(regOut)):
        firstnamePad=10-len(regOut[count][2])
        surnamePad=12-len(regOut[count][3])
        dobOut=regOut[count][4].split("-")
        if regOut[count][11]=="N" or regOut[count][11]=="I":
            print(regOut[count][2]+" "*firstnamePad,regOut[count][3]+" "*surnamePad,dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0],\
                  " "*3,regOut[count][11]," "*2,regOut[count][8])
                                            
def loadMenu():
    #The menu is simple with choices from A-G
    print("Choose a task from:\n\
A) Enter and Store Student Details\n\
B) Retrieve and Display Student Details\n\
C) Report 1: Contact Home List\n\
D) Report 2: Today's Register\n\
E) Report 3: Absent or ill List\n\
F) Logout \n\
G) Exit \n")

    #These lists cater for valid responses
    alist=["a","enter and store student details","enter"]
    blist=["b","retrieve and display student details","retrieve"]
    clist=["c","report 1","contact home list","Report 1: Contact Home List"]
    dlist=["d","report 2","today's register","Report 1: today's register"]
    elist=["e","report 3","detention list","Report 1: detention list"]
    flist=["f","logout"]
    glist=["g","exit"]
    #The input is cast to lower case to minimise possible cases in the lists above. Each option is linked to a procedure
    topic=input().lower()
    if topic in alist:
        enterStudentDetailsProcedure()
    elif topic in blist:
        retrieveStudentDetailsProcedure()    
    elif topic in clist:
        report1()
    elif topic in dlist:
        report2()
    elif topic in elist:
        report3()
    elif topic in flist:
        return main()
    elif topic in glist:
        print("Exiting program")
        time.sleep(3)
        exit()
    else:
        print("Invalid input")
        loadMenu()

    logout=input("\n"+"Do you wish to logout").lower()
    if logout == "yes":
        return main()
    else:
        return loadMenu()
        

def loginProcedure(username):
    #An empty array is initialised 
    checkList=["",""]
    #The username is formatted to include speech marks as per the text file
    username2='"'+username+'"'
    #Check if the username exists in any of the lines
    with open ("users.txt","r") as UsersFile:
        for line in UsersFile:
            if username2 in line:
                checkList=eval(line)
    if checkList[0]=="":
        print("Incorrect username")
        main()
    #As the checklist is now populated with the username and password, we can check the password against pos 1 of the list
    password=input("Please enter your password")
    if checkList[1]==password:
        print("logged in")
        #If the login credentials match, load the menu otherwise give a meaningful error message
        return loadMenu()
    else:
        print("incorrect password")
        return loginProcedure(username)
        
def main():    
    
    username=input("Please enter your username")

    #I've passed the username to the loginProcedure as an arguement. If the username is invalid a return call to main is made
    loginProcedure(username)
    
        

main()
    
    
    
