from django import forms
from .models import Zwierze, Adopcja, KartaZdrowia, Badanie, Kojec, Kwarantanna


class RejestracjaZwierze(forms.ModelForm):
    class Meta:
        model = Zwierze
        fields = ('imie', 'typ', 'rasa', 'szacowany_wiek', 'numer_ewidencyjny')


class AdopcjaZwierze(forms.Form):
    imie = forms.CharField()
    nazwisko = forms.CharField()
    email = forms.EmailField()
    numer = forms.IntegerField()
    zwierze = forms.ModelChoiceField(queryset=Zwierze.objects.filter(adoptowane=False))


class AdopcjaZwierzeModel(forms.ModelForm):
    zwierze = forms.ModelChoiceField(queryset=Zwierze.objects.exclude(zwierze_kwarantanna__status=Kwarantanna.StatusKwarantanny.ODBYWANA).filter(adoptowane=False))

    class Meta:
        model = Adopcja
        fields = ("imie_adoptujacego", "nazwisko_adoptujacego", "email_adoptujacego", "numer_telefonu_adoptujacego",
                  "zwierze")


class RejestracjaKarta(forms.ModelForm):
    class Meta:
        model = KartaZdrowia
        fields = ("zwierze", "szczepionka", "data_szczepienia", "data_nastepnego_szczepienia")
        widgets = {"data_szczepienia": forms.SelectDateWidget(),
                   "data_nastepnego_szczepienia": forms.SelectDateWidget()}


class RejestracjaBadanie(forms.ModelForm):
    class Meta:
        model = Badanie
        fields = ("zwierze", "rodzaj_badania", "data_badania")
        widgets = {"data_badania": forms.SelectDateWidget()}


class UpdateKojecPies(forms.ModelForm):
    zwierze = forms.ModelChoiceField(queryset=Zwierze.objects.filter(adoptowane=False).filter(typ='Pies').filter(kojec=False))

    class Meta:
        model = Kojec
        fields = ("zwierze",)


class UpdateKojecKot(forms.ModelForm):
    zwierze = forms.ModelChoiceField(queryset=Zwierze.objects.filter(adoptowane=False).filter(typ='Kot').filter(kojec=False))

    class Meta:
        model = Kojec
        fields = ("zwierze",)


class UpdateKwarantanna(forms.ModelForm):
    class Meta:
        model = Kwarantanna
        fields = ("miejsce",)
