import os
import json
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)

from tqdm import tqdm
from typing import List, Dict, Optional, Any

from dbgpt_hub.llm_base.chat_model import ChatModel
from dbgpt_hub.predict.singleton_model import Singleton

TWO_STAGE_PROMPT_DICT = {
    "prompt_table": (
        '''I want you to act as a SQL terminal in front of an example database, \
         you need only to return the table name to me.Below is an instruction that describes a task, \
         Write a response that appropriately completes the request.\n"
        "##Instruction:\n{instruction}\n###Input:\n{input}\n\n###Response:'''
    ),
    "prompt_sql": (
        '''I want you to act as a SQL terminal in front of an example database, \
         you need only to return the sql command to me.Below is an instruction that describes a task, \
         Write a response that appropriately completes the request.\n"
        "##Instruction:\n{instruction}\n###Input:\n{input}\n\n###Response:'''
    ),
}


def extract_two_stage_prompt_dataset(example: Dict[str, Any]) -> Dict[str, str]:
    instruction = example.get("instruction")
    if "return the table name" in instruction:
        prompt_format = TWO_STAGE_PROMPT_DICT["prompt_table"]
    else:
        prompt_format = TWO_STAGE_PROMPT_DICT["prompt_sql"]
    return {"input": prompt_format.format(**example)}


def prepare_dataset(
    predict_file_path: Optional[str] = None,
) -> List[Dict]:
    with open(predict_file_path, "r") as fp:
        data = json.load(fp)
    predict_data = [extract_two_stage_prompt_dataset(item) for item in data]
    return predict_data


def inference(model: ChatModel, predict_data: List[Dict], **input_kwargs):
    res = []
    # test
    # for item in predict_data[:20]:
    for item in tqdm(predict_data, desc="Inference Progress", unit="item"):
        # print(f"item[input] \n{item['input']}")
        response, _ = model.chat(query=item["input"], history=[], **input_kwargs)
        res.append(response)
    return res


def predict(model: ChatModel):
    args = model.data_args
    ## predict file can be give by param --predicted_input_filename ,output_file can be gived by param predicted_out_filename
    predict_data = prepare_dataset(args.predicted_input_filename)
    result = inference(model, predict_data)
    return result
    

def compare_test_pred(test_data:List, pred_data:List, output_path:str):
    res = []
    count_same = 0

    if len(test_data)==len(pred_data):
        for i in range(len(pred_data)):
            if test_data[i].lower() == pred_data[i].lower():
                count_same = count_same+1
            res.append({"test": test_data[i],
                        "predict": pred_data[i]})
    print('The prediction accuracy is: [{}]'.format(count_same/len(pred_data)))
    res.append('The prediction accuracy is: [{}]'.format(count_same/len(pred_data)))

    with open(output_path, 'w',encoding="utf-8") as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    

def export_sql_file(pred_data:List, output_path:str):
    if output_path==None:
        output_path = os.path.join(ROOT_PATH,"dbgpt_hub/output/pred/pred_tp_mis.sql")
    with open(output_path, "w") as f:
        for p in pred_data:
            try:
                f.write(p.replace("\n", " ") + "\n")
            except:
                f.write("Invalid Output!\n")


if __name__ == "__main__":
    # model = ChatModel()
    singleton= Singleton.instance()
    model = singleton.model
    model.data_args.predicted_input_filename = os.path.join(ROOT_PATH,"dbgpt_hub/data/prompt_train.json")
    pred_data = predict(model)

    with open(model.data_args.predicted_input_filename, "r") as fp:
        data = json.load(fp)
    test_data = [item.get("output") for item in data]

    output_path = os.path.join(ROOT_PATH,"dbgpt_hub/output/pred/compare_test_pred.json")
    compare_test_pred(test_data, pred_data, output_path)
    # 预测的sql存为一个.sql文件
    export_sql_file(pred_data, None)
