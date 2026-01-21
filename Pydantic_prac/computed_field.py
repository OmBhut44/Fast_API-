# what is computed field in pydantic
# -> A computed field is a field that is not directly set by the user but is derived from other fields in the model.
# Example : BMI = weight / (height ** 2)

from pydantic import BaseModel, EmailStr, computed_field

from typing import List, Dict

class Patient(BaseModel): 
    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str] 

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight / (self.height**2), 2)  # height in cm converted to meters
        return bmi

    
def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n age : {patient.age} \n  weight : {patient.weight} \n  height : {patient.height} \n bmi : {patient.bmi} \n married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

patient_info = {'name': "BEAST", 'email': "beast@gmail.com", 'age': 21, 'weight': 74.5, 'height': 1.75, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

patient1 = Patient(**patient_info)  

insert_patient_data(patient1)

