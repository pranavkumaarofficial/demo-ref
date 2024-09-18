import streamlit as st
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import datetime
import subprocess
import os

# Function to generate a self-signed certificate
def generate_self_signed_cert(common_name, country, org, validity_days):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())

    with open("CA.key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("CA.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return "CA.key", "CA.pem"


# Function to generate a client certificate signed by a CA
def generate_client_cert(common_name, country, org, validity_days, ca_key_data, ca_cert_data):
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        subject
    ).sign(key, hashes.SHA256(), default_backend())

    ca_key = serialization.load_pem_private_key(ca_key_data, None, default_backend())
    ca_cert = x509.load_pem_x509_certificate(ca_cert_data, default_backend())

    cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(ca_key, hashes.SHA256(), default_backend())

    client_key_filename = f"{common_name}_client.key"
    with open(client_key_filename, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    client_cert_filename = f"{common_name}_client.pem"
    with open(client_cert_filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return client_key_filename, client_cert_filename


# Function to sign a CSR using a signer's private key
def sign_csr(csr_data, signer_key_data):
    csr = x509.load_pem_x509_csr(csr_data, default_backend())
    signer_key = serialization.load_pem_private_key(signer_key_data, None, default_backend())

    cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        csr.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(signer_key, hashes.SHA256(), default_backend())

    with open("signed_client.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return "signed_client.pem"


# Function to validate a certificate chain
def validate_cert(ca_cert_data, client_cert_data, intermediate_cert_data=None):
    with open("temp_ca.pem", "wb") as f:
        f.write(ca_cert_data)

    with open("temp_client.pem", "wb") as f:
        f.write(client_cert_data)

    command = ["openssl", "verify", "-CAfile", "temp_ca.pem"]
    
    if intermediate_cert_data:
        with open("temp_intermediate.pem", "wb") as f:
            f.write(intermediate_cert_data)
        command.extend(["-untrusted", "temp_intermediate.pem"])

    command.append("temp_client.pem")

    result = subprocess.run(command, capture_output=True, text=True)

    os.remove("temp_ca.pem")
    os.remove("temp_client.pem")
    if intermediate_cert_data:
        os.remove("temp_intermediate.pem")

    if result.returncode == 0:
        return "Chain of Trust: PASS"
    else:
        return f"Chain of Trust: FAIL ({result.stderr.strip()})"


# Streamlit UI
st.title("Certificate Management App")

option = st.sidebar.selectbox("Choose an option", ("Create Certificate", "Sign CSR", "Validate Certificate"))

if option == "Create Certificate":
    st.subheader("Create a New Certificate")
    cert_type = st.radio("Select Certificate Type", ("Self-Signed Certificate", "Client Certificate"))

    common_name = st.text_input("Common Name (CN)")
    country = st.text_input("Country (C)")
    org = st.text_input("Organization (O)")
    validity_days = st.number_input("Validity (Days)", min_value=1, max_value=3650, value=365)

    if cert_type == "Self-Signed Certificate":
        if st.button("Generate Self-Signed Certificate"):
            ca_key, ca_cert = generate_self_signed_cert(common_name, country, org, validity_days)
            st.success(f"Generated {ca_key} and {ca_cert}")

    elif cert_type == "Client Certificate":
        ca_key_file = st.file_uploader("Upload CA Private Key", type=["key"])
        ca_cert_file = st.file_uploader("Upload CA Certificate", type=["pem"])

        if st.button("Generate Client Certificate"):
            if ca_key_file and ca_cert_file:
                client_key, client_cert = generate_client_cert(common_name, country, org, validity_days, ca_key_file.read(), ca_cert_file.read())
                st.success(f"Generated {client_key} and {client_cert}")
            else:
                st.error("Please upload both CA private key and CA certificate")

elif option == "Sign CSR":
    st.subheader("Sign CSR to Generate Certificate")
    csr_file = st.file_uploader("Upload Client CSR", type=["pem"])
    signer_key_file = st.file_uploader("Upload Signer's Private Key", type=["pem"])

    if st.button("Sign CSR"):
        if csr_file and signer_key_file:
            signed_cert = sign_csr(csr_file.read(), signer_key_file.read())
            st.success(f"Signed certificate generated: {signed_cert}")
        else:
            st.error("Please upload both CSR and Signer's Private Key")

elif option == "Validate Certificate":
    st.subheader("Validate Certificate Chain")
    ca_cert_file = st.file_uploader("Upload CA Certificate", type=["pem"])
    client_cert_file = st.file_uploader("Upload Client Certificate", type=["pem"])
    intermediate_cert_file = st.file_uploader("Upload Intermediate CA Certificate (Optional)", type=["pem"])

    if st.button("Validate Certificate"):
        if ca_cert_file and client_cert_file:
            validation_result = validate_cert(ca_cert_file.read(), client_cert_file.read(), intermediate_cert_file.read() if intermediate_cert_file else None)
            st.success(validation_result)
        else:
            st.error("Please upload both CA certificate and Client certificate")
