"""
Module d'intégration avec Freshdesk API
Permet la création automatique de tickets
"""

import requests
import json
import os
from datetime import datetime

class FreshdeskIntegration:
    """Gestionnaire d'intégration avec Freshdesk"""
    
    def __init__(self, domain=None, api_key=None):
        """
        Initialise l'intégration Freshdesk
        
        Args:
            domain: Domaine Freshdesk (ex: kangourou.freshdesk.com)
            api_key: Clé API Freshdesk
        """
        self.domain = domain or os.getenv('FRESHDESK_DOMAIN')
        self.api_key = api_key or os.getenv('FRESHDESK_API_KEY')
        
        if self.domain and self.api_key:
            self.base_url = f"https://{self.domain}/api/v2"
            self.headers = {
                'Content-Type': 'application/json',
            }
            self.auth = (self.api_key, 'X')
            self.enabled = True
        else:
            self.enabled = False
    
    def create_ticket(self, subject, description, priority=1, status=2, 
                     requester_email=None, requester_name=None, tags=None):
        """
        Crée un ticket Freshdesk
        
        Args:
            subject: Sujet du ticket
            description: Description complète
            priority: 1=Low, 2=Medium, 3=High, 4=Urgent
            status: 2=Open, 3=Pending, 4=Resolved, 5=Closed
            requester_email: Email du demandeur
            requester_name: Nom du demandeur
            tags: Liste de tags
        
        Returns:
            dict: Réponse de l'API ou None si erreur
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Configuration Freshdesk manquante',
                'message': 'Veuillez configurer FRESHDESK_DOMAIN et FRESHDESK_API_KEY'
            }
        
        # Données du ticket
        ticket_data = {
            'subject': subject,
            'description': description,
            'priority': priority,
            'status': status,
            'source': 2,  # Portal
        }
        
        # Ajouter le demandeur si fourni
        if requester_email:
            ticket_data['email'] = requester_email
        if requester_name:
            ticket_data['name'] = requester_name
        
        # Ajouter les tags si fournis
        if tags:
            ticket_data['tags'] = tags
        
        try:
            response = requests.post(
                f"{self.base_url}/tickets",
                auth=self.auth,
                headers=self.headers,
                json=ticket_data,
                timeout=30
            )
            
            if response.status_code == 201:
                ticket = response.json()
                return {
                    'success': True,
                    'ticket_id': ticket.get('id'),
                    'ticket_url': f"https://{self.domain}/a/tickets/{ticket.get('id')}",
                    'data': ticket
                }
            else:
                return {
                    'success': False,
                    'error': f"Erreur HTTP {response.status_code}",
                    'message': response.text
                }
        
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': 'Erreur de connexion',
                'message': str(e)
            }
    
    def create_ticket_from_search(self, query, search_results, user_info=None):
        """
        Crée un ticket Freshdesk à partir d'une recherche Kaizen
        
        Args:
            query: Question de l'utilisateur
            search_results: Résultats de la recherche
            user_info: Informations utilisateur (dict avec email, name, agency)
        
        Returns:
            dict: Résultat de la création du ticket
        """
        # Préparer le sujet
        subject = f"[Kaizen IA] Question : {query[:80]}"
        
        # Préparer la description
        description = self._format_ticket_description(query, search_results, user_info)
        
        # Tags
        tags = ['kaizen-ia', 'documentation', 'auto-generated']
        
        # Email et nom du demandeur
        email = user_info.get('email') if user_info else None
        name = user_info.get('name') if user_info else None
        
        # Créer le ticket
        return self.create_ticket(
            subject=subject,
            description=description,
            priority=2,  # Medium
            status=2,    # Open
            requester_email=email,
            requester_name=name,
            tags=tags
        )
    
    def _format_ticket_description(self, query, search_results, user_info):
        """Formate la description du ticket"""
        
        description = f"""<h2>🔍 Question posée</h2>
<p><strong>{query}</strong></p>

<h2>📊 Résultats de recherche automatique</h2>
"""
        
        if search_results:
            description += f"<p>{len(search_results)} section(s) pertinente(s) trouvée(s) dans le manuel Kaizen.</p>"
            description += "<h3>Extraits trouvés :</h3><ul>"
            
            for i, result in enumerate(search_results[:3], 1):
                excerpt = result['text'][:300].replace('\n', ' ')
                description += f"<li><strong>Extrait {i}</strong> : {excerpt}...</li>"
            
            description += "</ul>"
        else:
            description += "<p><em>Aucun résultat trouvé dans le manuel Kaizen.</em></p>"
        
        # Informations utilisateur
        if user_info:
            description += f"""
<h2>👤 Informations utilisateur</h2>
<ul>
<li><strong>Nom :</strong> {user_info.get('name', 'N/A')}</li>
<li><strong>Email :</strong> {user_info.get('email', 'N/A')}</li>
<li><strong>Agence :</strong> {user_info.get('agency', 'N/A')}</li>
</ul>
"""
        
        # Métadonnées
        description += f"""
<hr>
<h2>ℹ️ Informations système</h2>
<ul>
<li><strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</li>
<li><strong>Source :</strong> Assistant IA Kaizen</li>
<li><strong>Version :</strong> 1.0</li>
</ul>

<p><em>✅ Ce ticket a été créé automatiquement par l'Assistant IA Kaizen suite à une recherche infructueuse dans le manuel opératoire.</em></p>
"""
        
        return description

def test_connection(domain=None, api_key=None):
    """
    Teste la connexion à l'API Freshdesk
    
    Returns:
        dict: Résultat du test
    """
    freshdesk = FreshdeskIntegration(domain, api_key)
    
    if not freshdesk.enabled:
        return {
            'success': False,
            'message': 'Configuration manquante'
        }
    
    try:
        response = requests.get(
            f"{freshdesk.base_url}/tickets?per_page=1",
            auth=freshdesk.auth,
            headers=freshdesk.headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                'success': True,
                'message': 'Connexion réussie à Freshdesk'
            }
        else:
            return {
                'success': False,
                'message': f'Erreur HTTP {response.status_code}'
            }
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Erreur : {str(e)}'
        }

# Exemple d'utilisation
if __name__ == "__main__":
    print("🧪 Test du module Freshdesk")
    print("-" * 50)
    
    # Test de connexion
    result = test_connection()
    print(f"Test de connexion : {result}")
    
    # Exemple de création de ticket (si configuré)
    freshdesk = FreshdeskIntegration()
    if freshdesk.enabled:
        test_ticket = freshdesk.create_ticket_from_search(
            query="Comment créer un devis dans Kaizen ?",
            search_results=[
                {'text': 'Pour créer un devis...', 'score': 5, 'line': 100}
            ],
            user_info={
                'email': 'test@example.com',
                'name': 'Test User',
                'agency': 'Paris 15'
            }
        )
        print(f"\nCréation de ticket test : {test_ticket}")
    else:
        print("\n⚠️  Configuration Freshdesk non trouvée.")
        print("Pour activer l'intégration :")
        print("1. Créez un fichier .env")
        print("2. Ajoutez : FRESHDESK_DOMAIN=votre-domaine.freshdesk.com")
        print("3. Ajoutez : FRESHDESK_API_KEY=votre_clé_api")
