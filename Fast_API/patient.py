# -------------------- Imports --------------------

# FastAPI framework and exception handling
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Pydantic is used for request validation
from pydantic import BaseModel

# Used for optional fields and fixed values
from typing import Optional, Literal

# Used to work with JSON files and file system
import json
import os


# -------------------- App Initialization --------------------

# Create FastAPI application instance
app = FastAPI()

# Name of the JSON file where patient data is stored
DATA_FILE = "patient.json"


# -------------------- Data Models --------------------

# Patient model for CREATE operation
# All fields are REQUIRED when creating a patient
class Patient(BaseModel):
    ID: str                  # Unique patient ID
    name: str                # Patient name
    city: str                # Patient city
    age: int                 # Patient age
    gender: Literal["Male", "Female", "Other"]  # Allowed gender values
    height: float            # Height in cm
    weight: float            # Weight in kg


# Patient model for UPDATE operation
# All fields are OPTIONAL because client may update only a few fields
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    height: Optional[float] = None
    weight: Optional[float] = None


# -------------------- Helper Functions --------------------

def load_data():
    """
    Loads patient data from the JSON file.

    - If the file does not exist, return an empty dictionary.
    - If the file exists but is empty or corrupted, return an empty dictionary.
    - This prevents the API from crashing (500 Internal Server Error).
    """

    # Check whether the file exists in the project directory
    if not os.path.exists(DATA_FILE):
        return {}  # No file → no patients yet

    try:
        # Open file and convert JSON into Python dictionary
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        # Handles case where file is empty or invalid JSON
        return {}


def save_data(data):
    """
    Saves patient data into the JSON file.
    indent=4 is used to make the file readable for humans.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------- API Routes --------------------

# Simple route to check if API is running
@app.get("/")
def home():
    return {"message": "API is working successfully 🚀"}


# -------------------- Create Patient --------------------

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    """
    Creates a new patient.
    - Patient ID is used as the unique key.
    - Patient ID is NOT duplicated inside the JSON object.
    """

    # Load existing patients
    data = load_data()

    # Check if patient ID already exists
    if patient.ID in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Store patient data (excluding ID because ID is used as key)
    data[patient.ID] = patient.model_dump(exclude={"ID"})

    # Save updated data to file
    save_data(data)

    return {"message": "Patient created successfully ✅"}


# -------------------- Update Patient --------------------

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Updates an existing patient.
    - Only fields sent by the client are updated.
    - Other fields remain unchanged.
    """

    # Load existing data
    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get existing patient information
    patient_data = data[patient_id]

    # Extract only the fields provided by client
    updates = patient_update.model_dump(exclude_unset=True)

    # Update only those fields
    for key, value in updates.items():
        patient_data[key] = value

    # Save updated patient data
    data[patient_id] = patient_data
    save_data(data)

    return {"message": "Patient updated successfully ✅"}


# -------------------- Delete Patient --------------------

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    """
    Deletes a patient using patient ID.
    """

    # Load existing data
    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Remove patient from dictionary
    del data[patient_id]

    # Save updated data
    save_data(data)

    # Correct usage: status_code (NOT status)
    return JSONResponse(
        status_code=200,
        content={"message": "Patient deleted successfully ✅"}
    )
