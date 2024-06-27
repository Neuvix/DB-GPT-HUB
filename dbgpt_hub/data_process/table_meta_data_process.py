# -*- encoding: utf-8 -*-
import json
import os
import sys
from typing import Optional, Dict, List

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from dbgpt_hub.data_process.excel_processor import ExcelProcessor
excel_processor = ExcelProcessor()

DATA_PATH = "dbgpt_hub/data"
DB_ID = "tp_mis"
SCHEMA = "schema"

def get_all_table_name() -> Optional[Dict]:
        all_tables = excel_processor.read_excel(os.path.join(ROOT_PATH, DATA_PATH, DB_ID, "all_table.xlsx"))
        tables = [str(item[1]) for item in all_tables]
        tables_description = [str(item[2]) for item in all_tables]
        all_table_dict = {"tables":tables,
                          "tables_description":tables_description}
        return all_table_dict

def get_all_table_meta_data() -> Optional[Dict]:
        tables = get_all_table_name()['tables']
        all_table_dict = {}
        for item in tables:  # 一个item是一个表
            table = item
            schema_file = os.path.join(ROOT_PATH, DATA_PATH, DB_ID, SCHEMA, table + ".xlsx")
            meta_data = excel_processor.read_excel(schema_file)
            columns = []
            column_comments = []
            primary_key = None
            for md in meta_data:
                columns.append(md[1])
                column_comments.append(md[3])
                if md[4]==1:
                    primary_key=md[1]
            new_dict = {
                 "columns":columns,
                 "column_comments":column_comments,
                 "primary_key":primary_key
            }
            all_table_dict[table] = new_dict
        return all_table_dict   

# if __name__ == "__main__":
    # # 获得table的schema元数据
    # res = generate_table_prompt()
    # # output_path = "/root/Neuvix/DB-GPT-HUB/dbgpt_hub/data/table_prompt_train.json"
    # # with open(output_path, 'w',encoding="utf-8") as f:
    # #      json.dump(res, f, indent=4,ensure_ascii=False)
    # print(res)