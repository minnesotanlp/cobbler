import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np 

if __name__ == "__main__":

    position_rbo_human_machine = {'vicuna': 0.524, 'baize': 0.11, 'koala': 0.509, 'wizardlm': 0.223, 'chatgpt': 0.619, 'instructgpt': 0.395, 'gpt4': 0.456, 'cohere': 0.529, 'dolly': 0.607, 'openassist': 0.467, 'redpajama': 0.255, 'mpt': 0.502, 'alpaca': 0.153, 'falcon': 0.57, 'llama': 0.471}
    model_names = list(position_rbo_human_machine.keys())
    avg_rbo_human_machine = list(position_rbo_human_machine.values())
    model_positions = [7, 10, 11, 12, 1, 2, 0, 4, 9, 8, 14, 13, 6, 5, 3]
    model_params = ['10B >', '10B <', '10B <', '10B <', '100B >', '100B >', '100B >', '40B >', '10B >', '10B >', '10B <', '10B <', '10B >', '40B >', '40B >']
    param_orders = ['100B >', '40B >', '10B >', '10B <']
    group_colors = {
        "100B >": '#F26B21',
        "40B >": '#FBB040',
        "10B >": '#CBDB47',
        "10B <": '#208B3A',
    }
    df = pd.DataFrame(data={'model_names': model_names, 'avg_rbo_human_machine': avg_rbo_human_machine, 'position': model_positions, 'model_param': model_params})
    plt.figure(figsize=(6,7))
    ax = sns.barplot(x='avg_rbo_human_machine', y='position', data=df, orient='h', hue='model_param',hue_order=param_orders, dodge=False, palette=group_colors)
    sns.despine()

    for p in ax.patches:
        width = p.get_width()    # get bar length
        ax.text(width+0.045,       # set the text at 3 unit right of the bar
                p.get_y() + p.get_height() / 2, # get Y coordinate + X coordinate / 2
                '{:1.3f}'.format(width), # set variable to display, 2 decimals
                ha = 'center',   # horizontal alignment
                va = 'center', fontsize=13)  # vertical alignment


    plt.legend(title='', fontsize=12, bbox_to_anchor= (1,0.65))
    plt.tick_params(labelsize=17)
    plt.yticks(df['position'], df['model_names'])
    # plt.yticks(rotation=45, ha='right')
    plt.ylabel('', fontsize=20)
    plt.xlabel('Avg. RBO w/ Human Preference', fontsize=18)
    plt.savefig('fig.pdf', format="pdf", bbox_inches="tight")