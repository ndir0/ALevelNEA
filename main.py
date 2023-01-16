from appJar import gui
import mainsql
import sqlite3
import random
import re

#sqlite3 library used to create database and tables
conn = sqlite3.connect("users.db")
c = conn.cursor()
#these set of functions create database tables using the mainsql python file
mainsql.createLoginTable()
mainsql.createDetailsTable()
mainsql.createClassTable()
mainsql.createUserClassTable()
mainsql.createMatchedTable()
counter = 0

#cipher used to encrypt password
#the user's inputted password and a list is passed inside
#the cipher will encrypted the inputted password and append it to the list
def cipher(password, encryptedPassword):
    characters = []
    shift = len(password)
    for i in password:
        #the integer that represents the unicode of each character
        #will be added alongside the length of the password
        #the sum of that will be added to this characters list
        characters.append(ord(i) + shift)
    for i in characters:
        #after the characters list is formed, the unicode character
        #of each number in the characters list will be added to the
        #encrypted password list, alongside a random integer
        encryptedPassword.append(chr(i))
        encryptedPassword.append(str(random.randint(1,9)))

#cipher used to decrypt password
#the program will retrieve the password for the user that is logging in
#this retrieved password will be passed in this function as searchc2
#password2 is a list that is passed in which will contain the decrypted
#string that will be produced from this function
def cipher2(searchc2, password2):
    characters = []
    characters2 = []
    shift = len(searchc2)
    #the following will reverse the instructions that have occured in the
    #cipher function
    for i in searchc2:
        characters.append(ord(i) - shift)
    for i in characters:
        characters2.append(chr(i))
    characters3 = ("".join(characters2))
    password2.append(characters3)

#this function will handle actions that will be caused from the buttons in
    #the login page
def login(button):
    encryptedPassword = []
    password2 = []
    #if the exit button is pressed in the login window, the program will shut
    if button == "Exit":
        app.stop()
    #if the sign up button is pressed in the login window, the sign up window
    #will open and the information box containing the password requirements
    #will pop up
    elif button == "Sign Up":
        launch("Sign Up")
        app.infoBox("passwordRequirements", "Password must include: Uppercase, Lowercase, Numbers, Between 8-18 Characters",
                    parent = None)
    #if the log in button is pressed in the login window, the following
    #instructions will run
    elif button == "Log In":
        try:
            user = app.getEntry("Username")
            password = app.getEntry("Password")
            #the password inputted by the user and an empty list will
            #be passed in to this cipher function
            cipher(password, encryptedPassword)
            #this sql statement will retrieve the user's encrypted password
            #from the database table
            c.execute("SELECT password FROM logins WHERE username = ?", [user])
            searchPassword = c.fetchone()
            searchc = ("".join(searchPassword))
            #this will remove the random integers that have been added
            #to the password when it has been encrypted
            searchc2 = searchc[::2]
            #this is then passed into the cipher2 function in order
            #to receive the normal string from the encrypted password
            cipher2(searchc2, password2)
            #if the user's inputted password is valid, it will allow
            #the user to access the program
            if password == ("".join(password2)):
                app.hideSubWindow("Login")
                app.show()
                #this will set the header in the details frame in the
                #profile window
                app.setLabel("profileName", user)
            #if the password inputted is invalid, it will notify the user
            #that the username or password is wrong
            else:
                app.errorBox("wrong", "Wrong username or password!", parent = None)
        #an error box will show if the user causes a wrong input
        except:
            app.errorBox("wrong", "Wrong username or password!", parent = None)

#checks if the user created password meets the requirements
#if the password does not meet the requirements, it will return a false value
def validatePassword(password, validity1):
    while validity1 == False:
        if len(password) < 8 or len(password) > 18:
            break
        elif not re.search("[a-z]", password):
            break
        elif not re.search("[A-Z]", password):
            break
        elif not re.search("[0-9]", password):
            break
        else:
            validity1 = True
            break
    if validity1 == False:
        pass
    return password, validity1

#checks if the user created username exists or if it has a valid input
def validateUsername(username, validity2):
    c.execute("SELECT * FROM logins")
    records = c.fetchall()
    usernames = []
    #this will obtain all existing usernames and place them in a list
    for i in records:
        usernames.append(i[0])
    #if the username exists, it will return a false value
    if username in usernames:
        validity2 = False
    #if the username is less than one character, it will return a false value
    elif len(username) < 1:
        validity2 = False
    #if the username is valid, it will return a true value
    else:
        validity2 = True
    return username, validity2

#this function is used to perform instructions for the register button
#or the check strength button
def register(button):
    encryptedPassword = []
    #as you can see "username2" and "password2" are the inputs in the
    #register window, not the login window
    username = app.getEntry("Username2")
    password = app.getEntry("Password2")
    validity1 = False
    validity2 = False
    #the username and password entered must be valid inputs
    validity1 = validatePassword(password, validity1)
    validity2 = validateUsername(username, validity2)
    #if the created username and password is valid, the user can either register
    #or check the strength of the password
    if validity1[1] == True and validity2[1] == True:
        num = 0
        if button == "Register":
            app.clearEntry("Username2", callFunction = False)
            app.clearEntry("Password2", callFunction = False)
            #the password will initially be encrypted
            cipher(password, encryptedPassword)
            #the encrypted password will be made into a string
            encryptedPassword2 = ("".join(encryptedPassword))
            #the encrypted password will be inserted into the login table along with
            #the valid username
            c.execute("INSERT INTO logins VALUES(?, ?)", (username, encryptedPassword2))
            conn.commit()
            encryptedPassword.clear()
            #information box will confirm the registeration
            app.infoBox("register", "Registered!")
        #determines the strength of the created password
        elif button == "Check Strength":
            numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            #0.8 will be added to the num variable, if the password contains an uppercase,
            #number or is greater than 12 characters
            #0.2 will be added to the num variable, if the password contains a lowercase or
            #is less than or equal to 10 characters
            for i in password:
                if i == i.upper():
                    num += 0.8
                elif i == i.lower():
                    num += 0.2
                elif i in numbers:
                    num += 0.8
            if len(password) <= 10:
                num += 0.2
            elif len(password) > 12:
                num += 0.8
        #after the num adds up all the points, it will be made into a percentage
        #and will be displayed in the meter
        percentage = num * 10
        #if the percentage is less than or equal to 30, it will display a red colour
        if percentage <= 30:
            app.setMeter("passwordStrength", percentage, text = None)
            app.setMeterFill("passwordStrength", "red")
        #if the percentage is less than or equal to 70, it will display an orange colour
        elif percentage <= 70:
            app.setMeter("passwordStrength", percentage, text = None)
            app.setMeterFill("passwordStrength", "orange")
        #if the percentage is greater than 70, it will display a green colour
        elif percentage > 70:
            app.setMeter("passwordStrength", percentage, text = None)
            app.setMeterFill("passwordStrength", "green")
    #if the inputted username or password is not valid, it will display an error box
    else:
        if validity1[1] == False:
            app.errorBox("passwordRequirements", "Password did not meet requirements!", parent = None)
        elif validity2[1] == False:
            app.errorBox("usernameExists", "Username already exists or is not a valid input!", parent = None)

#this function is used to make calculations
def fitnessCalculator(button):
    #exception is used to avoid errors occuring from
    #failed inputs
    try:
        app.showOptionBox("activity")
        app.setLabel("display", "")
        username = app.getEntry("Username")
        age = int(app.getEntry("age"))
        weight = float(app.getEntry("weight"))
        height = float(app.getEntry("height"))
        gender = str(app.getOptionBox("gender"))
        activity = app.getOptionBox("activity")
        bmi2 = ""
        calorie = ""
        if button == "Calculate BMI":
            app.hideOptionBox("activity")
            #bmi is calculated from the weight and height inputted
            bmi = weight / ((height/100) ** 2)
            #calculation is rounded
            bmi2 = (round(bmi), "kg/m^2")
            app.setLabel("display", bmi2)
        elif button == "Calculate Calories":
            if gender == "Male":
                calorie = weight * 24
            elif gender == "Female":
                calorie = (weight * 0.9) * 24
            if activity == "Light":
                calorie = calorie * 1.55
            elif activity == "Moderate":
                calorie = calorie * 1.65
            elif activity == "Active":
                calorie = calorie * 1.8
            elif activity == "Very Active":
                calorie = calorie * 2
            #calculation is rounded
            calorie = (round(calorie), "kCal")
            app.setLabel("display", calorie)
    except:
        pass

#this function will used for a lot of the buttons inside the profile window
def profileData(button):
    username = app.getEntry("Username")
    age = app.getEntry("Age ")
    gender = app.getOptionBox("Gender ")
    height = app.getEntry("Height ")
    weight = app.getEntry("Weight ")
    existingPassword = app.getEntry("Existing Password")
    newPassword = app.getEntry("New Password")
    selectItems = app.getAllListItems("classList")
    firstClass = app.getLabel("1st")
    secondClass = app.getLabel("2nd")
    thirdClass = app.getLabel("3rd")
    c.execute("SELECT * FROM matches")
    matched = c.fetchall()
    #if the my profile button is pressed, the right frame will change to
    #the correct frame
    if button == "My Profile":
        app.firstFrame("profileStack")
    #if the select class button is press, the right frame will change to
    #correct frame
    elif button == "Select Class":
        c.execute("SELECT * FROM class")
        newClass = c.fetchone()
        try:
            #this will place the weekly classes in the list box that can be
            #found inside the profile window
            app.setListItemAtPos("classList", 0, newClass[0])
            app.setListItemAtPos("classList", 1, newClass[1])
            app.setListItemAtPos("classList", 2, newClass[2])
        except:
            pass
        c.execute("SELECT * FROM userclass WHERE username = ?", [username])
        savedClass = c.fetchone()
        #this will set the boxes in the profile window to the user's
        #preferred classes, if they have already been chosen
        try:
            if len(savedClass) == 4:
                app.setLabel("1st", savedClass[1])
                app.setLabel("2nd", savedClass[2])
                app.setLabel("3rd", savedClass[3])
        except:
            pass
        app.lastFrame("profileStack")
    #if the edit details button is pressed, a new window will open
    elif button == "Edit Details":
        launch("Edit Details")
    #if this button within the edit details window is pressed, it will update the
    #details depending if the user has met the requirements
    elif button == "Update":
        #as long as the number input fields contain only numbers, the details will update
        if re.search("[0-9]", age) and re.search("[0-9]", height) and re.search("[0-9]", weight):
            #this will delete the user's current details and update them
            try:
                c.execute("DELETE FROM details WHERE username = ?", [username])
                conn.commit()
            except:
                pass
            c.execute("INSERT INTO details VALUES(?, ?, ?, ?, ?)", (username, age, gender, height, weight))
            conn.commit()
            #informs the user that the details have been updated
            app.infoBox("updateDetails", "Updated Details!")
        else:
            #if the input details are not valid, an error box will show
            app.errorBox("incorrectDetails", "Incorrect input!")
    #if the user presses the change password button, a new window will open
    elif button == "Change Password":
        launch("Change Password")
    #if this button within the change password window is pressed, it will update the
    #password depending on if the user has inputted the existing password correctly
    #and has met the password requirements for the new password
    elif button == "Update ":
        #this sql statement will retrieve the encrypted password for the existing password
        c.execute("SELECT password FROM logins WHERE username = ?", [username])
        existingPassword3 = []
        existingPassword2 = c.fetchone()
        searchc = ("".join(existingPassword2))
        searchc2 = searchc[::2]
        #this will decrypt the user's existing encrypted password
        cipher2(searchc2, existingPassword3)
        validity1 = False
        #this will validate whether the new password meets the requirements
        validity1 = validatePassword(newPassword, validity1)
        encryptedPassword = []
        #this will encrypt the new inputted password
        cipher(newPassword, encryptedPassword)
        encryptedPassword2 = ("".join(encryptedPassword))
        #if the existing password matches and the new password meets the requirements,
        #the password will successfully change
        if existingPassword == ("".join(existingPassword3)) and validity1[1] == True:
            #information box will confirm the updated password
            app.infoBox("updatePassword", "Updated Password!")
            #this will delete and update the user's password
            c.execute("DELETE FROM logins WHERE username = ?", [username])
            c.execute("INSERT INTO logins VALUES(?, ?)", (username, encryptedPassword2))
            conn.commit()
        #if the user's existing password input does not match the existing password,
        #it will not update the password and an error box will pop up
        elif existingPassword != ("".join(existingPassword3)):
            app.errorBox("updatePassword1", "Existing password is incorrect!")
        #if the user's new password does not meet the requirements, an error box
        #will pop up
        else:
            app.errorBox("updatePassword2", "New password has failed to meet requirements!")
    #the following will place the highlighted item from the list box into the boxes
    #to display the user's preferences
    elif button == "Select" and len(selectItems) == 3:
        selectItem = app.getListBox("classList")
        app.setLabel("1st", "{}".format("".join(selectItem)))
        app.removeListItem("classList", selectItem)
    elif button == "Select" and len(selectItems) == 2:
        selectItem = app.getListBox("classList")
        app.setLabel("2nd", "{}".format("".join(selectItem)))
        app.removeListItem("classList", selectItem)
    elif button == "Select" and len(selectItems) == 1:
        selectItem = app.getListBox("classList")
        app.setLabel("3rd", "{}".format("".join(selectItem)))
        app.removeListItem("classList", selectItem)
    #the preferences will save, if the user has chosen all the classes
    elif button == "Save":
        if len(selectItems) == 0:
            #this will delete the user's preferences
            try:
                c.execute("DELETE FROM userclass WHERE username = ?", [username])
                conn.commit()
            except:
                pass
            #this will update the user's preferences
            c.execute("INSERT INTO userclass VALUES(?, ?, ?, ?)", (username, firstClass, secondClass, thirdClass))
            conn.commit()
            #the information box will clarify that the preferences have been saved
            app.infoBox("class", "Saved Preferences!")
        else:
            #an error box will show, if all the classes were not selected
            app.errorBox("class", "Not all the preferences were selected!")
    #these buttons will launch the windows that display who is attending which class
    elif button == "firstClass":
        launch("First Class")
        try:
            app.setLabel("firstClassPerson", matched[0][0])
        except:
            pass
    elif button == "secondClass":
        launch("Second Class")
        try:
            app.setLabel("secondClassPerson", matched[1][0])
        except:
            pass
    elif button == "thirdClass":
        launch("Third Class")
        try:
            app.setLabel("thirdClassPerson", matched[2][0])
        except:
            pass

#this function is used for the buttons found in the admin set class window
def setClass(button):
    global counter
    #this will retrieve the date and time selected and will structure them in this format
    newClass = str(app.getDatePicker("datePicker")) + " " + app.getEntry("time")
    firstClass = app.getLabel("1st ")
    secondClass = app.getLabel("2nd ")
    thirdClass = app.getLabel("3rd ")
    #the select button is used to choose the weekly classes
    #the classes selected will be displayed in the boxes in order
    if button == "Select " and counter == 0:
        app.setLabel("1st ", newClass)
        counter += 1
    elif button == "Select " and counter == 1:
        app.setLabel("2nd ", newClass)
        counter += 1
    elif button == "Select " and counter == 2:
        app.setLabel("3rd ", newClass)
    #the save button will save/store the classes that have been set for the week
    elif button == "Save ":
        #this will delete the classes that have been set previously
        try:
            c.execute("DELETE FROM class")
        except:
            pass
        #this checks whether there is date and time for all the 3 classes
        if len(app.getLabel("3rd ")) > 3:
            #this sql statement will place the weekly classes in the classes table
            c.execute("INSERT INTO class VALUES(?, ?, ?)", (firstClass, secondClass, thirdClass))
            conn.commit()
            c.execute("SELECT * FROM class")
            newClass = c.fetchone()
            #this will set the items that are found in the profile window
            app.setListItemAtPos("classList", 0, newClass[0])
            app.setListItemAtPos("classList", 1, newClass[1])
            app.setListItemAtPos("classList", 2, newClass[2])
            #this will display the classes on the buttons found in the classes window
            app.setButton("firstClass", newClass[0])
            app.setButton("secondClass", newClass[1])
            app.setButton("thirdClass", newClass[2])
            #this will confirm to the admin that the classes have been saved
            app.infoBox("class2", "Saved Classes!")
        #this will check whether all the classes have been selected for the week
        elif len(app.getLabel("3rd ")) == 3:
            #an error box will show to inform the admin that not all the classes were selected
            app.errorBox("class2", "Not all the classes were selected!")
    #this button will apply the matching algorithm in order to match all the classes to a member
    elif button == "Generate":
        #due to the new matches being set for the new week, the matches from the previous week
        #will be deleted
        try:
            c.execute("DELETE FROM matches")
            conn.commit()
        except:
            pass
        prefer = []
        matches2 = []
        num = 0
        #this will create a preference list in the format required for the matching algorithm
        createPreferenceList(prefer, matches2)
        for i in prefer:
            if len(i) == 3:
                num += 1
        #if enough people have chosen classes, the matches will generate
        if num == 6:
            app.infoBox("generate", "Generated!")
            GaleShapley(prefer, matches2)
        #if enough people have not chosen classes yet, the matches will not generate
        #and an error box will pop up to notify the admin
        else:
            app.errorBox("needPeople", "Not enough people have chosen their preferences!")

#this function is used to create a preference list in the format that is suitable for the
#matching algorithm
#the structure of the preference list will altogether have 6 items
#each item will have 3 preferences
#the first 3 items will have the same preferences as they are targeting members with the largest bmi
#the members will be represented by the last 3 items of the preference list, therefore, the first 3
#class items will order their preferences through the index position of the members in the preference list
#this is the same for the members, the classes they prefer will be represented by the first 3 items of
#the preference list, therefore, they will order their preferences through the index position of the classes
def createPreferenceList(prefer, matches2):
    c.execute("SELECT * FROM class")
    classes = c.fetchall()
    c.execute("SELECT * FROM userclass")
    users = c.fetchall()
    c.execute("SELECT * FROM details")
    details = c.fetchall()
    firstClass = classes[0][0]
    secondClass = classes[0][1]
    thirdClass = classes[0][2]
    bmis = []
    personPreferences = []
    #this will obtain the bmis for every person who has selected their preferences
    for i in users:
        for j in details:
            if i[0] == j[0]:
                bmis2 = []
                weight = j[4]
                height = j[3]
                bmi = weight / ((height/100) ** 2)
                bmis2.append(bmi)
                bmis2.append(i[0])
                bmis.append(bmis2)
    #the list of the users and bmis will be sorted from largest to smallest
    bmis.sort(reverse = True)
    #the list will be reversed so the algorithm knows which user has the largest bmi
    for x in bmis:
        x.reverse()
        for z in users:
            if x[0] == z[0]:
                #the following will obtain the classes preferred by the members that
                #the class prefers
                #the classes want members with the largest bmi
                personPreferences2 = [z[0]] + [z[1]] + [z[2]] + [z[3]]
                personPreferences.append(personPreferences2)
    personPreferences = personPreferences[0:3]
    classPreferences = bmis[0][0].split() + bmis[1][0].split() + bmis[2][0].split()
    preferences = [classPreferences, classPreferences, classPreferences,
                   personPreferences[0], personPreferences[1], personPreferences[2]]
    preferences2 = preferences[0]
    preferences3 = preferences[3:6]
    prefer2 = []
    #the following will retrieve the index positions for the classes or members that they prefer
    #therefore, this will be placed in a structure suitable for the matching algorithm
    for b in preferences2:
        for v in preferences3:
            if b == v[0]:
                personPosition2 = preferences3.index(v)
                personPosition = int(personPosition2) + 3
                prefer2.append(personPosition)
    #the "prefer" list will hold the index positions of the preferences
    #the first 3 items will hold the class preferences
    prefer.append(prefer2)
    prefer.append(prefer2)
    prefer.append(prefer2)
    #the following will hold the member preferences by appending the index position of the classes
    #they prefer
    #as mentioned before, the first 3 items represent the classes, therefore, if the member prefers the
    #the second class, "1" will be appended as this represents the position of the second class
    for d in preferences3:
        prefer3 = []
        for e in d:
            if e == firstClass:
                prefer3.append(0)
            elif e == secondClass:
                prefer3.append(1)
            elif e == thirdClass:
                prefer3.append(2)
        prefer.append(prefer3)
    for z in preferences:
        matches2.append(z)
    return prefer
    return matches2

#this function will return a true value, if the member prefers the new class
#over their current class
def personPrefers(N, prefer, person, class1, class2):
    for i in range(N):
        if prefer[person][i] == class1: 
            return False
        if prefer[person][i] == class2: 
            return True

#this algorithm is used to match every class with a member through looking at
#the the classes and members preferences
def GaleShapley(prefer, matches2):
    #3 classes will be set weekly, hence why this variable is set to 3
    N = 3
    freeCount = N
    #this will store whether a class is free
    classFree = [False for i in range(N)]
    #this stores the members matches
    #-1 shows that N+i member is free
    personClass = [-1 for i in range(N)]
    matches = []
    #until all the classes are matched, this loop will continue to run
    while freeCount > 0:
        class1 = 0
        while class1 < N: 
            if classFree[class1] == False: 
                break
            class1 += 1
        i = 0
        while i < N and classFree[class1] == False: 
            person = prefer[class1][i]
            #if the class's preference is free, they will be matched
            if personClass[person - N] == -1: 
                personClass[person - N] = class1 
                classFree[class1] = True
                freeCount -= 1
            else:
                class2 = personClass[person - N]
                #if the member prefers the new class over the current class,
                #the match will be replaced
                if personPrefers(N, prefer, person, class1, class2) == False: 
                    personClass[person - N] = class1 
                    classFree[class1] = True
                    classFree[class2] = False
            i += 1
    for i in range(N):
        #this list will store the index position of the matches
        matches3 = []
        matches3.append(i + N)
        matches3.append(personClass[i])
        matches.append(matches3)
    #the matches list will be passed onto the second part of the matching algorithm
    GaleShapley2(matches, matches2)

#this function is used to match will find the classes and members matched by retrieving the
#index positions from the previous function
#after this is complete, the matches can be stored 
def GaleShapley2(matches, matches2):
    #this list displays the original "prefer" list from the preference function
    #instead of the index position, the actual classes and members are displayed
    matches3 = ["firstClass", "secondClass", "thirdClass", matches2[3][0], matches2[4][0], matches2[5][0]]
    #this list will store the matches made
    matched = []
    for i in matches:
        matched2 = []
        matched2.append(matches3[i[0]])
        matched2.append(matches3[i[1]])
        matched.append(matched2)
    for j in matched:
        user = j[0]
        class1 = j[1]
        #this will store the matches into the matches database table
        c.execute("INSERT INTO matches VALUES(?, ?)", (user, class1))
        conn.commit()

def launch(win):
    app.showSubWindow(win)

#this function is used for the buttons displayed in the main menu
def window(button):
    username = app.getEntry("Username")
    #if the classes button is pressed, the labels will display the date and time of the classes
    if button == "Classes":
        c.execute("SELECT * FROM class")
        newClass = c.fetchone()
        try:
            app.setLabel("1st ", newClass[0])
            app.setLabel("2nd ", newClass[1])
            app.setLabel("3rd ", newClass[2])
        except:
            pass
        #if the user is the admin, the classes button will direct them to the admin
        #set class window instead
        if username == "admin":
            launch("Admin Class")
        #this will display the classes on the buttons found in the classes window
        else:
            try:
                c.execute("SELECT * FROM class")
                newClass = c.fetchone()
                app.setButton("firstClass", newClass[0])
                app.setButton("secondClass", newClass[1])
                app.setButton("thirdClass", newClass[2])
            except:
                pass
            launch("Classes")
    #this will launch the calculator window
    elif button == "Calculator":
        launch("Calculator")
    #this will launch the my profile window
    elif button == "My Profile ":
        #the profile will display the user's details
        try:
            c.execute("SELECT * FROM details WHERE username = ?", [username])
            detail = c.fetchone()
            app.setMessage("profileData", """
            Age: {}
            Gender: {}
            Height: {}cm
            Weight: {}kg
            BMI: {}
            """.format(detail[1], detail[2], detail[3], detail[4], round(detail[4] / ((detail[3]/100) ** 2))))
        except:
            pass
        #after the details have either been display or not, the profile window will launch
        launch("Profile")
    #this button will close the program
    elif button == "Log Out":
        app.stop()

#main menu window
app = gui("Main Menu", "400x300")
app.setBg("lightgrey")
app.setFont(16)
app.startFrame("mainLeft", 0, 0)
app.setPadding([5, 5])
app.addButton("Classes", window)
app.addButton("My Profile ", window)
app.stopFrame()
app.startFrame("mainRight", 0, 1)
app.setPadding([5, 5])
app.addButton("Calculator", window)
app.addButton("Log Out", window)
app.stopFrame()

#login window
app.startSubWindow("Login")
app.setSize("400x300")
app.setSticky("NEW")
app.setBg("lightgrey")
app.setInPadding([5, 5])
app.addLabel("loginTitle", "Club", 0, 0, 2)
app.setLabelBg("loginTitle", "grey")
app.setLabelFg("loginTitle", "white")
app.setPadding([5, 5])
app.addImage("usernameIcon", "username.gif", 1, 0)
app.addEntry("Username", 1, 1)
app.setEntryWidth("Username", 26)
app.setEntryRelief("Username", "flat")
app.setEntryDefault("Username", "Username")
app.setEntryAlign("Username", "left")
app.addImage("passwordIcon", "password.gif", 2, 0)
app.addSecretEntry("Password", 2, 1)
app.setEntryRelief("Password", "flat")
app.setEntryDefault("Password", "Password")
app.setEntryAlign("Password", "left")
app.addButtons(["Sign Up", "Log In", "Exit"], login, 3, 0, 2)
app.stopSubWindow()

#sign up window
app.startSubWindow("Sign Up", modal = True)
app.setSize("400x300")
app.setSticky("NEW")
app.setBg("lightgrey")
app.setInPadding([5, 5])
app.addLabel("signupTitle", "Club")
app.setLabelBg("signupTitle", "grey")
app.setLabelFg("signupTitle", "white")
app.addEntry("Username2")
app.addEntry("Password2")
app.setEntryDefault("Username2", "Create Username")
app.setEntryDefault("Password2", "Create Password")
app.addMeter("passwordStrength")
app.addButtons(["Check Strength", "Register"], register)
app.stopSubWindow()

#classes window
app.startSubWindow("Classes", modal = True)
app.setSize("400x230")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.setInPadding([5, 5])
app.addLabel("classTitle", "This Week")
app.setLabelBg("classTitle", "silver")
app.setLabelFg("classTitle", "white")
app.setPadding([5, 5])
app.addButton("firstClass", profileData)
app.addButton("secondClass", profileData)
app.addButton("thirdClass", profileData)
app.setButtonBg("firstClass", "white")
app.setButtonBg("secondClass", "white")
app.setButtonBg("thirdClass", "white")
app.setButtonRelief("firstClass", "flat")
app.setButtonRelief("secondClass", "flat")
app.setButtonRelief("thirdClass", "flat")
app.stopSubWindow()
    
#admin class window
app.startSubWindow("Admin Class", modal = True)
app.setSize("400x420")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.setInPadding([5, 5])
app.addLabel("adminTitle", "This Weeks Class")
app.setLabelBg("adminTitle", "silver")
app.setLabelFg("adminTitle", "white")
app.setPadding([5, 5])
app.addLabel("1st ", "1st")
app.addLabel("2nd ", "2nd")
app.addLabel("3rd ", "3rd")
app.setLabelBg("1st ", "white")
app.setLabelBg("2nd ", "white")
app.setLabelBg("3rd ", "white")
app.setLabelFg("1st ", "grey")
app.setLabelFg("2nd ", "grey")
app.setLabelFg("3rd ", "grey")
app.setPadding([90, 0])
app.addDatePicker("datePicker")
app.setDatePickerRange("datePicker", 2020, 2030)
app.setPadding([5, 5])
app.addEntry("time")
app.setEntryDefault("time", "Time")
app.addButtons(["Select ", "Save ", "Generate"], setClass)
app.stopSubWindow()

#first class window
app.startSubWindow("First Class", modal = True)
app.setSize("300x75")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.addLabel("firstClass", "First Class")
app.setLabelBg("firstClass", "darkgrey")
app.setLabelFg("firstClass", "white")
app.setPadding([5, 5])
app.addLabel("firstClassPerson", "")
app.setLabelBg("firstClassPerson", "white")
app.stopSubWindow()

#second class window
app.startSubWindow("Second Class", modal = True)
app.setSize("300x75")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.addLabel("secondClass", "Second Class")
app.setLabelBg("secondClass", "darkgrey")
app.setLabelFg("secondClass", "white")
app.setPadding([5, 5])
app.addLabel("secondClassPerson", "")
app.setLabelBg("secondClassPerson", "white")
app.stopSubWindow()

#third class window
app.startSubWindow("Third Class", modal = True)
app.setSize("300x75")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.addLabel("thirdClass", "Third Class")
app.setLabelBg("thirdClass", "darkgrey")
app.setLabelFg("thirdClass", "white")
app.setPadding([5, 5])
app.addLabel("thirdClassPerson", "")
app.setLabelBg("thirdClassPerson", "white")
app.stopSubWindow()

#calculator window
app.startSubWindow("Calculator", modal = True)
app.setSize("500x300")
app.setBg("lightgrey")
app.setSticky("NEWS")
app.startFrame("calculatorLeft", 0, 0)
app.setPadding([5, 5])
app.addButton("Calculate BMI", fitnessCalculator)
app.addButton("Calculate Calories", fitnessCalculator)
app.setSticky("EW")
app.stopFrame()
app.startFrame("calculatorRight", 0, 1)
app.setPadding([5, 5])
app.addEntry("age")
app.setEntryDefault("age", "Age")
app.addOptionBox("gender", ["Male", "Female"])
app.addEntry("height")
app.setEntryDefault("height", "Height (cm)")
app.addEntry("weight")
app.setEntryDefault("weight", "Weight (kg)")
app.addOptionBox("activity", ["Light", "Moderate", "Active", "Very Active"])
app.addLabel("display", "")
app.setLabelBg("display", "white")
app.stopFrame()
app.stopSubWindow()

#profile window
app.startSubWindow("Profile", modal = True)
app.setSize("400x321")
app.setBg("lightgrey")
app.setSticky("NEWS")
app.startFrame("profileLeft", 0, 0)
app.setPadding([5, 5])
app.addButton("My Profile", profileData)
app.addButton("Select Class", profileData)
app.stopFrame()
app.startFrame("profileRight", 0, 1)
app.startFrameStack("profileStack", start = 0)
app.startFrame("profileFrame")
app.setStretch("COLUMN")
app.setInPadding([5, 5])
app.addLabel("profileName", "Profile: {}".format(app.getEntry("Username")))
app.setLabelBg("profileName", "silver")
app.setLabelFg("profileName", "white")
app.setInPadding([0, 0])
app.addMessage("profileData", """
Age: {}
Gender: {}
Height: {}cm
Weight: {}kg
BMI: {}
""")
app.setMessageBg("profileData", "gainsboro")
app.setMessageAlign("profileData", "left")
app.setPadding([5, 5])
app.addButton("Edit Details", profileData)
app.addButton("Change Password", profileData)
app.stopFrame()
app.startFrame("classesFrame")
app.setInPadding([5, 5])
app.setStretch("COLUMN")
app.addLabel("className", "This Week")
app.setLabelBg("className", "silver")
app.setLabelFg("className", "white")
app.setInPadding([0, 0])
app.setPadding([5, 5])
app.addLabel("1st", "1st")
app.addLabel("2nd", "2nd")
app.addLabel("3rd", "3rd")
app.setLabelBg("1st", "white")
app.setLabelBg("2nd", "white")
app.setLabelBg("3rd", "white")
app.setLabelFg("1st", "grey")
app.setLabelFg("2nd", "grey")
app.setLabelFg("3rd", "grey")
app.addListBox("classList", ["", "", ""])
app.setListBoxHeight("classList", "3")
app.addButtons(["Select", "Save"], profileData)
app.stopFrame()
app.stopFrameStack()
app.stopFrame()
app.stopSubWindow()

#edit details window
app.startSubWindow("Edit Details", modal = True)
app.setSize("300x230")
app.setBg("lightgrey")
app.setStretch("COLUMN")
app.setSticky("NEWS")
app.setPadding([5, 5])
app.addOptionBox("Gender ", ["Male", "Female"])
app.addLabelEntry("Age ")
app.addLabelEntry("Height ")
app.addLabelEntry("Weight ")
app.setEntryDefault("Height ", "cm")
app.setEntryDefault("Weight ", "kg")
app.addButton("Update", profileData)
app.stopSubWindow()

#change password window
app.startSubWindow("Change Password", modal = True)
app.setSize("400x150")
app.setStretch("COLUMN")
app.setPadding([5, 5])
app.addLabelEntry("Existing Password")
app.addLabelEntry("New Password")
app.addButton("Update ", profileData)
app.stopSubWindow()

app.go(startWindow = "Login")
