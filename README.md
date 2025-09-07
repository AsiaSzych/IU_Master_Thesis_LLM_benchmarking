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

BigCodeBench results for GPT-4.1 and DeepSeek-V3-0324 were taken from official leaderboard published on [HuggingFace](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). For Claude Opus 4 the results were calculated according to the instructions published on [BigCodeBench GitHub](https://huggingface.co/spaces/bigcode/bigcodebench-leaderboard). 

For the need of this project the Anthropic model should be evaluated without the thinking mode. Unfortunatelly, the default script provided by BigCodeBench team was enabling thinking mode, which resulted in error as no thinking budget was set. To remove this obstacle a part of code which sets the thinking mode to enable was comment out and it is provided in the *./bigcodebench/gen/util/anthropic_request.py* script. 

The results for this evaluation can be found in *./bigcodebench/results/* folder. The hard subset of tasks was used and both **instruct** and **complete** splits were used. 

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
For HumanEvalPlus benchmark there were no official results provided for any of the evaluated models. Due to this fact, there was a need to run the benchmarks for all three LLMs. For GPT4.1 and Claude Opus 4, the score was obtained by running `evalplus.evaluate` with necessary arguments, as presented in the [evalplus GitHub](https://github.com/evalplus/evalplus) repository readMe. 

Unfortunatelly, there was a small obstacle, while evaluating DeepSeek model, as at the time of running this benchmark the deepseek-chat alias was already pointing to DeepSeek-V3.1 model version. To access the DeepSeek-V3-0324 model, a third party provider [OpenRouter](https://openrouter.ai/deepseek/deepseek-chat-v3-0324) was used. OpenRouter supports using API via Langchain framework by using functions dedicated to OpenAI standards. Tihs allowed to quickly modiy the benchmark setup to include Openrouter as a provided - the only thing that was needed to change was the `./provider/openai.py` script, in which the base_url argumnet is now possible to be set up using system variable. So, to use OpenRouter two system variables need to be set: 
* OPENAI_API_KEY= api-key-from-the-openrouter-website 
* OPENAI_API_BASE="https://openrouter.ai/api/v1" 

After such a modificatoin, the results for the model are as follows:

| Model | Testing suit | Result|
|-----:|------:|------:|
|GPT-4.1-2025-04-14| HumanEvalPlus|92.1|
|claude-opus-4-20250514| HumanEvalPlus|90.2|
|DeepSeek-V3-0324| HumanEvalPlus|89.6|