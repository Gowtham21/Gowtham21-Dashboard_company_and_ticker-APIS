from django.shortcuts import render
from report import forms
import requests
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint
import yaml

# Create your views here.
def index(request):
    form = forms.user_input()

    if request.method == 'POST':
        form = forms.user_input(request.POST)

        if form.is_valid():
            with open("config.yaml", 'r') as stream:
                data_loaded = yaml.safe_load(stream)

            company = form.cleaned_data['Company_name']
            staticurl = data_loaded['staticurl']
            apiKey = data_loaded['apiKey']

            ticker = form.cleaned_data['Ticker_symbol']
            static_ticker = data_loaded['static_ticker']
            static_api = data_loaded['static_api']

            url = staticurl+company+apiKey
            turl = static_ticker+ticker+static_api

            response = requests.get(url)
            newsapi_json = response.json()
            json_dict = newsapi_json['articles']

            ticker_response = requests.get(turl)
            ticker_json = ticker_response.json()


            if len(json_dict) == 0 and len(ticker_json) == 2:
                no_ticker = ticker_json['error']
                no_company = "No News Found, Please check company name or give another company name"
                return render(request,'report/result.html',{'no_company':no_company,'company':company,'no_ticker':no_ticker})

            elif len(json_dict) > 0 and len(ticker_json) == 2:
                no_ticker = ticker_json['error']
                company_data = []
                for list_view in json_dict[0:5]:
                    company_data.append(list_view['title'])
                return render(request,'report/result.html',{'company_data':company_data,'company':company,'no_ticker':no_ticker})

            elif len(json_dict) == 0 and len(ticker_json) > 3:
                no_company = "No News Found, Please check company name or give another company name"
                ticker_data = ticker_json['short_description']

                return render(request,'report/result.html',{'no_company':no_company,'company':company,'ticker_data':ticker_data})
            else:
                company_data = []
                ticker_data = ticker_json['short_description']
                for list_view in json_dict[0:5]:
                    company_data.append(list_view['title'])


                return render(request,'report/result.html',{'company_data':company_data,'company':company,'ticker_data':ticker_data})

        else:
            form = forms.user_input()
    return render(request,'report/index.html',{'form':form})
