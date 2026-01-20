from pydantic import BaseModel, EmailStr, AnyUrl, Field

# build-in custom data types: EmailStr, AnyUrl
from typing import Annotated, List, Dict, Optional, Annotated

class Patient(BaseModel): 
    name: str
    email: EmailStr
    linkedin : AnyUrl
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 120", examples=[25, 30, 45])]

    # here strict=True ensures that only float values are accepted, not strings that can be converted to float
    weight: Annotated[float, Field(..., gt=0, strict=True, description="Weight must be a positive number")]
    married: bool
    allergies: Optional[List[str]] = Field(max_length=5, default=None, description="Maximum of 5 allergies allowed")
    contact_details: Dict[str, str] 


def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n linkedin: {patient.linkedin} \n age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

def update_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n linkedin: {patient.linkedin} \n age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data updated successfully")

patient_info = {'name': "Beast", 'email': "beast@gmail.com", 'linkedin': "https://www.linkedin.com/in/beast", 'age': 24, 'weight': 70.5, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

patient1 = Patient(**patient_info)  

insert_patient_data(patient1)
update_patient_data(patient1)