import sys
import os
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub'
sys.path.append(ROOT_PATH)

from typing import Any, Optional, Dict
from typing import List
from dbgpt_hub.dataset_util.excel_processor import ExcelProcessor
from dbgpt_hub.configs.config import (  # 从dbgpt_hub\configs\config.py导入
    DATA_PATH,
)


# -*- encoding: utf-8 -*-
class TableMetaDataProcessor(object):
    def __init__(
        self, config_data: Optional[Dict] = None
    ) -> Any:
        # self.__conn = conn
        self.__excel_processor = ExcelProcessor()
        self.__config_data = config_data

    # 生成表元数据信息 构造tables.json
    def _generate_table_meta_data(
        self,
        db: str = "",
        tables: Optional[List] = [],
        # pks: Optional[Dict] = None,
        fks: Optional[Dict] = None,
        schema: Optional[str] = None,
    ) -> Optional[Dict]:
        table_names_original = tables
        column_comments = [[-1, "*"]]  # 构造column_names
        column_names_original = [[-1, "*"]]
        column_types = []
        foreign_keys = []
        primary_keys = []
        table_names = []
        for i in range(len(tables)):
            # table_meta = self.__conn.get_table_metadata(db, tables[i])  # 这个方法构造sql查询指定表的元数据信息，(('wx_user', ''),)
            # table_names.append(table_meta[0][1])
            table_names.append(tables[i])
            # meta_data：表中的列表和类型
            schema_file = os.path.join(schema, tables[i] + ".xlsx") #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub\\dbgpt_hub/data\\neuvix\\schema\\change_ship_archives_basic_info.xlsx'
            meta_data = self.__excel_processor.read_excel(schema_file)
            # 循环加meta_data的列名和类型
            for md in meta_data:
                column_comments.append([i, md[3]]) # 第i张表，md[3]是表名的解释，比如md[1]是College_ID，md[3]是College ID
                column_names_original.append([i, md[1]])
                if md[2] == "varchar" or md[2] == "text":
                    column_types.append("text")
                elif md[2] == "timestamp" or md[2] == "datetime":
                    column_types.append("time")
                else:
                    column_types.append("number")
                # 解析主键
                # if pks[tables[i]] == md[1]: # pks的结构是{'wx_user': 'openid'}，所以要先从tables[i]中取出表名，再取出主键
                if md[4]==1:
                    primary_keys.append(len(column_names_original)-1) # [2]，所以primary_keys指向主键在column_names_original的索引，这里出错，应该-1

        # 解析外键，目前业务不需要解析外键
        if fks:
            for key, fk in fks.items():
                fk_item = []
                for item in fk:
                    for k, f in item.items():
                        table_index = table_names_original.index(k)
                        # 遍历 column_names_original
                        for cno in range(len(column_names_original)):
                            if (
                                column_names_original[cno][0] == table_index
                                and column_names_original[cno][1] == f
                            ):
                                fk_item.append(cno)
                                break
                foreign_keys.append(fk_item)

        return {
            "column_comments": column_comments,
            "column_names_original": column_names_original,
            "column_types": column_types,
            "db_id": db,
            "foreign_keys": foreign_keys,
            "primary_keys": primary_keys,
            "table_names": table_names,
            "table_names_original": table_names_original,
        }

    def generate_table_metadata(self) -> Optional[List]:
        table_configs = self.__config_data["table-configs"]  # db_config.yaml 中的配置table-configs，字典：{'change_ship_archives_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_driver_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_route_basic_info': {'tables': [...], 'foreign_keys': None}, 'change_shipping_basic_work_data': {'tables': [...], 'foreign_keys': None}}

        # 结果列表
        result = []
        db_id = self.__config_data["database"]["db"]  # 'puzzleprogram_DB'
        for key, value in table_configs.items():
            tables = value["tables"]  # ['change_ship_archives_basic_info', 'change_driver_basic_info', 'change_route_basic_info', 'change_shipping_basic_work_data']
            foreign_keys = value["foreign_keys"] # None，目前业务不涉及外键
            schema_path = os.path.join(DATA_PATH,db_id,'schema') #'c:\\Users\\HP\\Desktop\\Neuvix\\NL2SQL\\DB-GPT-Hub\\dbgpt_hub/data\\neuvix\\schema'

            # 表元数据
            table_meta_data = self._generate_table_meta_data(
                db_id, tables, foreign_keys,schema_path
            )
            result.append(table_meta_data)

        return result
