from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RejestracjaZwierze, AdopcjaZwierzeModel, RejestracjaKarta, RejestracjaBadanie, \
    UpdateKojecPies, UpdateKojecKot, UpdateKwarantanna
from .models import Zwierze, Kojec, KartaZdrowia, Badanie, Kwarantanna, Adopcja
from django.contrib import messages
from django.utils import timezone


@login_required
def dashboard(request):
    return render(request, 'schronisko/dashboard.html', {'section': 'dashboard'})


@login_required
def add_animal(request):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        animal_form = RejestracjaZwierze(request.POST)
        if animal_form.is_valid():
            new_animal = animal_form.save(commit=False)
            new_animal.pracownik = request.user.pracownik
            new_animal.save()
            Zwierze.adoptowane = False
            kwarantanna = Kwarantanna(zwierze=new_animal, weterynarz=None, status="Nieodbywana")
            kwarantanna.save()
            messages.success(request, 'Udało się zarejestrować zwierze.')
            return redirect('rejestruj_zwierze')
        else:
            messages.error(request, 'Wystąpił błąd podczas rejestracji zwierzęcia.')
    else:
        animal_form = RejestracjaZwierze()
    return render(request, 'schronisko/rejestruj_zwierze.html', {'animal_form': animal_form})


@login_required
def adopt_animal_model(request):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if request.method == "POST":
        adopt_form = AdopcjaZwierzeModel(request.POST)
        if adopt_form.is_valid():
            new_adopt = adopt_form.save(commit=False)
            new_adopt.pracownik = request.user.pracownik
            new_adopt.save()
            zwierze = Zwierze.objects.get(id=new_adopt.zwierze.id)
            zwierze.adoptowane = True
            zwierze.kojec = False
            update_kojec = Kojec.objects.get(zwierze=zwierze)
            if update_kojec:
                update_kojec.zwierze = None
                update_kojec.pracownik = None
                update_kojec.status = "Wolne"
                update_kojec.save()
            zwierze.save()
            messages.success(request, 'Udało się zapisać adopcję zwierzęcia.')
            return redirect('adoptuj_zwierze')
        else:
            messages.error(request, 'Wystąpił błąd podczas zapisywania adopcji zwierzęcia.')
    else:
        adopt_form = AdopcjaZwierzeModel()
    return render(request, 'schronisko/adoptuj_zwierze.html', {'adopt_form': adopt_form})


@login_required
def animal_list(request, order=""):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if order:
        animals = Zwierze.objects.filter(adoptowane=False).order_by(order)
    else:
        animals = Zwierze.objects.filter(adoptowane=False)
    return render(request, 'schronisko/lista_zwierze.html', {'animals': animals})


@login_required
def adoption_list(request, order=""):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if order:
        adoptions = Adopcja.objects.all().order_by(order)
    else:
        adoptions = Adopcja.objects.all()
    return render(request, 'schronisko/lista_adopcji.html', {'adoptions': adoptions})


@login_required
def animal_delete(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    animal = Zwierze.objects.get(id=id)
    return render(request, 'schronisko/usun_zwierze.html', {'animal': animal})


@login_required
def animal_delete_done(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    animal = Zwierze.objects.get(id=id)
    try:
        kojec = Kojec.objects.get(zwierze=animal)
        kojec.status = "Wolne"
        kojec.save()
    except:
        pass
    animal.delete()
    return redirect('lista_zwierze')


@login_required
def kojec_list(request, order=''):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if order:
        kojce = Kojec.objects.all().order_by(order)
    else:
        kojce = Kojec.objects.all()
    cats = Zwierze.objects.filter(typ='Kot').filter(kojec=False).filter(adoptowane=False)
    dogs = Zwierze.objects.filter(typ='Pies').filter(kojec=False).filter(adoptowane=False)
    return render(request, 'schronisko/lista_kojec.html', {'kojce': kojce, 'cats': cats, 'dogs': dogs})


@login_required
def dodaj_zwierze_kojec_pies(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        update_kojec_form = UpdateKojecPies(request.POST)
        if update_kojec_form.is_valid():
            cd = update_kojec_form.cleaned_data
            new_kojec = Kojec.objects.get(id=id)
            new_kojec.zwierze = cd['zwierze']
            update_zwierze = new_kojec.zwierze
            update_zwierze.kojec = True
            update_zwierze.save()
            new_kojec.pracownik = request.user.pracownik
            new_kojec.status = "Zajęte"
            new_kojec.save()
            messages.success(request, 'Udało się przypisać zwierze do kojca.')
            return redirect('lista_kojec')
        else:
            messages.error(request, 'Wystąpił błąd podczas przypisywania zwierzaka do kojca.')
    else:
        update_kojec_form = UpdateKojecPies()
    return render(request, 'schronisko/dodaj_zwierze_kojec.html', {'update_kojec_form': update_kojec_form})


@login_required
def dodaj_zwierze_kojec_kot(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        update_kojec_form = UpdateKojecKot(request.POST)
        if update_kojec_form.is_valid():
            cd = update_kojec_form.cleaned_data
            new_kojec = Kojec.objects.get(id=id)
            new_kojec.zwierze = cd['zwierze']
            update_zwierze = new_kojec.zwierze
            update_zwierze.kojec = True
            update_zwierze.save()
            new_kojec.pracownik = request.user.pracownik
            new_kojec.status = "Zajęte"
            new_kojec.save()
            messages.success(request, 'Udało się przypisać zwierze do kojca.')
            return redirect('lista_kojec')
        else:
            messages.error(request, 'Wystąpił błąd podczas przypisywania zwierzaka do kojca.')
    else:
        update_kojec_form = UpdateKojecKot()
    return render(request, 'schronisko/dodaj_zwierze_kojec.html', {'update_kojec_form': update_kojec_form})


@login_required
def usun_zwierze_kojec(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    new_kojec = Kojec.objects.get(id=id)
    old_animal = new_kojec.zwierze
    old_animal.kojec = False
    old_animal.save()
    return render(request, 'schronisko/usun_zwierze_kojec.html', {'old_animal': old_animal, 'id': id})


@login_required
def zwierze_kojec_done(request, id):
    try:
        request.user.pracownik
    except:
        return redirect('dashboard')
    new_kojec = Kojec.objects.get(id=id)
    new_kojec.zwierze = None
    new_kojec.pracownik = request.user.pracownik
    new_kojec.status = "Wolne"
    new_kojec.save()
    messages.success(request, 'Udało się wypisać zwierze z kojca.')
    return redirect('lista_kojec')


@login_required
def karty_list(request, order=""):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if order:
        karty = KartaZdrowia.objects.all().order_by(order)
    else:
        karty = KartaZdrowia.objects.all()
    return render(request, 'schronisko/lista_karty.html', {'karty': karty})


@login_required
def add_karta(request):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        karta_form = RejestracjaKarta(request.POST)
        if karta_form.is_valid():
            new_karta = karta_form.save(commit=False)
            new_karta.weterynarz = request.user.weterynarz
            new_karta.save()
            messages.success(request, 'Udało się dodać kartę.')
            return redirect('lista_karty')
        else:
            messages.error(request, 'Wystąpił błąd podczas dodawania wpisu.')
    else:
        karta_form = RejestracjaKarta()
    return render(request, 'schronisko/dodaj_karte.html', {'karta_form': karta_form})


@login_required
def add_badanie(request):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        badanie_form = RejestracjaBadanie(request.POST)
        if badanie_form.is_valid():
            new_badanie = badanie_form.save(commit=False)
            new_badanie.weterynarz = request.user.weterynarz
            new_badanie.save()
            messages.success(request, 'Udało się dodać badanie.')
            return redirect('lista_badania')
        else:
            messages.error(request, 'Wystąpił błąd podczas dodawania badania.')
    else:
        badanie_form = RejestracjaBadanie()
    return render(request, 'schronisko/dodaj_badanie.html', {'badanie_form': badanie_form})


@login_required
def badanie_list(request, order=""):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if order:
        badania = Badanie.objects.all().order_by(order)
    else:
        badania = Badanie.objects.all()
    return render(request, 'schronisko/lista_badania.html', {'badania': badania})


@login_required
def add_kwarantanna(request, id):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        miejsce_form = UpdateKwarantanna(request.POST)
        if miejsce_form.is_valid():
            cd = miejsce_form.cleaned_data
            new_kwarantanna = Kwarantanna.objects.get(id=id)
            new_kwarantanna.miejsce = cd['miejsce']
            new_kwarantanna.status = "Odbywana"
            new_kwarantanna.data_rozpoczecia = timezone.now()
            new_kwarantanna.save()
            messages.success(request, 'Udało się dodać kwarantannę.')
            return redirect('lista_kwarantanna')
        else:
            messages.error(request, 'Wystąpił błąd podczas dodawania kwarantanny.')
    else:
        miejsce_form = UpdateKwarantanna()
    return render(request, 'schronisko/dodaj_kwarantanna.html', {'miejsce_form': miejsce_form})

@login_required
def delete_kwarantanna(request, id):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    new_kwarantanna = Kwarantanna.objects.get(id=id)
    new_kwarantanna.status = "Nieodbywana"
    new_kwarantanna.miejsce = None
    new_kwarantanna.data_rozpoczecia = timezone.now()
    new_kwarantanna.save()
    return render(request, 'schronisko/usun_kwarantanna.html', {'new_kwarantanna': new_kwarantanna})


@login_required
def add_kwarantanna_done(request):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    messages.success(request, 'Udało się zaktualizować status kwarantanny.')
    return redirect('lista_kwarantanna')


@login_required
def kwarantanna_list(request, order=""):
    try:
        request.user.weterynarz
    except:
        return redirect('dashboard')
    if order:
        kwarantannay = Kwarantanna.objects.all().order_by(order)
    else:
        kwarantannay = Kwarantanna.objects.all()
    return render(request, 'schronisko/lista_kwarantanna.html', {'kwarantannay': kwarantannay})
