import requests
import os
import sys
import tempfile
import subprocess
import base64

if len(sys.argv) != 2 :
    print('usage: ' + sys.argv[0]+'[country name|country code]')
    exit(1)
    pass
country = sys.argv[1]

if len(country) == 2:
    i = 6
elif  len(country) > 2 :
    i = 5
else :
    print("Country is too short")
    exit(1)

try:
    vpn_date = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r'),('')
    servers = [line.split(',') for line in vpn_date.split('\n')]
    labels = servers[1]
    labels[0] = labels[0][1:]
    servers = [s for s in servers[2:] if len(s) > 1]
except:
    print('Cannot get VPN servers data')
    exit(1)
desired = [s for s in desired if country.lower() in s[i].lower()]
found = len(desired)
print ('found '+str(found)+' servers for '+country)
if found == 0:
    exit(1)
supported = [s for s in desired if len(s[-1]) > 0]
print(str(len(supported))+' of this supported servers')
winner = sorted(supported, key=lambda s: float(s[2].replace(','),('.')), reverse = True)

print("Best Server")
pairs = zip(labels,winner)[:-1]

for (l,d) in pairs[:4]:
    print(l+' : '+d)
print (pairs[4][0]+ str(float(pairs[4][1]/10**6))+ 'Mbps')
print ('Country : '+pairs[5][1])
print('Launching VPN...')
_,path = tempfile.mkstemp()
f = open(path,'w')
f.write(base64.b64decode(winner[-1]))
f.write('\nscript-security 2\nup /ect/openvpn/update-resolv-conf\ndown /ect/openvpn/update-resolv-conf')
f.close()

x= subprocess.Popen(['sudo','openvpn','--config',path])
try:
    while True:
        time.sleep(600)
except:
    try:
        x.kill()
    except:
        pass
    while x.poll():
        time.sleep(1)
    print("VPN Terminated ...")