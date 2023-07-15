# NOTE: Hello world
# from healthfirstai_prototype.application import (
#     start_std_chain,
#     start_sql_chain,
#     start_seq_chain,
#     start_sql_agent,
# )

from healthfirstai_prototype.redis_db import (
    create_nutrition_index,
    flush_all,
    insert_foods,
    search_similar_food,
)

from healthfirstai_prototype.query import get_food_vector, get_vector_from_id
import click


@click.group()
def cli():
    pass


@cli.command()
def init_redis():
    """
    Initialize Redis
    """
    click.echo("Initializing Redis")
    flush_all()
    click.echo("Flushing all documents")
    create_nutrition_index()
    click.echo("Creating nutrition index")
    food = get_food_vector()
    insert_foods(food)
    click.echo("Food inserted")
    click.echo("Finished initializing Redis")


@cli.command()
def get_similar_food():
    """
    Test get_similar_food
    """
    click.echo("Searching by ID...")
    output = search_similar_food(167755, "get_similar_foods", 10)
    click.echo(output)
    click.echo("Finished search")


@cli.command()
def get_food():
    """
    Test get_similar_food
    """
    click.echo("Searching by ID...")
    output = get_vector_from_id(167755)
    click.echo(output)
    click.echo(type(output))
    click.echo(len(output))
    click.echo("Finished search")


# @cli.command()
# def exec_sql():
#     """
#     SQL Execution Chain
#     """
#     user_input = click.prompt("Enter your query", type=str)
#     output = start_sql_chain(user_input, verbose=True)
#     click.echo(f"SQL Query: {output}")
#
#
# @cli.command()
# def exec_std():
#     """
#     Standard Execution Chain
#     """
#     user_input = click.prompt("Enter your query", type=str)
#     output = start_std_chain(user_input, verbose=True)
#     click.echo(f"SQL Query: {output['output_sql_query']}")
#     click.echo(f"Query Result: {output['result']}")
#
#
# @cli.command()
# def exec_seq():
#     """
#     Sequential Execution Chain
#     """
#     user_input = click.prompt("Enter your query", type=str)
#     output = start_seq_chain(user_input, verbose=True)
#     click.echo(f"SQL Query: {output['output_sql_query']}")
#     click.echo(f"Query Result: {output['result']}")
#
#
# @cli.command()
# def exec_agent():
#     """
#     Agent Execution Chain
#     """
#     user_input = click.prompt("Enter your query", type=str)
#     output = start_sql_agent(user_input, verbose=True)
#     click.echo(f"SQL Query: {output['output_sql_query']}")
#     click.echo(f"Query Result: {output['result']}")
#
#
# @cli.command()
# # Add filename to load_test_cases from
# @click.option(
#     "--filename",
#     default="select_queries.json",
#     help="Specify a json file to load test cases from",
# )
# @click.option(
#     "--json_file_name",
#     default="std_predictions",
#     help="Specify a json file to save predictions to",
# )
# # Add verbose option
# @click.option(
#     "--verbose",
#     default=False,
#     help="Verbose output",
# )
# # Add top k default to 5
# @click.option(
#     "--top_k",
#     default=5,
#     help="Specify maximum number of rows to be returned",
# )
# def test_std(filename, json_file_name, verbose, top_k):
#     """
#     Test Standard Execution Chain
#     """
#     dataset = load_test_queries(filename)
#     predictions, predicted_dataset, error_dataset = run_std_chain(
#         dataset, verbose, top_k
#     )
#     graded_results = grade_results(predicted_dataset, predictions)
#     log_ouput, json_file_name = log_predictions(
#         graded_results, "Std Chain", json_file_name=json_file_name
#     )
#     click.echo(f"Predictions logged to json/{json_file_name}.json")
#     click.echo(log_ouput)
#
#
# @cli.command()
# # Add filename to load_test_cases from
# @click.option(
#     "--filename",
#     default="select_queries.json",
#     help="Specify a json file to load test cases from",
# )
#
# # Specify a json_file_name
# @click.option(
#     "--json_file_name",
#     default="seq_predictions",
#     help="Specify a json file to save predictions to",
# )
# # Add verbose option
# @click.option(
#     "--verbose",
#     default=False,
#     help="Verbose output",
# )
# # Add top k default to 5
# @click.option(
#     "--top_k",
#     default=5,
#     help="Specify maximum number of rows to be returned",
# )
# def test_seq(filename, json_file_name, verbose, top_k):
#     """
#     Test Sequential Execution Chain
#     """
#     dataset = load_test_queries(filename)
#     predictions, predicted_dataset, error_dataset = run_seq_chain(
#         dataset, verbose, top_k
#     )
#     graded_results = grade_results(predicted_dataset, predictions)
#     log_ouput, json_file_name = log_predictions(
#         graded_results, "Seq Chain", json_file_name=json_file_name
#     )
#     click.echo(f"Predictions logged to json/{json_file_name}.json")
#     click.echo(log_ouput)
#
#
# @cli.command()
# # Add filename to load_test_cases from
# @click.option(
#     "--filename",
#     default="select_queries.json",
#     help="Specify a json file to load test cases from",
# )
# @click.option(
#     "--json_file_name",
#     default="agent_predictions",
#     help="Specify a json file to save predictions to",
# )
# # Add verbose option
# @click.option(
#     "--verbose",
#     default=False,
#     help="Verbose output",
# )
# # Add top k default to 5
# @click.option(
#     "--top_k",
#     default=5,
#     help="Specify maximum number of rows to be returned",
# )
# def test_agent(filename, json_file_name, verbose, top_k):
#     """
#     Test Agent Execution Chain
#     """
#     dataset = load_test_queries(filename)
#     predictions, predicted_dataset, error_dataset = run_agent(dataset, verbose, top_k)
#     graded_results = grade_results(predicted_dataset, predictions)
#     log_ouput, json_file_name = log_predictions(
#         graded_results, "Agent", json_file_name=json_file_name
#     )
#     click.echo(f"Predictions logged to json/{json_file_name}.json")
#     click.echo(log_ouput)


if __name__ == "__main__":
    cli()
