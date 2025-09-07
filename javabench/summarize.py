
import json
import os

base_dir = "./test_output"
eval_output_dir = "./eval_output"
models = ["gpt", "claude", "deepseek"]
projects = ["result-PA19", "result-PA20", "result-PA21", "result-PA22"]


def eval_project_test_wise(base_dir, model, project, mode, eval_output_data):
    file = os.path.join(base_dir, model, project, mode)
    with open(file) as json_data:
        data = json.load(json_data)
    tasks_keys = data.keys()

    all_passes = []
    all_compile = []
    for key in tasks_keys:
        task_data = data[key]
        task_data = task_data[0] #pass@1 
        compilable = task_data["compilable"]
        if compilable:
            all_compile.append(1)
            n_pass_ratio = task_data["n_pass"][0]/ task_data["n_pass"][1]
            all_passes.append(n_pass_ratio)
        else:
            all_compile.append(0)
            all_passes.append(0.0)

    pass_at_k = sum(all_passes)/len(all_passes)
    compile_at_k = sum(all_compile)/len(all_compile)

    eval_output_data[project] = {}
    eval_output_data[project]['pass'] = pass_at_k
    eval_output_data[project]['compile'] = compile_at_k

    return eval_output_data

def eval_project_class_wise(base_dir, model, project, mode, eval_output_data):
    file = os.path.join(base_dir, model, project, mode)
    with open(file) as json_data:
        data = json.load(json_data)

    evaluated_tasks = []
    all_passes = []
    all_compile = []
    all_errors = []
    for item in range(len(data)):
        task_data = data[item]
        if task_data['task_id'] not in evaluated_tasks:
            evaluated_tasks.append(task_data['task_id'])
            compile_errors = task_data["compile_errors"]
            if compile_errors==0:
                all_compile.append(1)
                all_errors.append(0)
                n_pass_ratio = task_data["test_result"][0]/ task_data["test_result"][1]
                all_passes.append(n_pass_ratio)
            else:
                all_compile.append(0)
                all_errors.append(compile_errors)
                all_passes.append(0.0)

            pass_at_k = sum(all_passes)/len(all_passes)
            compile_at_k = sum(all_compile)/len(all_compile)

            eval_output_data[project] = {}
            eval_output_data[project]['pass'] = pass_at_k
            eval_output_data[project]['compile'] = compile_at_k
                
    return eval_output_data

def add_average(data):
    sum_pass = 0
    sum_compile = 0
    data_keys = data.keys()
    number_of_project = len(data_keys)
    for key in data_keys:
        sum_pass += data[key]['pass']
        sum_compile += data[key]['compile']

    data["result_average"] = {}
    data["result_average"]['passs'] = sum_pass/number_of_project
    data["result_average"]['compile'] = sum_compile/number_of_project

    return data

def run_for_mode(mode):
    for model in models:
        eval_output_data = {}
        eval_output_file = os.path.join(eval_output_dir, f"{model}-{mode}-wise-eval.json")
        for project in projects:
            if mode == 'test':
                eval_output_data = eval_project_test_wise(base_dir, model, project, "result-full.json", eval_output_data)
            elif mode == 'class':
                eval_output_data = eval_project_class_wise(base_dir, model, project, "single_class.json", eval_output_data)
        eval_output_data = add_average(eval_output_data)
        with open(eval_output_file, 'a') as f:
            json.dump(eval_output_data, f)

if __name__=="__main__":
    run_for_mode("test")
    run_for_mode("class")

