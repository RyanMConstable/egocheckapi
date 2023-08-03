from flask import Flask, redirect, request
from json import dumps
from urllib.parse import urlencode

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
  returnval = request.args
  linkTosteamauth = '<br><br><a href="http://localhost:5000/auth">Login with steam</a>'
  home = '<a href="http://localhost:5000/">Home</a>'
  userid = str(returnval['openid.claimed_id']).split("/")[-1]
  if request.method == "POST":
    return "Posting!"
  return '''<form action="action_to_perform_after_submission" method = "POST">
    <p>Field1 <input type = "text" name = "Field1_name" /></p>
    <p>Field2 <input type = "text" name = "Field2_name" /></p>
    <p>Field3 <input type = "text" name = "Field3_name" /></p>
    <p><input type = "submit" value = "submit" /></p>
</form>'''

if __name__ == "__main__":
    app.run()
