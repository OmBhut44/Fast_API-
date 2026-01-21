from pydantic import BaseModel, EmailStr

from typing import List, Dict

class Patient(BaseModel): 
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] 


    
def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n age : {patient.age} \n  weight : {patient.weight} \n  height : {patient.height} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

patient_info = {'name': "BEAST", 'email': "beast@gmail.com", 'age': 90, 'weight': 70.5, 'height': 175.0, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

patient1 = Patient(**patient_info)  

insert_patient_data(patient1)
