from dbgpt_hub.llm_base.chat_model import ChatModel

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