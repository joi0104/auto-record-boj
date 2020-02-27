import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def get_setup_data():
    with open('setup.json') as json_file:
        setup_data = json.load(json_file)
    return setup_data

def get_boj_file_list(setup_data):
    file_extension = setup_data['file_extension']
    file_list = os.listdir(setup_data['path'])

    boj_file_list = [file[:file.index('.')] for file in file_list if file[file.index('.'):] in file_extension]
    return boj_file_list

def get_new_solved_list(setup_data):
    new_solved_list = []
    boj_file_list = get_boj_file_list(setup_data)

    with open('setup.json', 'w', encoding='utf-8') as make_file:
        for i in boj_file_list:
            if i in setup_data["already_solved_list"]: continue
            new_solved_list.append(i)
            setup_data["already_solved_list"].append(i)
        json.dump(setup_data, make_file, indent="\t")
    return new_solved_list

def get_worksheet(setup_data):
    scope = [setup_data['scope']]
    service_account_json_file_name = setup_data['service_account_json_file_name']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = setup_data['spreadsheet_url']
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet(setup_data['worksheet'])
    return worksheet

def write_new_solved_list_in_worksheet(setup_data):
    new_solved_list = get_new_solved_list(setup_data)
    worksheet = get_worksheet(setup_data)
    my_column = setup_data['my_column']

    idx = len(worksheet.col_values(ord(my_column)-64)) + 1
    for i in new_solved_list:
        worksheet.update_acell(my_column+str(idx),i)
        idx += 1

def main():
    setup_data = get_setup_data()
    write_new_solved_list_in_worksheet(setup_data)

if __name__ == "__main__":
    main()