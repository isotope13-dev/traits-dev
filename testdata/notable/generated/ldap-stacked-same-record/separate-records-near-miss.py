from impacket.ldap.ldapasn1 import BindRequest, ModifyRequest


def update_description(conn, dn, text):
    # Ordinary signed client: each request is protected and sent on its own.
    # Nothing concatenates the bind and modify buffers into one record.
    bind_request = BindRequest()
    bind_request["name"] = ""
    conn._socket.sendall(conn.encrypt(bind_request))

    modify_request = ModifyRequest()
    modify_request["object"] = dn
    conn._socket.sendall(conn.encrypt(modify_request))
    return text
