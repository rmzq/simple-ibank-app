from django import forms
from django.contrib.auth.models import User
from .models import Rekening, Riwayat
import datetime


# REKENING_CHOICES = [
# 	('1', 'satu'),
# 	('2', 'dua'),
# 	('3', 'tiga'),
	
# ]


# pilihan = Rekening.objects.filter(pemilik=3).values_list('id','no_rekening')

# class BuatRekening(forms.Form):
# 	norek = forms.CharField(label="No Rekening", min_length=16, max_length=16)
# 	saldo = forms.IntegerField(label="Saldo Awal")

class BuatRekening(forms.ModelForm):
	class Meta:
		model = Rekening
		fields = ('no_rekening', 'saldo')

		widgets={
			'no_rekening' : forms.NumberInput,
		}

		labels = {
			'no_rekening' : 'No Rekening',
		}


class BuatTransaksi(forms.ModelForm):
	class Meta:
		model = Riwayat
		fields = ('pengirim', 'penerima', 'jumlah')
		widgets = {
			'penerima': forms.NumberInput
		}

		labels = {
			'pengirim' : 'Pilih Rekening',
			'penerima' : 'Input Rekening Tujuan',
		}

class RangeTanggal(forms.Form):
	tanggal1 = forms.DateField(label='Dari', initial=datetime.date.today, widget=forms.SelectDateWidget())
	tanggal2 = forms.DateField(label='Sampai', initial=datetime.date.today, widget=forms.SelectDateWidget())
