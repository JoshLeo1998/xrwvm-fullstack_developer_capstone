from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from datetime import datetime
from django.http import JsonResponse
from .models import CarMake, CarModel
from .populate import initiate  # Import the populate function
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:  # Populate data if CarMake table is empty
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

# Update the `get_dealerships` method to render a list of dealerships
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_details` method to fetch details for a specific dealer
def get_dealer_details(request, dealer_id):
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer_details = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer_details": dealer_details})

# Create a `get_dealer_reviews` method to fetch reviews for a specific dealer
def get_dealer_reviews(request, dealer_id):
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    review_details = []

    # Analyze the sentiment of each review
    for review in reviews:
        sentiment = analyze_review_sentiments(review.get("review", ""))
        review_details.append({
            "id": review.get("id"),
            "name": review.get("name"),
            "review": review.get("review"),
            "purchase": review.get("purchase"),
            "purchase_date": review.get("purchase_date"),
            "car_make": review.get("car_make"),
            "car_model": review.get("car_model"),
            "car_year": review.get("car_year"),
            "sentiment": sentiment.get("sentiment", "neutral")  # Default to "neutral" if no sentiment is returned
        })

    return JsonResponse({"status": 200, "reviews": review_details})

# Add the `add_review` method to handle review submissions
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": 403, "message": "Unauthorized"})

        try:
            data = json.loads(request.body)
            response = post_review(data)
            if response:
                return JsonResponse({"status": 200, "message": "Review submitted successfully!"})
            else:
                return JsonResponse({"status": 500, "message": "Failed to submit review."})
        except json.JSONDecodeError as e:
            return JsonResponse({"status": 400, "message": f"Invalid JSON data: {str(e)}"})
        except Exception as e:
            return JsonResponse({"status": 500, "message": f"Unexpected error: {str(e)}"})
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed. Use POST."})


# Create a `login_user` view to handle sign-in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provided credentials can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_user` view to handle logout request
def logout_user(request):
    # Logs out the user
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `register_user` view to handle registration request
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "error": "Already Registered"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()
        login(request, user)
        return JsonResponse({"status": True, "userName": username})
    return JsonResponse({"status": False, "error": "Invalid Request Method"})

