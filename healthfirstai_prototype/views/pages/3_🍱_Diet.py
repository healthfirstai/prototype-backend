import streamlit as st
# TODO: Refactor this so that these functions are in the controller folder
from healthfirstai_prototype.agents.toolkits.diet_plan.utils import get_user_meal_plans_as_json
import json

st.set_page_config(
    page_title="Diet Plan",
    page_icon="❤️",
)

# TODO: Paramaratize this to get the user name
user_name = "Lawrence"
st.write("# Today's Diet Plan")


# TODO: Paramaratize get_user_meal_plans_as_json call in the future
user_meal_plan = json.loads(get_user_meal_plans_as_json(1, True))

meal_names = ["Breakfast", "Drink", "Lunch", "Snack", "Dinner"]
markdown_string_to_display = ""

calories_text = ":black[Calories: 2500/3000]"
carbs_text = ":black[Carbohydrates: 250g/300g]"
protein_text = ":black[Protein: 250g/300g]"
fat_text = ":black[Fat: 250g/300g]"

# TODO: Update this to be dynamic depending on the user's diet plan
calories_consumed_percent = 0.5
carbs_consumed_percent = 0.8
protein_consumed_percent = 0.6
fat_consumed_percent = 0.2

calories_progress_bar = st.progress(carbs_consumed_percent, text=calories_text)
carbs_progress_bar = st.progress(carbs_consumed_percent, text=carbs_text)
protein_progress_bar = st.progress(protein_consumed_percent, text=protein_text)
fat_progress_bar = st.progress(fat_consumed_percent, text=fat_text)

for key in meal_names:
    markdown_string_to_display += f"### {key} - {user_meal_plan[key]['description']}\n"
    markdown_string_to_display += "#### Ingredients\n"
    markdown_string_to_display += "| Food Name | Quantity |\n"
    markdown_string_to_display += "| --- | --- |\n"
    for ingredient in user_meal_plan[key]["ingredients"]:
        markdown_string_to_display += f"{ingredient['food_name']} | {ingredient['quantity']} {ingredient['unit_of_measurement']}\n"

    # markdown_string_to_display += "#### Nutrition\n"
    # markdown_string_to_display += f"Calories: {user_meal_plan[key]['calories']}\n"
    # markdown_string_to_display += f"Protein: {user_meal_plan[key]['protein']}\n"
    # markdown_string_to_display += f"Carbs: {user_meal_plan[key]['carbs']}\n"
    # markdown_string_to_display += f"Fat: {user_meal_plan[key]['fat']}\n"

st.markdown(markdown_string_to_display)
