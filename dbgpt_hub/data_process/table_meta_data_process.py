# -*- encoding: utf-8 -*-
'''
生成表的元数据文件tables.json
'''
import yaml
import json
import os
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub'
sys.path.append(ROOT_PATH)

from table_meta_data_processor import TableMetaDataProcessor

from dbgpt_hub.configs.config import (  # 从dbgpt_hub\configs\config.py导入
    DATA_PATH,
)

def get_config(path):
    config = None
    config_file_path = os.path.join(path, "db_config.yaml")
    with open(config_file_path, encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    return config

'''
构造tables.json
'''
if __name__ == "__main__":
    # current_path = os.path.split(os.path.realpath(__file__))[0]
    #获取父文件夹路径
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # db_config.yaml文件在工具包dataset_util文件夹下
    config_data_path = os.path.join(parent_path, "dataset_util")

    config_data = get_config(config_data_path) #config_data['table-configs']是字典：{'change_ship_archives_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_driver_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_route_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_shipping_basic_work_data': {'tables': [...], 'foreign_keys': None}}

    # # 生成mysql 工具对象
    # connect = None

    # # 暂时只实现mysql，其他版本数据库，后续扩展
    # if config_data["database"]["dbtype"] == "mysql":
    #     connect = MySQLConnector(
    #         host=config_data["database"]["host"],
    #         port=config_data["database"]["port"],
    #         user=config_data["database"]["user"],
    #         passwd=config_data["database"]["passwd"],
    #         db=config_data["database"]["db"],
    #     )
    # else:
    #     raise ()

    # 上面链接数据库可以不关注，只关注db_config.yaml文件即可
    processor = TableMetaDataProcessor(config_data)
    meta = processor.generate_table_metadata()

    # tables.json要写到data目录下当前数据库所对应的文件夹
    output_path = os.path.join(DATA_PATH, config_data["database"]["db"])
    with open(os.path.join(output_path, "tables.json"), "w",encoding="utf-8") as file:
        json.dump(meta, file, ensure_ascii=False, indent=1)  # indent=1表示缩进1个空格
