from django.urls import path
from . import views

urlpatterns = [
    # Endpoint per la pagina di indice
    path("", views.index, name="index"),
    
    # Endpoint per ottenere la lista di tutti i ristoranti
    path("api/ristoranti/", views.lista_ristoranti, name="lista_ristoranti"),
    
    # Endpoint per ottenere i ristoranti che cucinano la ricetta specificata
    path("api/ristoranti/ricetta/", views.ristoranti_per_ricetta, name="ristoranti_per_ricetta"),

    # Endpoint per ottenere le ricette relative ad un ristorante specificato
    path("api/ricette/ristorante/", views.ricette_per_ristorante, name="ricette_per_ristorante"),

    # Endpoint per ottenere le ricette che contengono un ingrediente specificato
    path("api/ricette/ingrediente/", views.ricette_per_ingrediente, name="ricette_per_ingrediente"),

    # Endpoint per ottenere gli ingredienti relativi ad una ricetta specificata
    path("api/ingredienti/ricetta/", views.ingredienti_per_ricetta, name="ingredienti_per_ricetta"),

    # Endpoint per ottenere gli ingredienti utilizzati da un ristorante specificato
    path("api/ingredienti/ristorante/", views.ingredienti_per_ristorante, name="ingredienti_per_ristorante"),
    
    # Endpoint per creare un nuovo ristorante
    path("api/ristoranti/create/", views.create_ristorante, name="create_ristorante"),
    
    # Endpoint per aggiornare un ristorante esistente
    path("api/ristoranti/update/", views.update_ristorante, name="update_ristorante"),
    
    # Endpoint per eliminare un ristorante esistente
    path("api/ristoranti/delete/", views.delete_ristorante, name="delete_ristorante"),
    
    # Endpoint per creare una nuova ricetta
    path("api/ricette/create/", views.create_ricetta, name="create_ricetta"),
    
    # Endpoint per aggiornare una ricetta esistente
    path("api/ricette/update/", views.update_ricetta, name="update_ricetta"),
    
    # Endpoint per eliminare una ricetta esistente
    path("api/ricette/delete/", views.delete_ricetta, name="delete_ricetta"),
    
    # Endpoint per creare un nuovo ingrediente
    path("api/ingredienti/create/", views.create_ingrediente, name="create_ingrediente"),
    
    # Endpoint per aggiornare un ingrediente esistente
    path("api/ingredienti/update/", views.update_ingrediente, name="update_ingrediente"),
    
    # Endpoint per eliminare un ingrediente esistente
    path("api/ingredienti/delete/", views.delete_ingrediente, name="delete_ingrediente"),
]