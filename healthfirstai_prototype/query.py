import numpy as np
import json

if __name__ == "__main__":
    from database import SessionLocal
    from my_types import Food
else:
    from healthfirstai_prototype.database import SessionLocal
    from healthfirstai_prototype.my_types import Food

session = SessionLocal()


def get_vector_from_id(food_id: int):
    """
    Get the vector from the database
    """
    food_query = (
        session.query(
            Food.ID,
            Food.Name,
            Food.Food_Group,
            Food.Fat_g,
            Food.Protein_g,
            Food.Carbohydrate_g,
            Food.Sugars_g,
            Food.Fiber_g,
            Food.Cholesterol_mg,
            Food.Saturated_Fats_g,
            Food.Calcium_mg,
            Food.Iron_Fe_mg,
            Food.Potassium_K_mg,
            Food.Magnesium_mg,
            Food.Vitamin_A_IU_IU,
            Food.Vitamin_A_RAE_mcg,
            Food.Vitamin_C_mg,
            Food.Vitamin_B_12_mcg,
            Food.Vitamin_D_mcg,
            Food.Vitamin_E_Alpha_Tocopherol_mg,
            Food.Added_Sugar_g,
            Food.Net_Carbs_g,
            Food.Water_g,
            Food.Omega_3s_mg,
            Food.Omega_6s_mg,
            Food.PRAL_score,
            Food.Trans_Fatty_Acids_g,
            Food.Soluble_Fiber_g,
            Food.Insoluble_Fiber_g,
            Food.Sucrose_g,
            Food.Glucose_Dextrose_g,
            Food.Fructose_g,
            Food.Lactose_g,
            Food.Maltose_g,
            Food.Galactose_g,
            Food.Starch_g,
            Food.Total_sugar_alcohols_g,
            Food.Phosphorus_P_mg,
            Food.Sodium_mg,
            Food.Zinc_Zn_mg,
            Food.Copper_Cu_mg,
            Food.Manganese_mg,
            Food.Selenium_Se_mcg,
            Food.Fluoride_F_mcg,
            Food.Molybdenum_mcg,
            Food.Chlorine_mg,
            Food.Thiamin_B1_mg,
            Food.Riboflavin_B2_mg,
            Food.Niacin_B3_mg,
            Food.Pantothenic_acid_B5_mg,
            Food.Vitamin_B6_mg,
            Food.Biotin_B7_mcg,
            Food.Folate_B9_mcg,
            Food.Folic_acid_mcg,
            Food.Food_Folate_mcg,
            Food.Folate_DFE_mcg,
            Food.Choline_mg,
            Food.Betaine_mg,
            Food.Retinol_mcg,
            Food.Carotene_beta_mcg,
            Food.Carotene_alpha_mcg,
            Food.Lycopene_mcg,
            Food.Lutein_Zeaxanthin_mcg,
            Food.Vitamin_D2_ergocalciferol_mcg,
            Food.Vitamin_D3_cholecalciferol_mcg,
            Food.Vitamin_D_IU_IU,
            Food.Vitamin_K_mcg,
            Food.Dihydrophylloquinone_mcg,
            Food.Menaquinone_4_mcg,
            Food.Fatty_acids_total_monounsaturated_mg,
            Food.Fatty_acids_total_polyunsaturated_mg,
            Food.ccc_ALA_mg,
            Food.EPA_mg,
            Food.DPA_mg,
            Food.DHA_mg,
            Food.Tryptophan_mg,
            Food.Threonine_mg,
            Food.Isoleucine_mg,
            Food.Leucine_mg,
            Food.Lysine_mg,
            Food.Methionine_mg,
            Food.Cystine_mg,
            Food.Phenylalanine_mg,
            Food.Tyrosine_mg,
            Food.Valine_mg,
            Food.Arginine_mg,
            Food.Histidine_mg,
            Food.Alanine_mg,
            Food.Aspartic_acid_mg,
            Food.Glutamic_acid_mg,
            Food.Glycine_mg,
            Food.Proline_mg,
            Food.Serine_mg,
            Food.Hydroxyproline_mg,
            Food.Alcohol_g,
            Food.Caffeine_mg,
            Food.Theobromine_mg,
            Food.Serving_Weight_1_g,
            Food.Serving_Description_1_g,
            Food.Serving_Weight_2_g,
            Food.Serving_Description_2_g,
            Food.Serving_Weight_3_g,
            Food.Serving_Description_3_g,
            Food.Serving_Weight_4_g,
            Food.Serving_Description_4_g,
            Food.Serving_Weight_5_g,
            Food.Serving_Description_5_g,
            Food.Serving_Weight_6_g,
            Food.Serving_Description_6_g,
            Food.Serving_Weight_7_g,
            Food.Serving_Description_7_g,
            Food.Serving_Weight_8_g,
            Food.Serving_Description_8_g,
            Food.Serving_Weight_9_g,
            Food.Serving_Description_9_g,
        )
        .filter(Food.ID == food_id)
        .first()
    )
    session.close()
    return None if food_query is None else np.array(food_query[3:])


def get_food_vector() -> list[tuple[int, str, str, np.ndarray]]:
    """
    Returns a dictionary of food vectors from the database.
    """
    food_query = session.query(
        Food.ID,
        Food.Name,
        Food.Food_Group,
        Food.Fat_g,
        Food.Protein_g,
        Food.Carbohydrate_g,
        Food.Sugars_g,
        Food.Fiber_g,
        Food.Cholesterol_mg,
        Food.Saturated_Fats_g,
        Food.Calcium_mg,
        Food.Iron_Fe_mg,
        Food.Potassium_K_mg,
        Food.Magnesium_mg,
        Food.Vitamin_A_IU_IU,
        Food.Vitamin_A_RAE_mcg,
        Food.Vitamin_C_mg,
        Food.Vitamin_B_12_mcg,
        Food.Vitamin_D_mcg,
        Food.Vitamin_E_Alpha_Tocopherol_mg,
        Food.Added_Sugar_g,
        Food.Net_Carbs_g,
        Food.Water_g,
        Food.Omega_3s_mg,
        Food.Omega_6s_mg,
        Food.PRAL_score,
        Food.Trans_Fatty_Acids_g,
        Food.Soluble_Fiber_g,
        Food.Insoluble_Fiber_g,
        Food.Sucrose_g,
        Food.Glucose_Dextrose_g,
        Food.Fructose_g,
        Food.Lactose_g,
        Food.Maltose_g,
        Food.Galactose_g,
        Food.Starch_g,
        Food.Total_sugar_alcohols_g,
        Food.Phosphorus_P_mg,
        Food.Sodium_mg,
        Food.Zinc_Zn_mg,
        Food.Copper_Cu_mg,
        Food.Manganese_mg,
        Food.Selenium_Se_mcg,
        Food.Fluoride_F_mcg,
        Food.Molybdenum_mcg,
        Food.Chlorine_mg,
        Food.Thiamin_B1_mg,
        Food.Riboflavin_B2_mg,
        Food.Niacin_B3_mg,
        Food.Pantothenic_acid_B5_mg,
        Food.Vitamin_B6_mg,
        Food.Biotin_B7_mcg,
        Food.Folate_B9_mcg,
        Food.Folic_acid_mcg,
        Food.Food_Folate_mcg,
        Food.Folate_DFE_mcg,
        Food.Choline_mg,
        Food.Betaine_mg,
        Food.Retinol_mcg,
        Food.Carotene_beta_mcg,
        Food.Carotene_alpha_mcg,
        Food.Lycopene_mcg,
        Food.Lutein_Zeaxanthin_mcg,
        Food.Vitamin_D2_ergocalciferol_mcg,
        Food.Vitamin_D3_cholecalciferol_mcg,
        Food.Vitamin_D_IU_IU,
        Food.Vitamin_K_mcg,
        Food.Dihydrophylloquinone_mcg,
        Food.Menaquinone_4_mcg,
        Food.Fatty_acids_total_monounsaturated_mg,
        Food.Fatty_acids_total_polyunsaturated_mg,
        Food.ccc_ALA_mg,
        Food.EPA_mg,
        Food.DPA_mg,
        Food.DHA_mg,
        Food.Tryptophan_mg,
        Food.Threonine_mg,
        Food.Isoleucine_mg,
        Food.Leucine_mg,
        Food.Lysine_mg,
        Food.Methionine_mg,
        Food.Cystine_mg,
        Food.Phenylalanine_mg,
        Food.Tyrosine_mg,
        Food.Valine_mg,
        Food.Arginine_mg,
        Food.Histidine_mg,
        Food.Alanine_mg,
        Food.Aspartic_acid_mg,
        Food.Glutamic_acid_mg,
        Food.Glycine_mg,
        Food.Proline_mg,
        Food.Serine_mg,
        Food.Hydroxyproline_mg,
        Food.Alcohol_g,
        Food.Caffeine_mg,
        Food.Theobromine_mg,
        Food.Serving_Weight_1_g,
        Food.Serving_Description_1_g,
        Food.Serving_Weight_2_g,
        Food.Serving_Description_2_g,
        Food.Serving_Weight_3_g,
        Food.Serving_Description_3_g,
        Food.Serving_Weight_4_g,
        Food.Serving_Description_4_g,
        Food.Serving_Weight_5_g,
        Food.Serving_Description_5_g,
        Food.Serving_Weight_6_g,
        Food.Serving_Description_6_g,
        Food.Serving_Weight_7_g,
        Food.Serving_Description_7_g,
        Food.Serving_Weight_8_g,
        Food.Serving_Description_8_g,
        Food.Serving_Weight_9_g,
        Food.Serving_Description_9_g,
    ).all()

    food_query = [(food[0], food[1], food[2], food[3:]) for food in food_query]
    # replace all None values with 0
    food_query = [
        (food[0], food[1], food[2], [0.0 if i is None else i for i in food[3]])
        for food in food_query
    ]

    # Don't forget to close the session when you're done
    session.close()
    return food_query


if __name__ == "__main__":
    vectors = get_food_vector()
    target = get_vector_from_id(167755)

    def cosine_similarity(vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    # Convert vectors to numpy arrays
    target_vector = np.array(target)
    vectors = [np.array(vec[2]) for vec in vectors]

    # Initialize variables to keep track of the most similar vector and its similarity
    most_similar_vector = None
    highest_similarity = -1  # Cosine similarity ranges from -1 to 1

    # Loop over all vectors in the list
    for vector in vectors:
        similarity = cosine_similarity(target_vector, vector)
        if similarity > highest_similarity:
            most_similar_vector = vector
            highest_similarity = similarity

    print("The most similar vector is:", most_similar_vector)
    print("With a cosine similarity of:", highest_similarity)
