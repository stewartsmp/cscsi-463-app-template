# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 19:20:02 2022

CSCI 463 - Team Project Spring 2022 - Bug SMASHER 
1/29/2021 - Start, initial skeleton

@author: Stewart
"""


from ctypes import alignment
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import sys
from tkinter.tix import NoteBook
from turtle import bgcolor, heading
from functools import partial

def disable_event():
    pass
    #if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
     #   root.destroy()
    #print("Exiting")

def close_program():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

def validateLogin(username, password):
	print("username entered :", username.get())
	print("password entered :", password.get())
	return

def displayRowInfo(event):
    top = Toplevel()
    top.geometry("500x400")
    top.title("Bug Information")
    bugInfoFrame = LabelFrame(top, text = "Bug Information")
    bugInfoFrame.pack(fill = "both", expand = "yes", padx = 20, pady = 20)
    topQuit = Button(top, text = "EXIT", command = top.destroy, fg = "red")
    topQuit.pack()
    rowid = treeView1.identify_row(event.y)
    item = treeView1.item(treeView1.focus())


def updateDatabase(rows, treeview):
    treeview.delete(*treeview.get_children())
    for i in rows:
        treeview.insert("", "end", values = i)

def searchDB_masterFrame2():
    q2 = q.get()
    query = "SELECT bug_number, bug_description, project, assignee, expected_completion_date FROM bugs WHERE bug_number LIKE '%"+q2+"%' OR bug_description LIKE '%"+q2+"%' OR project LIKE '%"+q2+"%' OR assignee LIKE '%"+q2+"%' OR expected_completion_date LIKE '%"+q2+"%'"
    cur.execute(query)
    rows = cur.fetchall()
    updateDatabase(rows)

def searchDB_masterFrame1():
    q2 = q.get()
    query = "SELECT bug_number, bug_description, project, expected_completion_date, status FROM bugs WHERE bug_number LIKE '%"+q2+"%' OR bug_description LIKE '%"+q2+"%' OR project LIKE '%"+q2+"%' OR assignee LIKE '%"+q2+"%' OR expected_completion_date LIKE '%"+q2+"%'"
    cur.execute(query)
    rows = cur.fetchall()
    updateDatabase(rows)

############################################
"""
Create local database of bugs
"""
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("create table bugs (bug_number, bug_description, project, assignee, expected_completion_date, status, completion_date)")
bug_list = [
    ("1","GUI needs to be refined, only one view", "CSCI 463 Team Poject", "Simon", "5/13/2020", "Created", None),
    ("2","Database requests need to be refined", "CSCI 463 Team Poject", "Cole", "5/13/2020", "In Progress", None),
    ("3","Export function not yet working", "CSCI 463 Team Poject", "Simon", "5/13/2020", "Complete", "2/20/2022")
]
cur.executemany("insert into bugs values (?,?,?,?,?,?,?)", bug_list)
############################################

############################################
"""
Create local database of user names and password
"""
user_pass = sqlite3.connect(":memory:")
cursor_user_pass = user_pass.cursor()
cursor_user_pass.execute("create table user_pass (username, password)")
user_list = [
    ("simon.million", "123"),
    ("cole.levine", "123")
]
cursor_user_pass.executemany("insert into user_pass values (?,?)", user_list)
############################################



#cur.execute("select * from bug where first_appeared>:year", {"year": 1972})
#print(cur.fetchall())

root = Tk()
"""
#Everything needs to go below the root
"""
# opening size parameters
root.geometry("1100x700")
# app title
root.title("BugSMASHER")
# logon page
logonPage = Toplevel(root)
logonPage.geometry("400x200")
logonPage.title("Logon Page")
logonPage.focus_force()
logonPage.grab_set()
logonPage.attributes("-topmost", True)
#username label and text entry box
usernameLabel = Label(logonPage, text="User Name").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(logonPage, textvariable=username).grid(row=0, column=1)  
#password label and password entry box
passwordLabel = Label(logonPage,text="Password").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(logonPage, textvariable=password, show='*').grid(row=1, column=1)  
validateLogin = partial(validateLogin, username, password)
#login button
loginButton = Button(logonPage, text="Login", command=validateLogin).grid(row=4, column=0)  
logonPage.protocol("WM_DELETE_WINDOW", disable_event)
btn = Button(logonPage, text = "Click me to close", command = close_program).grid(row=5, column = 1)

root.protocol("WM_DELETE_WINDOW", close_program)

# notebook initialization
notebookMaster = ttk.Notebook(root)
notebookMaster.pack(expand = 1, fill = "both")
masterFrame1 = Frame(notebookMaster, bg="Skyblue2")
masterFrame2 = Frame(notebookMaster, bg = "Skyblue2")
masterFrame3= Frame(notebookMaster, bg = "Skyblue2")
notebookMaster.add(masterFrame1, text="User Information")
notebookMaster.add(masterFrame2, text="Search/Update")
notebookMaster.add(masterFrame3, text="Export & Reports")


"""
------------------------------------------------------------------
masterFrame1 section:
- User specific assignment
- Change status, add notes
------------------------------------------------------------------
"""
user = "'Simon'" # Need to change to pull from loging page
userViewWrap1 = LabelFrame(masterFrame1, text = "My Bug Assignments")
userViewWrap1.pack(fill = "both", expand = "yes", padx = 15, pady = 15)
userTreeview1 = ttk.Treeview(userViewWrap1, columns=(1,2,3,4,5), show = "headings")
userTreeview1.pack()
# fix bug number and description columns
userTreeview1.column("#1", anchor = CENTER, width = 90)
userTreeview1.column("#2", anchor = CENTER, width = 290)
# heading description
userTreeview1.heading(1, text = "Bug Number")
userTreeview1.heading(2, text = "Bug Description")
userTreeview1.heading(3, text = "Project")
userTreeview1.heading(4, text = "Expected Completion Date")
userTreeview1.heading(5, text = "Status")
# view user informaiton
queryUserview = "SELECT bug_number, bug_description, project, expected_completion_date, status FROM bugs WHERE assignee = " + user
cur.execute(queryUserview)
userviewRows = cur.fetchall()
# Call updateDatabase to view current dB contents into wrapper1
updateDatabase(userviewRows, userTreeview1)
# Event listener
userTreeview1.bind('<Double 1>', displayRowInfo)

"""
------------------------------------------------------------------
masterFrame2 section:
- Display all bugs in database
- Search database for results, display results
------------------------------------------------------------------
"""
min_w = 50
max_w = 200
cur_width = min_w
expanded = False

# Label Frames - Bug list, Search, Bug Data
wrapper1 = LabelFrame(masterFrame2, text = "Bug List")
wrapper1.pack(fill = "both", expand = "yes", padx = 20, pady = 20)
wrapper2 = LabelFrame(masterFrame2, text = "Search")
wrapper2.pack(fill = "both", expand = "yes", padx = 20, pady = 20)
wrapper3 = LabelFrame(masterFrame2, text = "Bug Data")
wrapper3.pack(fill = "both", expand = "yes", padx = 20, pady = 20)

# Tree view in wrapper 1
treeView1 = ttk.Treeview(wrapper1, columns=(1,2,3,4,5), show= "headings", height = "6")
treeView1.pack()
# Column Description
treeView1.column("#1", anchor = CENTER, width = 90)
treeView1.column("#2", anchor = CENTER, width = 290)
# Heading descriptions
treeView1.heading(1, text = "Bug Number")
treeView1.heading(2, text = "Bug Description")
treeView1.heading(3, text = "Project")
treeView1.heading(4, text = "Assignee")
treeView1.heading(5, text = "Expected Completion Date")
#Pull data from dB
query = "SELECT bug_number, bug_description, project, assignee, expected_completion_date FROM bugs"
cur.execute(query)
rows = cur.fetchall()
# Call updateDatabase to view current dB contents into wrapper1
updateDatabase(rows, treeView1)
# Event listener
treeView1.bind('<Double 1>', displayRowInfo)

"""
Search Section
"""
q = StringVar()
searchLabel = Label(wrapper2, text = "Search")
searchLabel.pack(side=LEFT, padx =10)
searchItem = Entry(wrapper2, textvariable=q)
searchItem.pack(side =LEFT, padx = 6)
searchButton = Button(wrapper2, text = "Search", command = searchDB_masterFrame2)
searchButton.pack(side = LEFT, padx = 5)

"""
Bug Data Section
"""

notebook1 = ttk.Notebook(wrapper3)
notebook1.pack(expand = 1, fill = "both")
notebook1Frame1 = ttk.Frame(notebook1)
notebook1Frame2 = ttk.Frame(notebook1)
notebook1.add(notebook1Frame1, text = "User Bugs")
notebook1.add(notebook1Frame2, text = "User Reports")
user_information = LabelFrame(notebook1Frame1, text = "User Information")
user_information.pack(fill = "both", expand = "yes")
user_reports = LabelFrame(notebook1Frame2, text = "User Reports")
user_reports.pack(fill = "both", expand = "yes")

# Exit button
exitButton = Button(root, text = "EXIT", command = root.destroy, bg = "blue", fg = "red")
exitButton.pack(padx = 10, pady = 10)

# Finish looping 
root.mainloop()

# Close databases
con.close()
user_pass.close()