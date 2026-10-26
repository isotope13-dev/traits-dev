import frida
device = frida.get_usb_device()
session = device.attach("test.application")
script = session.create_script("""
Java.perform(function() {
    var V = Java.use('okhttp3.internal.tls.OkHostnameVerifier');
    V.verify.overload('java.lang.String', 'javax.net.ssl.SSLSession').implementation = function(host, session) {
        return this.verify(host, session);
    };
});
""")
script.load()
