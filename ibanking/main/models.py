from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

class Rekening(models.Model):
	no_rekening = models.CharField(unique=True,max_length=16, validators=[MinLengthValidator(16)])
	saldo = models.PositiveIntegerField(default=0)
	pemilik = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.no_rekening

class Riwayat(models.Model):
	pengirim = models.ForeignKey(Rekening, on_delete=models.CASCADE, related_name="kirim")
	penerima = models.ForeignKey(Rekening,on_delete=models.CASCADE, related_name="terima")
	jumlah = models.PositiveIntegerField()
	tanggal_transaksi = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return (str(self.pengirim) + "_" + str(self.penerima) + "_" + str(self.tanggal_transaksi))