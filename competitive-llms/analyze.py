import sys
import json
import numpy

def organize_data(file_path):
    nested_arrays = []
    current_array = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if not line:
                # Treat line breaks as separate arrays
                if current_array:
                    nested_arrays.append(current_array)
                    current_array = []
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Skip lines that are not valid JSON objects
                continue

            current_array.append(data)

    if current_array:
        # Append the last array if it's not empty
        nested_arrays.append(current_array)

    return nested_arrays

def normalize_scores(scores, new_min, new_max):
    # Find the minimum and maximum scores
    min_score = min(scores.values())
    max_score = max(scores.values()) 

    # Normalize the scores using the custom scaling factors
    normalized_scores = {}
    for key, value in scores.items():
        # inverted_value = max_score + min_score - value
        normalized_value = new_min + (((value - min_score) * (new_max - new_min)) / (max_score - min_score))
        normalized_scores[key] = normalized_value

    return normalized_scores

def normalize_ranks(scores):
    data = scores
    points_dict = {}
    for model, points in data.items():
        if points not in points_dict:
            points_dict[points] = []
        points_dict[points].append(model)

    # Sort the points in descending order
    sorted_points = sorted(points_dict.keys(), reverse=True)

    # Create a nested list of models based on points
    result = []
    for points in sorted_points:
        models = points_dict[points]
        result.append(models)
    return result
    
def find_length_bias(pairs, responses):
    shorter_bias = 0
    longer_bias = 0
    valid_responses = 0
    
    for idx, samples in enumerate(pairs):
        for sample in samples:
            winner = sample['model']
            combo = sample['combination']
            # No order bias -> can't have length bias if there is order bias
            if winner != "Invalid response" and "fo bias" not in combo and "lo bias" not in combo:
                if len(responses[combo[0]][idx]) > len(responses[combo[1]][idx]):
                    if winner == combo[0]:
                        longer_bias += 1
                    else:
                        shorter_bias += 1
                else:
                    if winner == combo[1]:
                        longer_bias +=1
                    else:
                        shorter_bias += 1
                valid_responses += 1
                
    return valid_responses, shorter_bias, longer_bias

def extract_valid_responses(path):
    with open(path) as file:
        lines = file.readlines()

    valid_responses_line = [line for line in lines if 'Valid responses' in line]
    if valid_responses_line:
        valid_responses = valid_responses_line[0].split(':')[1].strip()
        return int(valid_responses)
        # print(valid_responses)
    else:
        print("Valid responses line not found in the file.")
    
    return None

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

def calculate(mode, model, human=None):
    stats_path = f'n15_evaluations/{model}/{mode}_statistics_{model}.json'
    path_scores = f'n15_evaluations/{model}/{mode}_preferences_{model}.json'
    if human:
        stats_path = f'n15_evaluations/{human}_{model}/{human}_{mode}_statistics_{model}.json'
        path_scores = f'n15_evaluations/{human}_{model}/{human}_{mode}_preferences_{model}.json'
    
    with open(f'n15_rankings/ranking_normalized_{model}.json', "w") as fs:
        # TODO: Implement reference/human response included eval
        scores_file = read_json_file(path_scores)
        
        avg_rankings = {}
        total_scores = scores_file[0]
        for key in scores_file[0]:
            avg_rankings[key] = 0
        # print(rankings)
        
        for idx, scores in enumerate(scores_file):
            norm_ranks = normalize_ranks(scores)
            for ind, sc in enumerate(norm_ranks):
                for mod in sc:
                    avg_rankings[mod] += (ind+1)
            fs.write(json.dumps(norm_ranks) + "\n")
            if idx != 0:
                for i in scores:
                    total_scores[i] += scores[i]
        
        ar = {k : v / 50 for k, v in avg_rankings.items()}
        fs.write("\nAverage rankings: " + json.dumps(ar) + "\n")
         
        # extract placements from total scores
        total_scores = normalize_ranks(total_scores)
        tr = {}
        for key in ar:
            tr[key] = 0
            
        for ind, sc in enumerate(total_scores):
            for mod in sc:
                tr[mod] = (ind+1)        
        fs.write("Total overall rankings: " + json.dumps(tr) + "\n")
                
    valid_responses = extract_valid_responses(stats_path)
    responses = read_json_file("../competitive-llms/n15_responses/full_n15_model_generations.json")[0]
    
    to_path = f'n15_evaluations/{model}/{mode}_true_order_{model}.json'
    pairs = organize_data(to_path)
    lb = find_length_bias(pairs, responses)
    
    with open(f'n15_bias/{model}_length_bias.json', "w") as lob:
        valid = lb[0]
        short = lb[1]
        long = lb[2]
        
        statistics = "Valid responses: " + str(valid) + "\nRetention Percentage: " + str(valid / valid_responses) + "\nShort Bias: " + str(short / valid) + "\nLong Bias: " + str(long / valid)
        lob.write(statistics)
    
def main(arg1, arg2, arg3=None):
    models = ["chatgpt", "instructgpt", "gpt4", 
              "cohere", "llama", "falcon"
              "openassist", "dolly", "alpaca", "baize",
              "redpajama", "koala", "vicuna", "wizardlm", "mpt"
              ]
    if arg2 == "all":
        for model in models:
            calculate(mode=arg1, model=model)
    else:
        calculate(mode=arg1, model=arg2)
    
if __name__ == "__main__":
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    # if len(sys.argv) > 2:
    #     arg3 = sys.argv[3]
    # else:
    #     arg3 = None
        
    main(arg1, arg2) #, human=arg3)