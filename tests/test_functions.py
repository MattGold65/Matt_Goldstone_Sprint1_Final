from main import issue_get_request, convert_request_to_json,\
    newDatabase, newDatabaseTable
from secreteclass import api_key
import requests
import sqlite3
import pytest

def test_issue_get_request():

    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    API = api_key
    test_get_request = issue_get_request(base_url, API, password)
    assert test_get_request.status_code == 200
    assert test_get_request.text != ""


def test_convert_to_json():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    API = api_key
    get_request = issue_get_request(base_url, API, password)

    try:
        json_data = convert_request_to_json(get_request)

    except requests.exceptions.JSONDecodeError as json_decode_error:
        assert False, (f'An error occurred while trying to convert the '
                       f'response content to a JSON object:'
                       f' \n'f'{json_decode_error}')

    assert len(json_data['Entries'][0]) > 10


def test_newDatabase():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    API = api_key
    get_request = issue_get_request(base_url, API, password)

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
