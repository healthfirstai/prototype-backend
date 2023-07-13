import json
import asyncio
import tqdm
from typing import List, Tuple
from collections import Counter

# Import from Python file
from knn3_nl_to_sql.application import (
    start_std_chain,
    start_std_chain_async,
    start_seq_chain_async,
    start_seq_chain,
    start_sql_agent,
)

from langchain import OpenAI

# Tools for evaluation
from langchain.evaluation.qa import QAEvalChain


def load_test_queries(
    test_query_filename="select_queries.json",
    test_query_dir_name="queries",
) -> List[dict]:
    with open(f"app/{test_query_dir_name}/{test_query_filename}", "r") as f:
        dataset = json.load(f)
    return dataset


def run_seq_chain(dataset, verbose, top_k) -> Tuple[List[dict], List[dict], List[dict]]:
    """
    Executes sequential chain on test dataset
    """
    predictions = []
    predicted_dataset = []
    error_dataset = []
    # Run sequential chain
    # TODO: There may be an issue here
    for input_dict in tqdm.tqdm(dataset):
        try:
            result_dict = start_seq_chain(input_dict["user_input"], verbose, top_k)
            combined = {**input_dict, **result_dict}
            predictions.append(combined)
            predicted_dataset.append(combined)
        except Exception as e:
            # write e to file
            with open("seq_error.txt", "w") as f:
                f.write(str(e))
            error_dataset.append(input_dict)

    return predictions, predicted_dataset, error_dataset


async def run_seq_chain_async(
    dataset, verbose, top_k
) -> Tuple[List[dict], List[dict], List[dict]]:
    """
    Executes Sequential chain on test dataset
    """
    predictions = []
    predicted_dataset = []
    error_dataset = []
    tasks = []

    for input_dict in dataset:
        task = asyncio.ensure_future(
            start_seq_chain_async(input_dict["user_input"], verbose, top_k)
        )
        tasks.append(task)

    print("Gathering tasks...")
    results = await asyncio.gather(*tasks)
    print("Done gathering!")

    for input_dict, result_dict in zip(dataset, results):
        try:
            combined = {**input_dict, **result_dict}
            predictions.append(combined)
            predicted_dataset.append(combined)
        except Exception as e:
            # TODO: make this error logging better
            with open("seq_error.txt", "w") as f:
                f.write(str(e))
            error_dataset.append(input_dict)

    return predictions, predicted_dataset, error_dataset


async def run_std_chain_async(
    dataset, verbose, top_k
) -> Tuple[List[dict], List[dict], List[dict]]:
    """
    Executes standard chain on test dataset
    """
    predictions = []
    predicted_dataset = []
    error_dataset = []
    tasks = []

    for input_dict in dataset:
        task = asyncio.ensure_future(
            start_std_chain_async(input_dict["user_input"], verbose, top_k)
        )
        tasks.append(task)

    print("Gathering tasks...")
    results = await asyncio.gather(*tasks)
    print("Done gathering!")

    for input_dict, result_dict in zip(dataset, results):
        try:
            combined = {**input_dict, **result_dict}
            predictions.append(combined)
            predicted_dataset.append(combined)
        except Exception as e:
            # TODO: make this error logging better
            with open("std_error.txt", "w") as f:
                f.write(str(e))
            error_dataset.append(input_dict)

    return predictions, predicted_dataset, error_dataset


def run_std_chain(dataset, verbose, top_k) -> Tuple[List[dict], List[dict], List[dict]]:
    """
    Executes standard chain on test dataset
    """
    predictions = []
    predicted_dataset = []
    error_dataset = []
    # TODO: Convert to async to make this much faster
    for input_dict in tqdm.tqdm(dataset):
        try:
            result_dict = start_std_chain(input_dict["user_input"], verbose, top_k)
            combined = {**input_dict, **result_dict}
            predictions.append(combined)
            predicted_dataset.append(combined)
        except Exception as e:
            # TODO: make this error logging better
            with open("std_error.txt", "w") as f:
                f.write(str(e))
            error_dataset.append(input_dict)
    return predictions, predicted_dataset, error_dataset


def run_agent(dataset, verbose, top_k) -> Tuple[List[dict], List[dict], List[dict]]:
    """
    Executes agent on test dataset
    """
    predictions = []
    predicted_dataset = []
    error_dataset = []
    for input_dict in tqdm.tqdm(dataset):
        try:
            # combine temp and data dict
            result_dict = start_sql_agent(input_dict["user_input"], verbose, top_k)
            combined = {**input_dict, **result_dict}
            predictions.append(combined)
            predicted_dataset.append(combined)
        except Exception as e:
            with open("agent_error.txt", "w") as f:
                f.write(str(e))
            error_dataset.append(input_dict)
    return predictions, predicted_dataset, error_dataset


def grade_results(predicted_dataset: List[dict], predictions: List[dict]) -> List[dict]:
    """
    Sets up evaluation chain and returns prediction with grades
    """
    llm = OpenAI(temperature=0)
    eval_chain = QAEvalChain.from_llm(llm)
    graded_outputs = eval_chain.evaluate(
        predicted_dataset,
        predictions,
        question_key="user_input",
        answer_key="correct_sql_query",
        prediction_key="output_sql_query",
    )
    # Add grade to predictions
    for i, prediction in enumerate(predictions):
        prediction["grade"] = graded_outputs[i]["text"]
    return predictions


def log_predictions(
    predictions: List[dict], prediction_type: str, json_file_name="predictions"
) -> Tuple[Counter, str]:
    """
    Logs predictions to JSON file and prints path
    """
    with open(f"app/json/{json_file_name}.json", "w") as f:
        json.dump(predictions, f, indent=4)

    return Counter([pred["grade"] for pred in predictions]), json_file_name


def main():
    pass


if __name__ == "__main__":
    main()
