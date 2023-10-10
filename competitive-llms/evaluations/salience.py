import sys

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize

import json

def count_tokens(input_string):
    tokens = word_tokenize(input_string)
    num_tokens = len(tokens)
    return num_tokens

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

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

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

def evaluate_salience(model, mode="nC2"):
    if mode == "size":
        print(model)
        stats_path = f'n15_evaluations_order/_size/nC2_statistics_{model}.json'
        valid_responses = extract_valid_responses(stats_path)
        to_path = f'n15_evaluations_order/_size/nC2_true_order_{model}.json'
        if 'llamav2' in model:
            responses = read_json_file("/home/kooryan/competitive-llms/n15_responses/full_n15_model_generations_llamav2.json")[0]
        else:
            responses = read_json_file("/home/kooryan/competitive-llms/n15_responses/full_n15_model_generations_llamav2.json")[0]
    else:
        stats_path = f'n15_evaluations_order/_official/{model}/{mode}_statistics_{model}.json'
        valid_responses = extract_valid_responses(stats_path)
        responses = read_json_file("/home/kooryan/competitive-llms/n15_responses/full_n15_model_generations.json")[0]
        
        to_path = f'n15_evaluations_order/_official/{model}/{mode}_true_order_{model}.json'
    pairs = organize_data(to_path)    
    lb = find_length_bias(pairs, responses)

    with open(f'n15_evaluations_salience/{model}_salience_bias.json', "w") as lob:
        valid = lb[0]
        short = lb[1]
        long = lb[2]
        
        statistics = "Valid responses: " + str(valid) + "\nRetention Percentage: " + str(valid / (valid_responses + 1e-6)) + "\nShort Bias: " + str(short / valid) + "\nLong Bias: " + str(long / valid)
        lob.write(statistics)
    
def main(arg1, arg2):
    evaluate_salience(arg1, arg2)
    
    
if __name__ == '__main__':
    arg1 = sys.argv[1]
    # Include "human" response / ground truth
    if len(sys.argv) > 2:
        arg2 = sys.argv[2]
        print(f"Evaluating _size experiments")
    else:
        arg2 = None
    main(arg1,arg2)