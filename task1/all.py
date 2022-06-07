import numpy as np
import pandas as pd
import json
import os


def read_json():
    path_to_json = './'
    all_json = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(all_json)
    return all_json


def parse_json(file, fc):
    with open(file, "r") as f:
        file_content = json.load(f)
    data_normal = pd.json_normalize(file_content["data"])
    df_normal = pd.DataFrame(data_normal)
    df_header = df_normal[df_normal['element'] == 'TH']
    header = (df_header['text'].tolist())  # -> taking only texts of the header
    header.append('')  # -> done because header has four fields and data has 5
    df_contents = df_normal[
        df_normal['element'].str.contains('TD') & df_normal['attributes.class'].str.contains('SH30Lb') & df_normal[
            'y'] != 0]

    unique_y = df_contents['y'].unique()
    var1 = len(unique_y)
    data = [None] * var1
    title_list = []
    indexlist = []
    datas = []

    if len(df_contents) == 0:
        for i in range(len(header) - 1):
            title_list.append(header[i])
            datas.append(np.nan)
            indexlist.append(str(fc) + '.' + str(1) + '.' + str(i + 1))
        final_df = pd.DataFrame(datas)
    else:
        for i in range(var1):
            data[i] = df_contents[df_contents['y'] == unique_y[i]]['text'].reset_index(drop=True)

        df_horizontal = pd.DataFrame(data).reset_index(drop=True)
        df_horizontal.columns = header
        df_horizontal["Sold by"] = df_horizontal["Sold by"].str.split('Opens in a new window').str[0]
        df_horizontal["Total price"] = df_horizontal["Total price"].str.split('Item').str[0]

        columns = len(df_horizontal.columns)
        for i in range(columns):
            column = df_horizontal.iloc[:, i - 1]
            datas = pd.Series(datas.append(column))
        final_df = pd.DataFrame(datas)

        for i in range(len(header) - 1):
            for j in range(len(df_horizontal)):
                title_list.append(header[i])
                indexlist.append(str(fc) + '.' + str(j + 1) + '.' + str(i + 1))

    final_df.index = indexlist
    final_df.insert(loc=0, column='', value=title_list)
    return final_df


def main():
    file_count = 1
    map_list = []
    df_mapping = pd.DataFrame()
    output = pd.DataFrame()
    json_files = read_json()
    for files in json_files:
        out = parse_json(files, file_count)
        mapping = mapper(files, file_count)
        map_list.append(mapping)
        output = output.append(out)
        file_count = file_count + 1
    # print(f"her it is {map_list}")
    df_mapping = df_mapping.append(map_list)
    print(df_mapping)
    df_mapping.to_csv('mapper.csv', index=False)
    fields = ['Fields', 'Values']
    output.columns = fields
    output.index.name = 'Index'
    print(output)
    output.to_csv('output.csv')


map_list = []


def mapper(file, fc):
    mapping = {}
    mapping['file_name'] = file
    mapping['index'] = fc
    return mapping


if __name__ == '__main__':
    main()
