#!/bin/bash

# Script pour générer des certificats SSL auto-signés pour le développement
# NE PAS UTILISER EN PRODUCTION

CERT_DIR="./certs"

# Créer le répertoire des certificats
mkdir -p $CERT_DIR

echo "Génération des certificats SSL auto-signés..."

# Générer la clé privée
openssl genrsa -out $CERT_DIR/key.pem 2048

# Générer le certificat auto-signé
openssl req -new -x509 -key $CERT_DIR/key.pem -out $CERT_DIR/cert.pem -days 365 \
    -subj "/C=FR/ST=Paris/L=Paris/O=Bills API/OU=Development/CN=localhost"

# Générer également un certificat pour le domaine de développement
openssl req -new -x509 -key $CERT_DIR/key.pem -out $CERT_DIR/cert-dev.pem -days 365 \
    -subj "/C=FR/ST=Paris/L=Paris/O=Bills API/OU=Development/CN=ton-domaine.com"

echo "Certificats générés avec succès dans le répertoire $CERT_DIR"
echo ""
echo "ATTENTION : Ce sont des certificats auto-signés pour le développement uniquement."
echo "Les navigateurs afficheront des avertissements de sécurité."
echo ""
echo "Pour la production, utilisez des certificats d'une autorité de certification (Let's Encrypt, DigiCert, etc.)"
