from decimal import Decimal
import numpy as np
from numpy.typing import NDArray

if __name__ == "__main__":
    from database import SessionLocal
    from datatypes import Food, Nutrition_Vector
else:
    from healthfirstai_prototype.database import SessionLocal
    from healthfirstai_prototype.datatypes import Food, Nutrition_Vector


def get_all_foods() -> list[Food]:
    """
    Returns all foods in the food table
    """
    session = SessionLocal()
    output = session.query(Food).all()
    session.close()
    return output


def clean_nutrition_vector(food_dict: dict) -> NDArray:
    """
    Cleans the nutrition vector by removing all non-numerical information
    This should be ran when we need to update the nutrition vectors
    Returns a list of values
    """
    # Clean the dictionary
    food_dict.pop("_sa_instance_state")
    food_dict.pop("Food_Group")
    food_dict.pop("Name")
    food_dict = {k: v for k, v in food_dict.items() if "Serving" not in k}

    # Extract the macronutrients from the dictionary and add it to a list
    macros = [
        food_dict.pop("Calories"),
        food_dict.pop("Protein_g"),
        food_dict.pop("Carbohydrate_g"),
        food_dict.pop("Fat_g"),
    ]

    # Convert the dictionary to a list of tuples
    micro_tuples_list = list(food_dict.items())
    # Replace all null values with Decimal(0)
    micro_tuples_list = [
        (k, 0.0) if v is None else (k, v) for k, v in micro_tuples_list
    ]
    micro_tuples_list = [(k, float(v)) for k, v in micro_tuples_list]
    # Sort the list of tuples by key
    sorted_list_of_micro_tuples = sorted(micro_tuples_list, key=lambda x: x[0])
    # Remove the keys from the list of tuples
    micro_values_list = [v for _, v in sorted_list_of_micro_tuples]
    # Add the macronutrients to the front of list of micronutrients
    list_of_nutrients = macros + micro_values_list
    return np.array(list_of_nutrients)


def insert_vector(food_id: int, vector: NDArray):
    """
    Inserts a nutrition vector into the nutrition_vector table
    """
    session = SessionLocal()
    # if vector is full of nan values, then replace with 0
    vector = np.nan_to_num(vector)
    item = Nutrition_Vector(food_id=food_id, embedding=vector.tolist())
    session.add(item)
    session.commit()
    session.close()


def normalize_vector(vector: NDArray) -> NDArray:
    """
    Calculates the magnitude of the vector and divides each element by the magnitude
    """
    magnitude = np.linalg.norm(vector)
    return vector / magnitude


# TODO: You should change these weights given the following factors
# 1. The importance of the macronutrient vs the micronutrients
# 2. The food group the food belongs too and the user's goal
# For example, for fruits and vegetables, you should pay more attention to the micronutrients if your goal is to get healthy
# And for meats, you should pay more attention to the macronutrients if your goal is to gain muscle for example
def add_vector_weights(v_normalized: NDArray) -> NDArray:
    """
    Adds weights to the nutrition vector to account for macro/micronutrient importance
    """
    weights = np.ones_like(v_normalized)
    # weights = np.zeros_like(v_normalized) # This is for testing
    # Weights for macronutrients
    weights[0] = 100  # Calories
    weights[1] = 100  # Protein
    weights[2] = 100  # Carbohydrates
    weights[3] = 100  # Fat
    return v_normalized * weights


def delete_all_vectors():
    """
    Deletes all vectors from the nutrition_vector table
    """
    session = SessionLocal()
    session.query(Nutrition_Vector).delete()
    session.commit()
    session.close()


def insert_all_vectors(foods: list[Food]):
    """
    Delete all vectors in nutrition_vectors and insert new vectors
    """
    for food in foods:
        food_dict = food.__dict__
        food_id = food_dict.pop("id")
        v_cleaned = clean_nutrition_vector(food_dict)
        v_weighted = add_vector_weights(v_cleaned)
        v_normalized = normalize_vector(v_weighted)
        insert_vector(food_id, v_normalized)


# NOTE: Right now, by running this file, we delete all the vectors in the db and reinsert everything
def main():
    delete_all_vectors()
    foods = get_all_foods()
    insert_all_vectors(foods)


if __name__ == "__main__":
    main()
