from healthfirstai_prototype.nutrition_utils import (
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
    get_user_meal_info_json,
    get_user_info_dict,
    store_diet_plan,
    get_cached_plan_json,
)
from healthfirstai_prototype.nutrition_agent import (
    start_nutrition_temp_agent,
    init_agent,
    init_new_agent,
    init_plan_and_execute_diet_agent,
)
from healthfirstai_prototype.advice_agent import faiss_vector_search, serp_api_search
from healthfirstai_prototype.transform import (
    delete_all_vectors,
    get_all_foods,
    insert_all_vectors,
)

import typer

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def get_diet_plan(
    uid: int = 1,
    include_ingredients: bool = True,
):
    """
    Get a meal plan from the database
    """
    typer.echo("Getting meal plan")
    meal_plan = get_user_meal_plans_as_json(uid, include_ingredients)
    typer.echo(meal_plan)
    typer.echo("Finished search")


@app.command()
def get_meal(
    uid: int = 1,
    include_ingredients: bool = True,
    include_nutrients: bool = True,
    meal_choice: str = "b",
):
    """
    Get meal from the database given meal name
    """
    typer.echo("Getting breakfast")
    if meal_choice == "b":
        meal = get_user_meal_info_json(
            uid, include_ingredients, include_nutrients, "Breakfast"
        )
    elif meal_choice == "l":
        meal = get_user_meal_info_json(
            uid, include_ingredients, include_nutrients, "Lunch"
        )
    elif meal_choice == "d":
        meal = get_user_meal_info_json(
            uid, include_ingredients, include_nutrients, "Dinner"
        )
    elif meal_choice == "s":
        meal = get_user_meal_info_json(
            uid, include_ingredients, include_nutrients, "Snack"
        )
    else:
        typer.echo("Invalid meal choice")
        return
    typer.echo(meal)
    typer.echo("Finished search")


@app.command()
def test_agent(uid: int = 1, input: str = "What am I having for dinner?"):
    """
    Test ReAct Diet Plan Agent
    """
    diet_agent = init_agent(input, uid)
    diet_agent(input)


@app.command()
def get_user_info(uid: int = 1):
    """
    Get user info from the database
    """
    typer.echo(f"Getting user info for user {uid}")
    user_info = get_user_info_for_json_agent(uid)
    typer.echo(user_info)
    typer.echo("Finished search")


@app.command()
def reinsert_vectors():
    """
    Delete all vectors in nutrition_vectors and insert new vectors
    """
    typer.echo("Reinserting nutrition vectors")
    delete_all_vectors()
    typer.echo("Deleted all old vectors")
    foods = get_all_foods()
    typer.echo("Queried and got all foods")
    insert_all_vectors(foods)
    typer.echo("Inserted new food vectors")
    typer.echo("Finished search")


@app.command()
def store_plan(uid: int = 1):
    """
    Store a plan in the database
    """
    typer.echo("Storing plan")
    store_diet_plan(uid)
    typer.echo("Finished storing plan")


@app.command()
def get_cached_plan(uid: int = 1):
    """
    Get diet plan from Redis
    """
    typer.echo("Getting plan")
    plan = get_cached_plan_json(uid)
    typer.echo(plan)
    typer.echo("Finished getting plan")


@app.callback()
def cli():
    """
    HealthFirstAI Prototype CLI
    """


# @cli.command()
# def test_advice_agent():
#     """
#     Test the core functionality of the advice agent
#     """
#     click.echo("Testing advice agent...")
#     query = input("Enter a query: ")
#     faiss_response = faiss_vector_search(query)
#     google_response = serp_api_search(query)
#     click.echo("Finished search. Wait for the results below:")
#     click.echo(f"K-Base search response: {faiss_response}")
#     click.echo("------------------------------------------")
#     click.echo(f"Google search response: {google_response}")
#     click.echo("------------------------------------------")
#     click.echo("Finished testing advice agent.")


if __name__ == "__main__":
    app()
