# What is model validator in pydantic?
# -> A model validator is a method that allows you to define validation logic that applies to the entire model rather than individual fields.
# This enables you to enforce constraints that depend on multiple fields or the overall state of the model.
# Example: Ensuring that if age is greater than 60, then an emergency contact must be provided in the contact details.



from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator

from typing import Annotated, List, Dict, Optional, Annotated

class Patient(BaseModel): 
    name: str
    email: EmailStr
    linkedin : AnyUrl
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] 

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patients older tan 60 must have an emergency contact in their contact details.")
        return model

    
def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n linkedin: {patient.linkedin} \n age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

patient_info = {'name': "BEAST", 'email': "beast@gmail.com", 'linkedin': "https://www.linkedin.com/in/beast", 'age': 90, 'weight': 70.5, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com', 'emergency': '987-654-3210'}}

patient1 = Patient(**patient_info)  

insert_patient_data(patient1)
