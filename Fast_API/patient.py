from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json
import os

app = FastAPI()

# ---------------- Patient Model ---------------- #

class Patient(BaseModel):
    ID: Annotated[str, Field(..., description="ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="City where the patient is living", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in cm")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    # BMI Calculation (convert cm → meters)
    @computed_field
    @property
    def bmi(self) -> float:
        height_in_m = self.height / 100
        return round(self.weight / (height_in_m ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


# ---------------- Helper Functions ---------------- #

DATA_FILE = "patient.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}   # if file not exists, return empty dict

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4) 
        # what it means -> indent=4 -> indentation of 4 spaces, for better readability


# ---------------- Routes ---------------- #

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "Fully functional patient management system API."}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient ID", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by height, weight or bmi"),
    order: str = Query("asc", description="asc or desc")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Must be one of {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")

    data = load_data()
    reverse = True if order == "desc" else False

    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=reverse)
    return {"sorted_patients": sorted_data}


# ---------------- Create Patient ---------------- #

@app.post("/create", status_code=201)
def create_patient(patient: Patient):

    data = load_data()

    # Use patient.ID (not patient.id)
    if patient.ID in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Save patient (exclude ID inside object because ID is key)
    data[patient.ID] = patient.model_dump(exclude=["ID"])

    save_data(data)

    return {"message": "Patient created successfully"}
