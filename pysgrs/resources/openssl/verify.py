from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

with open('jgoffinet/VPN-Client.crt', 'r') as cert_file:
    cert_data = cert_file.read()
cert = x509.load_pem_x509_certificate(data=cert_data, backend=default_backend())

with open('jgoffinet/CA.crt', 'r') as chain_file:
    chain_data = chain_file.read()
chain = x509.load_pem_x509_certificate(data=chain_data, backend=default_backend())

public_key = chain.public_key()

try:
    # Return None or Raise an error
    chain.public_key().verify(
        data = cert.tbs_certificate_bytes,
        signature = cert.signature,
        padding = padding.PKCS1v15(),
        algorithm = hashes.SHA256()
    )
    print("Certificate is verified")
except:
    print("Not verified")
    