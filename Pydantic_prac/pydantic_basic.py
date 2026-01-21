# what is pydantic ?
# -> Pydantic is a data validation and settings management library for Python, based on type annotations.
# It allows you to define data models using Python classes and type hints, and automatically validates and parses the data according to the specified types.
# Example: Ensuring name is a string, age is an integer, weight is a float etc.
# In simple words Real-Life Example : When you fill a form online, the data you enter needs to be validated to ensure it is correct and in the right format. Pydantic does the same thing for data in Python applications.
# Non-technical Example - 2 : When you go to a restaurant and order food, the waiter takes your order and ensures that it is valid (e.g., they check if the items you ordered are available, if you have any dietary restrictions, etc.) before sending it to the kitchen. Pydantic acts like the waiter, validating and ensuring that the data you provide is correct before it is processed further in your application.

# What is type checking in pydantic?
# -> Type checking in Pydantic is the process of verifying that the data being modeled conforms to the specified types.
# Pydantic uses Python's type hints to enforce type constraints on model fields, ensuring that the data is of the correct type when creating model instances.
# Example: Ensuring name is a string, age is an integer, weight is a float etc.

def insert_patient_data(name: str, age:int):

    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cannot be negative")
        print(name)
        print(age)
        print("Data inserted successfully")
    else:
        raise TypeError("Incorrect data types")
    
insert_patient_data("John", 30)

# update_patient_data function with type checking
def update_patient_data(name: str, age:int):

    if type(name) == str and type(age) == int:
        if age < 0:
            raise ValueError("Age cannot be negative")
        print(name)
        print(age)
        print("Data updated successfully")
    else:
        raise TypeError("Incorrect data types")

update_patient_data("John", 30)




