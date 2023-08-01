import streamlit as st
import time

# TODO: Refactor this so that these functions are in the controller folder
from healthfirstai_prototype.agents.toolkits.diet_plan.utils import (
    get_user_meal_plans_as_json,
)
from healthfirstai_prototype.agents.toolkits.exercise_plan.utils import (
    get_cached_schedule_json,
)
import json

from healthfirstai_prototype.enums.exercise_enums import DaysOfTheWeek

st.set_page_config(
    page_title="Diet Plan",
    page_icon="❤️",
)

# TODO: Paramaratize this to get the user name
user_name = "Lawrence"
st.title("Today's Workout Plan")


def count_down(ts):
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = "{:02d}:{:02d}".format(mins, secs)
            st.header(f"{time_now}")
            time.sleep(1)
            ts -= 1


st.write("## Workout Timer")
time_minutes = st.number_input("Enter the time in minutes and seconds", 0, 60, 1)
time_in_seconds = time_minutes * 60
if st.button("START"):
    count_down(time_in_seconds)


# TODO: Paramaratize get_user_meal_plans_as_json call in the future
user_meal_plan = json.loads(get_cached_schedule_json(1, True, DaysOfTheWeek.today))

markdown_string_to_display = ""
workout_name = user_meal_plan["workout_name"]

exercise_list = user_meal_plan["exercises"]

st.write(f"### {workout_name}")
st.write(user_meal_plan["workout_description"])

for exercise_info in exercise_list:
    markdown_string_to_display += f"### {exercise_info['name']}\n"
    markdown_string_to_display += "| Reps | Sets |\n"
    markdown_string_to_display += "| --- | --- |\n"
    markdown_string_to_display += f"| {exercise_info['reps']} | {exercise_info['sets']} |\n"

st.markdown(markdown_string_to_display)
