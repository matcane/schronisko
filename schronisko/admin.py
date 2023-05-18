from django.contrib import admin
from .models import Zwierze, Kojec, KartaZdrowia, Kwarantanna, Badanie, Pracownik, Weterynarz, Kierownik, Adopcja

admin.site.register(Zwierze)
admin.site.register(Kojec)
admin.site.register(Badanie)
admin.site.register(Kwarantanna)
admin.site.register(KartaZdrowia)
admin.site.register(Pracownik)
admin.site.register(Weterynarz)
admin.site.register(Kierownik)
admin.site.register(Adopcja)
