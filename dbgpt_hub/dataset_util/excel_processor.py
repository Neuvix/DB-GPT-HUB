import os
import sys
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub'
sys.path.append(ROOT_PATH)

import pandas as pd
import json

# 这个类用于读取excel文件
class ExcelProcessor:
    # 这个方法会读取excel文件，将excel文件中的一行变成一个元组，然后将所有元组放到一个列表中
    def read_excel(self,file_path):
        data = pd.read_excel(file_path)
        return [tuple(row) for row in data.values.tolist()]
    
    # 这个方法会读取excel文件，将excel文件中的一行变成一个json对象，然后将所有字典放到一个列表中
    def read_excel_to_json(self, file_path, db_id):
        json_data = []
        data = pd.read_excel(file_path)
        data.dropna(inplace=True)
        for row in data.values.tolist():
            # 把查询、sql、数据库、表名整合到一起
            db = {"db_id":db_id}
            row_dict = dict(zip(data.columns, row))
            row_dict.update(db)
            json_data.append(row_dict)
        return json_data
    

# if __name__ == "__main__":
#     data_folder = os.path.join(ROOT_PATH, "dbgpt_hub/data")
#     print(data_folder)

    # excel_processor = ExcelProcessor()
    # # result = excel_processor.read_excel(r'C:\Users\HP\Desktop\Neuvix\NL2SQL\DB-GPT-Hub\dbgpt_hub\data\spider\mydb.xlsx')
    # # print(result)

    # data = excel_processor.read_excel_to_json(r'C:\Users\HP\Desktop\Neuvix\NL2SQL\DB-GPT-Hub\dbgpt_hub\data\neuvix\query_sql.xlsx')
    # json_data = excel_processor.convert_to_json(data)
