import socket
from OpenSSL import crypto
import os
import sys
from datetime import datetime

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA
currentDate = str(datetime.now().date())

cn = "exoduspi.com"
key = crypto.PKey()
keypath = f"{cn}-{currentDate}.key"
csrpath = f"{cn}-{currentDate}.csr"
crtpath = f"{cn}-{currentDate}.crt"


def generate_cert():
    def generatekey():
        print("Generating SSL key...")
        key.generate_key(TYPE_RSA, 4096)
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()
        print("Success")

    generatekey()

    def generatecsr():
        print("Generating SSL Certificate Request...")
        c = "US"
        st = "California"
        l = "Berkeley"  # Go Bears
        o = "CQB"
        ou = "Network Operations"

        req = crypto.X509Req()
        req.get_subject().CN = cn
        req.get_subject().C = c
        req.get_subject().ST = st
        req.get_subject().L = l
        req.get_subject().O = o
        req.get_subject().OU = ou
        req.set_pubkey(key)
        req.sign(key, "sha256")

        f = open(csrpath, "wb")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()
        print("Success")

        print("Generating SSL Certificate...")
        cert = crypto.X509()
        cert.get_subject().CN = cn
        cert.get_subject().C = c
        cert.get_subject().ST = st
        cert.get_subject().L = l
        cert.get_subject().O = o
        cert.get_subject().OU = ou
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, "sha256")
        f = open(crtpath, "wb")
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        f.close()
        print("Success")

    generatecsr()


if __name__ == "__main__":
    generate_cert()
