from flask import Flask, redirect, request
from json import dumps
from urllib.parse import urlencode
import findMatchSteamAPI

app = Flask(__name__)
app.debug = True

steam_openid_url = 'https://steamcommunity.com/openid/login'

@app.route("/")
def hello():
    return '<a href="http://localhost:5000/auth">Login with steam</a>'

@app.route("/auth")
def auth_with_steam():

  params = {
    'openid.ns': "http://specs.openid.net/auth/2.0",
    'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
    'openid.mode': 'checkid_setup',
    'openid.return_to': 'http://127.0.0.1:5000/authorize',
    'openid.realm': 'http://127.0.0.1:5000'
  }

  query_string = urlencode(params)
  auth_url = steam_openid_url + "?" + query_string
  return redirect(auth_url)

@app.route("/authorize", methods = ['POST', 'GET'])
def authorize():
  if request.method == "POST":
    data = request.form
    if findMatchSteamAPI.trueValidation(data["steamid"], data["steamidkey"], data["gamecode"]) == False:
      return auth_with_steam()
    return "Posting! " + data["steamid"] + " " + data["steamidkey"] + " " + data["gamecode"]
  
  
  returnval = request.args
  linkTosteamauth = '<br><br><a href="http://localhost:5000/auth">Login with steam</a>'
  home = '<a href="http://localhost:5000/">Home</a>'
  userid = str(returnval['openid.claimed_id']).split("/")[-1]
  return f'''<form action="/authorize" method = "POST">
    <p>{userid}</p>
    <input type = "hidden" name = "steamid" value={userid}>
    <p>Steam id key <input type = "text" name = "steamidkey" placeholder = "XXXX-XXXXX-XXXX" required/></p>
    <p>Known Match Game Code <input type = "text" name = "gamecode" placeholder = "CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx" required/></p>
    <p>To find your most recent Steam id key and match code go to the following link: <a href="https://help.steampowered.com/en/wizard/HelpWithGameIssue/?appid=730&issueid=128">SteamLink<a/></p>
    <p><input type = "submit" value = "submit" /></p>
</form>'''

if __name__ == "__main__":
    app.run()
