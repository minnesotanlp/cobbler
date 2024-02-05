import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
tqdm.pandas()

import json
import os
import re

from itertools import combinations
import rbo

def convert_amt_to_df(batch_path):

    d = pd.read_csv(batch_path)
    d = d[['AssignmentId', 'WorkerId', 'Answer.taskAnswers', 'SubmitTime', 'WorkTimeInSeconds']]
    d['WorkTime_min'] = d['WorkTimeInSeconds']/60
    d = d[['AssignmentId', 'WorkerId', 'Answer.taskAnswers', 'SubmitTime','WorkTime_min']]

    return d


def manual_amt_preprocess():

    batch_pilot = '../batches/AMT/batch_pilot.csv'
    batch_mid_1 = '../batches/AMT/batch_mid_1.csv'
    batch_mid_2 = '../batches/AMT/batch_mid_2.csv'
    batch_final_1 = '../batches/AMT/batch_final_1.csv'
    batch_final_2= '../batches/AMT/batch_final_2.csv'

    batch_pilot_2nd = '../batches/AMT/batch_pilot_2nd.csv'
    batch_mid_1_2nd = '../batches/AMT/batch_mid_1_2nd.csv'
    batch_mid_2_2nd = '../batches/AMT/batch_mid_2_2nd.csv'
    batch_final_1_2nd = '../batches/AMT/batch_final_1_2nd.csv'
    batch_final_2_2nd = '../batches/AMT/batch_final_2_2nd.csv'

    df_pilot = convert_amt_to_df(batch_pilot)
    df_mid1 = convert_amt_to_df(batch_mid_1)
    df_mid2 = convert_amt_to_df(batch_mid_2)
    df_final1 = convert_amt_to_df(batch_final_1)
    df_final2 = convert_amt_to_df(batch_final_2)

    df_pilot_2 = convert_amt_to_df(batch_pilot_2nd)
    df_mid1_2 = convert_amt_to_df(batch_mid_1_2nd)
    df_mid2_2 = convert_amt_to_df(batch_mid_2_2nd)
    df_final1_2 = convert_amt_to_df(batch_final_1_2nd)
    df_final2_2 = convert_amt_to_df(batch_final_2_2nd)

    df_pilot.drop(4, inplace=True)
    df_pilot_2 = df_pilot_2.loc[(df_pilot_2.WorkerId == 'AAHQAOHHLCBQE') | (df_pilot_2.WorkerId == 'A8L4X8QCFIKVZ')]    

    df_mid = df_pilot.merge(df_mid1[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_mid = df_mid.rename(columns={'Answer.taskAnswers_x':'pilot', 'Answer.taskAnswers_y':'mid1', 'WorkTime_min_x':'time_pilot', 'WorkTime_min_y':'time_mid1'})
    df_mid = df_mid.merge(df_mid2[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_mid = df_mid.rename(columns={'Answer.taskAnswers':'mid2', 'WorkTime_min':'time_mid2'})

    df_all = df_mid.merge(df_final1[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_all = df_all.rename(columns={'Answer.taskAnswers':'final1', 'WorkTime_min':'time_final1'})
    df_all = df_all.merge(df_final2[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_all = df_all.rename(columns={'Answer.taskAnswers':'final2', 'WorkTime_min':'time_final2'})

    df_mid_2 = df_pilot_2.merge(df_mid1_2[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_mid_2 = df_mid_2.rename(columns={'Answer.taskAnswers_x':'pilot', 'Answer.taskAnswers_y':'mid1', 'WorkTime_min_x':'time_pilot', 'WorkTime_min_y':'time_mid1'})
    df_mid_2 = df_mid_2.merge(df_mid2_2[['WorkerId', 'Answer.taskAnswers','WorkTime_min' ]], how='left', on='WorkerId')
    df_mid_2 = df_mid_2.rename(columns={'Answer.taskAnswers':'mid2', 'WorkTime_min':'time_mid2'})

    df_all_2 = df_mid_2.merge(df_final1_2[['WorkerId', 'Answer.taskAnswers',  'WorkTime_min']], how='left', on='WorkerId')
    df_all_2 = df_all_2.rename(columns={'Answer.taskAnswers':'final1', 'WorkTime_min':'time_final1'})
    df_all_2 = df_all_2.merge(df_final2_2[['WorkerId', 'Answer.taskAnswers', 'WorkTime_min']], how='left', on='WorkerId')
    df_all_2 = df_all_2.rename(columns={'Answer.taskAnswers':'final2', 'WorkTime_min':'time_final2'})

    df_all = pd.concat([df_all, df_all_2]) # concat first four amt with the last two amt workers
    df_all = df_all.reset_index(drop=True)

    return df_all


def parse_amt_answers(pd_answer):

    input_string = pd_answer

    # Convert the string to a list of dictionaries
    list_of_dicts = json.loads(input_string)

    # The inner JSON string is still escaped, so we need to parse it again
    inner_json_str = list_of_dicts[0]["amt_output_toy"]
    inner_list_of_dicts = json.loads(inner_json_str)

    # Update the outer dictionary with the processed inner list
    list_of_dicts[0]["amt_output_toy"] = inner_list_of_dicts

    # Print the final result as a Python dictionary
    result_dict = list_of_dicts[0]['amt_output_toy']

    return result_dict


def combine_outputs_by_annotator(annot_idx):

    """
    Combine rankings of 15 models for all 50 examples, by each annotator. 
    Ex. 
    idx|rank_1 | rank_2 | .... | rank_15 | 
    -------------------------------------
    0 | vicuna | baize | ..... | falcon
    """

    rounds = ['pilot', 'mid1', 'mid2', 'final1', 'final2']
    df = pd.DataFrame()
    df_all = manual_amt_preprocess()

    for round in rounds:
        A = parse_amt_answers(df_all[round][annot_idx])
                
        # Extract the 'exampleIndex' and 'methods' lists from each dictionary
        example_indices = [item['exampleIndex'] for item in A]
        # methods_lists = [item['methods'] for item in A]
        methods_lists = [[method for method in item['methods'] if method != 'black-bar'] for item in A]

        # Create a DataFrame
        df = pd.concat([df, pd.DataFrame(methods_lists, index=example_indices, columns=['rank_{}'.format(i) for i in range(1, len(methods_lists[0]) + 1)])]).reset_index(drop=True)

    # Convert system to corresponding model name
    with open('model_annotations/human_annotation_gt_formatted.json', 'r') as f:
        model_info = json.load(f)
    for idx, examples in enumerate(model_info):
        systems_lst = list(examples.values())
        model_lst = list(examples.keys())
        for column in df.columns:
            if df.at[idx, column] in systems_lst:
                corr_model_idx = systems_lst.index(df.at[idx, column])
                df.at[idx, column] = model_lst[corr_model_idx]
    
    df.to_csv('../batches/AMT/model_annot{}.csv'.format(annot_idx), index=False)
    return df


def compute_pairwise_counts(df, annot_idx):
    """
    Create a JSON object, where each element looks like this: 
    [
        {
        "vicuna": 14,
        "baize": 13,
        "koala": 6,
        "wizardlm": 12,
        "chatgpt": 8,
        "instructgpt": 9,
        "gpt4": 11,
        "cohere": 10,
        "dolly": 7,
        "openassist": 4,
        "redpajama": 3,
        "mpt": 5,
        "alpaca": 1,
        "falcon": 0,
        "llama": 2
        },
    ]
    """
    with open('model_annotations/human_annotation_gt_formatted.json', 'r') as f:
        model_info = json.load(f)

    f.close()

    models = list(model_info[0].keys()) # a list of all LLM names (15)
    model_pairs = list(combinations(models, 2))
    default_value = 0
    all_count_dicts = []

    with open('human_annotations/annot_{}.json'.format(annot_idx), 'w') as j:

        for idx in tqdm(range(df.shape[0])):
            count_dict = dict.fromkeys(models, default_value)
            annot_example = df.loc[idx].values
            for i, pair in enumerate(model_pairs):
                if np.where(annot_example == pair[0]) < np.where(annot_example == pair[1]):
                    count_dict[pair[0]] += 1
                else:
                    count_dict[pair[1]] += 1
            all_count_dicts.append(count_dict)
        
        json.dump(all_count_dicts, j, indent=4)

    j.close()


def create_pairwise_win_by_model():
    """
    Creates a JSON object that compiles 15 ranking outputs for all 50 examples, for each model as an evaluator

    {'vicuna': 
        [{'vicuna': 14,
        'baize': 13,
        'koala': 11,
        'wizardlm': 11,
        'chatgpt': 10,
        'instructgpt': 8,
        'gpt4': 6,
        'cohere': 6,
        'dolly': 4,
        'openassist': 2,
        'redpajama': 4,
        'mpt': 4,
        'alpaca': 4,
        'falcon': 2,
        'llama': 1},
        {'vicuna': 9,
        'baize': 13,
        'koala': 11,
        'wizardlm': 10,
        'chatgpt': 11,
        'instructgpt': 7,
        'gpt4': 6,
        'cohere': 6,
        'dolly': 4,
        'openassist': 6,
    """
    with open('model_annotations/human_annotation_gt_formatted.json', 'r') as f:
        model_info = json.load(f)

    f.close()

    model_rank_data = {}

    model_names = list(model_info[0].keys()) 
    for model in model_names:
        print('loading {}'.format(model))
        with open('model_annotations/nC2_preferences_{}.json'.format(model), 'r') as f:
            data = json.load(f)
        model_rank_data[model] = data

    # Sort the ranking of 15 models per example
    sorted_rank_data = {}

    for model, ranks in model_rank_data.items():
            sorted_model = [sorted(example_output, key=lambda x: (-example_output[x], x)) for example_output in ranks]
            sorted_rank_data[model] = sorted_model

    return sorted_rank_data


