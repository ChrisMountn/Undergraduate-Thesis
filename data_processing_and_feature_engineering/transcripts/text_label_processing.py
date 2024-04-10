import pandas as pd
import json
import os

def generateTextLabelsDictionary(bucketed=False):
    
    data_folder = 'data'
    excel_file_name = 'labels.xlsx'
    excel_file_path = os.path.join(data_folder, excel_file_name)

    sheet_name = 'Data_Both'

    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    df['ID'] = df['ID'].apply(format_id)

    df['ID_TASK'] = df['ID'].apply(lambda x: str(x)) + '_' + df['Task'].apply(lambda x: str(x))

    result_dict = {}
    for index, row in df.iterrows():
        key = row['ID_TASK'] + '.txt'
        if not pd.isna(row['RIFL_Total']):
            value = row['RIFL_Total']
            if bucketed:
                result_dict[key] = bucket(key, value)
            else:
                result_dict[key] = value

    json_file_path = 'labels_dict.json'

    with open(json_file_path, 'w') as json_file:
        json.dump(result_dict, json_file)

def format_id(id_value):
    # Split the string into numeric and non-numeric parts
    parts = str(id_value).split('(', 1)
    
    numeric_part = ''.join(filter(str.isdigit, parts[0]))
    formatted_numeric_part = numeric_part.zfill(3)
    
    if len(parts) > 1:
        formatted_id = formatted_numeric_part + '(' + parts[1]
    else:
        formatted_id = formatted_numeric_part
    
    return formatted_id

def bucket(key, value):
    if value < 2.5:
        return 0
    elif value >= 2.5 and value < 4.0:
        return 1
    elif value >= 4.0:
        return 2
    else:
        print(f"error: {key} does not have a valid RIFL value. The value is {value}")

if __name__ == "__main__":
    generateTextLabelsDictionary(bucketed=True)