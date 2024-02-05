import json
import random
import re

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

def create_json_to_examples():
    with open('/home/ryan/TextRankerJS/results/llm_preference_evalset.json', 'r') as file:
        data = file.read()
        dataset = json.loads(data)

    instructions = [data['instruction'] for data in dataset]
    references = [data['reference'] for data in dataset]
    N = 50
    responses = read_json_file("/home/ryan/TextRankerJS/results/full_n15_model_generations.json")[0]
    # print(responses)
    
    formatted_responses = []
    ground_truth = []
    K = len(responses) # num of modles
    with open("results/human_annotation_exp.json", "w") as hae, open("results/human_annotation_ground_truth.json", "w") as gt, open("results/human_annotation_gt_formatted.json", "w") as gtf:
        keys = [keys for keys in responses]
        
        for i in range(N):
            true_order = {}  
            models = []
            for idx in range(K):
                models.append(f'System {chr(ord("A") + idx)}')          
            exp = {"gold_label": "na", "contrast_label": "na", "instruction": instructions[i], "reference": references[i]}
            exp["black-bar"] = "black-bar"
            for j in keys:
                model = models.pop(random.randrange(len(models)))
                true_order[j] = model
                exp[model] = responses[j][i]
            formatted_responses.append(exp)
            ground_truth.append(true_order)
        
        json.dump(formatted_responses, hae, indent=4)
        json.dump(ground_truth, gt)
        json.dump(ground_truth, gtf, indent=4)


def parse_txt_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        examples_toy = []
        current_example = {}
        
        for line in file:
            line = line.strip()
            
            if line.startswith("### Context:"):
                continue
            
            elif line.startswith("### Instruction:"):
                current_example = {"gold_label": "na", "contrast_label": "na", "instruction": "", "reference": "", "black-bar": "black-bar"}
                current_example["instruction"] = re.search(r"### Instruction:(.*)", line).group(1).strip()
                
            elif line.startswith("### Reference:"):
                current_example["reference"] = re.search(r"### Reference:(.*)", line).group(1).strip()
            
            elif line.startswith("System "):
                system_name, system_content = re.match(r"System ([A-Za-z]):(.*)", line).groups()
                current_example["System {}".format(system_name)] = system_content.strip()
            
            elif line == "":
                if current_example:
                    examples_toy.append(current_example)
                    current_example = {}
        
        if current_example:
            examples_toy.append(current_example)
        
        return examples_toy


if __name__ == "__main__":
    random.seed(42)
    filename = "json_examples/human_judgement_study.txt"
    examples_toy = parse_txt_file(filename)

    random_examples = random.sample(examples_toy, 5)

    with open("js/examples_toy.js", "w", encoding="utf-8") as js_file:
        js_file.write("const examples_toy = ")
        json.dump(random_examples, js_file, indent=4)
        js_file.write(";")

