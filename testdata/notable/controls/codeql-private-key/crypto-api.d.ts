declare module "crypto" {
    function diffieHellman(options: { privateKey: KeyObject; publicKey: KeyObject }): Buffer;
}
