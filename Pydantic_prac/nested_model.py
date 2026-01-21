# what is nested model in pydantic?
# -> Nested models in Pydantic allow you to create complex data structures by embedding one model within another.
# This is useful for representing hierarchical data and reusing models across different parts of your application.
# Example: A Patient model containing an Address model to represent the patient's address details. 


from pydantic import BaseModel, EmailStr

class Address(BaseModel): 
    city: str
    state: str
    pin: str 

class Patient(BaseModel): 
    name: str
    gender: str 
    
    # try for exclude_unset
    gender: str = "male"
    age: int
    address: Address 

address_dict = {'city': "New York", 'state': "NY", 'pin': "10001"}

address = Address(**address_dict)

patient_info = {'name' : "BEAST", 'gender': "male", 'age': 25, 'address': address}

# try for exclude_unset
# patient_info = {'name' : "BEAST", 'age': 25, 'address': address}

patient_1 = Patient(**patient_info)

# print(patient_1)
# print("The name of patient_1 is : ", patient_1.name)
# print("The full address of patient_1 is : ", patient_1.address)
# print("The city of patient_1 is : ", patient_1.address.city)



# we can export the model as python dict or json 

# let's export in dict 
# temp = patient_1.model_dump() # ye aapke existing pydantic model ko dict me convert kar dega
# print("Patient model as dict : ", temp)
# print(type(temp))


# you can even control ke konsee field aapko export karne hai

# here there is 2 option include and exclude 
# Example: include=['name', 'address'] and exclude=['age', 'gender']
# inclide -> jo fields aapko chahiye sirf wahi aayenge
# exclude -> jo fields aapko nahi chahiye wahi exclude ho jayenge baaki

# include example
temp = patient_1.model_dump(include=['name', 'address']) 
print("I am include : ", temp)
print(type(temp))


# exclude example
temp = patient_1.model_dump(exclude=['age', 'gender']) 
print("I am excliude : ", temp)
print(type(temp))

# exclude_unset example
# for example kisi ne gender default male set kia hai aur aapne patient create karte time gender specify nahi kia to wo unset hoga, too exclude_unset us case me kya karega ki jo fields unset hai unko exclude kar dega

# temp = patient_1.model_dump(exclude_unset=False) # gender ke value nahi show karega
# temp = patient_1.model_dump(exclude_unset=True) # gender ke value show karega 
# print("I am exclude_unset : ", temp)
# print(type(temp))



# let's export in json
# temp_json = patient_1.model_dump_json() # ye aapke existing pydantic model ko json me convert kar dega
# print("Patient model as json : ", temp_json)
# print(type(temp_json)) # Python will receive it as string but aagar aap isko export kartee ho to ye as a json export ho jayega 
 