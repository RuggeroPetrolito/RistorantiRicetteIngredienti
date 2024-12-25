import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import Ristorante, Ricetta, Ingrediente, RistoranteToRicetta, RicettaToIngrediente
import json

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# crea un formatter per definire il formato dei log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# crea un handler per scrivere i log su file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# crea uno stream handler per stampare i log sulla console
console_handler = logging.StreamHandler()
# il livello di logging può essere settato su uno dei seguenti valori:
# - NOTSET
# - DEBUG
# - INFO
# - WARNING
# - ERROR
# - CRITICAL
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# aggiunge gli handler al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def index(request):
    """
    Vista per la pagina di indice.
    """
    logger.info("Accesso alla pagina di indice")
    return HttpResponse("Hello, world. You're at the restaurants/recipes/ingredients index.")

def lista_ristoranti(request):
    """
    Vista per ottenere la lista di tutti i ristoranti.
    Metodo: GET
    """
    logger.info("Richiesta per ottenere la lista di tutti i ristoranti")
    ristoranti = Ristorante.objects.all().values()
    return JsonResponse(list(ristoranti), safe=False)

def ristoranti_per_ricetta(request):
    """
    Vista per ottenere i ristoranti che cucinano una specifica ricetta.
    Metodo: GET
    Parametri:
        - ricetta_id: ID della ricetta
    """
    logger.info("Richiesta per ottenere i ristoranti che cucinano una specifica ricetta")
    if request.method == 'GET':
        ricetta_id = request.GET.get('ricetta_id')
        if not ricetta_id:
            logger.warning("Parametro 'ricetta_id' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_id' parameter")
        try:
            ricetta = Ricetta.objects.get(id=ricetta_id)
            ristoranti = Ristorante.objects.filter(ristorantetoricetta__ricetta=ricetta).values()
            logger.info(f"Ristoranti trovati per la ricetta {ricetta_id}: {list(ristoranti)}")
            return JsonResponse(list(ristoranti), safe=False)
        except Ricetta.DoesNotExist:
            logger.error(f"Ricetta con id {ricetta_id} non trovata")
            return JsonResponse({'error': 'Ricetta non trovata'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def ricette_per_ristorante(request):
    """
    Vista per ottenere le ricette relative ad un ristorante specificato.
    Metodo: GET
    Parametri:
        - ristorante_id: ID del ristorante
    """
    logger.info("Richiesta per ottenere le ricette relative ad un ristorante specificato")
    if request.method == 'GET':
        ristorante_id = request.GET.get('ristorante_id')
        if not ristorante_id:
            logger.warning("Parametro 'ristorante_id' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_id' parameter")
        try:
            ristorante = Ristorante.objects.get(id=ristorante_id)
            ricette = Ricetta.objects.filter(ristorantetoricetta__ristorante=ristorante).values()
            logger.info(f"Ricette trovate per il ristorante {ristorante_id}: {list(ricette)}")
            return JsonResponse(list(ricette), safe=False)
        except Ristorante.DoesNotExist:
            logger.error(f"Ristorante con id {ristorante_id} non trovato")
            return JsonResponse({'error': 'Ristorante non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def ricette_per_ingrediente(request):
    """
    Vista per ottenere le ricette che contengono un ingrediente specificato.
    Metodo: GET
    Parametri:
        - ingrediente_id: ID dell'ingrediente
    """
    logger.info("Richiesta per ottenere le ricette che contengono un ingrediente specificato")
    if request.method == 'GET':
        ingrediente_id = request.GET.get('ingrediente_id')
        if not ingrediente_id:
            logger.warning("Parametro 'ingrediente_id' mancante")
            return HttpResponseBadRequest("Missing 'ingrediente_id' parameter")
        try:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            ricette = Ricetta.objects.filter(ricettatoingrediente__ingrediente=ingrediente).values()
            logger.info(f"Ricette trovate per l'ingrediente {ingrediente_id}: {list(ricette)}")
            return JsonResponse(list(ricette), safe=False)
        except Ingrediente.DoesNotExist:
            logger.error(f"Ingrediente con id {ingrediente_id} non trovato")
            return JsonResponse({'error': 'Ingrediente non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")
    
def ingredienti_per_ricetta(request):
    """
    Vista per ottenere gli ingredienti relativi ad una ricetta specificata.
    Metodo: GET
    Parametri:
        - ricetta_id: ID della ricetta
    """
    logger.info("Richiesta per ottenere gli ingredienti relativi ad una ricetta specificata")
    if request.method == 'GET':
        ricetta_id = request.GET.get('ricetta_id')
        if not ricetta_id:
            logger.warning("Parametro 'ricetta_id' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_id' parameter")
        try:
            ricetta = Ricetta.objects.get(id=ricetta_id)
            ingredienti = Ingrediente.objects.filter(ricettatoingrediente__ricetta=ricetta).values()
            logger.info(f"Ingredienti trovati per la ricetta {ricetta_id}: {list(ingredienti)}")
            return JsonResponse(list(ingredienti), safe=False)
        except Ricetta.DoesNotExist:
            logger.error(f"Ricetta con id {ricetta_id} non trovata")
            return JsonResponse({'error': 'Ricetta non trovata'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def ingredienti_per_ristorante(request):
    """
    Vista per ottenere gli ingredienti utilizzati in uno specifico ristorante
    Metodo: GET
    Parametri:
        - ristorante_id: ID del ristorante
    """
    logger.info("Richiesta per ottenere gli ingredienti utilizzati in uno specifico ristorante")
    if request.method == 'GET':
        ristorante_id = request.GET.get('ristorante_id')
        if not ristorante_id:
            logger.warning("Parametro 'ristorante_id' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_id' parameter")
        try:
            ristorante = Ristorante.objects.get(id=ristorante_id)
            ricette = Ricetta.objects.filter(ristorantetoricetta__ristorante=ristorante)
            logger.info(f"Ricette trovate per il ristorante {ristorante_id}: {list(ricette)}")
            ingredienti = Ingrediente.objects.filter(ricettatoingrediente__ricetta__in=ricette).values()
            logger.info(f"Ingredienti trovati per il ristorante {ristorante_id}: {list(ingredienti)}")
            return JsonResponse(list(ingredienti), safe=False)
        except Ristorante.DoesNotExist:
            logger.error(f"Ristorante con id {ristorante_id} non trovato")
            return JsonResponse({'error': 'Ristorante non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def create_ristorante(request):
    """
    Vista per creare un nuovo ristorante.
    Metodo: GET
    Parametri:
        - ristorante_text: Nome del ristorante
    """
    logger.info("Richiesta per creare un nuovo ristorante")
    if request.method == 'GET':
        ristorante_text = request.GET.get('ristorante_text')
        if not ristorante_text:
            logger.warning("Parametro 'ristorante_text' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_text' parameter")
        ristorante = Ristorante.objects.create(ristorante_text=ristorante_text)
        logger.info(f"Ristorante creato: {ristorante.id}, {ristorante.ristorante_text}")
        return JsonResponse({'id': ristorante.id, 'ristorante_text': ristorante.ristorante_text})
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def update_ristorante(request):
    """
    Vista per aggiornare un ristorante esistente.
    Metodo: GET
    Parametri:
        - ristorante_id: ID del ristorante
        - ristorante_text: Nuovo nome del ristorante
    """
    logger.info("Richiesta per aggiornare un ristorante esistente")
    if request.method == 'GET':
        ristorante_id = request.GET.get('ristorante_id')
        ristorante_text = request.GET.get('ristorante_text')
        if not ristorante_id and not ristorante_text:
            logger.warning("Parametri 'ristorante_id' e 'ristorante_text' mancanti")
            return HttpResponseBadRequest("Missing 'ristorante_id' and 'ristorante_text' parameters")
        elif not ristorante_id:
            logger.warning("Parametro 'ristorante_id' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_id' parameter")
        elif not ristorante_text:
            logger.warning("Parametro 'ristorante_text' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_text' parameter")
        try:
            ristorante = Ristorante.objects.get(id=ristorante_id)
            ristorante.ristorante_text = ristorante_text
            ristorante.save()
            logger.info(f"Ristorante aggiornato: {ristorante.id}, {ristorante.ristorante_text}")
            return JsonResponse({'id': ristorante.id, 'ristorante_text': ristorante.ristorante_text})
        except Ristorante.DoesNotExist:
            logger.error(f"Ristorante con id {ristorante_id} non trovato")
            return JsonResponse({'error': 'Ristorante non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def delete_ristorante(request):
    """
    Vista per eliminare un ristorante esistente.
    Metodo: GET
    Parametri:
        - ristorante_id: ID del ristorante
    """
    logger.info("Richiesta per eliminare un ristorante esistente")
    if request.method == 'GET':
        ristorante_id = request.GET.get('ristorante_id')
        if not ristorante_id:
            logger.warning("Parametro 'ristorante_id' mancante")
            return HttpResponseBadRequest("Missing 'ristorante_id' parameter")
        try:
            ristorante = Ristorante.objects.get(id=ristorante_id)
            ristorante.delete()
            logger.info(f"Ristorante eliminato: {ristorante.id}, {ristorante.ristorante_text}")
            return JsonResponse({
                'message': 'Ristorante deleted',
                'id': ristorante_id,
                'ristorante_text': ristorante.ristorante_text
            })
        except Ristorante.DoesNotExist:
            logger.error(f"Ristorante con id {ristorante_id} non trovato")
            return JsonResponse({'error': 'Ristorante non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def create_ricetta(request):
    """
    Vista per creare una nuova ricetta.
    Metodo: GET
    Parametri:
        - ricetta_text: nome della ricetta
    """
    logger.info("Richiesta per creare una nuova ricetta")
    if request.method == 'GET':
        ricetta_text = request.GET.get('ricetta_text')
        if not ricetta_text:
            logger.warning("Parametro 'ricetta_text' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_text' parameter")
        ricetta = Ricetta.objects.create(ricetta_text=ricetta_text)
        logger.info(f"Ricetta creata: {ricetta.id}, {ricetta.ricetta_text}")
        return JsonResponse({'id': ricetta.id, 'ricetta_text': ricetta.ricetta_text})
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def update_ricetta(request):
    """
    Vista per aggiornare una ricetta esistente.
    Metodo: GET
    Parametri:
        - ricetta_id: ID della ricetta
        - ricetta_text: Nuovo nome della ricetta
    """
    logger.info("Richiesta per aggiornare una ricetta esistente")
    if request.method == 'GET':
        ricetta_id = request.GET.get('ricetta_id')
        ricetta_text = request.GET.get('ricetta_text')
        if not ricetta_id and not ricetta_text:
            logger.warning("Parametri 'ricetta_id' e 'ricetta_text' mancanti")
            return HttpResponseBadRequest("Missing 'ricetta_id' and 'ricetta_text' parameter")
        elif not ricetta_id:
            logger.warning("Parametro 'ricetta_id' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_id' parameter")
        elif not ricetta_text:
            logger.warning("Parametro 'ricetta_text' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_text' parameter")
        try:
            ricetta = Ricetta.objects.get(id=ricetta_id)
            ricetta.ricetta_text = ricetta_text
            ricetta.save()
            logger.info(f"Ricetta aggiornata: {ricetta.id}, {ricetta.ricetta_text}")
            return JsonResponse({'id': ricetta.id, 'ricetta_text': ricetta.ricetta_text})
        except Ricetta.DoesNotExist:
            logger.error(f"Ricetta con id {ricetta_id} non trovata")
            return JsonResponse({'error': 'Ricetta non trovata'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def delete_ricetta(request):
    """
    Vista per eliminare una ricetta esistente.
    Metodo: GET
    Parametri:
        - ricetta_id: ID della ricetta
    """
    logger.info("Richiesta per eliminare una ricetta esistente")
    if request.method == 'GET':
        ricetta_id = request.GET.get('ricetta_id')
        if not ricetta_id:
            logger.warning("Parametro 'ricetta_id' mancante")
            return HttpResponseBadRequest("Missing 'ricetta_id' parameter")
        try:
            ricetta = Ricetta.objects.get(id=ricetta_id)
            ricetta.delete()
            logger.info(f"Ricetta eliminata: {ricetta.id}, {ricetta.ricetta_text}")
            return JsonResponse({'message': 'Ricetta deleted', 'id': ricetta_id, 'ricetta_text': ricetta.ricetta_text})
        except Ricetta.DoesNotExist:
            logger.error(f"Ricetta con id {ricetta_id} non trovata")
            return JsonResponse({'error': 'Ricetta non trovata'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def create_ingrediente(request):
    """
    Vista per creare un nuovo ingrediente.
    Metodo: GET
    Parametri:
        - ingrediente_text: Nome dell'ingrediente
    """
    logger.info("Richiesta per creare un nuovo ingrediente")
    if request.method == 'GET':
        ingrediente_text = request.GET.get('ingrediente_text')
        if not ingrediente_text:
            logger.warning("Parametro 'ingrediente_text' mancante")
            return HttpResponseBadRequest("Missing 'ingrediente_text' parameter")
        ingrediente = Ingrediente.objects.create(ingrediente_text=ingrediente_text)
        logger.info(f"Ingrediente creato: {ingrediente.id}, {ingrediente.ingrediente_text}")
        return JsonResponse({'id': ingrediente.id, 'ingrediente_text': ingrediente.ingrediente_text})
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def update_ingrediente(request):
    """
    Vista per aggiornare un ingrediente esistente.
    Metodo: GET
    Parametri:
        - ingrediente_id: ID dell'ingrediente
        - ingrediente_text: Nuovo nome dell'ingrediente
    """
    logger.info("Richiesta per aggiornare un ingrediente esistente")
    if request.method == 'GET':
        ingrediente_id = request.GET.get('ingrediente_id')
        ingrediente_text = request.GET.get('ingrediente_text')
        if not ingrediente_id and not ingrediente_text:
            logger.warning("Parametri 'ingrediente_id' e 'ingrediente_text' mancanti")
            return HttpResponseBadRequest("Missing 'ingrediente_id' and 'ingrediente_text' parameter")
        elif not ingrediente_id:
            logger.warning("Parametro 'ingrediente_id' mancante")
            return HttpResponseBadRequest("Missing 'ingrediente_id' parameter")
        elif not ingrediente_text:
            logger.warning("Parametro 'ingrediente_text' mancante")
            return HttpResponseBadRequest("Missing 'ingrediente_text' parameter")
        try:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            ingrediente.ingrediente_text = ingrediente_text
            ingrediente.save()
            logger.info(f"Ingrediente aggiornato: {ingrediente.id}, {ingrediente.ingrediente_text}")
            return JsonResponse({'id': ingrediente.id, 'ingrediente_text': ingrediente.ingrediente_text})
        except Ingrediente.DoesNotExist:
            logger.error(f"Ingrediente con id {ingrediente_id} non trovato")
            return JsonResponse({'error': 'Ingrediente non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")

def delete_ingrediente(request):
    """
    Vista per eliminare un ingrediente esistente.
    Metodo: GET
    Parametri:
        - ingrediente_id: ID dell'ingrediente
    """
    logger.info("Richiesta per eliminare un ingrediente esistente")
    if request.method == 'GET':
        ingrediente_id = request.GET.get('ingrediente_id')
        if not ingrediente_id:
            logger.warning("Parametro 'ingrediente_id' mancante")
            return HttpResponseBadRequest("Missing 'ingrediente_id' parameter")
        try:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            ingrediente.delete()
            logger.info(f"Ingrediente eliminato: {ingrediente.id}, {ingrediente.ingrediente_text}")
            return JsonResponse({'message': 'Ingrediente deleted', 'id': ingrediente_id, 'ingrediente_text': ingrediente.ingrediente_text})
        except Ingrediente.DoesNotExist:
            logger.error(f"Ingrediente con id {ingrediente_id} non trovato")
            return JsonResponse({'error': 'Ingrediente non trovato'}, status=404)
    else:
        logger.warning("Metodo di richiesta non valido")
        return HttpResponseBadRequest("Invalid request method")