from tkinter import Tk, Frame, Label, Button, Entry
import requests
import json
from secreteclass import api_key
import sqlite3
from PIL import ImageTk, Image
from itertools import chain


def issue_get_request(target_url: str, password: str):
    """This function passes in a Wufoo url, username, and password
    and returns a response object. If a get request is made unsuccessfully
    this function will return the error code and a description."""
    response = requests.get(target_url, auth=(api_key, password))
    if response.status_code != 200:
        print(f'The GET request was NOT successful\n'
              f'{response.status_code} [{response.reason}]')
        return response
    else:
        print(f'The get request was successful\n'
              f'{response.status_code} [{response.reason}]')
        return response


def convert_request_to_json(response_obj):
    """This function take a passes in a response object and
    converts it to json. If the response object cannot be
    converted to JSON this function will return an error
    message"""
    json_data_obj = None
    try:
        json_data_obj = response_obj.json()
        print(f'{"Response object content converted to JSON object."}')
    except requests.exceptions.JSONDecodeError as json_decode_error:
        print(f'An error occurred while trying to convert the response'
              f' content to a JSON object: \n'f'{json_decode_error}')
    finally:
        return json_data_obj


def write_to_file(data):
    """This object passes in JSON data and
    writes it to a .json file."""
    file_object = open(r"Entries.json", "w")
    file_object.write(json.dumps(data, indent=4))
    file_object.close()
    print("Entries sucessfully written")


def newDatabase(database_name):
    """This function passes in a database name as
     a parameter and creates a database connection """
    db_connection = None
    try:
        db_connection = sqlite3.connect(database_name)

    except sqlite3.Error as error:
        print(f'Database {error} has occurred'
              f' trying to connect to a new database')

    finally:
        return db_connection


def createDatabaseCursor(db_connection: sqlite3.Connection):
    """This function creates passes in a database connection
     as a parameter and returns a dbcursor. This function
    also checks for sqlite3 errors and returns
     an error message if the cursor cannot be created."""
    dbcursor = None

    try:

        dbcursor = db_connection.cursor()

    except sqlite3.Error as error:

        print(f'Database {error} has occurred trying to create a cursor')

    finally:
        return dbcursor


def newDatabaseTable(cursor: sqlite3.Cursor, tablename, *fields):
    """This function passes in a database cursor, a tablename,
    and table fields. Then it creates a table in the database
     if it does not already exist. The function will also return
      an error message if the table cannot be created."""
    try:
        tableCreationString = f'CREATE TABLE ' \
                              f'IF NOT EXISTS {tablename}{fields};'
        cursor.execute(tableCreationString)

    except sqlite3.Error as error:

        print(f'Database {error} has occurred trying to create a table')

def establishDatabase(dbcursor, json):
    dbcursor.execute('DELETE FROM guest_infomation')
    dbcursor.execute('DELETE FROM collab_opps')
    dbcursor.execute('DELETE FROM collab_time')

    for entry in json['Entries']:
        dbcursor.execute('''INSERT INTO guest_infomation
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (entry.get('EntryId', None),
                          entry.get('Field715', None),
                          entry.get('Field1', None),
                          entry.get('Field2', None),
                          entry.get('Field711', None),
                          entry.get('Field713', None),
                          entry.get('Field917', None),
                          entry.get('Field716', None),
                          entry.get('Field714', None),
                          entry.get('Field918', None)))

        dbcursor.execute('''INSERT INTO collab_opps
            VALUES(?,?,?,?,?,?,?,?)''',
                         (entry.get('EntryId', None),
                          entry.get('Field717', None),
                          entry.get('Field718', None),
                          entry.get('Field719', None),
                          entry.get('Field720', None),
                          entry.get('Field721', None),
                          entry.get('Field722', None),
                          entry.get('Field723', None)))

        dbcursor.execute('''INSERT INTO collab_time
            VALUES(?,?,?,?,?,?)''',
                         (entry.get('EntryId', None),
                          entry.get('Field817', None),
                          entry.get('Field818', None),
                          entry.get('Field819', None),
                          entry.get('Field820', None),
                          entry.get('Field821', None)))




def generateButtons(frame, root, dbcursor, dbconnection):
    unclaimed_entries = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'guest_infomation'").fetchall()
    Prefix = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Prefix FROM 'guest_infomation'").fetchall()
    Orgname = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Orgname FROM 'guest_infomation'").fetchall()
    Last = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT LastName FROM 'guest_infomation'").fetchall()
    Entry_count = len(unclaimed_entries)


    claimed_entries = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'claimed_projects'").fetchall()

    claimed_entries_list = tuple(map(int,chain.from_iterable(claimed_entries)))

    unclaimed_entries_list = tuple(map(int,chain.from_iterable(unclaimed_entries)))

    print(claimed_entries_list)
    print(unclaimed_entries_list)

    for entry in range(Entry_count):

        if(unclaimed_entries_list[entry] in claimed_entries_list):
            Button(frame, text=Prefix[entry][0]
                               + Last[entry][0] + " : " +
                               Orgname[entry][0],
                   font=("TKHeadingFont", 10), bg="green", fg="white",
                   cursor="hand2", activebackground="#badee2",
                   activeforeground="#f00505",
                   command=lambda entry=entry:
                   fetchDataframe(root, entry, dbcursor, dbconnection)).pack(pady=10)
        else:
            Button(frame, text=Prefix[entry][0]
                   + Last[entry][0] + " : " +
                   Orgname[entry][0],
                   font=("TKHeadingFont", 10), bg="#89191F", fg="white",
                   cursor="hand2", activebackground="#badee2",
                   activeforeground="#f00505",
                   command=lambda entry=entry:
                   fetchDataframe(root, entry, dbcursor, dbconnection)).pack(pady=10)

def refreshButtons(json, frame, root, dbcursor, dbconnection):
    claimed_entries = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'claimed_projects'").fetchall()
    fixed_tuple = chain.from_iterable(claimed_entries)
    claimed_entries_list = tuple(map(int, fixed_tuple))

    unclaimed_entries = sqlite3.connect('Wufoo_Enries_db.db').execute(
        "SELECT EntryID FROM 'guest_infomation'").fetchall()

    unclaimed_entries_list = tuple(map(int, chain.from_iterable(unclaimed_entries)))

    iterator = 0
    for entry in json['Entries']:
        if(unclaimed_entries_list[iterator] in claimed_entries_list):
            Button(frame, text=entry.get('Field715', None)
                               + entry.get('Field2', None) + " : " +
                               entry.get('Field713', None),
                   font=("TKHeadingFont", 10), bg="green", fg="white",
                   cursor="hand2", activebackground="#badee2",
                   activeforeground="#f00505",
                   command=lambda entry=entry:
                   refreshDataframe(root, entry, dbcursor, dbconnection)).pack(pady=10)
        else:
            Button(frame, text=entry.get('Field715', None)
                   + entry.get('Field2', None) + " : " +
                   entry.get('Field713', None),
                   font=("TKHeadingFont", 10), bg="#89191F", fg="white",
                   cursor="hand2", activebackground="#badee2",
                   activeforeground="#f00505",
                   command=lambda entry=entry:
                   refreshDataframe(root, entry, dbcursor, dbconnection)).pack(pady=10)

        iterator = iterator + 1





def generateMainframe(root, dbcursor,dbconnection):
    Mainframe = Frame(root, width=1000, height=1200, bg="white")
    Mainframe.grid(row=0, column=0, sticky="nesw")
    Mainframe.pack_propagate(False)

    pic = Image.open("standard.png")
    resized_pic = pic.resize((450, 120), Image.Resampling.LANCZOS)
    photo_label = ImageTk.PhotoImage(resized_pic)
    img_label = Label(Mainframe, image=photo_label)
    img_label.image_ref = photo_label
    img_label.pack(pady=20)

    Label(Mainframe, text="Refresh:", bg="white",
          fg="#3d3d3d", font=("TkDefaultFont", 14, "bold")).pack()

    Button(Mainframe, text="Refresh",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="#f00505",
           command= lambda: refreashMainframe(root)).pack(pady=10)

    Label(Mainframe, text="Select an Entry:", bg="white",
          fg="#3d3d3d", font=("TkDefaultFont", 14, "bold")).pack()
    generateButtons(Mainframe, root, dbcursor, dbconnection)


def refreashMainframe(root):
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    get_request = issue_get_request(base_url, password)
    json = convert_request_to_json(get_request)

    dbconnection = newDatabase('Wufoo_Enries_db.db')
    dbcursor = createDatabaseCursor(dbconnection)
    newDatabaseTable(dbcursor, 'guest_infomation', 'EntryID', 'Prefix',
                     'FirstName', 'LastName', 'Title', 'OrgName',
                     'Email', 'OrgWebsite', 'PhoneNum', 'NameAuth')
    newDatabaseTable(dbcursor, 'collab_opps', 'EntryID',
                     'CoursePro', 'GuestSpeak', 'SiteVisit', 'JobShadow',
                     'Internship', 'CareerPan', 'NetEvent')
    newDatabaseTable(dbcursor, 'collab_time', 'EntryID', 'Summer2022',
                     'Fall2022', 'Spring2023', 'Summer2023', 'Other')
    newDatabaseTable(dbcursor, 'claimed_projects', 'Email', 'EntryID', 'FirstName', 'LastName', 'Title', 'Department')
    establishDatabase(dbcursor, json)

    dbconnection.commit()

    newMainframe = Frame(root, width=1000, height=1200, bg="white")
    newMainframe.grid(row=0, column=0, sticky="nesw")
    newMainframe.pack_propagate(False)

    pic = Image.open("standard.png")
    resized_pic = pic.resize((450, 120), Image.Resampling.LANCZOS)
    photo_label = ImageTk.PhotoImage(resized_pic)
    img_label = Label(newMainframe, image=photo_label)
    img_label.image_ref = photo_label
    img_label.pack(pady=20)

    Label(newMainframe, text="Select an Entry:", bg="white",
          fg="#3d3d3d", font=("TkDefaultFont", 14, "bold")).pack()
    refreshButtons(json, newMainframe, root, dbcursor, dbconnection)







def fetchDataframe(root, entry, dbcursor, dbconnection):
    EntryID = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'guest_infomation'").fetchall()
    claimed_entries = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'claimed_projects'").fetchall()
    Prefix = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Prefix FROM 'guest_infomation'").fetchall()
    First = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT FirstName FROM 'guest_infomation'").fetchall()
    Last = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT LastName FROM 'guest_infomation'").fetchall()
    Title = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Title FROM 'guest_infomation'").fetchall()
    OrgName = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT OrgName FROM 'guest_infomation'").fetchall()
    Email = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Email FROM 'guest_infomation'").fetchall()
    OrgWebsite = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT OrgWebsite FROM 'guest_infomation'").fetchall()
    PhoneNum = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT PhoneNum FROM 'guest_infomation'").fetchall()
    NameAuth = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT NameAuth FROM 'guest_infomation'").fetchall()

    Summer2022 = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Summer2022 FROM 'collab_time'").fetchall()
    Fall2022 = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Fall2022 FROM 'collab_time'").fetchall()
    Spring2023 = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Spring2023 FROM 'collab_time'").fetchall()
    Summer2023 = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Summer2023 FROM 'collab_time'").fetchall()
    Other = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Other FROM 'collab_time'").fetchall()

    CoursePro = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT CoursePro FROM 'collab_opps'").fetchall()
    GuestSpeak = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT GuestSpeak FROM 'collab_opps'").fetchall()
    SiteVisit = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT SiteVisit FROM 'collab_opps'").fetchall()
    JobShadow = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT JobShadow FROM 'collab_opps'").fetchall()
    Internship = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Internship FROM 'collab_opps'").fetchall()
    CareerPan = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT CareerPan FROM 'collab_opps'").fetchall()
    NetEvent = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT NetEvent FROM 'collab_opps'").fetchall()

    bsuEmail = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Email FROM 'claimed_projects'").fetchall()
    FirstName = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT FirstName FROM 'claimed_projects'").fetchall()
    LastName = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT LastName FROM 'claimed_projects'").fetchall()
    bsuTitle = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Title FROM 'claimed_projects'").fetchall()
    Department = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT Department FROM 'claimed_projects'").fetchall()


    Dataframe = Frame(root, bg="#89191F")
    Dataframe.grid(row=0, column=0, sticky="nesw")

    Label(Dataframe, text="Name: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=Prefix[entry][0]
          + First[entry][0]
          + " " + Last[entry][0],
          bg="#89191F", fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Company: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=OrgName[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Title: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=Title[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Email: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=Email[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Organization Website: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=OrgWebsite[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Phone Number: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=PhoneNum[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Permission: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=NameAuth[entry][0], bg="#89191F",
          fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Collaberation Opportunities: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=" [" + CoursePro[entry][0] + "]" +
                          "\n" + " [" + GuestSpeak[entry][0] + "]" +
                          "\n" + " [" + SiteVisit[entry][0] + "]" +
                          "\n" + " [" + JobShadow[entry][0] + "]" +
                          "\n" + " [" + Internship[entry][0] + "]" +
                          "\n" + " [" + CareerPan[entry][0] + "]" +
                          "\n" + " [" + NetEvent[entry][0] + "]",
                          bg="#89191F", fg="white",
                          font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="Collaberation Time: ",
                          bg="#89191F", fg="white",
                          font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=" [" + Summer2022[entry][0] + "]" +
                          "\n" + " [" + Fall2022[entry][0] + "]" +
                          "\n" + " [" + Spring2023[entry][0] + "]" +
                          "\n" + " [" + Summer2023[entry][0] + "]" +
                          "\n" + " [" + Other[entry][0] + "]",
                          bg="#89191F", fg="white",
                          font=("TkDefaultFont", 12)).pack()

    Button(Dataframe,
           text="Claim Project",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: claimProject(root, entry, dbcursor, dbconnection)).pack(pady=10)

    Button(Dataframe,
           text="Go Back",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: generateMainframe(root, dbcursor,dbconnection)).pack(pady=10)

    #Name = entry.get('Field715', None) +\
        #entry.get('Field1', None) +\
        #entry.get('Field2', None)
    #Company = entry.get('Field713', None)
    #phone_number = entry.get('Field714', None)
    #collab_opps = entry.get('Field918', None) + entry.get('Field718', None)
    #collab_time = entry.get('Field817', None) + entry.get('Field820', None)

    #return Name, Company, phone_number, collab_opps, collab_time

def refreshDataframe(root, entry, dbcursor, dbconnection):
    sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'guest_infomation'").fetchall()


    Dataframe = Frame(root, bg="#89191F")
    Dataframe.grid(row=0, column=0, sticky="nesw")

    Label(Dataframe, text="Full Name:", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field715', None)
                            + entry.get('Field1', None)
                            + " " + entry.get('Field2', None),
            bg="#89191F", fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Company: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field713', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Title: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field711', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Email: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field917', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Organization Website: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field716', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Phone Number: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field714', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Permission: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    Label(Dataframe, text=entry.get('Field918', None), bg="#89191F",
            fg="white", font=("TkDefaultFont", 10)).pack()

    Label(Dataframe, text="Collaberation Opportunities: ", bg="#89191F",
            fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=" [" + entry.get('Field717', None) + "]" +
                            "\n" + " [" + entry.get('Field718', None) + "]" +
                            "\n" + " [" + entry.get('Field719', None) + "]" +
                            "\n" + " [" + entry.get('Field720', None) + "]" +
                            "\n" + " [" + entry.get('Field721', None) + "]" +
                            "\n" + " [" + entry.get('Field722', None) + "]" +
                            "\n" + " [" + entry.get('Field723', None) + "]",
            bg="#89191F", fg="white",
            font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="Collaberation Time: ",
            bg="#89191F", fg="white",
            font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=" [" + entry.get('Field817', None) + "]" +
                            "\n" + " [" + entry.get('Field818', None) + "]" +
                            "\n" + " [" + entry.get('Field819', None) + "]" +
                            "\n" + " [" + entry.get('Field820', None) + "]" +
                            "\n" + " [" + entry.get('Field821', None) + "]",
            bg="#89191F", fg="white",
            font=("TkDefaultFont", 12)).pack()
    Button(Dataframe,
           text="Claim Project",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: claimProject(root, entry, dbcursor, dbconnection)).pack(pady=10)

    Button(Dataframe,
            text="Go Back",
            font=("TKHeadingFont", 10), bg="#89191F", fg="white",
            cursor="hand2", activebackground="#badee2",
            activeforeground="blue",
            command=lambda: generateMainframe(root, dbcursor, dbconnection)).pack(pady=10)

def claimProject(root, entry, dbcursor, dbconnection):
    Dataframe = Frame(root, bg="#89191F")
    Dataframe.grid(row=0, column=0, sticky="nesw")

    Label(Dataframe, text="First Name:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    firstnamefield = Entry(Dataframe, width=50, borderwidth=5)
    firstnamefield.pack()

    Label(Dataframe, text="Last Name:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    lastnamefield = Entry(Dataframe, width=50, borderwidth=5)
    lastnamefield.pack()

    Label(Dataframe, text="Title:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    titlefield = Entry(Dataframe, width=50, borderwidth=5)
    titlefield.pack()

    Label(Dataframe, text="BSU Email:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    BSUfield = Entry(Dataframe, width=50, borderwidth=5)
    BSUfield.pack()

    Label(Dataframe, text="Department:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 12, "bold")).pack()
    departmentfield = Entry(Dataframe, width=50, borderwidth=5)
    departmentfield.pack()

    EntryQuerry = sqlite3.connect('Wufoo_Enries_db.db').execute("SELECT EntryID FROM 'guest_infomation'").fetchall()

    if(isinstance((entry),int)):
        EntryID = EntryQuerry[entry][0]
    else:
        EntryID = entry.get('EntryId', None)

    print(EntryID)


    Button(Dataframe,
           text="Submit",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: SubmitEntry(dbcursor, dbconnection, BSUfield.get(), EntryID, firstnamefield.get(), lastnamefield.get(),titlefield.get(), departmentfield.get())).pack(pady=10)


    Button(Dataframe,
           text="Go Back",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: generateMainframe(root, dbcursor, dbconnection)).pack(pady=10)

    """
    **NOTE**
    CREATE A NEW DATAFRAME THAT ONLY APPEARS WHEN YOU SELECT A CHOSEN (GREEN) BUTTON BY CHANGING THE COMMAND,
    FOR THE BUTTONS THAT HAVE ALREADY BEEN CHOSEN AND TURN GREEN, TO NAVIGATE TO A NEW DATAFRAME THAT HAS 
    INFOMATION ABOUT THE PERSON WHO SELECTED THAT PROJECT
    """

def SubmitEntry(dbcursor, dbconnection, email, EntryID, first, last, title, department):
    dbcursor.execute('''INSERT INTO 'claimed_projects'
                    VALUES(?,?,?,?,?,?)''',
                     (email, EntryID, first, last, title, department))

    dbconnection.commit()


def initiallizeGUI(dbcursor, dbconnection):
    root = Tk()
    root.title("WUFOO Database")
    root.eval("tk::PlaceWindow . center")
    generateMainframe(root,dbcursor,dbconnection)
    root.mainloop()


def main():
    """This function calls all the functions
     above and runs the program."""


    dbconnection = newDatabase('Wufoo_Enries_db.db')
    dbcursor = createDatabaseCursor(dbconnection)
    newDatabaseTable(dbcursor, 'guest_infomation', 'EntryID', 'Prefix',
                     'FirstName', 'LastName', 'Title', 'OrgName',
                     'Email', 'OrgWebsite', 'PhoneNum', 'NameAuth')
    newDatabaseTable(dbcursor, 'collab_opps', 'EntryID',
                     'CoursePro', 'GuestSpeak', 'SiteVisit', 'JobShadow',
                     'Internship', 'CareerPan', 'NetEvent')
    newDatabaseTable(dbcursor, 'collab_time', 'EntryID', 'Summer2022',
                     'Fall2022', 'Spring2023', 'Summer2023', 'Other')
    newDatabaseTable(dbcursor,'claimed_projects', 'Email', 'EntryID', 'FirstName', 'LastName', 'Title', 'Department')

    initiallizeGUI(dbcursor, dbconnection)


    dbconnection.commit()
    dbconnection.close()


if __name__ == "__main__":
    main()
