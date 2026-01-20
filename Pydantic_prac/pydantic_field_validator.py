from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator

# build-in custom data types: EmailStr, AnyUrl
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

    # email validator -> only allow specific domains
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain '{domain_name}' is not allowed. Allowed domains are: {', '.join(valid_domains)}")
        return value
    
    # name validator -> capitalize first letter of the name
    @field_validator('name')
    @classmethod
    def name_validator(cls, value): 
        return value.title()
    
def insert_patient_data(patient: Patient):
    print(f"name : {patient.name} \n email: {patient.email} \n linkedin: {patient.linkedin} \n age : {patient.age} \n  weight : {patient.weight} \n  married : {patient.married} \n  allergies : {patient.allergies} \n  contact_details : {patient.contact_details}")
    print("Data inserted successfully")

patient_info = {'name': "BEAST", 'email': "beast@gmail.com", 'linkedin': "https://www.linkedin.com/in/beast", 'age': 24, 'weight': 70.5, 'married': False, 'allergies': ['pollen', 'nuts'], 'contact_details': {'phone': '123-456-7890', 'email': 'beast@abc.com'}}

patient1 = Patient(**patient_info)  

insert_patient_data(patient1)
