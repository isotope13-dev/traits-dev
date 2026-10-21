import urllib.parse
import urllib.request

fields = {'ateFunc': '1', 'ateGain': '', 'ateTxCount': '', 'ateChan': '', 'ateRate': '', 'ateMacID': '', 'e2pTxPower1': '', 'e2pTxPower2': '', 'e2pTxPower3': '', 'e2pTxPower4': '', 'e2pTxPower5': '', 'e2pTxPower6': '', 'e2pTxPower7': '', 'e2pTx2Power1': '', 'e2pTx2Power2': '', 'e2pTx2Power3': '', 'e2pTx2Power4': '', 'e2pTx2Power5': '', 'e2pTx2Power6': '', 'e2pTx2Power7': '', 'ateTxFreqOffset': '', 'ateMode': '', 'ateBW': '', 'ateAntenna': '', 'e2pTxFreqOffset': '', 'e2pTxPwDeltaB': '', 'e2pTxPwDeltaG': '', 'e2pTxPwDeltaMix': '', 'e2pTxPwDeltaN': '', 'readE2P': '', 'submit-url': '/wlan_mp.asp'}
body = urllib.parse.urlencode(fields).encode('ascii')
request = urllib.request.Request(
    'http://127.0.0.1/goform/formWlanMP', data=body, method='POST',
    headers={'Authorization': 'Basic YWRtaW46MTIzNA==',
             'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status)
