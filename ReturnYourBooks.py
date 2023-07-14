
import tkinter as t

window = t.Tk()
window.title("Library Assistant")
window.resizable(0, 0)

bgimage = t.PhotoImage(file="library_bg.gif")
bg = t.Label(window, image=bgimage, bg="black").grid(row=0, column=0)

intro = t.Label(window, text="Welcome to IISD", bg="black", fg="white", font="impact 48 bold")
intro.place(height=100, width=500, relx=0.3, rely=0.3)

# Placeholder for the sql tables
passworddatabase = {"avi": "nerd", "roger": "notanerd", "Username :)": "Password :)"}
bookdatabase = {"Harry Potter": "Available", "Cinderella": "Available", "Chemistry": "Available"}

namevar = t.StringVar()
passwordvar = t.StringVar()
nameentry = t.Entry(window, textvariable=namevar, font=('calibre', 24, 'normal'))
passwordentry = t.Entry(window, textvariable=passwordvar, font=('calibre', 24, 'normal'), show='*')
nameentry.place(height=45, width=300, relx=0.38, rely=0.60)
passwordentry.place(height=45, width=300, relx=0.38, rely=0.67)

hello = t.Label(window, text="Hello There!!!", bg="black", fg="white", font="impact 24 bold")


def hellopress():
    hello.place(height=45, width=250, relx=0.4, rely=0.52)

    namevar.set("Username :)")
    passwordvar.set("Password :)")


invalid = t.Label(window, text="Invalid User!", bg="black", fg="white", font="impact 24")
wrongpassword = t.Label(window, text="Password Incorrect!", bg="black", fg="white", font="impact 24")
success = t.Label(window, text="Logged In!", bg="black", fg="white", font="impact 24")


def loginpress():
    global logname, logissue, name, issuedbook
    name = nameentry.get()
    password = passwordentry.get()

    if name not in passworddatabase:
        wrongpassword.place_forget()
        invalid.place(height=45, width=300, relx=0.38, rely=0.85)
    else:
        if password != passworddatabase[name]:
            invalid.place_forget()
            wrongpassword.place(height=45, width=300, relx=0.38, rely=0.85)
        else:
            success.place(height=45, width=300, relx=0.38, rely=0.85)
            loginmenuchange()

            for book in bookdatabase:
                if name == bookdatabase[book]:
                    issuedbook = book
                    break
            else:
                issuedbook = "No Book Issued"
            logname = t.Label(window, text=F"Username: {name}", bg="black", fg="white", font="impact 24")
            logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
            logname.place(height=45, width=400, relx=0.1, rely=0.67)
            logissue.place(height=45, width=400, relx=0.6, rely=0.67)

    namevar.set("")
    passwordvar.set("")


heading = t.Label(window, text="IISD Library Assistant", bg="black", fg="white", font="impact 48 bold")
libvar = t.StringVar()
libentry = t.Entry(window, textvariable=libvar, font=('calibre', 24, 'normal'))


def logoutpress():
    logoutmenuchange()
    libvar.set("")
    # Also some sql stuff to finalize the changes made to sql table or something


# change all this with sql later
def issuepress():
    global name, issuedbook, logissue, books

    issueinput = libentry.get()
    if issuedbook == "No Book Issued":
        for book in bookdatabase:
            if book == issueinput:
                bookdatabase[book] = name
                issuedbook = book
                break
        else:
            libvar.set("Write book name here :)")
    else:
        libvar.set("Return Your Book First >:(")

    count = 2
    books = t.Toplevel(window)
    books.configure(background="black")

    t.Label(books, text="Read A Book Today!!", bg="black", fg="white", font="impact 24").grid(row=0, column=0)
    t.Label(books, text="Available Books:", bg="black", fg="white", font="impact 24").grid(row=1, column=0)
    for book in bookdatabase:
        if bookdatabase[book] == "Available":
            t.Label(books, text=F"{book}", bg="black", fg="white", font="impact 24").grid(row=count, column=0)
            count += 1

    logissue.destroy()
    logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
    logissue.place(height=45, width=400, relx=0.6, rely=0.67)
    closebutton.place(height=45, width=100, relx=0.46, rely=0.65)


def returnpress():
    global name, issuedbook, logissue
    if issuedbook != "No Book Issued":
        for book in bookdatabase:
            if bookdatabase[book] == name:
                bookdatabase[book] = "Available"
                issuedbook = "No Book Issued"
                libvar.set("Book Returned :)")
                break
    else:
        libvar.set("No Books Due :)")

    logissue.destroy()
    logissue = t.Label(window, text=F"Issued Book: {issuedbook}", bg="black", fg="white", font="impact 24")
    logissue.place(height=45, width=400, relx=0.6, rely=0.67)


def browsepress():
    global books
    count = 1
    books = t.Toplevel(window)
    books.configure(background="black")
    t.Label(books, text="Books in IISD:", bg="black", fg="white", font="impact 24").grid(row=0, column=0)
    for book in bookdatabase:
        t.Label(books, text=F"{book}", bg="black", fg="white", font="impact 24").grid(row=count, column=0)
        if bookdatabase[book] == "Available":
            t.Label(books, text="Available", bg="black", fg="white", font="impact 24").grid(row=count, column=1)
        else:
            t.Label(books, text="Unavailable", bg="black", fg="white", font="impact 24").grid(row=count, column=1)
        count += 1
    closebutton.place(height=45, width=100, relx=0.46, rely=0.65)

def closepress():
    global books
    books.destroy()
    closebutton.place_forget()


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


hellobutton = t.Button(window, text="Hello", command=hellopress)
loginbutton = t.Button(window, text="Login", command=loginpress)
hellobutton.place(height=45, width=100, relx=0.46, rely=0.45)
loginbutton.place(height=45, width=100, relx=0.46, rely=0.75)

issuebutton = t.Button(window, text="Issue Book", command=issuepress)
returnbutton = t.Button(window, text="Return Book", command=returnpress)
browsebutton = t.Button(window, text="Browse Books", command=browsepress)
closebutton = t.Button(window, text="Close Window", command=closepress)
logoutbutton = t.Button(window, text="Logout", command=logoutpress)

window.mainloop()
