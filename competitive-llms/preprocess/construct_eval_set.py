## generating the evaluation set for n=15 experiment

from huggingface_hub import hf_hub_download
from datasets import load_dataset
import json
import numpy as np
    
bb_dataset = load_dataset("tasksource/bigbench",'strategyqa')
eli_dataset = dataset = load_dataset("eli5")

# Open the JSON file
with open('../competitive-llms/datasets/ai_society_instructions.json', 'r') as file:
    # Read the contents of the file
    data = file.read()

    # Parse the JSON data
    ca_dataset = json.loads(data)
    
    
llm_preference_evalset = "datasets/llm_preference_evalset_2.json"
llm_evalset = []

N = 25
with open(llm_preference_evalset, "w") as lp:
    sample_bb = np.random.choice(len(bb_dataset['validation']), N, replace=False)
    sample_eli = np.random.choice(len(eli_dataset['validation_eli5']), N, replace=False)
    
    sampled_bb = np.array(bb_dataset['validation'])[sample_bb]
    for inp in sampled_bb:
        input = {"instruction": inp['inputs'].replace("Q: ", "").replace("A:", "").replace("\n", ""), "reference": inp['targets'][0]}
        # llm_evalset.append(input)
        lp.write(json.dumps(input) + "\n")
    
    sampled_eli = np.array(eli_dataset['validation_eli5'])[sample_eli]
    for inp in sampled_eli:
        idx = inp['answers']['score'].index(max(inp['answers']['score']))
        input = {"instruction": inp['title'], "reference": inp['answers']['text'][idx]}
        lp.write(json.dumps(input) + "\n") 
        # llm_evalset.append(input)
    
    # np.random.shuffle(llm_evalset)
    # lp.write(json.dumps(llm_evalset))



