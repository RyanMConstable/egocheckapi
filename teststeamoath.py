from flask import Flask, redirect, request
from json import dumps
from urllib.parse import urlencode
import findMatchSteamAPI, CSGOsql

IP_ADDRESS = '10.0.0.130'

app = Flask(__name__)
app.debug = True

steam_openid_url = 'https://steamcommunity.com/openid/login'

@app.route("/")
def auth_with_steam():

  params = {
    'openid.ns': "http://specs.openid.net/auth/2.0",
    'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.mode': 'checkid_setup',
    'openid.return_to': f'http://{IP_ADDRESS}/authorize',
    'openid.realm': f'http://{IP_ADDRESS}'
  }

  query_string = urlencode(params)
  auth_url = steam_openid_url + "?" + query_string
  return redirect(auth_url)

@app.route("/authorize", methods = ['POST', 'GET'])
def authorize():
  if request.method == "POST":
    data = request.form
    steamid, steamidkey, gamecode, discordid = data["steamid"], data["steamidkey"], data["gamecode"], data["discordid"]
    if findMatchSteamAPI.trueValidation(data["steamid"], data["steamidkey"], data["gamecode"]) == False:
      return auth_with_steam()
    
    CSGOsql.setDiscordUser(data["discordid"], data["steamid"], data["steamidkey"])
    CSGOsql.newRecentGame(data["steamid"], data["gamecode"])
    return success()
  
  
  returnval = request.args
  userid = str(returnval['openid.claimed_id']).split("/")[-1]
  return f'''<form action="/authorize" method = "POST">
    <input type = "hidden" name = "steamid" value={userid}>
    <p>Your Steam id key and Match game code are required linking your discord is required for access through discord</p>
    <br>
    <p>Steam ID Key: <input type = "text" name = "steamidkey" placeholder = "XXXX-XXXXX-XXXX" required/></p>
    <p>Known Match Game Code: <input type = "text" name = "gamecode" placeholder = "CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx" required/></p>
    <p>To find your most recent Steam id key and match code go to the following link: <a href="https://help.steampowered.com/en/wizard/HelpWithGameIssue/?appid=730&issueid=128">SteamLink<a/></p>
    <br>
    <p>Open Discord, then right click your name and copy user ID</p>
    <p>DiscordID: <input type = "text" name = "discordid" placeholder = "18 numbers" required/></p>
    <p><input type = "submit" value = "submit" /></p>
</form>'''

@app.route("/success")
def success():
  return "<h1>You may now close your browser</h1>"
  
if __name__ == "__main__":
    app.run()
