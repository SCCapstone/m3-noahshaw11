from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.exceptions import *
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import requests

API_URL = 'https://raider.io/api/v1/'

@csrf_exempt
def home(request):
   template = loader.get_template('form.html')
   return HttpResponse(template.render())

@csrf_exempt
def search(request):
    if request.method == 'POST':
        region = request.POST.get('regions', None)
        realm = request.POST.get('realm', None)
        character_name = request.POST.get('character_name', None)
        try:
            response = requests.get(API_URL + 'characters/profile?region=' + region + '&realm=' + realm + '&name=' + character_name + '&fields=gear,raid_progression,mythic_plus_ranks').json()
            results = create_response(response)
            return HttpResponse(results)
        except:
            return render(request, 'form.html')
    else:
        return render(request, 'form.html')

def create_response(json_obj):
    thumbnail = json_obj['thumbnail_url']
    name = json_obj['name']
    realm = json_obj['realm']
    race = json_obj['race']
    gender = json_obj['gender']
    character_class = json_obj['class']
    spec = json_obj['active_spec_name']
    achievement_points = json_obj['achievement_points']
    ilvl = json_obj['gear']['item_level_equipped']
    current_raid_progression = json_obj['raid_progression']['nyalotha-the-waking-city']['summary']
    current_mythic_plus_ranking = json_obj['mythic_plus_ranks']['overall']['world']
    response = """
    <form method="POST" action="/home/">
    <html>
    <img src=""" + thumbnail + """alt="Character Picture">
    <h1 for="websites">""" + name + """ - """ + realm + """</h1>
    <label for="textfield"><strong>Gender/Race:</strong> """ + gender.capitalize() + """ """ + race + """</label><br><br>
    <label for="textfield"><strong>Spec/Class:</strong> """ + spec + """ """ + character_class + """</label><br><br>
    <label for="textfield"><strong>Item Level:</strong> """ + str(ilvl) + """</label><br><br>
    <label for="textfield"><strong>Current Raid Progression:</strong> """ + current_raid_progression + """</label><br><br>
    <label for="textfield"><strong>Current Mythic Plus Ranking:</strong> """ + str(current_mythic_plus_ranking) + """</label><br><br>
    <button type="back">Back</button>
    </html>
    </form>"""
    return response
