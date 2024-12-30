from django.shortcuts import render
import requests

# Create your views here.

def Index(request):
    
    data = 0
    try:
        if request.method == "POST":
            Id = request.POST.get('Id')
            SepalLengthCm = request.POST.get('SepalLengthCm')
            SepalWidthCm = request.POST.get('SepalWidthCm')
            PetalLengthCm = request.POST.get('PetalLengthCm')
            PetalWidthCm = request.POST.get('PetalWidthCm')
                

                # print(N,P,K,T,H,PH,R)

            Id = int(Id)
            SepalLengthCm = float(SepalLengthCm)
            SepalWidthCm = float(SepalWidthCm)
            PetalLengthCm = float(PetalLengthCm)
            PetalWidthCm = float(PetalWidthCm)
            
            

                
            if Id:

                API_KEY = "pwckFajRps6HWJg31azJwsQCzsb3wte7zUtw53IADDic"
                Public_endpoint = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/ee1de501-ffd8-4eb6-bff4-983f5b291ae4/predictions?version=2021-05-01"

                token_response = requests.post(
                        'https://iam.cloud.ibm.com/identity/token',
                        data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
                    )

                if token_response.status_code != 200:
                    print("Error fetching token:", token_response.json())
                    exit()

                mltoken = token_response.json().get("access_token")



                header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

                payload_scoring = {
                        "input_data": [
                            {
                                "fields": ["Id", "SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"],
                                "values": [[Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm]]
                            }
                        ]
                    }


                response_scoring = requests.post(
                    Public_endpoint,
                    json=payload_scoring,
                    headers=header,
                        
                    )

                print(response_scoring)

                    

                if response_scoring.status_code != 200:
                    print("Error in prediction:", response_scoring.json())
                    data = "Error"
                else:
                    # print("Scoring response:", response_scoring.json())
                    print(response_scoring.json()['predictions'][0]['values'][0][0])
                    data = response_scoring.json()['predictions'][0]['values'][0][0]
            
                        
        context = {'prediction':data}
    except:
        data = 0
        context = {'prediction':data}
        print("error")



    return render(request,'index.html', context)
