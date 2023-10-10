import json
import yaml
from tqdm import tqdm
# from talkative_llm.llm import get_supported_llm
import sys
import os
sys.path.append('../talkative-llm')
from talkative_llm.llm import get_supported_llm

from datasets import load_dataset
import numpy as np
import pandas as pd

COHERE_API_KEY = ""
OPENAI_API_KEY = ""
OPENAI_ORGANIZATION_ID = ""

models = ["openassist", "mpt", "redpajama", "alpaca", "dolly"]

def process_generation(generation, it, ct=None):
    prefix = "Response:"
    prompters = ["Instruction:", it, "###", "<|prompter|>", "<|endoftext|>", "<|assistant|>"]
    if ct:
        output = generation.replace("\n", "", 1).replace(ct, "").replace(it, "").replace("###", "").replace("Context:", "").replace("Instruction:", "")
    else:
        output = generation.replace("\n", "", 1).replace(it, "").replace("###", "").replace("Instruction:", "")
        
    for prompter in prompters:
        output = output.replace(prompter, "")

    # Take all output after "Response: "
    if prefix in output:
        index = output.index(prefix) + len(prefix)
        output = output[index:]
        output.strip()  # Remove leading/trailing whitespaces

    return output

    
def generate_responses(inputs, N):
    instructions = inputs
    
    outputs = {}
    for i in range(len(models)):
        outputs[models[i]] = []
        
    for i in tqdm(range(N), total=N):
        # ct = context[i]
        # ct = ' '.join(context[i].split(' ')[:100])
        ct = None
        it = instructions[i]
        # prompt = "### Context: " + ct + '\n' + "### Instruction: " + it + "\n### Answer:"
        
        prompt = "### Instruction: " + it + "\n### Response:"
        # prompt = it
        # print(prompt)
        
        if "chatgpt" in models:
            chat_output = openai_caller([{'role': 'user', 'content': prompt}], 'chat')
            generation = process_generation(chat_output['generation'], it, ct)
            outputs["chatgpt"].append(generation)
        if "instructgpt" in models:
            completion_output = openai_caller([prompt], 'completion')
            generation = process_generation(completion_output[0]['generation'], it)
            outputs["instructgpt"].append(generation)
        if "falcon" in models:
            config = "../competitive-llms/configs/falcon_llm_example.yml"
            falcon_output = llm_caller([prompt], config_p=config)
            generation = process_generation(falcon_output[0]['generation'], it, ct)
            outputs["falcon"].append(generation)
        if "alpaca" in models:
            config = "../competitive-llms/configs/alpaca_lora_example.yml"
            alpaca_lora_output = llm_caller([prompt], config_p=config)
            generation = process_generation(alpaca_lora_output[0]['generation'], it, ct)
            outputs["alpaca"].append(generation)
        if "vicuna" in models:
            config = "../competitive-llms/configs/vicuna_llm_7b_example.yml"
            vicuna_output = llm_caller([prompt], config_p=config)
            generation = process_generation(vicuna_output[0]['generation'], it, ct)
            outputs["vicuna"].append(generation)
        if "mpt" in models:
            config = "../competitive-llms/configs/mpt_llm_example.yml"
            mpt_output = llm_caller([prompt], config_p=config)
            generation = process_generation(mpt_output[0]['generation'], it, ct)
            outputs["mpt"].append(generation)
        if "baize" in models:
            config = "../competitive-llms/configs/baize_llm_example.yml"
            output = llm_caller([prompt], config_p=config)
            generation = process_generation(output[0]['generation'], it, ct)
            outputs["baize"].append(generation)
        if "openassist" in models: 
            oa_prompt = f"<|prompter|>{it}<|endoftext|><|assistant|>"
            config = "../competitive-llms/configs/open_assist_llm_example.yml"
            output = llm_caller([oa_prompt], config_p=config)
            generation = process_generation(output[0]['generation'], it, ct)
            outputs["openassist"].append(generation)
        if "dolly" in models:
            config = "../competitive-llms/configs/dolly_llm_example.yml"
            dolly_output = llm_caller([prompt], config_p=config)
            generation = process_generation(dolly_output[0]['generation'], it, ct)
            outputs["dolly"].append(generation)
        if "redpajama" in models:
            config = "../competitive-llms/configs/redpajama_llm_example.yml"
            dolly_output = llm_caller([prompt], config_p=config)
            generation = process_generation(dolly_output[0]['generation'], it, ct)
            outputs["redpajama"].append(generation)
        if "koala" in models:
            config = "../competitive-llms/configs/koala_llm_example.yml"
            output = llm_caller([prompt], config_p=config)
            generation = process_generation(output[0]['generation'], it, ct)
            outputs["koala"].append(generation)
        if "wizardlm" in models:
            config = "../competitive-llms/configs/wizard_llm_example.yml"
            output = llm_caller([prompt], config_p=config)
            generation = process_generation(output[0]['generation'], it, ct)
            outputs["wizardlm"].append(generation)
        if "cohere" in models:
            pass
        if "gpt4" in models:
            pass
            
    with open("llm_responses_n15_2.json", "w") as fp:
        print("Saved LLM generations\n")
        json.dump(outputs, fp)

    return outputs

def llm_caller(prompt, config_p=None):
    config_path = config_p
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    caller = get_supported_llm(config)
    response = caller.generate(prompt)
    return response


def openai_caller(prompt, mode, config_params=None):
    # modes are: chat, completion, gpt4

    config_path = f"../competitive-llms/configs/open_ai_{mode}_example.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    # print(config)
    caller = get_supported_llm(config)
    response = caller.generate(prompt)
    return response

def main():
    N = 50
    
    # dataset = load_dataset("databricks/databricks-dolly-15k") 
    
    # try: 
    #     sample = np.load("../competitive-llms/dolly_100.npy")
    # except FileNotFoundError:
    #     sample = np.random.choice(len(dataset['train']), N, replace=False)
    #     np.save("dolly_100", sample)
    
    with open('../competitive-llms/datasets/llm_preference_evalset.json', 'r') as file:
        data = file.read()
        dataset = json.loads(data)

    instructions = [data['instruction'] for data in dataset]
    references = [data['reference'] for data in dataset]
    
    responses = generate_responses(instructions, N)
    # instructions = np.array(dataset[0]['instruction'])
    # context = np.array(dataset['train']['context'])[sample]
    # category = np.array(dataset['train']['category'])[sample]
    # reference = np.array(dataset['reference'])
    # responses = generate_responses((instructions, context), N)


if __name__ == "__main__":
    main()
