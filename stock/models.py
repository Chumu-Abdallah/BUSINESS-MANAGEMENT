from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    jina = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, blank=True, null=True)
    stock = models.IntegerField(default=0)
    bei_kununua = models.IntegerField()
    bei_kuuza = models.IntegerField()
    tarehe = models.DateTimeField(auto_now_add=True)

    @property
    def faida(self):
        return self.bei_kuuza - self.bei_kununua
    def __str__(self): 
        return self.jina

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    kiasi = models.IntegerField(default=1)
    muuzaji = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tarehe = models.DateTimeField(auto_now_add=True)

    @property
    def faida_yake(self):
        return (self.product.bei_kuuza - self.product.bei_kununua) * self.kiasi


# Matumizi ya fsida
class MatumiziYaFaida(models.Model):
    matumizi = models.IntegerField()
    maelezo = models.CharField(max_length=200) # mfano: kodi yaduka,nyumba, Chakula
    tarehe = models.DateTimeField(auto_now_add=True)
    alietoa = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.maelezo} - {self.matumizi} TSh" 

# Hisabu zakila mwezi na ya mwaka kw ujumla
class RepotiYaMwezi(models.Model):
    mwaka = models.IntegerField() # 2026
    mwezi = models.IntegerField() # 1-2
    faida_kabla = models.IntegerField()
    faida_baada = models.IntegerField()
    jumla_faida = models.IntegerField()
    jumla_bidhaa = models.IntegerField()
    jumla_matumizi = models.IntegerField()
    class Meta:
        unique_together = ('mwaka', 'mwezi')

class RepotYaMwaka(models.Model):
    mwaka = models.IntegerField(unique=True)
    faida_kabla = models.IntegerField()
    faida_baada = models.IntegerField()
    jumla_faida = models.IntegerField()
    jumla_bidhaa = models.IntegerField()
    jumla_matumizi =models.IntegerField()        
