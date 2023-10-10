import json

model_gens = {}

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

combine = False
if combine:     
    llm_path = "n15_model_generations.json"
    with open(llm_path, "w") as fp:
        resp1 = read_json_file("../competitive-llms/n15_responses/llm_responses_n15.json")
        print(len(resp1[0]))
        resp2 = read_json_file("../competitive-llms/n15_responses/model_gens_batch_api.json")
        print(len(resp2[0]))
        resp3 = read_json_file("../competitive-llms/n15_responses/v_model_gens_batch_hf.json")
        print(len(resp3[0]))
        resp4 = read_json_file("../competitive-llms/n15_responses/v_model_gens_falcon.json")
        print(len(resp4[0]))
        resp5 = read_json_file("../competitive-llms/n15_responses/v_model_gens_llama.json")
        print(len(resp5[0]))
        
        responses  = {**resp1[0], **resp2[0], **resp3[0], **resp4[0], **resp5[0]}
        print(len(responses))
        json.dump(responses, fp)

resp = read_json_file("../competitive-llms/n15_responses/full_n15_model_generations.json")[0]
print(len(resp))
print([key for key in resp])
