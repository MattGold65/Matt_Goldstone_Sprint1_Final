import tkinter
from main import issue_get_request, convert_request_to_json,\
    newDatabase, newDatabaseTable, fetchDataframe
import requests
import sqlite3


def test_issue_get_request():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    test_get_request = issue_get_request(base_url, password)
    assert test_get_request.status_code == 200
    assert test_get_request.text != ""


def test_convert_to_json():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    get_request = issue_get_request(base_url, password)

    try:
        json_data = convert_request_to_json(get_request)

    except requests.exceptions.JSONDecodeError as json_decode_error:
        assert False, (f'An error occurred while trying to convert the '
                       f'response content to a JSON object:'
                       f' \n'f'{json_decode_error}')

    assert len(json_data['Entries']) >= 10


def test_newDatabase():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    get_request = issue_get_request(base_url, password)

    json_data = convert_request_to_json(get_request)

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

    for entry in json_data['Entries']:
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


def test_fetchDataframe():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    get_request = issue_get_request(base_url, password)

    json_data = convert_request_to_json(get_request)

    root = tkinter.Tk()

    entry = json_data['Entries'][5]

    assert fetchDataframe(root, entry, json_data)[0] \
           == json_data['Entries'][5].get('Field715', None) \
           + json_data['Entries'][5].get('Field1', None) \
           + json_data['Entries'][5].get('Field2', None)
    assert fetchDataframe(root, entry, json_data)[1] \
           == json_data['Entries'][5].get('Field713', None)
    assert fetchDataframe(root, entry, json_data)[2] \
           == json_data['Entries'][5].get('Field714', None)
    assert fetchDataframe(root, entry, json_data)[3] \
           == json_data['Entries'][5].get('Field918', None) \
           + json_data['Entries'][5].get('Field718', None)
    assert fetchDataframe(root, entry, json_data)[4] \
           == json_data['Entries'][5].get('Field817', None) \
           + json_data['Entries'][5].get('Field820', None)


def test_databaseTable():
    assert len(sqlite3.connect('testdb').execute
               ("SELECT testfield1 FROM 'testtable'").fetchall()) > 1
