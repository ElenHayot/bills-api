#!/bin/bash

# Script pour configurer Let's Encrypt (certificats non autosignés pour la production)
# NÉCESSITE UN DOMAINE RÉEL ET UN SERVEUR ACCESSIBLE INTERNET

DOMAIN="ton-domaine.com"
EMAIL="admin@ton-domaine.com"
CERT_DIR="./certs"

# Vérifier si le domaine est configuré
echo "Vérification du domaine $DOMAIN..."
if ! nslookup $DOMAIN > /dev/null 2>&1; then
    echo "ERREUR : Le domaine $DOMAIN n'est pas configuré ou n'est pas accessible."
    echo "Assurez-vous que le domaine pointe vers l'adresse IP de ce serveur."
    exit 1
fi

# Créer le répertoire des certificats
mkdir -p $CERT_DIR

# Installer Certbot si nécessaire
if ! command -v certbot &> /dev/null; then
    echo "Installation de Certbot..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y certbot
    elif command -v yum &> /dev/null; then
        sudo yum install -y certbot
    else
        echo "Veuillez installer Certbot manuellement : https://certbot.eff.org/"
        exit 1
    fi
fi

echo "Génération des certificats Let's Encrypt pour $DOMAIN..."

# Obtenir les certificats (mode standalone - nécessite d'arrêter nginx temporairement)
sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive

# Copier les certificats dans notre répertoire
sudo cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $CERT_DIR/cert.pem
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $CERT_DIR/key.pem
sudo chown $USER:$USER $CERT_DIR/*.pem

echo "Certificats Let's Encrypt configurés avec succès !"
echo ""
echo "Configuration du renouvellement automatique..."
echo "0 12 * * * /usr/bin/certbot renew --quiet && docker-compose -f docker-compose.https.yml restart nginx" | sudo crontab -

echo "Renouvellement automatique configuré (tous les jours à 12h)."
