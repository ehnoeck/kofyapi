from django.urls import path
from .views import flights,book_flight,payment_intent,confirm_payment_intent,docs,handler404,services,order_cancellation,confirm_order_cancellation

urlpatterns = [
    path('flights/', flights,name='flights'),
    path('payment_intent/',payment_intent, name='payment_intent'),
    path('confirm_payment_intent/',confirm_payment_intent, name='confirm_payment_intent'),
    path('book_flight/',book_flight, name='book_flight'),
    path('services/',services, name='services'),
    path('order_cancellation/',order_cancellation, name='order_cancellation'),
    path('confirm_order_cancellation/',confirm_order_cancellation, name='confirm_order_cancellation'),
    path('',docs, name='docs'),
    path('404',handler404, name='404')

]

handler404 = 'kofiapi.views.handler404'