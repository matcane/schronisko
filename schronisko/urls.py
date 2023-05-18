from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('rejestruj_zwierze/', views.add_animal, name='rejestruj_zwierze'),
    path('adoptuj_zwierze/', views.adopt_animal_model, name='adoptuj_zwierze'),
    path('lista_zwierze/', views.animal_list, name='lista_zwierze'),
    path('lista_zwierze/<slug:order>/', views.animal_list, name='lista_zwierze'),
    path('lista_adopcja/', views.adoption_list, name='lista_adopcji'),
    path('lista_adopcja/<slug:order>/', views.adoption_list, name='lista_adopcji'),
    path('lista_kojec/', views.kojec_list, name='lista_kojec'),
    path('lista_kojec/<slug:order>/', views.kojec_list, name='lista_kojec'),
    path('dodaj_zwierze_kojec_pies/<int:id>/', views.dodaj_zwierze_kojec_pies, name='dodaj_zwierze_kojec_pies'),
    path('dodaj_zwierze_kojec_kot/<int:id>/', views.dodaj_zwierze_kojec_kot, name='dodaj_zwierze_kojec_kot'),
    path('usun_zwierze_kojec/<int:id>/', views.usun_zwierze_kojec, name='usun_zwierze_kojec'),
    path('zwierze_kojec/done/<int:id>/', views.zwierze_kojec_done, name='zwierze_kojec_done'),
    path('lista_karty/', views.karty_list, name='lista_karty'),
    path('lista_karty/<slug:order>/', views.karty_list, name='lista_karty'),
    path('lista_badania/', views.badanie_list, name='lista_badania'),
    path('lista_badania/<slug:order>/', views.badanie_list, name='lista_badania'),
    path('lista_kwarantanna/', views.kwarantanna_list, name='lista_kwarantanna'),
    path('lista_kwarantanna/<slug:order>/', views.kwarantanna_list, name='lista_kwarantanna'),
    path('dodaj_karte/', views.add_karta, name='dodaj_karte'),
    path('dodaj_badanie/', views.add_badanie, name='dodaj_badanie'),
    path('dodaj_kwarantanna/<int:id>/', views.add_kwarantanna, name='dodaj_kwarantanna'),
    path('usun_kwarantanna/<int:id>/', views.delete_kwarantanna, name='usun_kwarantanna'),
    path('dodaj_kwarantanna/done/', views.add_kwarantanna_done, name='dodaj_kwarantanna_done'),
    path('usun_zwierze/<int:id>/', views.animal_delete, name='usun_zwierze'),
    path('usun_zwierze/done/<int:id>', views.animal_delete_done, name='usun_zwierze_done'),
]
