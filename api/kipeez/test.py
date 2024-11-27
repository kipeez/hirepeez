import requests
from requests.auth import HTTPBasicAuth

kodi_url = "http://192.168.1.12:8081/jsonrpc"
payload_1 = {"jsonrpc":"2.0","method":"Playlist.Clear","params":[1],"id":1}
payload_2 = {"jsonrpc":"2.0","method":"Playlist.Insert","params":[1,0,{"file":"/storage/emulated/0/Download/[ Torrent911.re ] The.First.Slam.Dunk.2022.MULTi.1080p.WEB.x264-FW.mkv"}],"id":2}
payload_3= {"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"position":0,"playlistid":1},"options":{}},"id":3}
#  {"jsonrpc":"2.0","id":1,"method":"Player.Open","params":{"item":{"file":"1_1920x800@30.mp4"}}}
username = "kodi"
password = "kodi"

response = requests.post(kodi_url, json=payload_1, auth=HTTPBasicAuth(username, password))
print("Status code:", response.status_code)
print("Headers:", response.headers)
print("Content:", response.content)
response = requests.post(kodi_url, json=payload_2, auth=HTTPBasicAuth(username, password))
print("Status code:", response.status_code)
print("Headers:", response.headers)
print("Content:", response.content)
response = requests.post(kodi_url, json=payload_3, auth=HTTPBasicAuth(username, password))
print("Status code:", response.status_code)
print("Headers:", response.headers)
print("Content:", response.content)
if response.status_code == 200:
    print("Movie started successfully.")
else:
    print("Error starting movie:", response.text)
