
import pandas as pd
import numpy as np
from django.shortcuts import render
import warnings
import pickle
import json
warnings.filterwarnings("ignore")

m6 = pickle.load(open(r'C:/Users/VIKRAM/Downloads/files/APP/Asset/datasets/6years.pickle','rb'))
m5 = pickle.load(open(r'C:/Users/VIKRAM/Downloads/files/APP/Asset/datasets/5years.pickle','rb'))
m4 = pickle.load(open(r'C:/Users/VIKRAM/Downloads/files/APP/Asset/datasets/4years.pickle','rb'))

__data_columns = None
f = open('C:/Users/VIKRAM/Downloads/data/columns.json','rb')
__data_columns = json.loads(f.read())['data_columns']

def get22(input):
    try:
        loc_index = __data_columns.index(input['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = input['sqft']
    x[1] = input['bath']
    x[2] = input['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(m4.predict([x])[0],2)
    return result

def get23(input):
    try:
        loc_index = __data_columns.index(input['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = input['sqft']
    x[1] = input['bath']
    x[2] = input['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(m5.predict([x])[0],2)
    return result

def get24(input):
    try:
        loc_index = __data_columns.index(input['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = input['sqft']
    x[1] = input['bath']
    x[2] = input['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(m6.predict([x])[0],2)
    return result


def convert(n,var5):
    if n==1:
      var5*=9
    elif n==2:
      var5*=43560  
    elif n==3:
        var5*=435.6
    return int(var5)

def c(n):
     if n==1:
       a="Sq_Yards"
     elif n==2:
      a="Acre"  
     elif n==3:
        a="Cents"
     return a

def c1(n):
     if n==1:
       a="Sq Feets"
     elif n==2:
      a="Sq Yards"  
     return a     

def f(n1,n2):
    if(n2==1):
        n1=n1*500
    elif(n2==2):
        n1=n1*400    
    elif(n2==3):
        n1=n1*300
    elif(n2==4):
        n1=n1*200    
    return n1    

def home(request):
    return render(request,'home.html')

def house_predict(request):
    data=pd.read_excel(r'C:/Users/VIKRAM/Downloads/data/upto 4 years.xlsx')
    locations=sorted(data['location'].unique())
    return render(request,'house_predict.html',{'locations':locations})

def land_predict(request):
    data=pd.read_excel(r'C:/Users/VIKRAM/Downloads/data/upto 4 years.xlsx')
    locations=sorted(data['location'].unique())
    return render(request,'land_predict.html',{'locations':locations})    
#house_function
def result1(request):
    var1=str(request.GET['location'])
    var2=str(request.GET['ct'])
    var7=int(request.GET['ft'])
    var3=int(request.GET['bath'])
    var4=int(request.GET['bhk'])
    var5=int(request.GET['total_sqft'])
    var6=int(request.GET['dim'])
    n5=var5
    print(var2)
    if var6==2:
      var5=var5*9
    print("sq_feets",+var5)
    input_json = {
            "location": var1,
            "sqft": var5,
            "bhk": var3,
            "bath":var4
        }
    g22= get22(input_json)
    g23= get23(input_json)
    g24= get24(input_json)   
    c="NA"
    if var2=="Appartment":
        if var7==1:
            c="Ground Floor"
        elif var7==2:
            c="First Floor"    
        elif var7==3:
            c="Second Floor"
        elif var7==4:
            c="Above Second Floor"
    fc=f(var5,var7)
    a1,a2,a3=g22+fc,g23+fc,g24+fc        
    n=c1(var6)
    d1=" "+str(n5)+" "+n
    g2=" Present price  is"+" "+str(a1)+" "+"INR"
    g3="At 2023,the Predicted price  is"+" "+str(a2)+" "+"INR"
    g4="At 2024,the Predicted price  is"+" "+str(a3)+" "+"INR"
    return render(request,'HouReport.html',{"result22":g2,"result23":g3,"result24":g4,"location":var1,"dm":d1,"ht":var2,"cf":c,"bat":var3,"bed":var4})

#Land Function()
def result(request):
    loc=str(request.GET['location'])
    var5=int(request.GET['total_sqft'])
    dim=int(request.GET['dim'])
    dm=convert(dim,var5)
    print("sq_feets",+dm) 
    input_json = {
            "location": str(request.GET['location']),
            "sqft": dm,
            "bhk":1,
            "bath":1,
        }
    g22= get22(input_json)
    g23= get23(input_json)
    g24= get24(input_json)
   
    n=c(dim)
    d=" "+str(var5)+" "+n
    g2=" Present price  is"+" "+str(g22)+" "+"INR"
    g3="The Predicted price at 2023 is"+" "+str(g23)+" "+"INR"
    g4="The Predicted price at 2024 is"+" "+str(g24)+" "+"INR"
    return render(request,'landReport.html',{"result22":g2,"result23":g3,"result24":g4,"location":loc,"dm":d})       
       