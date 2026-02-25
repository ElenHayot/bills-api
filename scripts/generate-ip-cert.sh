#!/bin/bash

# Script pour générer un certificat SSL pour une IP spécifique
# Utile pour le développement mobile

IP="172.20.10.3"
CERT_DIR="./certs"

# Créer le répertoire des certificats
mkdir -p $CERT_DIR

echo "Génération des certificats SSL pour l'IP $IP..."

# Créer un fichier de configuration OpenSSL
cat > $CERT_DIR/openssl.conf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = $IP

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP
DNS.1 = localhost
EOF

# Générer la clé privée
openssl genrsa -out $CERT_DIR/key-ip.pem 2048

# Générer le certificat avec l'IP
openssl req -new -x509 -key $CERT_DIR/key-ip.pem -out $CERT_DIR/cert-ip.pem -days 365 \
    -config $CERT_DIR/openssl.conf -extensions v3_req

echo "Certificat généré pour l'IP $IP"
echo "Certificats disponibles dans $CERT_DIR :"
echo "  - cert-ip.pem (certificat pour $IP)"
echo "  - key-ip.pem (clé privée)"

# Mettre à jour nginx pour utiliser ce certificat
echo ""
echo "Pour utiliser ce certificat, mettez à jour nginx.conf :"
echo "  ssl_certificate /etc/nginx/certs/cert-ip.pem;"
echo "  ssl_certificate_key /etc/nginx/certs/key-ip.pem;"
