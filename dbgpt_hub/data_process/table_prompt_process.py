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
# TABLE_PROMPT = '''I want you to act as a SQL terminal in front of an example database, \
#          you need only to return the table name to me.Below is an instruction that describes a task, \
#          Write a response that appropriately completes the request.\n"
#         "##Instruction:\n{instruction}\n###Input:\n{input}\n\n###Response:'''
BASE_INSTRUCTION_PROMPT = """\
I want you to act as a SQL terminal in front of an example database, \
you need only to return the table name to me.Below is an instruction that describes a task, \
Write a response that appropriately completes the request.\n"
##Instruction:\n{}\n"""
INPUT_PROMPT = "###Input:\n{}\n\n###Response:"

def generate_table_des_data() -> Optional[Dict]:
        all_tables = excel_processor.read_excel(os.path.join(DATA_PATH, DB_ID, "all_table.xlsx"))
        tables = [str(item[1]) for item in all_tables]
        tables_description = [str(item[2]) for item in all_tables]
        all_table_dict = {"tables":tables,
                          "tables_description":tables_description}
        return all_table_dict
             

if __name__ == "__main__":
    # 获得table的schema元数据
    all_table_dict = generate_table_des_data()
    all_tables = all_table_dict['tables']
    all_tables_description = all_table_dict['tables_description']
    file_path = os.path.join(DATA_PATH, DB_ID,"question_sql.xlsx")
    table_sql_json_data = excel_processor.read_excel_to_json(file_path,DB_ID)
    res = []
    for i in range(len(table_sql_json_data)):
        current_data = table_sql_json_data[i]
        current_tables = current_data['table'].replace(" ", "").split(',')
        question = current_data['question']
        # query_sql = current_data['query']
        source = (DB_ID + " contains tables such as " + ", ".join(all_tables) + ". ")
        source += ("The descriptions of these tables are " + ", ".join(all_tables_description)+ "\n")
        input = {"db_id": DB_ID,  # 构造prompt_train.json!!!
                 "table": current_tables,
                 "instruction": BASE_INSTRUCTION_PROMPT.format(source),
                 "input": INPUT_PROMPT.format(question),
                 "output": ",".join(current_tables)}
        res.append(input)
    output_path = "/root/Neuvix/DB-GPT-HUB/dbgpt_hub/data/table_prompt_train.json"
    with open(output_path, 'w',encoding="utf-8") as f:
         json.dump(res, f, indent=4,ensure_ascii=False)