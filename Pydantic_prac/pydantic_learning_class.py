from pydantic import BaseModel
from typing import Optional

# Step - 1 : build a pydantic model for patient data [we will create the sche of our data over here]
class Patient(BaseModel): 
    name: str # this is required field [bydefault it is required]
    age: int
    married: bool = False # we can add default value to this field also 

    # this is how we can make a field optional [we need to make optional field as None because it will not have any value if not provided]
    weight: Optional[float] = None # this is optional field  

# Step - 2 : create an object of the class 

def insert_patient_data(patient: Patient):
    print(f"Name : {patient.name} \n Age : {patient.age} \n  Married : {patient.married} \n Weight : {patient.weight}")
    print("Data inserted successfully")

def update_patient_data(patient: Patient):
    print(f"Name : {patient.name} \n Age : {patient.age} \n  Married : {patient.married} \n Weight : {patient.weight}")
    print("Data updated successfully")

patient_info = {'name': "Beast", 'age': 24}
# patient_info = {'name': "Beast", 'age': 'two'}  # this will raise a validation error because age is not an intj

patient1 = Patient(**patient_info)  # unpacking the dictionary to match the model fields

insert_patient_data(patient1)
update_patient_data(patient1)