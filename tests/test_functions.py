from tkinter import Tk, Frame
from main import issue_get_request, convert_request_to_json,\
    newDatabase, newDatabaseTable, refreshDataframe
import requests
import sqlite3


def test_issue_get_request():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    test_get_request = issue_get_request(base_url, password)
    assert test_get_request.status_code == 200
    assert test_get_request.text != ""
    return test_get_request


def test_convert_to_json():

    try:
        json_data = convert_request_to_json(test_issue_get_request())

    except requests.exceptions.JSONDecodeError as json_decode_error:
        assert False, (f'An error occurred while trying to convert the '
                       f'response content to a JSON object:'
                       f' \n'f'{json_decode_error}')

    assert len(json_data['Entries']) >= 10

    return json_data


def test_newDatabase():

    database_name = 'testdb'
    table_name = 'testtable'

    try:
        test_database = newDatabase(database_name)

    except sqlite3.Error as error:
        assert False, print(f'Database {error} has occurred'
                            f' trying to connect to a new database')

    assert test_database is not None

    try:
        dbcursor = test_database.cursor()

    except sqlite3.Error as error:
        assert False, print(f'Database {error} has occurred'
                            f' trying to create a cursor')

    assert dbcursor is not None

    try:
        tableCreationString = newDatabaseTable(dbcursor, table_name,
                                               'testfield1', 'testfield2',
                                               'testfield3', 'testfield4',
                                               'testfield5', 'testfield6')

    except sqlite3.Error as error:

        assert False, print(f'Database {error} has occurred'
                            f' trying to create a table')

    assert tableCreationString != ""

    dbcursor.execute('DELETE FROM testtable')

    for entry in test_convert_to_json()['Entries']:
        dbcursor.execute('''INSERT INTO 'testtable'
         VALUES(?, ?, ?, ?, ?, ?)''',
                         (entry.get('EntryId', None),
                          entry.get('Field715', None),
                          entry.get('Field1', None),
                          entry.get('Field2', None),
                          entry.get('Field711', None),
                          entry.get('Field723', None)))

    assert len(entry) > 5
    test_database.commit()
    test_database.close()

    return dbcursor, test_database


def test_refreshDataframe():
    root = tkinter.Tk()
    json_data = test_convert_to_json()

    entry = json_data['Entries'][5]
    assert refreshDataframe(root, entry, test_newDatabase()[0], test_newDatabase()[1])[0] \
           == json_data['Entries'][5].get('Field715', None) \
           + json_data['Entries'][5].get('Field1', None) \
           + json_data['Entries'][5].get('Field2', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0], test_newDatabase()[1])[1] \
           == json_data['Entries'][5].get('Field713', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0], test_newDatabase()[1])[2] \
           == json_data['Entries'][5].get('Field714', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0], test_newDatabase()[1])[3] \
           == json_data['Entries'][5].get('Field918', None) \
           + json_data['Entries'][5].get('Field718', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0], test_newDatabase()[1])[4] \
           == json_data['Entries'][5].get('Field817', None) \
           + json_data['Entries'][5].get('Field820', None)


def test_databaseTable():
    assert len(sqlite3.connect('testdb').execute
               ("SELECT testfield1 FROM 'testtable'").fetchall()) > 1
def test_fetchDataframe():
    Prefix = sqlite3.connect('testdb'). \
        execute("SELECT Prefix FROM 'testtable'").fetchall()
    First = sqlite3.connect('testdb'). \
        execute("SELECT FirstName FROM 'testtable'").fetchall()
    Last = sqlite3.connect('testdb'). \
        execute("SELECT LastName FROM 'testtable'").fetchall()
    OrgWebsite = sqlite3.connect('testdb'). \
        execute("SELECT OrgWebsite FROM 'testtable'").fetchall()
    PhoneNum = sqlite3.connect('Wufoo_Enries_db.db'). \
        execute("SELECT PhoneNum FROM 'testtable'").fetchall()

    GuestSpeak = sqlite3.connect('testdb'). \
        execute("SELECT GuestSpeak FROM 'testtable'").fetchall()
    SiteVisit = sqlite3.connect('testdb'). \
        execute("SELECT SiteVisit FROM 'testtable'").fetchall()

    Spring2023 = sqlite3.connect('testdb'). \
        execute("SELECT Spring2023 FROM 'testtable'").fetchall()
    Summer2023 = sqlite3.connect('testdb'). \
        execute("SELECT Summer2023 FROM 'testtable'").fetchall()
    json = test_convert_to_json()
    root = Tk()
    frame = Frame(root, width=1000, height=1200, bg="white")
    dbcursor = test_newDatabase()[0]
    dbconnection = test_newDatabase()[1]



    assert refreshDataframe(json, frame, root, dbcursor, dbconnection)[0] == Prefix + First + Last