from tkinter import Tk, Frame, Label, Button
import requests
import json
from secreteclass import api_key
import sqlite3
from PIL import ImageTk, Image


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


def generateButtons(json, frame, root):

    for entry in json['Entries']:

        Button(frame, text=entry.get('Field715', None)
               + entry.get('Field2', None) + " : " +
               entry.get('Field713', None),
               font=("TKHeadingFont", 10), bg="#89191F", fg="white",
               cursor="hand2", activebackground="#badee2",
               activeforeground="#f00505",
               command=lambda entry=entry:
               fetchDataframe(root, entry, json)).pack(pady=10)


def generateMainframe(json, root):
    Mainframe = Frame(root, width=1000, height=1200, bg="white")
    Mainframe.grid(row=0, column=0, sticky="nesw")
    Mainframe.pack_propagate(False)

    pic = Image.open("standard.png")
    resized_pic = pic.resize((450, 120), Image.Resampling.LANCZOS)
    photo_label = ImageTk.PhotoImage(resized_pic)
    img_label = Label(Mainframe, image=photo_label)
    img_label.image_ref = photo_label
    img_label.pack(pady=20)

    Label(Mainframe, text="Select an Entry:", bg="white",
          fg="#3d3d3d", font=("TkDefaultFont", 14, "bold")).pack()
    generateButtons(json, Mainframe, root)


def fetchDataframe(root, entry, json):
    Dataframe = Frame(root, bg="#89191F")
    Dataframe.grid(row=0, column=0, sticky="nesw")

    Label(Dataframe, text="Full Name:", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field715', None)
          + entry.get('Field1', None)
          + " " + entry.get('Field2', None),
          bg="#89191F", fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Company: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field713', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Title: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field711', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Email: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field917', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Organization Website: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field716', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Phone Number: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field714', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Permission: ", bg="#89191F",
          fg="white", font=("TkDefaultFont", 14, "bold")).pack()
    Label(Dataframe, text=entry.get('Field918', None), bg="#89191F",
          fg="white", font=("TkDefaultFont", 12)).pack()

    Label(Dataframe, text="\n" + "Collaberation Opportunities: ", bg="#89191F",
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

    Label(Dataframe, text="\n" + "Collaberation Time: ",
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
           text="Go Back",
           font=("TKHeadingFont", 10), bg="#89191F", fg="white",
           cursor="hand2", activebackground="#badee2",
           activeforeground="blue",
           command=lambda: generateMainframe(json, root)).pack(pady=10)

    Name = entry.get('Field715', None) +\
        entry.get('Field1', None) +\
        entry.get('Field2', None)
    Company = entry.get('Field713', None)
    phone_number = entry.get('Field714', None)
    collab_opps = entry.get('Field918', None) + entry.get('Field718', None)
    collab_time = entry.get('Field817', None) + entry.get('Field820', None)

    return Name, Company, phone_number, collab_opps, collab_time


def initiallizeGUI(json):
    root = Tk()
    root.title("WUFOO Database")
    root.eval("tk::PlaceWindow . center")
    generateMainframe(json, root)
    root.mainloop()


def main():
    """This function calls all the functions
     above and runs the program."""
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
        'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    get_request = issue_get_request(base_url, password)
    json = convert_request_to_json(get_request)
    initiallizeGUI(json)
    entry = json['Entries'][5]
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
    write_to_file(json)

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

    dbconnection.commit()
    dbconnection.close()


if __name__ == "__main__":
    main()
