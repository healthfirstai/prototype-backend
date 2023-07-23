from healthfirstai_prototype.nutrition_utils import (
    get_user_meal_plans_as_json,
    get_user_info_for_json_agent,
    get_user_info_dict,
)
from healthfirstai_prototype.nutrition_agent import (
    start_nutrition_temp_agent,
    init_agent,
    init_plan_and_execute_diet_agent
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
def user_diet_plan(uid: int, include_ingredients: bool):
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
    diet_agent = init_agent()
    diet_agent(f"User_{uid} says: {input}")
    click.echo("\nOutput Finished")

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


if __name__ == "__main__":
    cli()
