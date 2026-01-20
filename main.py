from fastapi import FastAPI, Path, HTTPException
# FastAPI -> to create the API
# Path -> to validate path parameters

import json
# to handle json data

app = FastAPI()

# function to load dat afrom json : helper function 
def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def hello(): 
    return {"message": "Patient management System API"}

@app.get("/about")
def about():
    return {"message": "Fully functional patient management system API."} 

@app.get("/view")
def view():
    data = load_data() # fetching the data using helper [load_data] function
    return data


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")): 
    # here ... means that this parameter is required
    # load all the patient data
    data = load_data()
    
    # filter the data based on patient_id
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")
