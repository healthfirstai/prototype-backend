"""Utility Functions Used by Chat Agent

This module contains utility functions used by the chat agent. These functions
May be used inside the chat agent toolkits

"""
from .toolkits.diet_plan.utils import get_user_info_for_json_agent


# TODO: This is a duplicated function. In the future, refactor and remove the other one in utils.py
def get_user_info(user_id: int):
    """
    Given a user ID, query the database and return the user's information.
    """
    return get_user_info_for_json_agent(user_id)
