from tkinter import Tk
from main import issue_get_request, convert_request_to_json,\
    newDatabase, newDatabaseTable, refreshDataframe
import requests
import sqlite3
from itertools import chain


def test_issue_get_request():
    """Tests the functions issue_get_request() to make sure the
     program can make a successful get request"""
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    test_get_request = issue_get_request(base_url, password)
    assert test_get_request.status_code == 200
    assert test_get_request.text != ""
    return test_get_request


def test_convert_to_json():
    """Tests function convert_request_to_json to ensure
    the program can sucesfully take the get request and
    convert it into a json object"""

    try:
        json_data = convert_request_to_json(test_issue_get_request())

    except requests.exceptions.JSONDecodeError as json_decode_error:
        assert False, (f'An error occurred while trying to convert the '
                       f'response content to a JSON object:'
                       f' \n'f'{json_decode_error}')

    assert len(json_data['Entries']) >= 10

    return json_data


def test_newDatabase():
    """Tests newDatabase() function to ensure that a new
    database is properly setup and the data from the json
    object is sucessfully entered into the database.
    This function also simulates user entry into testtable2
    that will be used in test_EntrySubmissionTable(),
    test_SubmitEntryWithExisitngEmail(), and test_refreshButtons()"""

    database_name = 'testdb'
    table_name = 'testtable'
    table_name2 = 'testtable2'
    testEmail = "test@bridgew.edu"
    EntryId = 8
    first_name_string = "testfirst"

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
                                               'testfield5', 'testfield6',
                                               )
        tableCreationString2 = newDatabaseTable(dbcursor, table_name2,
                                                'testemail', 'testEntryId',
                                                'testfirstname')

    except sqlite3.Error as error:

        assert False, print(f'Database {error} has occurred'
                            f' trying to create a table')

    assert tableCreationString != ""
    assert tableCreationString2 != ""

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
    dbcursor.execute('DELETE FROM testtable2')

    dbcursor.execute('''INSERT INTO 'testtable2'
                            VALUES(?,?,?)''',
                     (testEmail, EntryId, first_name_string))
    test_database.commit()

    return dbcursor, test_database


def test_refreshDataframe():
    """Tests refreshDataframe() and ensures that the data that is
    being written to the Dataframe page mataches the data
    in the json file"""
    root = Tk()
    json_data = test_convert_to_json()

    entry = json_data['Entries'][5]
    assert refreshDataframe(root, entry, test_newDatabase()[0],
                            test_newDatabase()[1])[0] \
           == json_data['Entries'][5].get('Field715', None) \
           + json_data['Entries'][5].get('Field1', None) \
           + json_data['Entries'][5].get('Field2', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0],
                            test_newDatabase()[1])[1] \
           == json_data['Entries'][5].get('Field713', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0],
                            test_newDatabase()[1])[2] \
           == json_data['Entries'][5].get('Field714', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0],
                            test_newDatabase()[1])[3] \
           == json_data['Entries'][5].get('Field918', None) \
           + json_data['Entries'][5].get('Field718', None)
    assert refreshDataframe(root, entry, test_newDatabase()[0],
                            test_newDatabase()[1])[4] \
           == json_data['Entries'][5].get('Field817', None) \
           + json_data['Entries'][5].get('Field820', None)


def test_databaseTable():
    """Tests the database testtable and makes sure data was
     sucessfully entered into the table"""
    assert len(sqlite3.connect('testdb').execute
               ("SELECT testfield1 FROM 'testtable'").fetchall()) > 1


def test_EntrySubmissionTable():
    """Tests the testtable2 and ensures the data was sucesfully entered
    into the table"""
    assert len(sqlite3.connect('testdb')
               .execute("SELECT testemail FROM 'testtable2'").fetchall()) > 0


def test_SubmitEntryWithExisitngEmail():
    """Tests the email autofill functionality by passing in a
     matching email and first name and ensuring that the sql
    querries pulls a matching email and name by only matching the emails
    in the where statement. Here we use the email as the primary key."""
    testEmail = "test@bridgew.edu"
    first_name_string = "testfirst"
    bsuEmail = sqlite3.connect('testdb') \
        .execute("SELECT testemail FROM 'testtable2'"
                 "WHERE testemail = (?)", (testEmail,)).fetchall()
    FirstName = sqlite3.connect('testdb') \
        .execute("SELECT testfirstName FROM 'testtable2'"
                 " WHERE testEmail = (?)", (testEmail,)).fetchall()

    assert testEmail == bsuEmail[0][0]
    assert first_name_string == FirstName[0][0]


def test_refreshButtons():
    """This function ensures that the refreshbuttons functions is
     producing the correct amount of red, green, and total buttons by
    ensuring that when an entryID on the testtable matches an entryID
    from testable2 the button is green. Otherwise this functon should
    produce a red button for every unclaimed entry. The red buttons
    + green buttons should equal the total amount of entries in the json
    file"""

    json = test_convert_to_json()
    claimed_entries = sqlite3.connect('testdb'). \
        execute("SELECT testEntryID FROM 'testtable2'").fetchall()
    fixed_tuple = chain.from_iterable(claimed_entries)
    claimed_entries_list = tuple(map(int, fixed_tuple))

    unclaimed_entries = sqlite3.connect('testdb').execute(
        "SELECT testfield1 FROM 'testtable'").fetchall()

    unclaimed_entries_list = \
        tuple(map(int, chain.from_iterable(unclaimed_entries)))

    iterator = 0
    red_button_counter = 0
    green_button_counter = 0
    for entry in test_convert_to_json()['Entries']:
        if (unclaimed_entries_list[iterator] in claimed_entries_list):
            green_button_counter = green_button_counter + 1
        else:
            red_button_counter = red_button_counter + 1

        iterator = iterator + 1

    assert iterator == len(test_convert_to_json()['Entries'])
    assert green_button_counter > 0
    assert red_button_counter > 5
    assert red_button_counter + green_button_counter == iterator
    assert iterator == len(json['Entries'])
