import requests
import json
import secreteclass
from secreteclass import api_key


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


def main():
    base_url = 'https://mattgold65.wufoo.com/api/v3/' \
               'forms/termination-checklist-copy/entries/json'
    password = 'footastic'
    API = secreteclass.api_key
    get_request = issue_get_request(base_url, API, password)
    json = convert_request_to_json(get_request)
    print(json)
    write_to_file(json)


if __name__ == "__main__":
    main()
    
