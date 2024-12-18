from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_sentiment, name='predict_sentiment'),
]
urlpatterns += [
    path('', views.sentiment_page, name='sentiment_page'),
]

