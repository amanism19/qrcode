from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home' ),
    path('openscanner', views.scan , name='scan' ),
    path('qrapi', views.qrdecode, name='qrapi'),
    path('adv', views.advScan),
]
