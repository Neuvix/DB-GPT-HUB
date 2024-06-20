import os
import yaml

class DBconfig:
    def get_config():
        # 读取数据库名称配置文件db_config.yaml，获得要使用的数据库名称
        parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_data_path = os.path.join(parent_path, "dataset_util")

        config = None
        config_file_path = os.path.join(config_data_path, "db_config.yaml")
        with open(config_file_path, encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
        return config
    
# if __name__ == "__main__":
#     db = DBconfig
#     config = db.get_config()
#     print(config)