# -------------------- Imports --------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
import json, os


# -------------------- App Initialization --------------------

# Create FastAPI app instance
app = FastAPI()

# JSON file where all patient data will be stored
DATA_FILE = "patient.json"


# -------------------- Data Models --------------------

# Model for creating a new patient (all fields required)
class Patient(BaseModel):
    ID: str
    name: str
    city: str
    age: int
    gender: Literal["Male", "Female", "Other"]
    height: float
    weight: float


# Model for updating patient (all fields optional)
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    height: Optional[float] = None
    weight: Optional[float] = None


# -------------------- Helper Functions --------------------

# Load patient data from JSON file
def load_data():

    # If file does not exist, return empty dictionary
    # os.path.exists() is a Python function that checks whether a file or folder exists on your computer.
    # It returns: True → if the file/folder exists, False → if the file/folder does not exist
    
    if not os.path.exists(DATA_FILE): # if not in our directory we will return an empty dictionary  
        return {}

    # Open and read JSON file
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# Save patient data into JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------- API Routes --------------------

# Home route to check if API is running
@app.get("/")
def home():
    return {"message": "API is working successfully 🚀"}


# Create a new patient
@app.post("/create")
def create_patient(patient: Patient):

    # Load existing data
    data = load_data()

    # Check if patient already exists
    if patient.ID in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Store patient data using ID as key (ID not duplicated inside object)
    data[patient.ID] = patient.model_dump(exclude={"ID"})

    # Save updated data
    save_data(data)

    return {"message": "Patient created successfully ✅"}


# Update existing patient
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    # Load existing data
    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get existing patient info
    patient_data = data[patient_id]

    # Extract only fields that client sent
    updates = patient_update.model_dump(exclude_unset=True)

    # Update only provided fields
    for key, value in updates.items():
        patient_data[key] = value

    # Save updated patient info
    data[patient_id] = patient_data
    save_data(data)

    return {"message": "Patient updated successfully ✅"}
