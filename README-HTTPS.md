# Configuration HTTPS pour Bills API

## Vue d'ensemble

Ce document explique comment configurer HTTPS pour votre API Bills avec différentes options de certificats.

## Types de certificats SSL

### 1. Certificats Auto-signés (Développement)

**Quand utiliser :**
- Développement local
- Tests internes
- Environnements isolés

**Avantages :**
- Gratuit et facile à générer
- Pas besoin d'autorité externe
- Configuration immédiate

**Inconvénients :**
- Navigateurs affichent des avertissements
- Non adapté pour la production
- Pas de validation d'identité

**Installation :**
```bash
# Générer des certificats auto-signés
./scripts/generate-certs.sh

# Démarrer avec HTTPS (développement)
docker-compose -f docker-compose.https.yml up
```

### 2. Certificats Non Autosignés (Production)

**Qu'est-ce qu'un certificat non autosigné ?**
Un certificat non autosigné (ou certificat signé par une autorité de certification) est un certificat SSL/TLS qui a été validé par une autorité de certification (CA) reconnue comme Let's Encrypt, DigiCert, GlobalSign, etc.

**Quand en aurait-on besoin :**
- **Production** : Sites web publics
- **Applications professionnelles** : Quand les utilisateurs doivent faire confiance à votre site
- **E-commerce** : Pour les transactions sécurisées
- **Applications mobiles** : Évitent les avertissements de sécurité
- **API publiques** : Pour les clients externes

**Avantages :**
- Reconnaissance par tous les navigateurs
- Aucun avertissement de sécurité
- Validation de l'identité du domaine
- Confiance des utilisateurs

**Inconvénients :**
- Coût (sauf Let's Encrypt gratuit)
- Validation requise
- Renouvellement nécessaire

**Installation avec Let's Encrypt (Gratuit) :**
```bash
# Pour la production avec un domaine réel
./scripts/setup-letsencrypt.sh

# Démarrer en production
docker-compose -f docker-compose.https.yml up
```

## Configuration

### Variables d'environnement

Ajoutez à votre `.env` :

```bash
# Production
ENVIRONMENT=production
ALLOWED_HOSTS=ton-domaine.com,www.ton-domaine.com
ALLOWED_ORIGINS=https://ton-domaine.com,https://www.ton-domaine.com

# Développement
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://localhost:8000
```

### Structure des fichiers

```
bills-api/
├── certs/
│   ├── cert.pem      # Certificat public
│   └── key.pem       # Clé privée
├── nginx.conf        # Configuration Nginx
├── docker-compose.https.yml
├── scripts/
│   ├── generate-certs.sh
│   └── setup-letsencrypt.sh
└── app/
    └── main.py       # Middleware HTTPS configuré
```

## Sécurité implémentée

1. **Redirection HTTP vers HTTPS** automatique
2. **Headers de sécurité** (HSTS, XSS Protection, etc.)
3. **Protocoles SSL modernes** (TLS 1.2+)
4. **Chiffrement fort** avec cipher suites sécurisés
5. **Hôtes de confiance** pour éviter les attaques host header

## Déploiement

### Développement local
```bash
# 1. Générer les certificats
./scripts/generate-certs.sh

# 2. Démarrer les services
docker-compose -f docker-compose.https.yml up

# 3. Accéder à https://localhost
# Accepter l'avertissement de sécurité (certificat auto-signé)
```

### Production
```bash
# 1. Configurer votre domaine pour pointer vers le serveur
# 2. Exécuter le script Let's Encrypt
./scripts/setup-letsencrypt.sh

# 3. Démarrer en production
ENVIRONMENT=production docker-compose -f docker-compose.https.yml up -d
```

## Maintenance

- **Renouvellement automatique** : Configuré pour Let's Encrypt via cron
- **Monitoring** : Vérifiez l'expiration des certificats
- **Backup** : Sauvegardez vos clés privées

## Dépannage

### Certificat non reconnu
- Vérifiez que le domaine pointe bien vers votre serveur
- Assurez-vous que le port 443 est ouvert
- Vérifiez la configuration Nginx

### Erreur SSL
- Vérifiez les permissions des fichiers de certificats
- Assurez-vous que les chemins dans nginx.conf sont corrects
- Redémarrez Nginx après modification
