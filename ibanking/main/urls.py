from django.urls import path
from . import views

urlpatterns=[
	path('', views.home, name='home'),
	path('rekening/', views.rekening, name='main-rekening'),
	path('transaksi/', views.transaksi, name='main-transaksi'),
	path('riwayat/', views.riwayat, name='main-riwayat'),
	path('delete/<int:id>/', views.deleteRekening, name='main-delete'),
]