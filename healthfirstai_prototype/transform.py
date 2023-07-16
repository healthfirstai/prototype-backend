from decimal import Decimal

if __name__ == "__main__":
    from database import SessionLocal
    from datatypes import Food, Nutrition_Vector
else:
    from healthfirstai_prototype.database import SessionLocal
    from healthfirstai_prototype.datatypes import Food


def get_all_foods() -> list[Food]:
    """
    Returns all foods in the food table
    """
    session = SessionLocal()
    output = session.query(Food).all()
    session.close()
    return output


def clean_nutrition_vector(food_dict: dict) -> list[Decimal]:
    """
    Cleans the nutrition vector by removing all non-numerical information
    This should be ran when we need to update the nutrition vectors
    Returns a list of values
    """
    # Clean the dictionary
    food_dict.pop("_sa_instance_state")
    food_dict.pop("Food_Group")
    food_dict.pop("Name")
    food_dict.pop("Calories")
    food_dict = {k: v for k, v in food_dict.items() if "Serving" not in k}

    # Convert the dictionary to a list of tuples
    list_of_tuples = list(food_dict.items())
    # Replace all null values with Decimal(0)
    list_of_tuples = [
        (k, Decimal("0")) if v is None else (k, v) for k, v in list_of_tuples
    ]
    # Sort the list of tuples by key
    sorted_list_of_tuples = sorted(list_of_tuples, key=lambda x: x[0])
    return [v for _, v in sorted_list_of_tuples]


def insert_vector(food_id: int, vector: list[Decimal]):
    """
    Inserts a nutrition vector into the nutrition_vector table
    """
    session = SessionLocal()
    item = Nutrition_Vector(food_id=food_id, embedding=vector)
    session.add(item)
    session.commit()
    session.close()


def main():
    foods = get_all_foods()
    for food in foods:
        food_dict = food.__dict__
        food_id = food_dict.pop("id")
        vector = clean_nutrition_vector(food_dict)
        insert_vector(food_id, vector)


if __name__ == "__main__":
    main()
