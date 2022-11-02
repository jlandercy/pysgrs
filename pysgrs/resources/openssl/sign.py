import datetime

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Create CA:
root_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BE"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Belgium"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Arquenne"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"GoffInnovation"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"My Fully Trusted Authority"),
])
root_cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    root_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=3650)
).sign(root_key, hashes.SHA256(), default_backend())

# Create Self-Signed Certificate:
cert_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
new_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BE"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Belgium"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Arquennes"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Trusted Application"),
])
cert = x509.CertificateBuilder().subject_name(
    new_subject
).issuer_name(
    root_cert.issuer
).public_key(
    cert_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"goffinnovation.com")]),
    critical=False,
).sign(root_key, hashes.SHA256(), default_backend())


# Dump certificates:

with open("CA.crt", "wb") as handler:
    handler.write(root_cert.public_bytes(serialization.Encoding.PEM))

with open("VPN-Client.crt", "wb") as handler:
    handler.write(cert.public_bytes(serialization.Encoding.PEM))

