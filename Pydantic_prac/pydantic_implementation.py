from pydantic import BaseModel
from typing import List, Dict, Optional

# Step - 1 : build a pydantic model for patient data [we will create the sche of our data over here]
class Patient(BaseModel): 
    name: str
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None # allergies khud me list hoga but uska har element str hoga
    contact_details: Dict[str, str] # contact detail me dictionary hoga jisme key str hogi and value bhi str hogi

# Step - 2 : create an object of the class 
def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n  age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

def update_patient_data(patient: Patient):
    print(f"name : {patient.name} \n  age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data updated successfully")

# Example for non optional field 
patient_info = {'name': "Beast", 'age': 24, 'weight': 70.5, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

# Example for optional field where we have removed allergies
# patient_info = {'name': "Beast", 'age': 24, 'weight': 70.5, 'married': False, 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

patient1 = Patient(**patient_info)  # unpacking the dictionary to match the model fields

insert_patient_data(patient1)
update_patient_data(patient1)