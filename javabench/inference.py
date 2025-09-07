import random
import argparse
import os
import itertools
import logging
from tqdm import tqdm
from fastchat.model import load_model, get_conversation_template, add_model_args
from app.prompt.template import complete_template
from app.static_analyzer.class_compose_tool import get_todo_methods, replace_method, retain_todo_method
from app.util.io import extract_code, stream_jsonl, write_jsonl
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def inference(args):
    is_openai = args.model_path.startswith("gpt") or args.model_path.startswith("deepseek")
    is_anthropic = args.model_path.startswith("claude")
    if is_openai:
        model = ChatOpenAI(model=args.model_path, temperature=args.temperature)
    elif is_anthropic:
        model = ChatAnthropic(model=args.model_path, temperature=args.temperature)
    else:
        model, tokenizer = load_model(
            args.model_path,
            device=args.device,
            num_gpus=args.num_gpus,
            max_gpu_memory=args.max_gpu_memory,
            load_8bit=args.load_8bit,
            cpu_offloading=args.cpu_offloading,
            revision=args.revision,
            debug=args.debug,
        )
        tokenizer.pad_token = tokenizer.eos_token

    def query(code, code_context):
        lc_messages = complete_template.format_messages(
            code_context=code_context,
            code=code,
        )

        if is_openai or is_anthropic:
            prompt = lc_messages[0].content + "\n" + lc_messages[1].content
            outputs = model.invoke(lc_messages).content
        else:
            conv = get_conversation_template(args.model_path)
            if "{system_message}" in conv.system_template:
                conv.system_message = lc_messages[0].content
            else:
                conv.append_message(conv.roles[0], lc_messages[0].content)
            conv.append_message(conv.roles[0], lc_messages[1].content)
            conv.append_message(conv.roles[1], None)
            prompt = conv.get_prompt()

            # Run inference
            inputs = tokenizer([prompt], return_tensors="pt").to(args.device)
            output_ids = model.generate(
                **inputs,
                do_sample=True if args.temperature > 1e-5 else False,
                temperature=args.temperature,
                repetition_penalty=args.repetition_penalty,
                max_new_tokens=args.max_new_tokens,
            )
            if model.config.is_encoder_decoder:
                output_ids = output_ids[0]
            else:
                output_ids = output_ids[0][len(inputs["input_ids"][0]) :]
            outputs = tokenizer.decode(
                output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
            )
        return prompt, outputs

    tasks = list(stream_jsonl(args.data))
    samples = list(stream_jsonl(args.output)) if os.path.exists(args.output) else []
    for task, _ in tqdm(itertools.islice(itertools.product(tasks, range(args.num_sample)), len(samples), None), total=len(tasks) * args.num_sample, initial=len(samples)):
        if args.mode == "holistic":
            prompt, outputs = query(task["code"], task["code_context"])
            samples.append(dict(
                task_id=task["task_id"],
                target=task["target"],
                prompt=prompt,
                completion=outputs,
            ))
        elif args.mode == "independent":
            result = task["code"]
            mediate = []

            todo_methods = get_todo_methods(result)
            progress = tqdm(todo_methods)
            for todo_method in progress:
                progress.set_description(f"{todo_method['name']} {todo_method['seq']}")
                source = retain_todo_method(task["code"], todo_method["name"], todo_method["seq"])
                prompt, outputs = query(source, task["code_context"])
                result = replace_method(result, extract_code(outputs), todo_method["name"], todo_method["seq"])
                new_mediate = dict(
                    name=todo_method["name"],
                    seq=todo_method["seq"],
                    prompt=prompt,
                    completion=outputs,
                )
                mediate.append(new_mediate)
                logging.info(f"{todo_method['name']} {todo_method['seq']} {new_mediate}")

            samples.append(dict(
                task_id=task["task_id"],
                target=task["target"],
                completion=result,
                mediate=mediate,
            ))
        elif args.mode == "incremental":
            result = task["code"]
            mediate = []

            todo_methods = get_todo_methods(result)
            if args.incremental_mode == "rev":
                todo_methods = reversed(todo_methods)
            elif args.incremental_mode == "rand":
                random.shuffle(todo_methods)
            progress = tqdm(todo_methods)
            for todo_method in progress:
                progress.set_description(f"{todo_method['name']} {todo_method['seq']}")
                source = retain_todo_method(result, todo_method["name"], todo_method["seq"])
                prompt, outputs = query(source, task["code_context"])
                result = replace_method(result, extract_code(outputs), todo_method["name"], todo_method["seq"])
                new_mediate = dict(
                    name=todo_method["name"],
                    seq=todo_method["seq"],
                    prompt=prompt,
                    completion=outputs,
                )
                mediate.append(new_mediate)
                logging.info(f"{todo_method['name']} {todo_method['seq']} {new_mediate}")

            samples.append(dict(
                task_id=task["task_id"],
                target=task["target"],
                completion=result,
                mediate=mediate,
            ))
        if os.path.dirname(args.output):
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
        write_jsonl(args.output, samples)


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S', filename=f"logs/inference-{os.getpid()}.log", filemode="w", level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    add_model_args(parser)
    parser.add_argument(
        "--mode", 
        type=str,
        choices=["holistic", "independent", "incremental"],
        default="holistic",
    )

    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--num-sample", type=int, default=10)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--incremental-mode", type=str, choices=["seq", "rev", "rand"], default="seq")

    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--repetition_penalty", type=float, default=1.0)
    parser.add_argument("--max-new-tokens", type=int, default=4096)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    inference(args)
