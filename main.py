import requests
from datetime import datetime
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()

configure()


APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

GENDER = "Male"
WEIGHT_KG = "70"
HEIGHT = "171"
AGE = "25"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/7aa2509ebf263a1b684ac30d5a6fd4b4/myWorkouts/workouts"

exercise_input = input("Tell me which exercise you did today? ")

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=header)
result = response.json()

# # Updating to Sheety

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer",
}

for exercise in result["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Sheety Authentication: Basic Auth
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_input,
        auth=(
            os.getenv("USERNAME"),
            os.getenv("PASSWORD")
        )
    )

    print(f"Sheety Response: \n {sheet_response.text}")
