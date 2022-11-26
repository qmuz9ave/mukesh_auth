def check_unique(id,key,value,my_data):
    count=0
    for data in my_data:
        if data[str(key)] ==  value:
            count+=1
    if count >1:
        print(f"data with id {id} key {key} value {value}  is not unique")
        
    
    

def  validate_queue(queue_constrain,my_data):
    worked_data = []
    for data in my_data:
        print(f"in data {data['id']}")
        for i in range(len(data)):
            key = list(data.keys())[i]
            # data[key]
            # keys of each and every datas
            
            '''
            now filter throughout the constrain
            
            qs = Queusconstrain.objects.filter(queue =  qui)
            here qs will be queue constrain
            ''' 
            for constrain in queue_constrain:
                constrain_header = constrain['header']
                if constrain_header == key:
                    # yadi hamro  header ko kura uta data ko key sanga match garchha bhane chai
                    # aba hami required ra unique check garchham
                    if (constrain["required"] == True) and (data[str(key)] ==None):
                        print(f"this row cant be  done because data with id: {data['id']}  --> key {constrain_header} is  null")
                    
                    if constrain['unique'] == True:
                        check_unique(data["id"],constrain_header,data[str(constrain_header)],worked_data)
        worked_data.append(data)
                    
            


queue_constrain = [{
    "queue":1,
    "header":"id",
    "required":False,
    "unique":True
},
{
    "queue":1,
    "header":"name",
    "required":False,
    "unique":False
},
{
    "queue":1,
    "header":"email",
    "required":True,
    "unique":True
},
{
    "queue":1,
    "header":"phone_number",
    "required":True,
    "unique":True
},
{
    "queue":1,
    "header":"address",
    "required":False,
    "unique":False
}]

my_data = [
{
"id":1,
"name":"Sangit Raj Kc",
"email":"sangitraj.kc1201@gmail.com",
"phone_number":"9841939263",
"address":"dolakha"
},
{
"id":2,
"name":"Sangit Raj Kc",
"email":"sangitraj.kc1201@gmail.com",
"phone_number":None,
"address":"dolakha"
},
{
"id":3,
"name":"Saurav Chhetri",
"email":"sangitraj.kc1202@gmail.com",
"phone_number":"9841939263",
"address":"dolakha"
},
{
"id":4,
"name":"Sangit Raj Kc",
"email":"sangitraj.kc1201@gmail.com",
"phone_number":"9841939265",
"address":"dolakha"
},
{
"id":5,
"name":"Sangit Raj Kc",
"email":"sangitraj.kc1205@gmail.com",
"phone_number":"9841939266",
"address":"dolakha"
}
]

validate_queue(queue_constrain,my_data)

