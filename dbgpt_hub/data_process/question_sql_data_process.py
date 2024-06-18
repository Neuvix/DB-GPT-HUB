import yaml
import os
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub'
sys.path.append(ROOT_PATH)

from dbgpt_hub.configs.config import (  # 从dbgpt_hub\configs\config.py导入
    DATA_PATH,
)
from dbgpt_hub.dataset_util.excel_processor import ExcelProcessor

'''
这个类，把sql和查询问题的文本对（excel形式）转换成json格式
'''
class QuestionSqlDataProcessor(object):
    def __init__(self, input_file: str = None, output_file: str = None) -> None:
        # 读取数据库名称配置文件db_config.yaml，获得要使用的数据库名称
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_data_path = os.path.join(parent_path, "dataset_util")
        config_data = self.__get_config(config_data_path)

        self.db_id = config_data["database"]["db"]

        if input_file is None:
            self.input_file = os.path.join(DATA_PATH, self.db_id,config_data["database"]["question_sql_pairs"][0])
        else:
            self.input_file = input_file

        if output_file is None:
            self.output_file = os.path.join(DATA_PATH, self.db_id,config_data["database"]["question_sql_pairs"][1])
        else:
            self.output_file = output_file


    def __get_config(self, path):
        config = None
        config_file_path = os.path.join(path, "db_config.yaml")
        with open(config_file_path, encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
        return config
    
    def generate_question_sql_json(self):
        processor = ExcelProcessor()
        processor.read_excel_to_json(self.input_file, self.output_file,self.db_id)


if __name__ == "__main__":
    processor = QuestionSqlDataProcessor()
    processor.generate_question_sql_json()
    