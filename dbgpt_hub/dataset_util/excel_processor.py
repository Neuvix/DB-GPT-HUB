import pandas as pd
import json

# 这个类用于读取excel文件，返回一个列表，列表中的每个元素是一个元组，元组中的元素是excel文件中的一行数据
class ExcelProcessor:
    def read_excel(self,file_path):
        data = pd.read_excel(file_path)
        return [tuple(row) for row in data.values.tolist()]
    
    def read_excel_to_json(self, file_path, output_path):
        json_data = []
        data = pd.read_excel(file_path)
        data.dropna(inplace=True)
        for row in data.values.tolist():
            db_id = {"db_id":"neuvix"}
            row_dict = dict(zip(data.columns, row))
            row_dict.update(db_id)
            json_data.append(row_dict)
        with open(output_path, 'w',encoding="utf-8") as f:
            json.dump(json_data, f, indent=4,ensure_ascii=False)
    

if __name__ == "__main__":
    excel_processor = ExcelProcessor()
    # result = excel_processor.read_excel(r'C:\Users\HP\Desktop\Neuvix\NL2SQL\DB-GPT-Hub\dbgpt_hub\data\spider\mydb.xlsx')
    # print(result)

    data = excel_processor.read_excel_to_json(r'C:\Users\HP\Desktop\Neuvix\NL2SQL\DB-GPT-Hub\dbgpt_hub\data\neuvix\query_sql.xlsx')
    # json_data = excel_processor.convert_to_json(data)
