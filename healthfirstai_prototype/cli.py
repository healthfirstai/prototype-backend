"""CLI for HealthFirstAI Prototype

This module contains the CLI for the HealthFirstAI prototype

"""
from typing_extensions import Annotated
from healthfirstai_prototype.nutrition_chains import edit_diet_plan_json
from healthfirstai_prototype.nutrition_logic import (
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
    get_user_meal_info_json,
    get_cached_plan_json,
    cache_diet_plan_redis,
)
from healthfirstai_prototype.chat_agent import (
    init_agent,
)
from healthfirstai_prototype.advice_agent import serp_api_search
from healthfirstai_prototype.util_models import MealNames, MealChoice
from healthfirstai_prototype.nutrition_vector_ops import (
    delete_all_vectors,
    get_all_foods,
    insert_all_vectors,
)


from healthfirstai_prototype.advice_prompts import (
    run_assessment_chain,
    template_to_assess_search_results,
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
def get_cached_meal(
    meal_choice: MealChoice = MealChoice.breakfast,
    uid: int = 1,
    include_ingredients: Annotated[bool, typer.Option("--ingredients", "-i")] = False,
    include_nutrients: Annotated[bool, typer.Option("--nutrients", "-n")] = False,
):
    """
    Get meal from the Redis Cache given meal name
    """
    typer.echo("Getting breakfast")
    if meal_choice == "b":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.breakfast,
            cached=True,
        )
    elif meal_choice == "l":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.lunch,
            cached=True,
        )
    elif meal_choice == "d":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.dinner,
            cached=True,
        )
    elif meal_choice == "s":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.snack,
            cached=True,
        )
    else:
        typer.echo("Invalid meal choice")
        return
    typer.echo(meal)
    typer.echo("Finished search")


@app.command()
def get_meal(
    meal_choice: MealChoice = MealChoice.breakfast,
    uid: int = 1,
    include_ingredients: Annotated[bool, typer.Option("--ingredients", "-i")] = False,
    include_nutrients: Annotated[bool, typer.Option("--nutrients", "-n")] = False,
):
    """
    Get meal from the SQL database given meal name
    """
    if meal_choice == "b":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.breakfast,
            cached=False,
        )
    elif meal_choice == "l":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.lunch,
            cached=False,
        )
    elif meal_choice == "d":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.dinner,
            cached=False,
        )
    elif meal_choice == "s":
        meal = get_user_meal_info_json(
            uid,
            include_ingredients,
            include_nutrients,
            MealNames.snack,
            cached=False,
        )
    else:
        typer.echo("Invalid meal choice")
        return
    typer.echo(meal)
    typer.echo("Finished search")


@app.command()
def test_agent(
    input: str,
    uid: int = 1,
    session_id="my-session",
):
    """
    Test ReAct Diet Plan Agent
    """
    diet_agent = init_agent(input, uid, session_id)
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
def cache_diet_plan(uid: int = 1):
    """
    Stores diet plan as it is in the SQL database in Redis
    """
    typer.echo("Storing plan")
    cache_diet_plan_redis(uid)
    typer.echo("Finished storing plan")


@app.command()
def get_cached_plan(
    uid: int = 1,
    include_ingredients: bool = True,
):
    """
    Get diet plan from Redis
    """
    typer.echo("Getting plan")
    plan = get_cached_plan_json(uid, include_ingredients)
    typer.echo(plan)
    typer.echo("Finished getting plan")


@app.command()
def edit_cached_meal(
    agent_input: str,
    meal_choice: MealNames,
    user_id: int = 1,
    include_ingredients: bool = False,
    store_in_cache: bool = False,
):
    """
    Get diet plan from Redis
    """
    typer.echo("Editing plan")
    new_plan = edit_diet_plan_json(
        agent_input,
        user_id,
        meal_choice,
        include_ingredients,
        store_in_cache,
    )
    typer.echo(new_plan)
    typer.echo("Finished editing plan")


@app.callback()
def cli():
    """
    HealthFirstAI Prototype CLI
    """


@app.command()
def test_advice_agent():
    """
    Test the core functionality of the advice agent
    """
    typer.echo("Testing advice agent...")
    query = input("Enter a query: ")
    kb_response = "" # FIX: Yan, function faiss_vector_search(query) does not exist anymore
    google_response = serp_api_search(query)
    typer.echo("Finished search. Wait for the results below:")
    typer.echo(f"K-Base search response: {kb_response}")
    typer.echo("------------------------------------------")
    typer.echo(f"Google search response: {google_response}")
    typer.echo("------------------------------------------")

    template = template_to_assess_search_results()
    response = run_assessment_chain(
        prompt_template=template,
        input_from_the_user=query,
        google_search_result=google_response,
        kb_search_result=kb_response,
    )["text"]

    typer.echo("------------------------------------------")
    typer.echo("Most relevant response after evaluation: ")
    if response == "B":
        typer.echo(kb_response)
    else:
        typer.echo(google_response)
    typer.echo("------------------------------------------")


if __name__ == "__main__":
    app()
