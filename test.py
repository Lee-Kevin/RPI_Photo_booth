import json
import time 

dict = {
        '0':'hello.jpg',
        '1':'world.jpg',
        '2':'seeed.jpg',
        '3':'seeed.jpg',
        '4':'seeed.jpg',
        '5':'seeed.jpg',
        '6':'seeed.jpg',
        '7':'seeed.jpg',
        '8':'seeed.jpg',
        '9':'seeed.jpg',
        }

# if __name__ == "__main__" :
    
    # f = open('rank.json','wb+')
    # # data_json = f.read()
    # jsonobj = json.dumps(dict)
    # f.write(jsonobj)
    # for i in range(0,2):
        # print dict[str(i)]
    
    # f.close()
    # # print jsonobj
    # time.sleep(2)
    
    # f = open('rank.json','rb+')
    # data = f.read()
    # print data
    # data_json = json.loads(data)
    # for i in range(0,2):
        # print data_json[str(i)]
    # f.close()
        
if __name__ == "__main__" :
    
    f = open('rank.json','rb')
    data_json = f.read()
    f.close()
    data = json.loads(data_json)
    
    for i in range(0,10):
        print data[str(i)]
    
    print("----------------")
    for i in range(9,0,-1):
        data[str(i)] = data[str(i-1)]
    data["0"] = "seeed.jpg"
    

        
    f = open('rank.json','wb')
    data_json = json.dumps(data)
    f.write(data_json)
    f.close()
    print data_json

    
    
    


