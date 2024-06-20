# -*- encoding: utf-8 -*-
import json
import os
import sys
from typing import Optional, Dict

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from dbgpt_hub.dataset_util.excel_processor import ExcelProcessor
excel_processor = ExcelProcessor()

DATA_PATH = "dbgpt_hub/data"
DB_ID = "tp_mis"
SCHEMA = "schema"
TABLE_PROMPT = '''I want you to act as a SQL terminal in front of an example database, \
         you need only to return the table name to me.Below is an instruction that describes a task, \
         Write a response that appropriately completes the request.\n"
        "##Instruction:\n{instruction}\n###Input:\n{input}\n\n###Response:'''
BASE_INSTRUCTION_PROMPT = """\
I want you to act as a SQL terminal in front of an example database, \
you need only to return the table name to me.Below is an instruction that describes a task, \
Write a response that appropriately completes the request.\n"
##Instruction:\n{}\n"""

def generate_table_meta_data() -> Optional[Dict]:
        all_tables = excel_processor.read_excel(os.path.join(DATA_PATH, DB_ID, "all_table.xlsx"))
        tables = [str(item[1]) for item in all_tables]
        all_table_dict = {}
        for item in tables:  # 一个item是一个表
            table = item
            schema_file = os.path.join(DATA_PATH, DB_ID, SCHEMA, table + ".xlsx")
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
             

if __name__ == "__main__":
    # 获得table的schema元数据
    all_table_dict = generate_table_meta_data()
    # for item in all_table_dict:
    #      print(item)
    #      print(all_table_dict[item])
    file_path = os.path.join(DATA_PATH, DB_ID,"question_sql.xlsx")
    table_sql_json_data = excel_processor.read_excel_to_json(file_path,DB_ID)
    res = []
    for i in range(len(table_sql_json_data)):
        current_data = table_sql_json_data[i]
        tables = current_data['table'].replace(" ", "").split(',')
        question = current_data['question']
        query_sql = current_data['query']
        source = (DB_ID + " contains tables such as " + ", ".join(tables) + ". ")
        for name in tables:
            columns = all_table_dict[name]["columns"]
            source += ("Table " + name + " has columns such as " + ", ".join(columns) + ". ")
            comments = all_table_dict[name]["column_comments"]
            source += "The comments of columns are " + ", ".join(comments) + ". "
            primary_key = all_table_dict[name]["primary_key"]
            source += (primary_key + " is the primary key."+ "\n")
        input = {"db_id": DB_ID,  # 构造prompt_train.json!!!
                 "table": tables,
                 "instruction": BASE_INSTRUCTION_PROMPT.format(source),
                 "input": question,
                 "output": tables}
        res.append(input)
    output_path = "/root/Neuvix/DB-GPT-HUB/dbgpt_hub/data/table_prompt_train.json"
    with open(output_path, 'w',encoding="utf-8") as f:
         json.dump(res, f, indent=4,ensure_ascii=False)