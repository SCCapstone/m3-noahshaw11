from django.core.exceptions import *
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import requests

# Base API URL for raider.io
API_URL = 'https://raider.io/api/v1/'

# Display initial form.html template to the client
@csrf_exempt
def home(request):
   template = loader.get_template('form.html')
   return HttpResponse(template.render())

# Use the API of raider.io to retrieve WoW stats of the character inputted by the user
@csrf_exempt
def search(request):
    if request.method == 'POST':
        # Retrieve the information inputted by the client
        region = request.POST.get('regions', None)
        realm = request.POST.get('realm', None)
        character_name = request.POST.get('character_name', None)
        try:
            # Send a GET request to the API of raider.io using the infomration inputted by the client
            response = requests.get(API_URL + 'characters/profile?region=' + region + '&realm=' + realm + '&name=' + character_name + '&fields=gear,raid_progression,mythic_plus_ranks').json()
            results = create_response(response)
            # Return the retreived stats to the client
            return HttpResponse(results)
        except:
            return render(request, 'form.html')
    else:
        return render(request, 'form.html')

# Create a response html message to send back to the client that displays the retrieved stats
def create_response(json_obj):
    # Extract the stats from the json message retrieved from raider.io
    thumbnail = json_obj['thumbnail_url']
    name = json_obj['name']
    realm = json_obj['realm']
    race = json_obj['race']
    gender = json_obj['gender']
    character_class = json_obj['class']
    spec = json_obj['active_spec_name']
    achievement_points = json_obj['achievement_points']
    ilvl = json_obj['gear']['item_level_equipped']
    nyalotha_raid_progression = json_obj['raid_progression']['nyalotha-the-waking-city']['summary']
    eternal_palace_raid_progression = json_obj['raid_progression']['the-eternal-palace']['summary']
    crucible_of_storms_raid_progression = json_obj['raid_progression']['crucible-of-storms']['summary']
    battle_of_dazaralor_raid_progression = json_obj['raid_progression']['battle-of-dazaralor']['summary']
    uldir_raid_progression = json_obj['raid_progression']['uldir']['summary']
    current_mythic_plus_ranking = json_obj['mythic_plus_ranks']['overall']['world']
    
    # Format an html response to send back to the client using the retrieved stats
    response = """
    <form method="POST" action="/home/">
    <html>
    <img src=""" + thumbnail + """alt="Character Picture">
    <h1 for="websites">""" + name + """ - """ + realm + """</h1>
    <label for="textfield"><strong>Gender/Race:</strong> """ + gender.capitalize() + """ """ + race + """</label><br><br>
    <label for="textfield"><strong>Spec/Class:</strong> """ + spec + """ """ + character_class + """</label><br><br>
    <label for="textfield"><strong>Item Level:</strong> """ + str(ilvl) + """</label><br><br>
    
    <label for="raids"><strong>Raid Progression:</strong></label>
    <select name="raids" id="raids" onchange="changeProgression()">
        <option value="Ny'alotha the Waking City">Ny'alotha the Waking City</option>
        <option value="The Eternal Palace">The Eternal Palace</option>
        <option value="Crucible of Storms">Crucible of Storms</option>
        <option value="Battle of Dazaralor">Battle of Dazaralor</option>
        <option value="Uldir">Uldir</option>
    </select>
    <label id="progression" for="progression">Select a Raid<strong></strong></label><br><br>
    <script type="text/javascript">
        function changeProgression() {
            let lbl = document.getElementById('progression')
            let raid = document.getElementById('raids').value
            if (raid == "Ny'alotha the Waking City") {
                lbl.innerText = '""" + nyalotha_raid_progression + """';
            } else if (raid == "Ny'alotha the Waking City") {
                lbl.innerText = '""" + eternal_palace_raid_progression + """';
            } else if (raid == "The Eternal Palace") {
                lbl.innerText = '""" + eternal_palace_raid_progression + """';
            } else if (raid == "Crucible of Storms") {
                lbl.innerText = '""" + crucible_of_storms_raid_progression + """';
            } else if (raid == "Battle of Dazaralor") {
                lbl.innerText = '""" + battle_of_dazaralor_raid_progression + """';
            } else if (raid == "Uldir") {
                lbl.innerText = '""" + uldir_raid_progression + """';
            }
        }
    </script>
    
    <label for="textfield"><strong>Current Mythic Plus Ranking (World):</strong> """ + str(current_mythic_plus_ranking) + """</label><br><br>
    <button type="back">Back</button>
    </html>
    </form>"""
    
    # Return the html message
    return response
