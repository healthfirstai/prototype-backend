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
from healthfirstai_prototype.transform import (
    delete_all_vectors,
    get_all_foods,
    insert_all_vectors,
)

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID to get the meal plan for",
)
@click.option(
    "--include-ingredients",
    default=True,
    help="Whether to include the ingredients in the meal plan",
)
def get_diet_plan(uid: int, include_ingredients: bool):
    """
    Get a meal plan from the database
    """
    click.echo("Getting meal plan")
    meal_plan = get_user_meal_plans_as_json(uid, include_ingredients)
    click.echo(meal_plan)
    click.echo("Finished search")


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID to get the meal plan for",
)
@click.argument(
    "meal_choice",
    default="b",
)
@click.option(
    "--include-ingredients",
    default=True,
    help="Whether to include the ingredients in the meal plan",
)
@click.option(
    "--include-nutrients",
    default=True,
    help="Whether to include the ingredients in the meal plan",
)
def get_meal(uid: int, include_ingredients: bool, include_nutrients: bool,meal_choice: str):
    """
    Get breakfast from the database
    """
    click.echo("Getting breakfast")
    if meal_choice == "b":
        meal = get_user_meal_info_json(uid, include_ingredients, include_nutrients,"Breakfast")
    elif meal_choice == "l":
        meal = get_user_meal_info_json(uid, include_ingredients, include_nutrients,"Lunch")
    elif meal_choice == "d":
        meal = get_user_meal_info_json(uid, include_ingredients, include_nutrients,"Dinner")
    elif meal_choice == "s":
        meal = get_user_meal_info_json(uid, include_ingredients, include_nutrients,"Snack")
    else:
        click.echo("Invalid meal choice")
        return
    click.echo(meal)
    click.echo("Finished search")


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID of the user who has the meal plan",
)
@click.argument(
    "input",
    default="What am I having for dinner?",
)
def test_agent(uid: int, input: str):
    """
    Test ReAct Diet Plan Agent
    """
    diet_agent = init_agent(input, uid)
    diet_agent(input)


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID of the user who has the meal plan",
)
@click.argument(
    "input",
    default="What am I having for dinner?",
)
def test_new_agent(uid: int, input: str):
    """
    Test New Diet Agent
    """
    diet_agent = init_new_agent(input)
    diet_agent(input)


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID of the user who has the meal plan",
)
@click.argument(
    "input",
    default="User_1 says: What am I having for dinner",
)
def test_plan_and_execute_agent(uid: int, input: str):
    """
    Test Plan and Execute Agent
    """
    diet_agent = init_plan_and_execute_diet_agent()
    diet_agent(f"User_{uid} says: {input}")
    click.echo("\nOutput Finished")


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID to get info for",
)
def user_info(uid: int):
    """
    Get user info from the database
    """
    click.echo(f"Getting user info for user {uid}")
    meal_plan = get_user_info_for_json_agent(uid)
    click.echo(meal_plan)
    click.echo("Finished search")


@cli.command()
def reinsert_vectors():
    """
    Delete all vectors in nutrition_vectors and insert new vectors
    """
    click.echo("Reinserting nutrition vectors")
    delete_all_vectors()
    click.echo("Deleted all old vectors")
    foods = get_all_foods()
    click.echo("Queried and got all foods")
    insert_all_vectors(foods)
    click.echo("Inserted new food vectors")
    click.echo("Finished search")


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID to get info for",
)
def store_plan(uid: int):
    """
    Store a plan in the database
    """
    click.echo("Storing plan")
    store_diet_plan(uid)
    click.echo("Finished storing plan")


@cli.command()
@click.option(
    "--uid",
    default=1,
    help="The user ID to get info for",
)
def get_cached_plan(uid: int):
    """
    Get diet plan from Redis
    """
    click.echo("Getting plan")
    plan = get_cached_plan_json(uid)
    click.echo(plan)
    click.echo("Finished getting plan")


if __name__ == "__main__":
    cli()
