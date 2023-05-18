from django.db import models
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Pracownik(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imie = models.CharField(max_length=250)
    nazwisko = models.CharField(max_length=250)

    class Meta:
        db_table = "Pracownik"

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Weterynarz(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imie = models.CharField(max_length=250)
    nazwisko = models.CharField(max_length=250)

    class Meta:
        db_table = "Weterynarz"

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Kierownik(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imie = models.CharField(max_length=250)
    nazwisko = models.CharField(max_length=250)

    class Meta:
        db_table = "Kierownik"

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Zwierze(models.Model):
    class Typ(models.TextChoices):
        PIES = 'Pies', 'pies'
        KOT = 'Kot', 'kot'

    class Status(models.TextChoices):
        ZAJETE = 'Zajęte', 'zajęte'
        WOLNE = 'Wolne', 'wolne'

    pracownik = models.ForeignKey(Pracownik, on_delete=models.DO_NOTHING, related_name='pracownik_zwierze', null=True, default=None)
    imie = models.CharField(max_length=250, unique=True)
    typ = models.CharField(max_length=4, choices=Typ.choices, default=Typ.PIES)
    rasa = models.CharField(max_length=250)
    szacowany_wiek = models.IntegerField(validators=[MaxValueValidator(16), MinValueValidator(1)])
    numer_ewidencyjny = models.IntegerField(unique=True)
    adoptowane = models.BooleanField(default=False)
    kojec = models.BooleanField(default=False)

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = "Zwierze"

    def __str__(self):
        return self.imie


class Kojec(models.Model):
    class Typ(models.TextChoices):
        PIES = 'Pies', 'pies'
        KOT = 'Kot', 'kot'

    class Status(models.TextChoices):
        ZAJETE = 'Zajęte', 'zajęte'
        WOLNE = 'Wolne', 'wolne'

    # zwierze = models.ForeignKey(Zwierze, on_delete=models.SET_DEFAULT, related_name='zwierze_kojec', null=True, default=None)
    zwierze = models.OneToOneField(Zwierze, on_delete=models.SET_DEFAULT, related_name='zwierze_kojec', default=None, null=True)
    pracownik = models.ForeignKey(Pracownik, on_delete=models.DO_NOTHING, related_name='pracownik_kojec', null=True, default=None)
    typ = models.CharField(max_length=4, choices=Typ.choices, default=Typ.PIES)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.WOLNE)
    numer = models.IntegerField()

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = "Kojec"

    def __str__(self):
        return self.status


class Kwarantanna(models.Model):
    class StatusKwarantanny(models.TextChoices):
        ODBYWANA = 'Odbywana', 'odbywana'
        NIEODBYWANA = 'Nieodbywana', 'nieodbywana'

    zwierze = models.ForeignKey(Zwierze, on_delete=models.CASCADE, related_name='zwierze_kwarantanna', null=True, default=None)
    weterynarz = models.ForeignKey(Weterynarz, on_delete=models.DO_NOTHING, related_name='weterynarz_kwarantanna', null=True, default=None)
    status = models.CharField(max_length=11, choices=StatusKwarantanny.choices, default=StatusKwarantanny.NIEODBYWANA)
    miejsce = models.IntegerField(null=True, unique=True, default=None)
    data_rozpoczecia = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = "Kwarantanna"

    def __str__(self):
        return self.status


class Badanie(models.Model):
    zwierze = models.ForeignKey(Zwierze, on_delete=models.CASCADE, related_name='zwierze_badanie', null=True)
    weterynarz = models.ForeignKey(Weterynarz, on_delete=models.DO_NOTHING, related_name='weterynarz_badanie')
    rodzaj_badania = models.CharField(max_length=250)
    data_badania = models.DateField()

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = "Badanie"

    def __str__(self):
        return self.rodzaj_badania


class KartaZdrowia(models.Model):
    zwierze = models.ForeignKey(Zwierze, on_delete=models.CASCADE, related_name='zwierze_karta_zdrowia', null=True)
    weterynarz = models.ForeignKey(Weterynarz, on_delete=models.DO_NOTHING, related_name='weterynarz_karta_zdrowia')
    szczepionka = models.CharField(max_length=250)
    data_szczepienia = models.DateField()
    data_nastepnego_szczepienia = models.DateField()

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = "KartaZdrowia"

    def __str__(self):
        return self.szczepionka


class Adopcja(models.Model):
    imie_adoptujacego = models.CharField(max_length=250)
    nazwisko_adoptujacego = models.CharField(max_length=250)
    email_adoptujacego = models.EmailField(unique=True)
    numer_telefonu_adoptujacego = models.IntegerField(unique=True)
    data_adopcji = models.DateTimeField(default=timezone.now)
    zwierze = models.OneToOneField(Zwierze, on_delete=models.CASCADE, related_name='zwierze_adopcja')
    pracownik = models.ForeignKey(Pracownik, on_delete=models.DO_NOTHING, related_name='pracownik_adopcja', default=None)

    objects = models.Manager()  # Menadżer domyślny

    class Meta:
        db_table = 'Adopcja'

    def __str__(self):
        return f'{self.imie_adoptujacego} {self.nazwisko_adoptujacego}'
