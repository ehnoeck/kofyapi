from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        return Response({
            'count': self.page.paginator.count,
            'next': next_url,
            'previous': previous_url,
            'results': data
        })

access_token = 'duffel_test_OKIiZ1F1RN3VFxOjr_IjDwpj-y5oYexVvpOVSsDF7Go'

import requests
from pprint import pprint
headers = {
    "Accept-Encoding": "gzip",
    "Accept": "application/json",
    "Content-Type" : "application/json",
    "Duffel-Version" : "v1",
    "Authorization": "Bearer duffel_test_NeTvLJYCLhVeEOkEqKsaaA_8oGmfB0d2OdUugY10rep" 
}

@api_view(['GET'])
def flights(request):
    cabin_class = request.query_params.get("cabin_class")
    child_qty = request.query_params.get('child')
    infant_qty = request.query_params.get('infant')
    adult_qty = request.query_params.get('adult')
    journey_type = request.query_params.get('journey_type').lower()

    slices = [
        {
            "origin": request.query_params.get('origin'),
            "destination": request.query_params.get('destination'),
            "departure_date": request.query_params.get('departure_date'),
        },
    ]
    if journey_type == 'return':
        slices.append(
            {
                "origin": request.query_params.get('destination'),
                "destination": request.query_params.get('origin') ,
                "departure_date": request.query_params.get('return_date')
            }
        )

    passengers = []
    if adult_qty:
        for _ in range(int(adult_qty)):
            passengers.append({"type": "adult" })
    if child_qty:
        for _ in range(int(child_qty)):
            passengers.append({"type": "child" })
    if infant_qty:
        for _ in range(int(infant_qty)):
            passengers.append({"type": "infant_without_seat"})
    
    #data takes slices,passengers and cabin
    data = {
        "data":{
            "slices":slices,
            "passengers":passengers,
            "cabin_class": cabin_class
        }
    }

    url = 'https://api.duffel.com/air/offer_requests'
    response = requests.post(url, headers=headers, json=data).json()
    # pprint(response['data']['offers'])

    
    # get passenger ids and types so as to fill their information
    passenger_ids_and_type = []

    for passenger in response['data']['passengers']:
        passenger_ids_and_type.append(
            {"passenger":passenger['id'],"type":passenger['type']}
        )

    offer= response['data']['offers'][0]



    ff = []  # list of offers with only required data
    if journey_type != 'return':
        for offer in response['data']['offers']:
            ff.append(
                {
                "offer_id":offer['id'],
                "airline":offer['owner']['name'],
                "airline_logo":offer['owner']['logo_symbol_url'],
                "departure_date":offer['slices'][0]['segments'][0]['departing_at'].split('T')[0],
                "departure_time":offer['slices'][0]['segments'][0]['departing_at'].split('T')[1],
                "arrival_date":offer['slices'][0]['segments'][0]['arriving_at'].split('T')[0],
                "arrival_time":offer['slices'][0]['segments'][0]['arriving_at'].split('T')[1],
                "duration":offer['slices'][0]['segments'][0]['duration'][2:],
                "price":offer['total_amount'],
                "currency":offer['total_currency'],
                "cabin_class":offer['slices'][0]['segments'][0]['passengers'][0]['cabin_class'],
                "payment_required_by":offer['payment_requirements']['payment_required_by'],
                "origin":{
                        "city_name" : offer['slices'][0]['segments'][0]['origin']['city_name'],
                        "iata_code": offer['slices'][0]['segments'][0]['origin']['iata_code'],
                        "airport_name":offer['slices'][0]['segments'][0]['origin']['name'],
                        "destination_time_zone":offer['slices'][0]['segments'][0]['origin']['time_zone'],
                        "destination_terminal":offer['slices'][0]['segments'][0]['origin_terminal'],
                    },
                "destination":{
                        "city_name" : offer['slices'][0]['segments'][0]['destination']['city_name'],
                        "iata_code": offer['slices'][0]['segments'][0]['destination']['iata_code'],
                        "airport_name":offer['slices'][0]['segments'][0]['destination']['name'],
                        "destination_time_zone":offer['slices'][0]['segments'][0]['destination']['time_zone'],
                        "destination_terminal":offer['slices'][0]['segments'][0]['destination_terminal'],
                    },
                "aircraft_name":offer['slices'][0]['segments'][0]['aircraft']['name'],
                "operating_carrier_flight_number":offer['slices'][0]['segments'][0]['operating_carrier_flight_number'],

                }
            )
    else:
        for offer in response['data']['offers']:
            ff.append(
                {
                "offer_id":offer['id'],
                "airline":offer['owner']['name'],
                "airline_logo":offer['owner']['logo_symbol_url'],
                "departure_date":offer['slices'][0]['segments'][0]['departing_at'].split('T')[0],
                "departure_time":offer['slices'][0]['segments'][0]['departing_at'].split('T')[1],
                "arrival_date":offer['slices'][0]['segments'][0]['arriving_at'].split('T')[0],
                "arrival_time":offer['slices'][0]['segments'][0]['arriving_at'].split('T')[1],
                "duration":offer['slices'][0]['segments'][0]['duration'][2:],
                "origin":{
                        "city_name" : offer['slices'][0]['segments'][0]['origin']['city_name'],
                        "iata_code": offer['slices'][0]['segments'][0]['origin']['iata_code'],
                        "airport_name":offer['slices'][0]['segments'][0]['origin']['name'],
                        "destination_time_zone":offer['slices'][0]['segments'][0]['origin']['time_zone'],
                        "destination_terminal":offer['slices'][0]['segments'][0]['origin_terminal'],
                    },
                "destination":{
                        "city_name" : offer['slices'][0]['segments'][0]['destination']['city_name'],
                        "iata_code": offer['slices'][0]['segments'][0]['destination']['iata_code'],
                        "airport_name":offer['slices'][0]['segments'][0]['destination']['name'],
                        "destination_time_zone":offer['slices'][0]['segments'][0]['destination']['time_zone'],
                        "destination_terminal":offer['slices'][0]['segments'][0]['destination_terminal'],
                    },
                "aircraft_name":offer['slices'][0]['segments'][0]['aircraft']['name'],
                "operating_carrier_flight_number":offer['slices'][0]['segments'][0]['operating_carrier_flight_number'],

                ##
                "return_departure_date":offer['slices'][1]['segments'][0]['departing_at'].split('T')[0],
                "return_departure_time":offer['slices'][1]['segments'][0]['departing_at'].split('T')[1],
                "return_arrival_date":offer['slices'][1]['segments'][0]['arriving_at'].split('T')[0],
                "return_arrival_time":offer['slices'][1]['segments'][0]['arriving_at'].split('T')[1],
                "return_duration":offer['slices'][1]['segments'][0]['duration'][2:],
                "price":offer['total_amount'],
                "currency":offer['total_currency'],
                "cabin_class":offer['slices'][0]['segments'][0]['passengers'][0]['cabin_class'],
                "payment_required_by":offer['payment_requirements']['payment_required_by'],

                "return_origin":{
                    "city_name" : offer['slices'][1]['segments'][0]['origin']['city_name'],
                    "iata_code": offer['slices'][1]['segments'][0]['origin']['iata_code'],
                    "airport_name":offer['slices'][1]['segments'][0]['origin']['name'],
                    "destination_time_zone":offer['slices'][1]['segments'][0]['origin']['time_zone'],
                    "destination_terminal":offer['slices'][1]['segments'][0]['origin_terminal'],
                },
                "return_destination":{
                    "city_name" : offer['slices'][1]['segments'][0]['destination']['city_name'],
                    "iata_code": offer['slices'][1]['segments'][0]['destination']['iata_code'],
                    "airport_name":offer['slices'][1]['segments'][0]['destination']['name'],
                    "destination_time_zone":offer['slices'][1]['segments'][0]['destination']['time_zone'],
                    "destination_terminal":offer['slices'][1]['segments'][0]['destination_terminal'],
                },
                "return_aircraft_name":offer['slices'][1]['segments'][0]['aircraft']['name'],
                "return_operating_carrier_flight_number":offer['slices'][1]['segments'][0]['operating_carrier_flight_number'],
            

                "total_emmsions":offer['total_emissions_kg'],

                }
            )

    paginator = CustomPagination()
    paginated_data = paginator.paginate_queryset(ff, request)
    return paginator.get_paginated_response({"passenger_ids_and_type":passenger_ids_and_type,"flight_offers":paginated_data})

@api_view(['POST'])
def payment_intent(request):
    # add the mark up and duffel chrages to total amount
    offer_id = request.data['offer_id']
    offer_url = f'https://api.duffel.com/air/offers/{offer_id}'
    offer = requests.get(url = offer_url,headers=headers).json()

    url='https://api.duffel.com/payments/payment_intents'

    data= {
        "data":{
            "currency": offer['data']['total_currency'],
            "amount": offer['data']['total_amount']
        }
    }

    response = requests.post(url=url, headers=headers, json=data).json()
    data = {"data":{"payment_intent_id":response['data']['id'],"client_token":response['data']['client_token']}}
    return Response(data)

@api_view(['POST'])
def confirm_payment_intent(request):
    pit = request.data['pit']
    url=f'https://api.duffel.com/payments/payment_intents/{pit}/actions/confirm'
    response = requests.post(url = url,headers=headers).json()
 
    return Response(response)
    
@api_view(['POST'])
def book_flight(request):
    offer_id = request.data['offer_id']
    offer_url = f'https://api.duffel.com/air/offers/{offer_id}'
    offer = requests.get(url = offer_url,headers=headers).json()

    url = 'https://api.duffel.com/air/orders'

    # instant order
    total = str(float(offer['data']['total_amount']) + float(request.data['services_total_amount']))
    payments = [
        {
            "type": "balance",
            "currency": offer['data']['total_currency'],
            "amount": total
        }
    ]

    data = { 
        "data":{
        "selected_offers":[offer_id],
        "payments":payments,
        "passengers":request.data['passengers'],
        "services":request.data['services'],
        "type":"instant"
        }
    }
    order = requests.post(url=url,headers=headers,json=data).json()
    return Response(order)
    # {"Booking_reference":order['data']['booking_reference'],"created_at":order['data']['created_at']}

@api_view(['GET'])
def services(request):
    offer_id = request.query_params.get("offer_id")
    seats = f'https://api.duffel.com/air/seat_maps?offer_id={offer_id}'
    seat_map_response = requests.get(seats, headers=headers).json()
    bags = f'https://api.duffel.com/air/offers/{offer_id}?return_available_services=true'
    bags_response = requests.get(bags, headers=headers).json()

    return Response(
        {
            'seat_map':seat_map_response,
            'extra_bags':bags_response['data']['available_services']
        })

    
















def docs(request):  
    return render(request,'docs.html')


def handler404(request, exception):
    return render(request,'404.html')