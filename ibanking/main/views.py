from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Rekening, Riwayat
from .forms import BuatRekening, BuatTransaksi, RangeTanggal
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def home(request):
	return render(request, 'main/home.html', {})

@login_required
def rekening(request):
	print(request.user.id)
	if request.method == "POST":
		form = BuatRekening(request.POST)
		if form.is_valid():
			rekening = form.cleaned_data["no_rekening"]
			saldo = form.cleaned_data["saldo"]
			user = User.objects.get(id=request.user.id)
			r = Rekening.objects.create(no_rekening=rekening, pemilik=user, saldo=saldo)
			r.save()
			messages.success(request, f'Rekening anda berhasil dibuat dengan nomor {rekening}!')
		# return redirect('main-rekening')
	else:
		form = BuatRekening()
	rekening = Rekening.objects.filter(pemilik=request.user.id)
	return render(request, 'main/rekening.html', {'rekening':rekening, 'form':form})

@login_required
def transaksi(request):
	if request.method == "POST":
		form = BuatTransaksi(request.POST)

		dBaru = request.POST.copy()
		try:
			idRek = Rekening.objects.get(no_rekening=dBaru['penerima'])
			dBaru.update({'penerima': idRek.id})
			# print(dBaru)
			form = BuatTransaksi(data=dBaru)
			form.fields["pengirim"].choices = Rekening.objects.filter(pemilik=request.user.id).values_list('id','no_rekening')
			print (dBaru)
			if form.is_valid():
				pengirim = form.cleaned_data['pengirim']
				jumlah = form.cleaned_data['jumlah']
				penerima = form.cleaned_data['penerima']
				if pengirim.saldo < jumlah:
					messages.warning(request, f'Saldo tidak cukup!')
					# form = BuatTransaksi(request.POST)
				elif pengirim == penerima:
					messages.warning(request, f'Nomor rekening harus berbeda!')
				else:
					rekTerima = Rekening.objects.get(no_rekening=penerima)
					rekKirim = Rekening.objects.get(no_rekening=pengirim)

					r = Riwayat.objects.create(pengirim=pengirim, penerima=penerima, jumlah=jumlah)

					rekTerima.saldo += jumlah
					rekKirim.saldo -= jumlah

					rekTerima.save()
					rekKirim.save()
					r.save()
					messages.success(request, f'Transaksi sukses!')
		except Exception as e:
			messages.warning(request, e)

		return redirect('main-transaksi')

	else:
		form = BuatTransaksi()
		print(form)
		form.fields["pengirim"].choices = Rekening.objects.filter(pemilik=request.user.id).values_list('id','no_rekening')
	return render(request, 'main/transaksi.html', {'form':form})



# coba class-base views

# class TransaksiView(View):
# 	form_class = BuatTransaksi
# 	template_name = 'main/transaksi.html'

# 	def transaksi(self, request, *args, **kwargs):
# 		if request.method == "post":
# 			form = self.form_class(request.post)
# 			if form.is_valid():
# 					pass	
# 		else:
# 			form = form_class
# 			# form.kirim = Rekening.objects.filter(pemilik=request.user.id).values_list('id','no_rekening')
# 			print(form)
# 		return render(request, self.template_name, {'form':form})


@login_required
def riwayat(request):
	if request.method == "POST":
		form = RangeTanggal(request.POST)
		if form.is_valid():
			awal = form.cleaned_data['tanggal1']
			akhir = form.cleaned_data['tanggal2']
			riwayat= Riwayat.objects.filter(
				Q(tanggal_transaksi__range=[awal,akhir]),
				# Q(tanggal_transaksi__gte=awal), 
				# Q(tanggal_transaksi__lte=akhir),
				Q(penerima__in=Rekening.objects.filter(pemilik=request.user)) | 
				Q(pengirim__in=Rekening.objects.filter(pemilik=request.user)))
			print(riwayat)
			# redirect('main-riwayat')
			return render(request, 'main/riwayat.html', {'form':form, 'riwayat':riwayat})
	else:
		form = RangeTanggal()
	return render(request, 'main/riwayat.html', {'form':form})

@login_required
def deleteRekening(request, id):
	rekening = Rekening.objects.get(id=id)
	rekening.delete()
	return redirect('main-rekening')

