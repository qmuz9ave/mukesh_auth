import copy
constraints = [
    {"header": "name","required": True,"unique": False}, 
    {"header": "email","required": True, "unique": True},
    {"header": "phone","required": True,"unique": True}
    ]

datas = [
        {"name": "rkp","email": "pnt.roshan@gmail.com", "phone": "9844897540","aa":11},
        {"name": "roshan","email": "qmuz9ave@gmail.com","phone": "9844897541","bb":22},
        {"name": "biren","email": "biren@gmail.com","phone": "9844897542","aa":22},
        {"name": "sangit","email": "sangit@gmail.com","phone": "9844897543","cc":22}
     ]

headers_list = [constraint.get("header") for constraint in constraints]
unique_constraints = list(filter(lambda x: x.get('unique'), constraints))
required_constraints = list(filter(lambda x: x.get('required'), constraints))
required_headers = [constraint.get("header") for constraint in required_constraints]
unique_headers = [constraint.get("header") for constraint in unique_constraints]

invalid_data = []
valid_data = []
#invalid_response
invalid_return_response = []

#headers
for header in headers_list:
    for data in datas:
        data_headers = [key for key,value in data.items()]
        if header not in data_headers:
            invalid_header_dict = {
                "data":data,
                "valid":False,
                "detail":f"{header} is missing"
            }

            invalid_return_response.append(invalid_header_dict)

#clean data
clean_data = []
for data in datas:
    pop_keys = []
    _data = copy.copy(data)
    for key, value in _data.items():
        if key not in headers_list:
            data.pop(key)
    clean_data.append(data)

#check required
for data in clean_data:
    valid_keys = []
    invalid_keys = []
    for key, value in data.items():
        
        if key in required_headers:
            if value and value != '' and value is not None:
                valid_keys.append(key)
            else:
                invalid_keys.append(key)
        else:
            valid_keys.append(key)
        
    #
    if invalid_keys:
        for key in invalid_keys:
            invalid_dict = {
                "data": data,
                "valid": False,
                "reason": "required"
            }
            invalid_return_response.append(invalid_dict)

#check uniquee together
processed_unique_together_set = {(),}
for data in clean_data:
    touple_set = ()
    for key, value in data.items():
        
        if key in unique_headers:
            touple_set = touple_set+(value,)

    # check if data_set exists in already processed data
    if touple_set in processed_unique_together_set:
        invalid_resp_dict = {
            "data":data,
            "valid": False,
            "reason": "Duplicate",
        }
        invalid_return_response.append(invalid_resp_dict)
    else:
        processed_unique_together_set.add(touple_set)

print(invalid_return_response)     
