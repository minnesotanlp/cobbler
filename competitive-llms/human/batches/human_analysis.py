import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm

import ast
import json
import os
import math
import string
import re

from itertools import combinations
from scipy.stats import kendalltau, spearmanr
import rbo


def convert_amt_to_df(batch_path):

    d = pd.read_csv(batch_path)
    d = d[['AssignmentId', 'WorkerId', 'Answer.taskAnswers', 'SubmitTime', 'WorkTimeInSeconds']]
    d['WorkTime_min'] = d['WorkTimeInSeconds']/60
    d = d[['AssignmentId', 'WorkerId', 'Answer.taskAnswers', 'SubmitTime','WorkTime_min']]

    return d

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

def compute_rbo_similarity(annotator_matrices_x, annotator_matrices_y, num_x, num_y, k): #rbo 
    rbo_matrix = np.zeros((num_x, num_y))

    avg_iaa_lst = []
    for i in range(num_x): # num on x-axis
        for j in range(i, num_y): # num on y-axis   
            flat_annotator_i = [sublist for sublist in annotator_matrices_x[i]]
            flat_annotator_j = [sublist for sublist in annotator_matrices_y[j]]
            all_rbo_scores = [rbo.RankingSimilarity(a,b).rbo(p=0.8) for a, b in zip(flat_annotator_i, flat_annotator_j)]
            avg_rbo = sum(all_rbo_scores)/len(all_rbo_scores)
            avg_rbo = round(avg_rbo, 3)
            rbo_matrix[i, j] = avg_rbo
            if avg_rbo != 1:
                avg_iaa_lst.append(avg_rbo)

    avg_iaa = sum(avg_iaa_lst)/len(avg_iaa_lst)

    # print("Pairwise Rank-biased Overlap Matrix: ")
    # print("Average IAA scores: ", avg_iaa)
    # print(rbo_matrix)
    return avg_iaa

def find_highest_iaa(annot_lists, num_comb):
    
    # combination of models 
    best_comb = None 
    best_iaa = 0
    best_k = 0
    all_annot_idx = [0, 1, 2, 3, 4, 5]
    for comb_annot in combinations(all_annot_idx, num_comb):
        print(f"Combinations: {comb_annot}")
        annot_lst = []
        for annot_idx in comb_annot:
            annot_lst.append(annot_lists[annot_idx])
        
        # run rbo similarity with different k
        for k in range(1, 16):
            avg_rbo = compute_rbo_similarity(annot_lst, annot_lst, len(annot_lst), len(annot_lst), k)
            if avg_rbo > best_iaa:
                best_comb = comb_annot 
                best_iaa = avg_rbo
                best_k = k

    print(f"Best comb: {best_comb}")
    print(f"Best IAA: {best_iaa}")
    print(f"Best top k: {best_k}") 

def position_wise_rank_normalization(input_dicts): # List of input dictionaries
    # Initialize the result list
    result_list = []

    # Iterate through the input dictionaries
    for dicts in zip(*input_dicts):
        sum_dict = {}
        for dict_ in dicts:
            for key, value in dict_.items():
                sum_dict[key] = sum_dict.get(key, 0) + value
        result_list.append(sum_dict)

    sorted_models = []

    for dictionary in result_list:
        sorted_keys = sorted(dictionary.keys(), key=lambda key: dictionary[key], reverse=True)
        sorted_models.append(sorted_keys)

    return sorted_models


