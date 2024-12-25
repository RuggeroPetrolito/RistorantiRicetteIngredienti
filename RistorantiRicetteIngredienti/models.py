from django.db import models

class Ristorante(models.Model):
    ristorante_text = models.CharField(max_length=200, default='test ristorante')
    class Meta:
        verbose_name_plural = 'Ristoranti'
    def __str__(self):
        return self.ristorante_text

class Ricetta(models.Model):
    ricetta_text = models.CharField(max_length=5000, default='test ricetta')
    class Meta:
        verbose_name_plural = 'Ricette'
    def __str__(self):
        return self.ricetta_text

class Ingrediente(models.Model):
    ingrediente_text = models.CharField(max_length=200, default='test ingrediente')
    class Meta:
        verbose_name_plural = 'Ingredienti'
    def __str__(self):
        return self.ingrediente_text

class RistoranteToRicetta(models.Model):
    ristorante = models.ForeignKey(Ristorante, on_delete=models.CASCADE, related_name='ristorantetoricetta')
    ricetta = models.ForeignKey(Ricetta, on_delete=models.CASCADE, related_name='ristorantetoricetta')

class RicettaToIngrediente(models.Model):
    ricetta = models.ForeignKey(Ricetta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)