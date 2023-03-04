from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
import pandas as pd
from stockprediction.models import get_df,get_plot
from stockprediction.utils import add_search, get_stock_count, get_user_count, getAllUsers
from django.contrib.staticfiles import finders
import json
from django.contrib.auth import get_user

result = finders.find('datasets/symbol.csv')
filename = pd.read_csv(result)
json_records = filename.reset_index().to_json(orient ='records')
data = []
data = json.loads(json_records)
def analysis(request):
	
	return render(request,'analysis.html', {'data': data})

def predictValue(request):
	temp = {}
	if request.method == 'POST':
		temp['stocksymbol'] = request.POST.get('stocksymbol')
		start = pd.to_datetime('12-05-2020')
		end = pd.to_datetime('12-05-2022')
		print(temp['stocksymbol'])
		df = get_df(temp['stocksymbol'], start , end)
		response = get_plot(df,temp['stocksymbol'])
		pred_value=''
		if request.user.is_authenticated:
			add_search(temp['stocksymbol'], request)
		txt = f'{response[1]}'
		pred_value = txt.replace('[','').replace(']','')
		return render(request,'analysis.html',{'chart': response[0], 'pred_price': pred_value})

def controlpanel(request):
	search = ''
	if request.method == 'GET':
		search = request.GET.get('search')
		users = getAllUsers(search)
		user_count = get_user_count()
		search_count = get_stock_count()
		response = render(request,'controlpanel.html', {'users': users,
		'users_count': user_count, 'searches': search_count , 'stocks' : '24024' })

		return response
	

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"form": form})

def research(request):
	if request.method == 'POST':
		stock = request.POST.get("stocksymbol")
		return render(request=request, template_name="research.html", context={'data': data, 'stock': stock})
	return render(request=request, template_name="research.html", context={'data': data, 'stock': 'AAPL'})

def homepage(request):
	return render (request=request, template_name="home.html")

def account_login(request):    
		if request.method == 'POST':
			if request.POST.get('submit') == 'sign_in':
				username = request.POST.get("username")
				password = request.POST.get("password")
				user = authenticate(request, username=username, password= password)
				if user is None:
					context = {"error": "Invalid User"}
					return render(request=request, template_name="registration/login.html",context=context)
				login(request, user)
				return redirect('/')
			if request.POST.get('submit') == 'sign_up':
				form = NewUserForm(request.POST)
				
				if form.is_valid():
					user = form.save()
					login(request, user)
					messages.success(request, "Registration successful." )
					print(user)
					return redirect("/")
				messages.error(request, "Unsuccessful registration. Invalid information.")
		form = NewUserForm()		
		return render(request=request, template_name="registration/login.html", context={"form": form})

def account_logout(request):
	logout(request)
	return redirect("/")
	