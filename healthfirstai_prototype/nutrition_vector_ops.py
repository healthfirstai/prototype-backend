"""Nutrition Vector Operations

This module includes functions for extracting, cleaning, normalizing, and weighting
nutrition vectors. It also interacts with the database to get food information and 
store the processed nutrition vectors.

"""
import numpy as np
from numpy.typing import NDArray

from healthfirstai_prototype.database import SessionLocal
from healthfirstai_prototype.data_models import Food, NutritionVector


def get_all_foods() -> list[Food]:
    """
    Returns all foods in the food table

    Returns:
        List of Food objects
    """
    session = SessionLocal()
    output = session.query(Food).all()
    session.close()
    return output


def clean_micronutrients(food_dict: dict) -> list[tuple[str, float]]:
    """
    Extracts the micro nutrients from the Food table dictionary
    Cleans the micro nutrients by replacing all None values with 0.0

    Args:
        food_dict: The dictionary with nutrition information.

    Returns:
        A list of tuples with the micro nutrient values.
    """
    return [(k, 0.0) if v is None else (k, float(v)) for k, v in food_dict.items()]


def get_micronutrients(cleaned_micro_tuples: list[tuple[str, float]]) -> list[float]:
    """
    Extracts and sorts the micro nutrients from the cleaned micro nutrient tuples.

    Args:
        cleaned_micro_tuples: A list of tuples with the micro nutrient names and float values.

    Returns:
        A sorted list of micro nutrient values.
    """
    return [v for _, v in sorted(cleaned_micro_tuples, key=lambda x: x[0])]


def get_macronutrients(food_dict: dict) -> list[float]:
    """
    Extracts the macronutrients from the food dictionary from the Food table

    Args:
        food_dict: The food dictionary from the Food table

    Returns:
        A list of the macronutrients
    """
    return [
        food_dict.pop("Calories"),
        food_dict.pop("Protein_g"),
        food_dict.pop("Carbohydrate_g"),
        food_dict.pop("Fat_g"),
    ]


def remove_unwanted_keys(food_dict: dict) -> dict:
    """
    Removes the unwanted keys from the given food dictionary.

    Args:
        food_dict (dict): The dictionary to be cleaned.

    Returns:
        dict: A cleaned dictionary with only relevant keys.
    """
    unwanted_keys = {"_sa_instance_state", "Food_Group", "Name"}
    for key in unwanted_keys:
        food_dict.pop(key, None)

    food_dict = {k: v for k, v in food_dict.items() if "Serving" not in k}

    return food_dict


def clean_nutrition_vector(food_dict: dict) -> NDArray:
    """
    Cleans the nutrition vector by removing all non-numerical information
    This should be run when we need to update the nutrition vectors

    Args:
        food_dict: The food dictionary from the Food table

    Returns:
        A cleaned nutrition vector as a numpy array
    """
    food_dict = remove_unwanted_keys(food_dict)
    macronutrients = get_macronutrients(food_dict)
    cleaned_micro_tuples = clean_micronutrients(food_dict)
    macronutrients = get_micronutrients(cleaned_micro_tuples)
    return np.array(macronutrients + macronutrients)


def insert_vector(food_id: int, vector: NDArray) -> None:
    """
    Inserts a nutrition vector into the nutrition_vector table

    Args:
        food_id: The food id of the food
        vector: The nutrition vector as a numpy array
    """
    session = SessionLocal()
    vector = np.nan_to_num(vector)  # Replace all nan values with 0
    item = NutritionVector(food_id=food_id, embedding=vector.tolist())
    session.add(item)
    session.commit()
    session.close()


def normalize_vector(vector: NDArray) -> NDArray:
    """
    Calculates the magnitude of the vector and divides each element by the magnitude

    Args:
        vector: The nutrition vector to be normalized

    Returns:
        The normalized nutrition vector
    """
    magnitude = np.linalg.norm(vector)  # Calculate the magnitude of the vector
    return vector / magnitude  # Divide each element by the magnitude to normalize


def add_vector_weights(v_normalized: NDArray) -> NDArray:
    """
    Adds weights to the nutrition vector to account for macro/micronutrient importance

    Args:
        v_normalized: The normalized nutrition vector

    Returns:
        The weighted nutrition vector

    TODO:
        * Change the weights based on the food group and user's goal

    NOTE:
        * For fruits and vegetables, you should pay more attention to the micronutrients if your goal is to get healthy
        * For meats, you should pay more attention to the macronutrients if your goal is to gain muscle for example
        * The weights are currently all 1
    """
    weights = np.ones_like(v_normalized)
    # weights = np.zeros_like(v_normalized) # This is for testing
    # Weights for macronutrients
    weights[0] = 100  # Calories
    weights[1] = 100  # Protein
    weights[2] = 100  # Carbohydrates
    weights[3] = 100  # Fat
    return v_normalized * weights  # Multiply the normalized vector by the weights


def delete_all_vectors() -> None:
    """
    Deletes all vectors from the nutrition_vector table
    """
    session = SessionLocal()
    session.query(NutritionVector).delete()
    session.commit()
    session.close()


def insert_all_vectors(foods: list[Food]) -> None:
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
