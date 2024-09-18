import streamlit as st
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

# Utility functions for certificate creation, signing, and validation

# Function to generate a self-signed certificate
def generate_self_signed_cert(common_name, country, org, validity_days):
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create CSR
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
        # The certificate will be valid for the specified number of days
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(common_name)]),
        critical=False,
    ).sign(key, hashes.SHA256(), default_backend())

    # Write key and certificate to PEM files
    with open("CA.key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("CA.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return "CA.key", "CA.pem"

# Function to generate client certificate signed by CA
def generate_client_cert(common_name, country, org, validity_days, ca_key_path, ca_cert_path):
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create CSR
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    csr = x509.CertificateSigningRequestBuilder().subject_name(
        subject
    ).sign(key, hashes.SHA256(), default_backend())

    # Load CA's key and certificate
    with open(ca_key_path, "rb") as f:
        ca_key = serialization.load_pem_private_key(f.read(), None, default_backend())

    with open(ca_cert_path, "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())

    # Sign CSR to generate client certificate
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

    # Write key and certificate to PEM files
    with open("client.key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("client.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return "client.key", "client.pem"

# Function to sign a CSR using a signer's private key
def sign_csr(csr_path, signer_key_path):
    # Load CSR
    with open(csr_path, "rb") as f:
        csr = x509.load_pem_x509_csr(f.read(), default_backend())

    # Load signer's private key
    with open(signer_key_path, "rb") as f:
        signer_key = serialization.load_pem_private_key(f.read(), None, default_backend())

    # Sign the CSR
    cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        csr.subject  # In this case, self-signed. You can modify for other signers.
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

# Function to validate certificate chain
def validate_cert(ca_cert_path, client_cert_path, intermediate_cert_path=None):
    # Prepare OpenSSL command for certificate verification
    command = [
        "openssl", "verify", "-CAfile", ca_cert_path
    ]
    
    if intermediate_cert_path:
        # Add intermediate certificate if provided
        command.extend(["-untrusted", intermediate_cert_path])
    
    # Append the client certificate to be verified
    command.append(client_cert_path)

    try:
        # Run the OpenSSL command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if verification passed
        if result.returncode == 0:
            return "Chain of Trust: PASS"
        else:
            return f"Chain of Trust: FAIL ({result.stderr.strip()})"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
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
        ca_key_path = st.file_uploader("Upload CA Private Key", type=["pem"])
        ca_cert_path = st.file_uploader("Upload CA Certificate", type=["pem"])
        if st.button("Generate Client Certificate"):
            if ca_key_path and ca_cert_path:
                client_key, client_cert = generate_client_cert(common_name, country, org, validity_days, ca_key_path.name, ca_cert_path.name)
                st.success(f"Generated {client_key} and {client_cert}")
            else:
                st.error("Please upload both CA private key and CA certificate")

elif option == "Sign CSR":
    st.subheader("Sign CSR to Generate Certificate")
    csr_path = st.file_uploader("Upload Client CSR", type=["pem"])
    signer_key_path = st.file_uploader("Upload Signer's Private Key", type=["pem"])

    if st.button("Sign CSR"):
        if csr_path and signer_key_path:
            signed_cert = sign_csr(csr_path.name, signer_key_path.name)
            st.success(f"Signed certificate generated: {signed_cert}")
        else:
            st.error("Please upload both CSR and Signer's Private Key")

elif option == "Validate Certificate":
    st.subheader("Validate Certificate Chain")
    ca_cert_path = st.file_uploader("Upload CA Certificate", type=["pem"])
    client_cert_path = st.file_uploader("Upload Client Certificate", type=["pem"])
    intermediate_cert_path = st.file_uploader("Upload Intermediate CA Certificate (Optional)", type=["pem"])

    if st.button("Validate Certificate"):
        if ca_cert_path and client_cert_path:
            validation_result = validate_cert(ca_cert_path.name, client_cert_path.name, intermediate_cert_path.name if intermediate_cert_path else None)
            st.success(validation_result)
        else:
            st.error("Please upload both CA certificate and Client certificate")
