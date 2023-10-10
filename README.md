# Benchmarking Cognitive Biases in Large Language Models as Evaluators

1. Your directory structure should now look like this where both repositories should be on the same level
```
Working directory
└───competitive-llms
└───talkative-llms
```

2. cd into `competitive-llms` now and install requirements
```
pip install -r requirements.txt
```

3. In each file, there are various `sys.append` that you should specify your home directory to the path where `competitive-llms` is located.

Now everything should be runnable. 

## CoBBLEr: **Co**gnitive **B**ias **B**enchmark for **L**LMs as **E**valuato**r**s

To replicate the results you can utilize the provided aggregated responses in the `n15_responses` folder.

### Adding your own model
To evaluate your own language model, you can add a config for your model in the `configs` folder under the `competitive-llms` directory. 

To benchmark your model on each bias module:

1. Add your model to `evaluations/model_configs.py` for the path to your models config file

2. Add your models to the list of evaluators array in `evaluate.py`

3. To run each script you can run the script from the `competitive-llms` directory as:

```
python3 evaluations/evaluate.py 1 order
```

which runs the first batch of the list of models defined on the order benchmark. 


