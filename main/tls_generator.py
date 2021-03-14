import socket
import random
from OpenSSL import crypto
from datetime import datetime

hostname = "exoduspi.com"
currentDate = str(datetime.now().date())

def gen_self_signed_cert():
    pkey = crypto.PKey()
    pkey.generate_key(crypto.TYPE_RSA, 4096)

    x509 = crypto.X509()
    subject = x509.get_subject()
    subject.commonName = hostname
    x509.set_issuer(subject)
    x509.gmtime_adj_notBefore(0)
    x509.gmtime_adj_notAfter(5*365*24*60*60)
    x509.set_pubkey(pkey)
    x509.set_serial_number(random.randrange(100000))
    x509.set_version(2)
    x509.add_extensions([
        crypto.X509Extension(b'subjectAltName', False,
            ','.join([
                f'DNS:{hostname}',
                f'DNS:*.{hostname}',
                'DNS:localhost',
                'DNS:*.localhost']).encode()),
        crypto.X509Extension(b"basicConstraints", True, b"CA:false")])

    x509.sign(pkey, 'SHA256')

    crtpath = f"{hostname}-{currentDate}.crt"
    keypath = f"{hostname}-{currentDate}.key"
    print("Creating TLS v1.3 Certificate ...")
    f = open(crtpath, "wb")
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, x509))
    f.close()
    print("Success")
    print("Creating TLS v1.3 Private Key ...")
    f = open(keypath, "wb")
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
    f.close()
    print("Success")
    return

if __name__ == '__main__':
    gen_self_signed_cert()