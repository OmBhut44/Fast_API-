# What is data validation in pydantic?
# -> Data validation in Pydantic is the process of ensuring that the data being modeled adheres to specified types and constraints.
# Pydantic automatically validates the data when creating model instances, ensuring that the data is of the correct type and format.
# Example: Ensuring email is in valid format, age is an integer, weight is a float, or the url of your linkedin profile is valid etc.


from pydantic import BaseModel, EmailStr, AnyUrl

# build-in custom data types: EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel): 
    name: str
    email: EmailStr
    linkedin : AnyUrl
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None 
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