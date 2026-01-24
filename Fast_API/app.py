# -------------------- Imports --------------------

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd


# -------------------- City Tier Data --------------------
# These lists are used to determine the city tier of the user

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam",
    "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur",
    "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur",
    "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur",
    "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode",
    "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur",
    "Asansol", "Siliguri"
]


# -------------------- Load ML Model --------------------
# Load trained ML model once when server starts
# rb = read binary mode

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


# -------------------- App Initialization --------------------

# Create FastAPI application instance
app = FastAPI()


# -------------------- Input Validation Model --------------------
# This model validates incoming JSON data from the user

class UserInput(BaseModel):

    # User's age (must be between 1 and 120)
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]

    # User's weight in kilograms
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user in kg")]

    # User's height in meters (IMPORTANT: used in BMI formula)
    height: Annotated[float, Field(..., gt=0, description="Height of the user in meters")]

    # User's annual income in LPA
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual income in LPA")]

    # Whether the user smokes or not
    smoker: Annotated[bool, Field(..., description="Is the user a smoker")]

    # City name of the user
    city: Annotated[str, Field(..., description="City of the user")]

    # User occupation (only allowed values)
    occupation: Literal[
        "retired", "freelancer", "student", "government_job",
        "business_owner", "unemployed", "private_job"
    ]

    # -------------------- Computed Fields --------------------

    # BMI is computed automatically from height & weight
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Lifestyle risk depends on smoking and BMI
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    # Age group is derived from age
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    # City tier is determined using predefined city lists
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


# -------------------- Prediction API --------------------

@app.post("/predict")
def predict_premium(data: UserInput):
    """
    Steps:
    1. Receive validated user input
    2. Convert computed fields into a pandas DataFrame
    3. Pass DataFrame to ML model
    4. Return predicted insurance category
    """

    # Convert user data into DataFrame (model expects DataFrame input)
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }]) 

    # Predict using trained ML model
    prediction = model.predict(input_df)[0]

    # Return prediction as JSON response
    return JSONResponse(
        status_code=200,
        content={"predicted_category": str(prediction)}
    )
