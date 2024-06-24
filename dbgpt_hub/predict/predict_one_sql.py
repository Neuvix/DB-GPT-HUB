# Neuvix NL2SQL推理文件
import os
import sys
from typing import List, Dict, Optional

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from dbgpt_hub.llm_base.chat_model import ChatModel
from dbgpt_hub.data_process.excel_processor import ExcelProcessor
from dbgpt_hub.data_process.table_meta_data_process import get_all_table_meta_data

# 单例模式
class Singleton(object):

    def __init__(self):
        args = {
            "model_name_or_path": "/root/Neuvix/hugging-face/models--defog--llama-3-sqlcoder-8b",
            "template": "llama2",
            "finetuning_type": "lora",
            "checkpoint_dir": "/root/Neuvix/DB-GPT-HUB/dbgpt_hub/output/adapter/llama-3-sqlcoder-lora",
        }
        print("Load fune-turning model...")
        # 加载模型
        self.model = ChatModel(args)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance

DATA_PATH = "dbgpt_hub/data"
DB_ID = "tp_mis"
SCHEMA = "schema"
excel_processor = ExcelProcessor()


# prompt模板
# 这是推理用哪些表
TABLE_PROMPT = '''I want you to act as a SQL terminal in front of an example database, \
         you need only to return the table name to me.Below is an instruction that describes a task, \
         Write a response that appropriately completes the request.\n"
        "##Instruction:\n{}\n###Input:\n{}\n\n###Response:'''
# 这是推理sql
SQL_PROMPT = '''I want you to act as a SQL terminal in front of an example database, \
         you need only to return the sql command to me.Below is an instruction that describes a task, \
         Write a response that appropriately completes the request.\n"
        "##Instruction:\n{}\n###Input:\n{}\n\n###Response:'''

# 准备用于推理table的输入数据
def prepare_table_data(input: Optional[str]) -> str:
    db_id = "tp_mis"
    all_tables = ExcelProcessor().read_excel(os.path.join(DATA_PATH, DB_ID, "all_table.xlsx"))
    tables = ', '.join(str(item[1]) for item in all_tables)
    tables_description = ', '.join(str(item[2]) for item in all_tables)
    instruction = '''I want you to act as a SQL terminal in front of an example database, you need only to return the table name to me.Below is an instruction that describes a task, Write a response that appropriately completes the request. {} contains tables such as {}. The descriptions of these tables are {}'''.format(db_id, tables,tables_description)
    return TABLE_PROMPT.format(instruction,input)

# 准备用于推理sql的数据
def prepare_sql_data(input: Optional[str], pred_tables:Optional[List]) -> str:
    all_table_dict = get_all_table_meta_data()
    instruction_sql = (DB_ID + " contains tables such as " + ", ".join(pred_tables) + ". ")
    for name in pred_tables:
        columns = all_table_dict[name]["columns"]
        instruction_sql += ("Table " + name + " has columns such as " + ", ".join(columns) + ". ")
        comments = all_table_dict[name]["column_comments"]
        instruction_sql += "The comments of columns are " + ", ".join(comments) + ". "
        primary_key = all_table_dict[name]["primary_key"]
        instruction_sql += (primary_key + " is the primary key."+ "\n")
    return SQL_PROMPT.format(instruction_sql,input)

def start_predict_one_sql(input):
    singleton= Singleton.instance()
    model = singleton.model
    # 获得tables列表
    print('Begin inferencing tables...')
    query = prepare_table_data(input)
    response_table, _ = model.chat(query=query)
    pred_tables = response_table.split(",")
    print('The inferred table is ',pred_tables)
    # 推理sql
    print('Begin inferencing sql...')
    query = prepare_sql_data(input,pred_tables)
    response_sql, _ = model.chat(query=query)
    return response_sql

if __name__ == "__main__":
    print(start_predict_one_sql("有多少司机"))
    print(start_predict_one_sql("查询aaa计划开工时间"))