#NEA Task 1 Sample#
#Author: William Lau#

#Here I have imported several libraries  which will be used
#os and sys are used to check file paths
#datetime is used to validate DOB
#re is used to validate the phone numbers against regular expressions
#time is used to add a delay before exiting

import os,sys,datetime,re,time
from easygui import *
from tkinter import *            
    

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

def dobFunction(dobRaw):
    #This checks that the DOB is in a valid format
    try:
        dobOut=datetime.datetime.strptime(dobRaw, "%d/%m/%Y").date()
        return dobRaw
    except:
        dobRaw="Invalid"
        return dobRaw

def phoneFunction(phoneNumRaw):
    #I used www.regexlib.com to find the patterns for UK landlines and mobiles
    ukphone="^((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$"
    ukmobile="^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$"
    #If the inputted number matches either patter it is valid, otherwise they are asked to re-enter
    if re.match(ukphone,phoneNumRaw) or re.match(ukmobile,phoneNumRaw):
        #print("valid")
        return phoneNumRaw
    else:
        phoneNumRaw="Invalid"
        return phoneNumRaw
    

def enterStudentDetailsProcedure():
    msg = "Enter a student's details"
    title = "Tree Road School Student Registration"
    fieldNames = ["First name","Surname","Date of Birth (DD/MM/YYYY)","Address 1","Address 2","Postcode","Phone Number",\
                  "Gender (M/F)","Tutor Group"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while True:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
          if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        #Modified functions to check the DOB is valid, passing back the original DOB or "Invalid" which triggers a meaningful error message
        dobCheck=dobFunction(fieldValues[2])
        if dobCheck =="Invalid":
            errmsg =errmsg + ("\nDOB is invalid, please use DD/MM/YYYY")

        #Validation for the phone number and gender    
        phoneCheck=phoneFunction(fieldValues[6])
        if phoneCheck =="Invalid":
            errmsg =errmsg + ("\nPhone number is invalid, please check to make sure it is correct")
            
        if fieldValues[7] not in ["M","F"]:
            errmsg =errmsg + ("\nGender is invalid, please enter M or F")
            
            
        
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    

    #Check if the DOB is valid
    firstname=fieldValues[0]
    surname=fieldValues[1]
    
    

    #We pass an intial uniqueID to a function which checks if it already exists
    #The uniqueID is generated based on the user's name and DOB. We sliced only two letters
    #as some (Chinese) names are quite short e.g. Bo Li 
    initialUniqueID=(firstname[:2]+surname[:2]+dobCheck[8:10]+dobCheck[3:5])
    uniqueID=usernameFunction(initialUniqueID)
    email=(uniqueID+"@TRS.sch.uk")
    msgbox("This is their unique ID: "+uniqueID+" and this is their email: "+email)
    
    dobOut=datetime.datetime.strptime(dobCheck, "%d/%m/%Y").date()
    dobOut=str(dobOut)
    
    studentDetails=str('["'+uniqueID+'","'+email+'","'+firstname+'","'+surname+'","'+dobOut+'","'+fieldValues[3]+'","'\
                       +fieldValues[4]+'","'+fieldValues[5]+'","'+fieldValues[6]+'","'+fieldValues[7]+'","'+fieldValues[8]+'"]')

    ##############################################################################################################
    #Check if the file exists, it may not do if you are running this for the first time. The path needs editing###
    ##############################################################################################################
    if not os.path.exists("C:/Users/William/Documents/BCS Cert/students.txt"):####edit this with your own path####
    ##############################################################################################################
        msgbox("Writing new file")
        with open ("students.txt","wt") as newStudentFile:            
            newStudentFile.write(studentDetails)
    else:
        #After the first time the program is run, we are merely appending a new list on a new line
        #A 2D List could have been implemented instead, however this was the simplest solution
        msgbox("Adding to existing file")
        with open ("students.txt","a") as studentFile:
            studentFile.write("\n"+studentDetails)
    return

def retrieveStudentDetailsProcedure():
    #A boolean flag is created so that invalid usernames are handled with a recursive call back to the procedure
    found=False

    uniqueIdIn=enterbox("Enter a student ID to retrieve their details","Tree Road School Tutor System")

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
            dobOut=studentDetails[4].split("-")

            #As studentDetails is a list, I have formatted the output to look more presentable
            userstr="Username: "+studentDetails[0]+"\n\
Full Name: "+studentDetails[2]+" "+studentDetails[3]+"\n\
Form: "+studentDetails[10]+"\n\
DOB: "+dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]+"\n\
Gender: "+studentDetails[9]+"\n\
Address: "+studentDetails[5]+" "+studentDetails[6]+" "+studentDetails[7]+"\n\
Email: "+studentDetails[1]+"\n\
Phone: "+studentDetails[8]
            
            msgbox(userstr,"Student Details")

        if not found:
            msgbox("User details not found, please check unique ID","Student Details")
            return retrieveStudentDetailsProcedure()

            
def report1():
    userHeadings="Username  "+" First Name"+" Surname     "+" Form"+" DOB       "+" M/F"+\
          " Address 1        "+" Address 2   "+" Postcode "+" Phone \n"
    
    #Create a tkinter root widget i.e. window
    root = Tk()

    #Both the scrollbar and text objects are children of the root widget
    S = Scrollbar(root)
    #T is an object based on the Text method. The height is 25lines and the width is 150 chars, enough for a form's data
    T = Text(root, height=25, width=150)

    #The scrollbar and text are aligned to the R and L respectively and take up the height of the widget
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    
    T.insert(END, userHeadings)
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
            userDetails=studentDetails[0]+" "*usernamePad+" "+studentDetails[2]+" "*firstnamePad+" "+studentDetails[3]+" "\
                         *surnamePad+" "+studentDetails[10]+" "+" "+dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]+" "+\
                  studentDetails[9]+" "*2+" "+studentDetails[5]+" "*add1Pad+" "+studentDetails[6]+" "*add2Pad+" "+\
                  studentDetails[7]+" "*postcodePad+" "+studentDetails[8]+"\n"

            #Convert userDetails from a tuple to a string
            userDetails=str(userDetails)
            
            T.insert(END,userDetails)

    #This is the event loop for the tkinter widget
    mainloop(  )
    

def report2():
    #Take a register and output the report
    form=enterbox("Please enter the form you wish to register")

    #Make a list so that a list can be appended within this to create a 2D List
    register=[]
    #Register each student in a given form line by line
    with open ("students.txt","r") as studentFile: 
        for line in studentFile:
            if form in line:
                studentDetails=eval(line)
                dobOut=studentDetails[4].split("-")
                currentStudent=studentDetails[2]+" "+studentDetails[3]+"\n("+dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]+")"
                msg = "Please select an option? \n\n"+currentStudent
                choices = ["Present","Absent","Ill"]
                reply = buttonbox(msg, choices=choices,title="Student attendance mark")
                replyDict={"Present":"/",
                          "Absent":"N",
                          "Ill":"I"}
                
                reg=replyDict[reply]
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
        #print("\nWritten")
        time.sleep(1)
        #print("Outputting register \n")


    regHeadings="First Name"+" Surname     "+" DOB       "+" Present?\n"
    

    root = Tk()
    S = Scrollbar(root)
    T = Text(root, height=25, width=150)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    
    T.insert(END, regHeadings)
    #Read the register, outputting only the names, DOB and reg mark
    with open (form+"-"+nowDate+".txt","r") as currentRegister:            
        regOut=eval(currentRegister.read())
    present=0
    
    for count in range(0,len(regOut)):
        firstnamePad=10-len(regOut[count][2])
        surnamePad=12-len(regOut[count][3])
        dobOut=regOut[count][4].split("-")

        
        regDetails=regOut[count][2]+" "*firstnamePad+regOut[count][3]+" "*surnamePad+" "+dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]+"  "*3\
                    +regOut[count][11]+"\n"
        regDetails=str(regDetails)
        
        if regOut[count][11]=="/":
            present=present+1
        
            
        T.insert(END,regDetails)
    attendance="Attendance percentage: "+str(round(present/len(regOut)*100,1))+"%"
    T.insert(END,attendance)
    mainloop(  )

    
def report3():
    form=enterbox("Please enter the form you wish to check for absences")
    now = datetime.datetime.now()
    nowDate=now.strftime("%d-%m-%Y")
    with open (form+"-"+nowDate+".txt","r") as currentRegister:            
        regOut=eval(currentRegister.read())

    callMsg="Please ensure all absences are chased up before 12pm\n\n"
    callHeadings="First Name"+" Surname     "+" DOB       "+" Present?"+" Phone\n"

    root = Tk()
    S = Scrollbar(root)
    T = Text(root, height=25, width=150)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    T.insert(END, callMsg)
    T.insert(END, callHeadings)
    
    for count in range(0,len(regOut)):
        firstnamePad=10-len(regOut[count][2])
        surnamePad=12-len(regOut[count][3])
        dobOut=regOut[count][4].split("-")
        if regOut[count][11]=="N" or regOut[count][11]=="I":
            callDetails=regOut[count][2]+" "*firstnamePad+" "+regOut[count][3]+" "*surnamePad+" "+\
                         dobOut[2]+"/"+dobOut[1]+"/"+dobOut[0]+" "+\
                  " "*3+regOut[count][11]+" "*2+" "+regOut[count][8]
            callDetails=str(callDetails)
            T.insert(END, callDetails)
    
    mainloop(  )
def loadMenu():
    msg = "Choose a task using the buttons below"
    choices = ["Enter new student details","Retrieve student details","Report 1: Contact Home List",\
               "Report 2: Today's Register","Report 3: Absent or ill List","Logout","Exit"]
    reply = buttonbox(msg, choices=choices, title="Tree Road School Tutor System")

    #The input is cast to lower case to minimise possible cases in the lists above. Each option is linked to a procedure
    
    if reply ==choices[0]:
        enterStudentDetailsProcedure()
    elif reply ==choices[1]:
        retrieveStudentDetailsProcedure()    
    elif reply ==choices[2]:
        report1()
    elif reply ==choices[3]:
        report2()
    elif reply ==choices[4]:
        report3()
    elif reply ==choices[5]:
        return main()
    elif reply ==choices[6]:
        quit()
    else:
        msgbox("Invalid input")
        loadMenu()

    msg = "Please select an option?"
    choices = ["Logout","Return to Main Menu","Exit"]
    reply = buttonbox(msg, choices=choices,title="Where next?")

    if reply == "Logout":
        return main()
    elif reply == "Return to Main Menu":
        return loadMenu()
    else:
        quit()
        

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
        msgbox("Incorrect username","Login to Tree Road School Tutor System")
        main()
    #As the checklist is now populated with the username and password, we can check the password against pos 1 of the list
    password=passwordbox("Please enter your password","Login to Tree Road School Tutor System")
    if checkList[1]==password:
        #print("logged in")
        #If the login credentials match, load the menu otherwise give a meaningful error message
        return loadMenu()
    else:
        msgbox("incorrect password","Login to Tree Road School Tutor System")
        return loginProcedure(username)
        
def main():    
    #Enterbox takes two arguements, a message and a window title
    username=enterbox("Please enter your username","Login to Tree Road School Tutor System")
    
    #I've passed the username to the loginProcedure as an arguement. If the username is invalid a return call to main is made
    loginProcedure(username)
    

main()
    
    
    
