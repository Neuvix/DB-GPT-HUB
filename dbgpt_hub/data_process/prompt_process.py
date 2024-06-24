# -*- encoding: utf-8 -*-
import json
import os
import sys
from typing import  Optional, List

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from dbgpt_hub.data_process.excel_processor import ExcelProcessor
from dbgpt_hub.data_process.table_meta_data_process import get_all_table_meta_data, get_all_table_name

DATA_PATH = "dbgpt_hub/data"
DB_ID = "tp_mis"
SCHEMA = "schema"
excel_processor = ExcelProcessor()

SQL_BASE_INSTRUCTION_PROMPT = """\
I want you to act as a SQL terminal in front of an example database, \
you need only to return the sql command to me.Below is an instruction that describes a task, \
Write a response that appropriately completes the request.\n"
##Instruction:\n{}\n"""
TABLE_BASE_INSTRUCTION_PROMPT = """\
I want you to act as a SQL terminal in front of an example database, \
you need only to return the table name to me.Below is an instruction that describes a task, \
Write a response that appropriately completes the request.\n"
##Instruction:\n{}\n"""
INPUT_PROMPT = "###Input:\n{}\n\n###Response:"

# 构造推理table名称的prompt
def generate_table_prompt() -> Optional[List]:
     # 获得table的schema元数据
    all_table_dict = get_all_table_name()
    all_tables = all_table_dict['tables']
    all_tables_description = all_table_dict['tables_description']
    # 从excel读取训练数据集：sql文本对
    file_path = os.path.join(DATA_PATH, DB_ID, "question_sql.xlsx") 
    table_sql_json_data = excel_processor.read_excel_to_json(file_path,DB_ID)
    res = []
    for i in range(len(table_sql_json_data)):
        current_data = table_sql_json_data[i]
        current_tables = current_data['table'].replace(" ", "").split(',')
        question = current_data['question']
        source = (DB_ID + " contains tables such as " + ", ".join(all_tables) + ". ")
        source += ("The descriptions of these tables are " + ", ".join(all_tables_description)+ "\n")
        input = {"db_id": DB_ID,  # 构造prompt_train.json
                 "table": current_tables,
                 "instruction": TABLE_BASE_INSTRUCTION_PROMPT.format(source),
                 "input": INPUT_PROMPT.format(question),
                 "output": ",".join(current_tables)}
        res.append(input)
    return res

# 构造推理sql的prompt
def generate_sql_prompt() -> Optional[List]:
    # 获得table的schema元数据
    all_table_meta_dict = get_all_table_meta_data()
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
            columns = all_table_meta_dict[name]["columns"]
            source += ("Table " + name + " has columns such as " + ", ".join(columns) + ". ")
            comments = all_table_meta_dict[name]["column_comments"]
            source += "The comments of columns are " + ", ".join(comments) + ". "
            primary_key = all_table_meta_dict[name]["primary_key"]
            source += (primary_key + " is the primary key."+ "\n")
        input = {"db_id": DB_ID,  # 构造prompt_train.json
                 "table": tables,
                 "instruction": SQL_BASE_INSTRUCTION_PROMPT.format(source),
                 "input": INPUT_PROMPT.format(question),
                 "output": query_sql}
        res.append(input)
    return res
             

if __name__ == "__main__":
    res  = []
    res.extend(generate_table_prompt())
    res.extend(generate_sql_prompt())
    output_path = os.path.join(DATA_PATH, "prompt_train.json")
    with open(output_path, 'w',encoding="utf-8") as f:
        json.dump(res, f, indent=4,ensure_ascii=False)