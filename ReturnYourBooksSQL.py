
# Library Assistant

import tkinter as t
import mysql.connector as sqlconnect

# Creating Main Window
window = t.Tk()
window.title("Library Assistant")
window.resizable(0, 0)

# Starts connection to mysql database
sqlcon = sqlconnect.connect(host='localhost', user='root', passwd='Th!sIs@passw0rd', db='computerproject')
cursor = sqlcon.cursor(buffered=True)

bgimage = t.PhotoImage(file="library_bg.gif")
bg = t.Label(window, image=bgimage, bg="black").grid(row=0, column=0)

intro = t.Label(window, text="Welcome to IISD", bg="black", fg="white", font="impact 48 bold")
intro.place(height=100, width=500, relx=0.3, rely=0.3)

namevar = t.StringVar()
passwordvar = t.StringVar()
nameentry = t.Entry(window, textvariable=namevar, font=('calibre', 24, 'normal'))
passwordentry = t.Entry(window, textvariable=passwordvar, font=('calibre', 24, 'normal'), show='*')
nameentry.place(height=45, width=300, relx=0.38, rely=0.60)
passwordentry.place(height=45, width=300, relx=0.38, rely=0.67)

hello = t.Label(window, text="Hello There!!!", bg="black", fg="white", font="impact 24 bold")


# Just shows where username and password go with friendly message
def hellopress():
    hello.place(height=45, width=250, relx=0.4, rely=0.52)

    namevar.set("Username :)")
    passwordvar.set("Password :)")


invalid = t.Label(window, text="Invalid User!", bg="black", fg="white", font="impact 24")
wrongpassword = t.Label(window, text="Password Incorrect!", bg="black", fg="white", font="impact 24")
success = t.Label(window, text="Logged In!", bg="black", fg="white", font="impact 24")


# Checks for valid username and then correct password from the database and logs in
def loginpress():
    global logname, logissue, name, issuedbookid, issuedbook

    name = nameentry.get()
    password = passwordentry.get()

    cursor.execute("SELECT * FROM class")
    for i in cursor:
        if name == i[2]:
            if password != i[7]:
                invalid.place_forget()
                wrongpassword.place(height=45, width=300, relx=0.38, rely=0.85)
                break
            else:
                success.place(height=45, width=300, relx=0.38, rely=0.85)
                loginmenuchange()

                issuedbookid = i[6]
                cursor.execute("SELECT * FROM library")
                for j in cursor:
                    if issuedbookid == j[0]:
                        issuedbook = j[1]
                        break
                if issuedbookid is None:
                    issuedbook = "No Book Issued"
                logname = t.Label(window, text=F"Username: {name}", bg="black", fg="white", font="impact 24")
                logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
                logname.place(height=45, width=400, relx=0.1, rely=0.67)
                logissue.place(height=45, width=500, relx=0.56, rely=0.67)
                break
    else:
        wrongpassword.place_forget()
        invalid.place(height=45, width=300, relx=0.38, rely=0.85)

    namevar.set("")
    passwordvar.set("")


heading = t.Label(window, text="IISD Library Assistant", bg="black", fg="white", font="impact 48 bold")
libvar = t.StringVar()
libentry = t.Entry(window, textvariable=libvar, font=('calibre', 24, 'normal'))


# Resets UI to original state, and finalizes the issue and return of books again
def logoutpress():
    logoutmenuchange()
    libvar.set("")
    sqlcon.commit()


# Issues book if valid ID is provided and book is available, and also provides table of available books
def issuepress():
    global name, issuedbook, issuedbookid, logissue, books

    issueinput = libentry.get()

    cursor.execute("SELECT * FROM library")
    if issuedbook == "No Book Issued":
        for i in cursor:
            if issueinput == str(i[0]) and i[5] == "AVAILABLE":
                cursor.execute(F"UPDATE class SET IssuedBookID = {i[0]} WHERE Name = '{name}'")
                cursor.execute(F"UPDATE library SET Availability = 'UNAVAILABLE' WHERE BookID = {i[0]}")
                issuedbook = i[1]
                issuedbookid = i[0]
                sqlcon.commit()
                break
        else:
            libvar.set("Enter BookID here :)")
    else:
        libvar.set("Return Your Book First >:(")

    count = 3
    books = t.Toplevel(window)
    books.configure(background="black")

    t.Label(books, text="Read A Book Today!!", bg="black", fg="white", font="impact 24").grid(row=0, column=0)
    t.Label(books, text="Available Books:", bg="black", fg="white", font="impact 24").grid(row=1, column=0)
    t.Label(books, text="BookID", bg="black", fg="white", font="impact 18").grid(row=2, column=0)
    t.Label(books, text="BookName", bg="black", fg="white", font="impact 18").grid(row=2, column=1)
    t.Label(books, text="Author", bg="black", fg="white", font="impact 18").grid(row=2, column=2)
    t.Label(books, text="YearPublished", bg="black", fg="white", font="impact 18").grid(row=2, column=3)
    t.Label(books, text="Genre", bg="black", fg="white", font="impact 18").grid(row=2, column=4)
    cursor.execute("SELECT * FROM library")
    for i in cursor:
        if i[5] == "AVAILABLE":
            for j in range(5):
                t.Label(books, text=i[j], bg="black", fg="white", font="impact 18").grid(row=count, column=j)
            count += 1

    logissue.destroy()
    logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
    logissue.place(height=45, width=500, relx=0.56, rely=0.67)
    closebutton.place(height=45, width=100, relx=0.46, rely=0.65)


# Returns book if book issued previously
def returnpress():
    global name, issuedbook, issuedbookid, logissue

    if issuedbook != "No Book Issued":
        cursor.execute(F"UPDATE class SET IssuedBookID = NULL WHERE Name = '{name}'")
        cursor.execute(F"UPDATE library SET Availability = 'AVAILABLE' WHERE BookID = {issuedbookid}")
        issuedbook = "No Book Issued"
        issuedbookid = None
        libvar.set("Book Returned :)")
        sqlcon.commit()
    else:
        libvar.set("No Books Due :)")

    logissue.destroy()
    logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
    logissue.place(height=45, width=500, relx=0.56, rely=0.67)


# Displays full table of books in library
def browsepress():
    global books
    count = 2
    books = t.Toplevel(window)
    books.configure(background="black")
    t.Label(books, text="Books in IISD", bg="black", fg="white", font="impact 24").grid(row=0, column=0)
    t.Label(books, text="BookID", bg="black", fg="white", font="impact 18").grid(row=1, column=0)
    t.Label(books, text="BookName", bg="black", fg="white", font="impact 18").grid(row=1, column=1)
    t.Label(books, text="Author", bg="black", fg="white", font="impact 18").grid(row=1, column=2)
    t.Label(books, text="YearPublished", bg="black", fg="white", font="impact 18").grid(row=1, column=3)
    t.Label(books, text="Genre", bg="black", fg="white", font="impact 18").grid(row=1, column=4)
    t.Label(books, text="Availability", bg="black", fg="white", font="impact 18").grid(row=1, column=5)

    cursor.execute("SELECT * FROM library")
    for i in cursor:
        for j in range(6):
            t.Label(books, text=i[j], bg="black", fg="white", font="impact 18").grid(row=count, column=j)
        count += 1

    closebutton.place(height=45, width=100, relx=0.46, rely=0.65)


# Closes extra window that is created from browsing and issuing (Can be closed manually as well)
def closepress():
    global books
    books.destroy()
    closebutton.place_forget()


# Hides login UI and displays library assistant UI
def loginmenuchange():
    intro.place_forget()
    hello.place_forget()
    nameentry.place_forget()
    passwordentry.place_forget()
    hellobutton.place_forget()
    loginbutton.place_forget()
    invalid.place_forget()
    wrongpassword.place_forget()
    heading.place(height=100, width=750, relx=0.18, rely=0.3)
    issuebutton.place(height=45, width=100, relx=0.26, rely=0.45)
    returnbutton.place(height=45, width=100, relx=0.46, rely=0.45)
    browsebutton.place(height=45, width=100, relx=0.66, rely=0.45)
    libentry.place(height=45, width=400, relx=0.33, rely=0.52)
    logoutbutton.place(height=45, width=100, relx=0.46, rely=0.75)


# Hides library assistant UI and displays login UI
def logoutmenuchange():
    global logname, logissue
    heading.place_forget()
    issuebutton.place_forget()
    returnbutton.place_forget()
    browsebutton.place_forget()
    closebutton.place_forget()
    libentry.place_forget()
    logname.place_forget()
    logissue.place_forget()
    logoutbutton.place_forget()
    success.place_forget()
    intro.place(height=100, width=500, relx=0.3, rely=0.3)
    nameentry.place(height=45, width=300, relx=0.38, rely=0.60)
    passwordentry.place(height=45, width=300, relx=0.38, rely=0.67)
    hellobutton.place(height=45, width=100, relx=0.46, rely=0.45)
    loginbutton.place(height=45, width=100, relx=0.46, rely=0.75)


# Buttons and their functions being assigned
hellobutton = t.Button(window, text="Hello", command=hellopress)
loginbutton = t.Button(window, text="Login", command=loginpress)
hellobutton.place(height=45, width=100, relx=0.46, rely=0.45)
loginbutton.place(height=45, width=100, relx=0.46, rely=0.75)

issuebutton = t.Button(window, text="Issue Book", command=issuepress)
returnbutton = t.Button(window, text="Return Book", command=returnpress)
browsebutton = t.Button(window, text="Browse Books", command=browsepress)
closebutton = t.Button(window, text="Close Window", command=closepress)
logoutbutton = t.Button(window, text="Logout", command=logoutpress)

# Initializes the main window and starts the program
window.mainloop()
