import json
import numpy as np
from datasets import load_dataset
import random

path = "human_judgement_study.txt"
path_ = "human_study_true_order.txt"

with open(path, "w") as hr, open("responses.json", "r") as res, open(path_, "w") as hh:
    responses = json.load(res)
    
    N=100
    dataset = load_dataset("databricks/databricks-dolly-15k") 
    try: 
        sample = np.load("../competitive-llms/dolly_100.npy")
    except FileNotFoundError:
        sample = np.random.choice(len(dataset['train']), N, replace=False)
        np.save("dolly_100", sample)
    
    instructions = np.array(dataset['train']['instruction'])[sample]
    context = np.array(dataset['train']['context'])[sample]
    reference = np.array(dataset['train']['response'])[sample]
    
    pairings = []
    for i in range(len(instructions)):
        pairs = []
        input = (instructions[i], context[i], reference[i])
        pairs.append(input)
        
        for item in responses:
            combination = (responses[item][i+1], item)
            pairs.append(combination)
            
        pairings.append(pairs)

    # print(pairings)
    random.shuffle(pairings) 
    for idx, samples in enumerate(pairings[:30]):
        resp = samples[1:]
        input = "### Context: " + samples[0][1] + "\n" + "### Instruction: " + samples[0][0] + "\n### Reference:" + samples[0][2]
        hr.write(input + "\n")
        
        random.shuffle(resp)
        systems = ['System A', 'System B', 'System C', 'System D']
        llm_resp = "System A: " + resp[0][0] + "\nSystem B: " + resp[1][0] + "\nSystem C: " + resp[2][0] + "\nSystem D: " + resp[3][0]
        # for i in resp:
        true_order = resp[0][1] + "\n" + resp[1][1] + "\n" + resp[2][1] + "\n" + resp[3][1]
        
        hr.write(llm_resp + "\n\n")
        hh.write(true_order + "\n\n")
        
        
        