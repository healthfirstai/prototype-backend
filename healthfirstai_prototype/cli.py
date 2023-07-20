# NOTE: This is an example of how to interact with our application code with the command line

from healthfirstai_prototype.redis_db import (
    search_similar_food,
)

from healthfirstai_prototype.generate import get_user_meal_plans
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
def get_meal_plan():
    """
    Get a meal plan from the database
    """
    click.echo("Getting meal plan")
    meal_plan = get_user_meal_plans(1) # NOTE: We are getting the meal plan for user 1
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
