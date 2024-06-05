import json
import yaml
import os
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub'
sys.path.append(ROOT_PATH)

from dbgpt_hub.configs.config import (  # 从dbgpt_hub\configs\config.py导入
    DATA_PATH,
)
from dbgpt_hub.dataset_util.excel_processor import ExcelProcessor

def get_config(path):
    config = None
    config_file_path = os.path.join(path, "db_config.yaml")
    with open(config_file_path, encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    return config


if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_data_path = os.path.join(parent_path, "dataset_util")
    config_data = get_config(config_data_path)

    processor = ExcelProcessor()
    file_path = os.path.join(DATA_PATH, config_data["database"]["db"],'query_sql.xlsx')
    output_path = os.path.join(DATA_PATH, config_data["database"]["db"],'query_sql_train.json')
    processor.read_excel_to_json(file_path, output_path)