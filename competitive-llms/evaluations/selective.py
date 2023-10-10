from tqdm import tqdm
import random
import json
import itertools
from math import comb
import re

from utils import uniform_prompt_selective, guidance_uniform_chat_selective, guidance_uniform_completion_selective
from utils import v_models, get_model_output, guidance_models, call_guidance, process_generation

random.seed(939)

bias_name = "selective"

def evaluate_selective(N, evaluator, instructions, reference, responses, eval_gen):
    true_order = f"n15_evaluations_{bias_name}/nC2_true_order_{evaluator}.json"
    preferences = f"n15_evaluations_{bias_name}/nC2_preferences_{evaluator}.json"
    stats = f"n15_evaluations_{bias_name}/nC2_statistics_{evaluator}.json"
    log_responses = f"n15_evaluations_{bias_name}/nC2_eval_gens_order_{evaluator}.json"
    
    selection_count = 0
    valid_responses = 0
        
    with open(true_order, "w") as txo, open(preferences, "w") as pw, open(stats, "w") as wr, open(log_responses, "w") as lr:
        keys = list(responses.keys())  # Get a list of keys
        
        count = 0
        # Iterate over indices
        for index in tqdm(range(0, N), total=N):
            # Generate unique combinations of items at the same index
            rankings = {}
            for i in keys:
                rankings[i] = 0
                
            item_combinations = list(itertools.combinations(keys, 2))
            random.shuffle(item_combinations)
            
            # Iterate over combinations
            for combination in item_combinations:
                count += 1
                model1, model2 = combination
                
                models = [model1, model2]
                
                order = ["System Star", "System Square"]
                selective = random.choice(order)
                
                # shuffle the models for certain bias tests
                random.shuffle(models)
                response1, response2 = responses[models[0]][index],  responses[models[1]][index]
                
                inp = order[0] + ": " + response1 + "\n" + order[1] + ": " + response2
                prompt = uniform_prompt_selective(instructions[index], reference[index], inp, selective)
                if evaluator not in guidance_models:
                    # caller
                    evaluation = eval_gen.generate([prompt])[0]['generation']
                elif evaluator in v_models:
                    evaluation = get_model_output(evaluator, eval_gen, prompt)
                else:
                    # prompter 
                    evaluation = call_guidance(eval_gen, instruction=instructions[index], input=inp, reference=reference[index])

                preference = process_generation(evaluation, instructions[index], reference[index], inp, response1, response2)                
                if count % 50 == 0:
                    lr.write("========================Generation for [" + ", ".join(models) + f"] for instance {index} ============================\n")
                    lr.write("---------RAW GENERATION--------\n" + evaluation + "\n")
                    lr.write("---------PATTERN MATCHED-------\n" + preference + "\n")

                pf = re.findall(r"(?i)(system star|system square)", preference)[0].title() if re.findall(r"(?i)(system star|system square)", preference) else None
                                
                # check for valid second-time response for reversed order
                if pf is not None:
                    valid_responses += 1
                
                if pf == "System Star":
                    rankings[models[0]] += 1
                    # check for selective bias 
                    if pf == selective:
                        selection_count += 1
                        models.append("selective")
                    txo.write(json.dumps({"model": models[0], "combination": models}) + "\n")
                elif pf == "System Square":
                    rankings[models[1]] += 1    
                    if pf == selective:
                        selection_count += 1  
                        models.append("selective")
                    txo.write(json.dumps({"model": models[1], "combination": models}) + "\n")
                else:
                    txo.write(json.dumps({"model": "Invalid response", "combination": models}) + "\n")

            txo.write("\n")
            pw.write(json.dumps(rankings) + "\n") 
            
        total_comparisons = N * comb(len(keys), 2)
        wr.write("Selection bias percentage: " + str(selection_count / total_comparisons) + "\n")
        wr.write("Selection bias count: " + str(selection_count) + "\n") 
        wr.write("Valid response percentage: " + str(valid_responses / total_comparisons) + "\n") 
        wr.write("Valid responses: " + str(valid_responses) + "\n")