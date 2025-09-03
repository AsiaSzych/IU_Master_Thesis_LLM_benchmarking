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

BigCodeBench results for GPT-4.1 and DeepSeek-V3-0324 were taken from official leaderboard published on [HuggingFace](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). For Claude Opus 4 the results were calculated accordin to the instructions published on [BigCodeBench GitHub](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). 

For the need of this projetc the Anthropic model should be evaluated without the thinking mode disabled. Unfortunatelly, the default script provided by BigCodeBench team was enabling thinking mode, which resulted in error as no thinking budget was set. To remove this obstacle a part of code which sets the thinking mode to enable was comment out and it is provided in the *./bigcodebench/gen/util/anthropic_request.py* script. 

The results for this evaluation can be found in *./bigcodebench/results/* folder. The hard subset of tasks was used and both **instruct** and **complete** splits were used. 

The results for Claude opus 4  as as follows: 

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
