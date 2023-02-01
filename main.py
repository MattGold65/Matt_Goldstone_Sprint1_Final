import requests
import json
from secreteclass import api_key
import sqlite3


def issue_get_request(target_url: str, username: str, password: str):
    response = requests.get(target_url, auth=(username, password))
    if response.status_code != 200:
        print(f'The GET request was NOT successful\n'
              f'{response.status_code} [{response.reason}]')
        return response
    else:
        print(f'The get request was successful\n'
              f'{response.status_code} [{response.reason}]')
        return response


def convert_request_to_json(response_obj):
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
    file_object = open(r"Entries.json", "w")
    file_object.write(json.dumps(data, indent=4))
    file_object.close()
    print("Entries sucessfully written")


def newDatabase(database_name):
    """This function passes in a database name as a parameter and creates a database connection """
    db_connection = None
    try:
        db_connection = sqlite3.connect(database_name)

    except sqlite3.Error as error:
        print(f'Database {error} has occurred trying to connect to a new database')

    finally:
        return db_connection


def createDatabaseCursor(db_connection: sqlite3.Connection):
    """This function creates passes in a database connection as a parameter and returns a dbcursor. This function
    also checks for sqlite3 errors and returns an error message if the cursor cannot be created."""
    dbcursor = None

    try:

        dbcursor = db_connection.cursor()


    except sqlite3.Error as error:

        print(f'Database {error} has occurred trying to create a cursor')


    finally:
        return dbcursor



def newDatabaseTable(cursor: sqlite3.Cursor, tablename):
    """This function passes in a database cursor and a tablename. Then it creates a table in the database if it does
    not already exist. The function will also return an error message if the table cannot be created. """
    try:
        tableCreationString = f'CREATE TABLE IF NOT EXISTS {tablename}(Entry_ID TEXT, Prefix TEXT, Emp_First TEXT, EMP_Last TEXT, Title TEXT, Org_Name TEXT,' \
                              f' Email TEXT, Org_Website TEXT, Phone_Num TEXT, Course_Project TEXT, Guest_Speaker TEXT, Site_Visit TEXT, Job_Shadow TEXT,' \
                              f'Internships TEXT, Career_Panel TEXT, Networking_Events TEXT, Summer_2022 TEXT, Fall_2022 TEXT, Spring_2023 TEXT, Summer_2023 TEXT, ' \
                              f'Other TEXT, Permission TEXT);'
        cursor.execute(tableCreationString)

    except sqlite3.Error as error:

        print(f'Database {error} has occurred trying to create a table')





def main():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    API = api_key
    get_request = issue_get_request(base_url, API, password)
    json = convert_request_to_json(get_request)
    print(json)
    dbconnection = newDatabase('Wufoo_Enries_db.db')
    dbcursor = createDatabaseCursor(dbconnection)
    newDatabaseTable(dbcursor, 'fourm_entries')
    write_to_file(json)

    dbcursor.execute('DELETE FROM fourm_entries')

    for entry in json['Entries']:
        dbcursor.execute('''INSERT INTO fourm_entries VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (entry.get('EntryId', None),
                                                                                entry.get('Field715', None),
                                                                                entry.get('Field1', None),
                                                                                entry.get('Field2', None),
                                                                                entry.get('Field711', None),
                                                                                entry.get('Field713', None),
                                                                                entry.get('Field917', None),
                                                                                entry.get('Field716', None),
                                                                                entry.get('Field714', None),
                                                                                entry.get('Field717', None),
                                                                                entry.get('Field718', None),
                                                                                entry.get('Field719', None),
                                                                                entry.get('Field720', None),
                                                                                entry.get('Field721', None),
                                                                                entry.get('Field722', None),
                                                                                entry.get('Field723', None),
                                                                                entry.get('Field817', None),
                                                                                entry.get('Field818', None),
                                                                                entry.get('Field819', None),
                                                                                entry.get('Field820', None),
                                                                                entry.get('Field821', None),
                                                                                entry.get('Field918', None)))


    dbconnection.commit()
    dbconnection.close()


if __name__ == "__main__":
    main()
