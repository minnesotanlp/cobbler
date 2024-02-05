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

from rbo_preprocess import combine_outputs_by_annotator, create_pairwise_win_by_model

def load_all_annotator_response():
    annot_0 = combine_outputs_by_annotator(0)
    annot_1 = combine_outputs_by_annotator(1)
    annot_2 = combine_outputs_by_annotator(2)
    annot_3 = combine_outputs_by_annotator(3)
    annot_4 = combine_outputs_by_annotator(4)
    annot_5 = combine_outputs_by_annotator(5)

    return (annot_0, annot_1, annot_2, annot_3, annot_4, annot_5)


def compute_rbo_similarity(annotator_matrices_x, annotator_matrices_y, num_x, num_y, k): #rbo 
    rbo_matrix = np.zeros((num_x, num_y))

    avg_iaa_lst = []
    for i in range(num_x): # num on x-axis
        for j in range(i+1, num_y): # num on y-axis   
            flat_annotator_i = [sublist for sublist in annotator_matrices_x[i]]
            flat_annotator_j = [sublist for sublist in annotator_matrices_y[j]]
            all_rbo_scores = [rbo.RankingSimilarity(a,b).rbo(p=0.8) for a, b in zip(flat_annotator_i, flat_annotator_j)]
            avg_rbo = sum(all_rbo_scores)/len(all_rbo_scores)
            avg_rbo = round(avg_rbo, 3)
            rbo_matrix[i, j] = avg_rbo
            if avg_rbo != 1:
                avg_iaa_lst.append(avg_rbo)

    avg_iaa = sum(avg_iaa_lst)/len(avg_iaa_lst)

    print("Pairwise Rank-biased Overlap Matrix: ")
    print("Average IAA scores: ", avg_iaa)
    print(rbo_matrix)
    return avg_iaa


def compute_rbo_similarity_human_machine(annotator_matrices_x, annotator_matrices_y, num_x, num_y, k): #rbo 
    rbo_matrix = np.zeros((num_x, num_y))

    avg_iaa_lst = []
    for i in range(num_x): # num on x-axis
        for j in range(num_y): # num on y-axis   
            flat_annotator_i = [sublist for sublist in annotator_matrices_x[i]]
            flat_annotator_j = [sublist for sublist in annotator_matrices_y[j]]
            all_rbo_scores = [rbo.RankingSimilarity(a,b).rbo(p=0.8) for a, b in zip(flat_annotator_i, flat_annotator_j)]
            avg_rbo = sum(all_rbo_scores)/len(all_rbo_scores)
            avg_rbo = round(avg_rbo, 3)
            rbo_matrix[i, j] = avg_rbo
            if avg_rbo != 1:
                avg_iaa_lst.append(avg_rbo)

    avg_iaa = sum(avg_iaa_lst)/len(avg_iaa_lst)

    print("Pairwise Rank-biased Overlap Matrix: ")
    print("Average IAA scores: ", avg_iaa)
    print(rbo_matrix)
    return avg_iaa


def main():

    ### IAA scores among 6 annotators
    (annot_0, annot_1, annot_2, annot_3, annot_4, annot_5) = load_all_annotator_response()
    rbo_iaa = compute_rbo_similarity([annot_0.values, annot_1.values, annot_2.values, annot_3.values, annot_4.values, annot_5.values], 
                           [annot_0.values, annot_1.values, annot_2.values, annot_3.values, annot_4.values, annot_5.values], 6,6, 15)

    print(f"IAA scores: {rbo_iaa}")


    ### Agreement between human and LLMs 
    # RBO (individual annotator ~ individual model) -> 90 pairs -> Average

    sorted_rank_data = create_pairwise_win_by_model()
    rbo_human_machine = compute_rbo_similarity_human_machine([annot_0.values, annot_1.values, annot_2.values, annot_3.values, annot_4.values, annot_5.values], list(sorted_rank_data.values()), 6, 15, 5)

    print(f"Human-Machine Agreement: {rbo_human_machine}")









if __name__ == "__main__":
    main()





