import java.security.Signature;
class SignatureUse { Signature make() throws Exception { return Signature.getInstance("SHA256withRSA"); } }
