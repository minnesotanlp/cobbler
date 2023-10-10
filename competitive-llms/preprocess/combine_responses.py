import json
import numpy as np

from datasets import load_dataset

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

def clean_responses(model, generations, it, ct):
    cleaned_generations = {model: [generations[0]]}
    for idx, generation in enumerate(generations[1:]):
        prefix = "Answer:"
        # output = generation[0]['generated_text'].replace("\n", "").replace(ct[idx], "").replace(it[idx], "").replace("###", "").replace("Context:", "").replace("Instruction:", "")
        output = generation.replace("\n", "", 1).replace(ct[idx], "").replace(it[idx], "").replace("###", "").replace("Context:", "").replace("Instruction:", "")
        
        if prefix in output:
            index = output.index(prefix) + len(prefix)
            output = output[index:]
            output.strip()  # Remove leading/trailing whitespaces
            
        ## take only the first 30 words
        gen = ' '.join(output.split()[:30])
        cleaned_generations[f'{model}'].append(gen)
    return cleaned_generations
    

llm_path = "responses/llm_responses.txt"   
with open(llm_path, "r") as fp, open("responses.json", "w") as fw:
    eagle_responses = json.load(fp)
    
    # fil = "responses/falcon_outputs.json"
    # with open(fil, "r") as r:
    #     ex_responses = json.load(r)
    
    N=100
    dataset = load_dataset("databricks/databricks-dolly-15k") 
    try: 
        sample = np.load("../competitive-llms/dolly_100.npy")
    except FileNotFoundError:
        sample = np.random.choice(len(dataset['train']), N, replace=False)
        np.save("dolly_100", sample)
    
    instructions = np.array(dataset['train']['instruction'])[sample]
    context = np.array(dataset['train']['context'])[sample]
    category = np.array(dataset['train']['category'])[sample]
    reference = np.array(dataset['train']['response'])[sample]
    
    model = "falcon"
    ext_responses = read_json_file("responses/falcon_outputs.json")
    ex_responses = ["System B"]
    for i in ext_responses:
        ex_responses.append(i['generated_output'])
    
    ext_responses = {"falcon": ex_responses}
    ext_responses = clean_responses(model, ext_responses[model], context, instructions)
    print(len(ext_responses[model]) - 1)
    
    # test
    # json.dump(ext_responses, fw)
    
    responses = {**eagle_responses, **ext_responses}
    json.dump(responses, fw)