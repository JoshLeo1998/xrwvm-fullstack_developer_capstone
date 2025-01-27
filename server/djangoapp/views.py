from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User  # Fix for F821
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response.get('sentiment', 'neutral')
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse(
                {"status": 200, "response": response}
            )
        except Exception:
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
    return JsonResponse({"status": 403, "message": "Unauthorized"})


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )
    return JsonResponse({"userName": username, "status": "Unauthorized"})


def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("userName")
        password = data.get("password")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")

        if User.objects.filter(username=username).exists():  # Fix for F821
            return JsonResponse(
                {"status": False, "error": "Already Registered"}
            )

        user = User.objects.create_user(  # Fix for F821
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()
        login(request, user)
        return JsonResponse(
            {"status": True, "userName": username}
        )
    return JsonResponse({"status": False, "error": "Invalid Request Method"})
