import streamlit as st
import openai
import requests
import faiss
import numpy as np
from dotenv import load_dotenv
import os
from database.user_database import UserDatabase
from faiss_storage.faiss_helper import FaissHelper

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"
openai.api_key = OPENAI_API_KEY


def ask_diet_plan_questions():
    age = st.number_input("What is your age?", min_value=1, step=1)
    gender = st.selectbox("What is your gender?", ["Male", "Female", "Non-Binary", "Prefer not to say"])
    height = st.number_input("What is your height (in cm)?", min_value=1, step=1)
    current_weight = st.number_input("What is your current weight (in kg)?", min_value=1, step=1)
    target_weight = st.number_input("What is your target weight (in kg)?", min_value=1, step=1)

    activity_level = st.selectbox("How would you describe your daily activity level?", [
        "Sedentary", "Light Activity", "Moderate Activity", "Heavy Activity"
    ])

    dietary_restrictions = st.multiselect("Do you have any dietary restrictions or preferences?", [
        "Vegetarian", "Vegan", "Gluten-Free", "Lactose Intolerant", "Other"
    ])

    allergies = st.text_input("Do you have any allergies or specific food intolerances?")

    health_goals = st.multiselect("Are there any specific health goals you're trying to achieve?", [
        "Muscle Building", "Fat Loss", "Maintaining Weight", "Improving Overall Health", "Other"
    ])

    meals_per_day = st.number_input("How many meals do you prefer to eat per day?", min_value=1, step=1)
    snacks_per_day = st.number_input("How many snacks do you prefer to eat per day?", min_value=0, step=1)

    meal_plan_preference = st.selectbox("Do you prefer a structured meal plan, or a more flexible approach?", [
        "Structured Meal Plan", "Flexible Approach"
    ])

    favorite_ingredients = st.text_input("Are there any specific foods or ingredients that you particularly enjoy?")
    least_favorite_ingredients = st.text_input("Are there any specific foods or ingredients that you particularly dislike?")
    user_input = {
            'age': age,
            'gender': gender,
            'height': height,
            'current_weight': current_weight,
            'target_weight': target_weight,
            'activity_level': activity_level,
            'dietary_restrictions': dietary_restrictions,
            'allergies': allergies,
            'health_goals': health_goals,
            'meals_per_day': meals_per_day,
            'snacks_per_day': snacks_per_day,
            'meal_plan_preference': meal_plan_preference,
            'favorite_ingredients': favorite_ingredients,
            'least_favorite_ingredients': least_favorite_ingredients
        }
    return user_input


def generate_diet_plan(user_input):
    prompt = (
        f"Create a personalized diet plan for a {user_input['age']} year old "
        f"{user_input['gender']} with the following information:\n"
        f"- Height: {user_input['height']} cm\n"
        f"- Current weight: {user_input['current_weight']} kg\n"
        f"- Target weight: {user_input['target_weight']} kg\n"
        f"- Activity level: {user_input['activity_level']}\n"
        f"- Dietary restrictions: {', '.join(user_input['dietary_restrictions'])}\n"
        f"- Allergies: {user_input['allergies']}\n"
        f"- Health goals: {', '.join(user_input['health_goals'])}\n"
        f"- Meals per day: {user_input['meals_per_day']}\n"
        f"- Snacks per day: {user_input['snacks_per_day']}\n"
        f"- Meal plan preference: {user_input['meal_plan_preference']}\n"
        f"- Favorite ingredients: {user_input['favorite_ingredients']}\n"
        f"- Least favorite ingredients: {user_input['least_favorite_ingredients']}\n\n"
        "Please provide a 1-day diet plan with meal and snack suggestions."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    diet_plan = response.choices[0].text.strip()
    return diet_plan

# def store_diet_plan_to_vector_db(user_diet_plan):
#     username, diet_plan = user_diet_plan

#     # Convert the diet plan text into a vector using the OpenAI API
#     response = openai.Embedding.create(
#         model="text-embedding-ada-002",
#         input=diet_plan
#         )

#     # Extract the embeddings from the response
#     embeddings = response['data'][0]['embedding']
#     vector = np.array(embeddings, dtype=np.float32).reshape(1, -1)

#      # Save the Faiss index to disk
#     faiss_helper = FaissHelper(dim=vector.shape[1])
#     faiss_helper.store_vector(username, vector)

def store_diet_plan_to_vector_db(user_diet_plan):
    # Convert the diet plan text into a vector using the OpenAI API
    username, diet_plan = user_diet_plan
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=diet_plan
        )

    # Extract the embeddings from the response
    embeddings = response['data'][0]['embedding']
    vector = np.array(embeddings, dtype=np.float32).reshape(1, -1)

    # Save the Faiss index to disk
    faiss_helper = FaissHelper()
    faiss_helper.store_vector(username, vector)
