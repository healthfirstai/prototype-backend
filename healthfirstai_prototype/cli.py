"""CLI for HealthFirstAI Prototype

This module contains the CLI for the HealthFirstAI prototype

"""
import os
from langchain.callbacks import get_openai_callback
from typing_extensions import Annotated
from .agents.toolkits.user_info.utils import get_user_info_for_json_agent
from .agents.toolkits.diet_plan.utils import (
    edit_diet_plan_json,
    get_user_meal_plans_as_json,
    get_user_meal_info_json,
    get_cached_plan_json,
    cache_diet_plan_redis,
)
from .agents.toolkits.exercise_plan.utils import (
    get_workout_schedule_json,
    cache_workout_schedule_redis,
    get_cached_schedule_json,
    edit_workout_schedule_json,
)
from .agents.chat_agent import (
    init_chat_agent,
)
from .agents.toolkits.advice.advice_agent import serp_api_search
from .enums.meal_enums import MealChoice, MealNames
from .controller.nutrition_vector_operations import (
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
def get_workout_schedule(
    uid: int = 1,
):
    """
    Get a workout schedule from the database
    """
    typer.echo("Getting workout schedule")
    workout_schedule = get_workout_schedule_json(uid)
    typer.echo(workout_schedule)
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
def test_chat_agent(
        input: str,
        uid: int = 1,
        session_id="my-session",
):
    """
    Test ReAct Diet Plan Agent
    """
    diet_agent = init_chat_agent(input, uid, session_id)
    with get_openai_callback() as cb:
        diet_agent(input)
        print(cb)


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
def cache_workout_schedule(uid: int = 1):
    """
    Stores workout schedule as it is in the SQL database in Redis
    """
    typer.echo("Storing schedule")
    cache_workout_schedule_redis(uid)
    typer.echo("Finished storing schedule")


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
def get_cached_schedule(
    uid: int = 1,
):
    """
    Get workout schedule from Redis
    """
    typer.echo("Getting schedule")
    schedule = get_cached_schedule_json(uid)
    typer.echo(schedule)
    typer.echo("Finished getting schedule")


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


@app.command()
def edit_cached_workout(
    agent_input: str,
    user_id: int = 1,
    store_in_cache: bool = False,
):
    """
    Get workout schedule from Redis
    """
    typer.echo("Editing schedule")
    new_schedule = edit_workout_schedule_json(
        agent_input,
        user_id,
        store_in_cache,
    )
    typer.echo(new_schedule)
    typer.echo("Finished editing schedule")


@app.command()
def build_docs():
    """
    Runs a chain of functions to build the documentation
    """
    shell_exec = (
        "mkdocs build && cp README.md docs/index.md && "
        "typer healthfirstai_prototype/cli.py utils docs --output docs/cli.md && "
        "cp README.md docs/index.md &&"
        "leasot --reporter markdown healthfirstai_prototype/*.py > docs/todo.md | prettier --write docs/todo.md"
    )

    os.system(shell_exec)


@app.command()
def test_advice_agent():
    """
    Test the core functionality of the advice agent
    """
    typer.echo("Testing advice agent...")
    query = input("Enter a query: ")
    kb_response = (
        ""  # FIX: Yan, function faiss_vector_search(query) does not exist anymore
    )
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


@app.callback()
def cli():
    """
    HealthFirstAI Prototype CLI
    """


if __name__ == "__main__":
    app()
