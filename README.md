# IU_Master_Thesis_LLM_benchmarking
Benchmarking of selected LLM for a part of master thesis

This repository is dedicated for storing results of benchmarking 3 Large Language Models: 
* GPT-4.1 
* DeepSeek-V3-0324
* Claude Opus 4

on following benchmarks: 
* BigCodeBench
* HumanEvalPlus
* Java Bench 


### BigCodeBench 

BigCodeBench results for GPT-4.1 and DeepSeek-V3-0324 were taken from the official leaderboard published on [HuggingFace](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). For Claude Opus 4, the results were calculated according to the instructions published on [BigCodeBench GitHub](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). 

For the needs of this project, the Anthropic model should be evaluated without the thinking mode. Unfortunately, the default script provided by the BigCodeBench team was enabling thinking mode, which resulted in an error as no thinking budget was set. To remove this obstacle, a part of the code that sets the thinking mode to enable was commented out, and it is provided in the `./bigcodebench/gen/util/anthropic_request.py` script. 

The results for this evaluation can be found in the `./bigcodebench/results/` folder. The hard subset of tasks was used, and both **instruct** and **complete** splits were used. 

**The results for Claude Opus 4 are as follows:**

| Model | Tasks subset | Split | Result|
|-----:|------:|------:|------:|
|claude-opus-4-20250514|Hard |Complete|37.8|
|claude-opus-4-20250514|Hard|Instruct|29.7|
|claude-opus-4-20250514|Hard|Average|33.8|

**Results for GPT-4.1 taken from the leaderboard:**
| Model | Tasks subset | Split | Result|
|-----:|------:|------:|------:|
|GPT-4.1-2025-04-14|Hard |Complete|33.8|
|GPT-4.1-2025-04-14|Hard|Instruct|31.8|
|GPT-4.1-2025-04-14|Hard|Average|32.8|
|DeepSeek-V3-0324|Hard |Complete|35.8|
|DeepSeek-V3-0324|Hard|Instruct|27.7|
|DeepSeek-V3-0324|Hard|Average|31.8|


### HumanEvalPlus 
For the HumanEvalPlus benchmark, there were no official results provided for any of the evaluated models. Due to this fact, there was a need to run the benchmarks for all three LLMs. For GPT4.1 and Claude Opus 4, the score was obtained by running `evalplus.evaluate` with necessary arguments, as presented in the [evalplus GitHub](https://github.com/evalplus/evalplus) repository README. 

Unfortunately, there was a small obstacle while evaluating the DeepSeek model, as at the time of running this benchmark, the deepseek-chat alias was already pointing to the DeepSeek-V3.1 model version. To access the DeepSeek-V3-0324 model, a third-party provider [OpenRouter](https://openrouter.ai/deepseek/deepseek-chat-v3-0324) was used. OpenRouter supports using the API via Langchain framework by using functions dedicated to OpenAI standards. This allowed to quickly modify the benchmark setup to include Openrouter as a provided - the only thing that was needed to change was the `./humanevalplus/provider/openai.py` script, in which the base_url argument is now possible to be set up using a system variable. So, to use OpenRouter, two system variables need to be set: 
* OPENAI_API_KEY= api-key-from-the-openrouter-website 
* OPENAI_API_BASE="https://openrouter.ai/api/v1" 

After such a modification, the results for the model are as follows:

| Model | Testing suit | Result|
|-----:|------:|------:|
|GPT-4.1-2025-04-14| HumanEvalPlus|92.1|
|claude-opus-4-20250514| HumanEvalPlus|90.2|
|DeepSeek-V3-0324| HumanEvalPlus|89.6|

### JavaBench
For the JavaBench benchmark, the official Leaderboard didn't include any of the selected models. Additionally, code generation scripts available in the [official repository](https://github.com/java-bench/JavaBench) supported only the OpenAI API usage. To evaluate the Anthropic and DeepSeek models, an extension using other versions of the LangChain framework was implemented, and it is available in the `./javabench/inference.py` script. This time, it is also possible to use OpenRouter as a provider, which was needed for DeepSeek-V3-0324 evaluation. 

In the JavaBench repository, the scripts for querying the LLMs and checking class-wise and test-wise correctness were provided. However, there is no single script for summarizing the scores and finalizing the benchmark results. To calculate such a final state of the evaluation, the `./javabench/summarize.py` script was implemented. It is prepared to evaluate a pass@1 and compile@1 metrics for both class-wise and test-wise methodologies. 

The results for evaluation are as follow:
| Model | Eval type | Metric | Result|
|-----:|------:|------:|------:|
|GPT-4.1-2025-04-14|Class-wise |pass@1|82.7|
|GPT-4.1-2025-04-14|Class-wise|compile@1|83.6|
|claude-opus-4-20250514|Class-wise |pass@1|91.7|
|claude-opus-4-20250514|Class-wise|compile@1|92.1|
|DeepSeek-V3-0324|Class-wise |pass@1|70.3|
|DeepSeek-V3-0324|Class-wise|compile@1|73.2|
|GPT-4.1-2025-04-14|Test-wise |pass@1|49.4|
|GPT-4.1-2025-04-14|Test-wise|compile@1|61.6|
|claude-opus-4-20250514|Test-wise |pass@1|54.8|
|claude-opus-4-20250514|Test-wise|compile@1|61.6|
|DeepSeek-V3-0324|Test-wise |pass@1|32.5|
|DeepSeek-V3-0324|Test-wise|compile@1|53.1|