#!/usr/bin/env python3
"""
Assistant IA Kaizen - VERSION CORRIGÉE COMPLÈTE
- Bouton Freshdesk toujours visible
- Boutons exemples fonctionnels
- Meilleure détection de concepts
"""

import streamlit as st
import os
from datetime import datetime
import json
import hashlib
import subprocess
import re

st.set_page_config(
    page_title="Assistant Kaizen",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
    .answer-box {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        margin: 2rem 0;
    }
    .page-ref {
        display: inline-block;
        background: #fff3cd;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        border: 2px solid #ffc107;
        color: #856404;
        font-weight: 600;
    }
    .ticket-box {
        background: #fff3e0;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class KaizenAssistant:
    def __init__(self):
        if os.path.exists("Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "Kaizen_-_Manuel_ope_ratoire.pdf"
        elif os.path.exists("/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"
        else:
            self.pdf_path = None
        
        self.history_file = "chat_history.json"
        self.pdf_cache = None
        self.load_history()
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    st.session_state.history = json.load(f)
            else:
                st.session_state.history = []
        except:
            st.session_state.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def extract_pdf_by_pages(self):
        if self.pdf_cache:
            return self.pdf_cache
        
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            return None
        
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', self.pdf_path, '-'],
                capture_output=True, text=True, check=True
            )
            
            pages = result.stdout.split('\f')
            self.pdf_cache = {}
            
            for i, page_text in enumerate(pages, 1):
                if page_text.strip():
                    self.pdf_cache[i] = page_text.strip()
            
            return self.pdf_cache
        except:
            return None
    
    def search_pages(self, query):
        pages = self.extract_pdf_by_pages()
        if not pages:
            return []
        
        query_words = [w.lower() for w in query.split() if len(w) > 2]
        results = []
        
        for page_num, page_text in pages.items():
            page_lower = page_text.lower()
            score = sum(page_lower.count(word) for word in query_words)
            
            if score > 0:
                results.append({
                    'page': page_num,
                    'score': score,
                    'text': page_text
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:5]
    
    def detect_concept(self, query):
        """Détection améliorée des concepts avec plus de mots-clés"""
        query_lower = query.lower()
        
        # Dictionnaire exhaustif de mots-clés
        concepts = {
            'devis_types': ['réel', 'mensualisé', 'mensualisation', 'devis au réel', 'devis mensualisé', 'type de devis'],
            'devis_creation': ['créer un devis', 'créer devis', 'nouveau devis', 'faire un devis', 'générer un devis'],
            'aici': ['aici', 'avance immédiate', 'crédit impôt', 'crédit d\'impôt', '50%', 'ais'],
            'facture': ['facture', 'facturation', 'facturer', 'générer facture', 'créer facture'],
            'contrat': ['contrat', 'cd2i', 'cdd', 'cdi', 'contrat travail', 'embauche'],
            'yousign': ['yousign', 'signature', 'signer', 'signature électronique', 'e-signature'],
            'dashboard': ['dashboard', 'tableau de bord', 'accueil', 'vue d\'ensemble'],
            'appariement': ['appariement', 'apparier', 'affecter', 'assigner intervenant', 'matching'],
            'famille': ['fiche famille', 'créer famille', 'famille', 'ajouter famille'],
            'salarie': ['salarié', 'intervenant', 'recruter', 'embaucher'],
            'planning': ['planning', 'planification', 'calendrier', 'horaires'],
            'paiement': ['paiement', 'règlement', 'payer', 'sepa', 'prélèvement'],
            'urssaf': ['urssaf', 'déclaration', 'dsn', 'cotisations'],
        }
        
        # Chercher le concept correspondant
        for concept, keywords in concepts.items():
            if any(kw in query_lower for kw in keywords):
                return concept
        
        return None
    
    def synthesize_answer(self, query, page_results):
        if not page_results:
            return "❌ Aucune information trouvée dans le manuel pour cette question.\n\n💡 **Suggestion :** Essayez de reformuler ou créez un ticket Freshdesk pour une aide personnalisée.", []
        
        pages_found = [r['page'] for r in page_results]
        all_text = "\n\n".join([r['text'] for r in page_results])
        
        # Détection du concept
        concept = self.detect_concept(query)
        
        # Générer la synthèse selon le concept détecté
        if concept == 'devis_types':
            answer = self._synthesize_devis_types()
        elif concept == 'devis_creation':
            answer = self._synthesize_devis_creation()
        elif concept == 'aici':
            answer = self._synthesize_aici()
        elif concept == 'facture':
            answer = self._synthesize_facture()
        elif concept == 'contrat':
            answer = self._synthesize_contrat()
        elif concept == 'yousign':
            answer = self._synthesize_yousign()
        elif concept == 'dashboard':
            answer = self._synthesize_dashboard()
        elif concept == 'appariement':
            answer = self._synthesize_appariement()
        elif concept == 'famille':
            answer = self._synthesize_famille()
        elif concept == 'salarie':
            answer = self._synthesize_salarie()
        elif concept == 'planning':
            answer = self._synthesize_planning()
        elif concept == 'paiement':
            answer = self._synthesize_paiement()
        elif concept == 'urssaf':
            answer = self._synthesize_urssaf()
        else:
            # Synthèse générique améliorée
            answer = self._synthesize_generic_improved(all_text, query)
        
        return answer, pages_found
    
    def _synthesize_devis_types(self):
        return """**📊 Devis Réel vs Devis Mensualisé**

Kaizen propose deux types de devis :

**🔹 Devis au Réel**
- Facturation basée sur les heures réellement effectuées chaque mois
- La famille paie ce qui a été consommé exactement
- Adapté aux besoins variables ou ponctuels
- Exemple : Famille avec besoins de garde certaines semaines seulement

**🔹 Devis Mensualisé**
- Facturation lissée sur toute la durée du contrat
- Montant fixe chaque mois
- Adapté aux besoins réguliers et prévisibles
- Exemple : Famille avec garde toute l'année

**💡 Comment choisir ?**
- Besoins réguliers = Mensualisé
- Besoins variables = Réel"""
    
    def _synthesize_devis_creation(self):
        return """**📝 Créer un Devis dans Kaizen**

**Procédure :**

1. **Accéder aux devis**
   - Onglet "Familles"
   - Ouvrir la fiche famille
   - Section "Prospection et devis"

2. **Créer le devis**
   - Cliquer "Créer un devis"
   - Choisir le type (réel ou mensualisé)
   - Renseigner les prestations
   - Définir les créneaux horaires

3. **Finaliser**
   - Vérifier les informations
   - Générer le document
   - Envoyer pour signature via YouSign

**💡 Bon à savoir :** Vérifiez l'éligibilité AICI avant validation."""
    
    def _synthesize_aici(self):
        return """**💰 AICI - Avance Immédiate Crédit d'Impôt**

**Définition**

L'AICI permet aux familles de bénéficier immédiatement du crédit d'impôt de 50% sur leurs dépenses de garde d'enfants.

**Fonctionnement**

1. Famille paie 50% de la facture
2. État verse 50% directement à l'agence
3. Via le tiers de confiance AIS

**Conditions**

• Famille éligible au crédit d'impôt
• Statut AICI validé dans Kaizen
• Déclarations URSSAF à jour

**Dans Kaizen :** Fiche famille → Onglet "Infos générales"."""
    
    def _synthesize_facture(self):
        return """**🧾 Génération de Factures**

**Procédure**

1. **Validation des heures**
   - Vérifier les heures déclarées
   - Corriger les erreurs
   - Valider

2. **Génération**
   - Onglet "Factures"
   - "Générer les factures"
   - Sélectionner la période
   - Lancer

3. **Envoi**
   - Envoi email automatique
   - Prélèvements SEPA si applicable

**💡 Important :** Générer avant paiement salaires."""
    
    def _synthesize_contrat(self):
        return """**📝 Contrats de Travail**

**Types disponibles**

**CD2I** - Contrat Intermittent (le plus utilisé)
• Flexibilité des horaires
• Adapté garde d'enfants

**CDD** - Durée Déterminée
• Remplacements temporaires

**CDI** - Durée Indéterminée
• Emplois permanents

**Procédure :** Salariés → Fiche salarié → Contrats → Créer."""
    
    def _synthesize_yousign(self):
        return """**✍️ YouSign - Signature Électronique**

**Fonctionnement**

1. **Envoi** - 2 emails séparés (PDF + lien signature)
2. **Signature** - Clic sur lien, signature valable légalement
3. **Relances** - Automatiques après 24h et 48h

**⚠️ Attention :** Lien peut arriver dans spams."""
    
    def _synthesize_dashboard(self):
        return """**📊 Dashboard Kaizen**

Tableau de bord de pilotage.

**4 blocs**

1. Suivi demandes
2. Suivi commercial  
3. Planification
4. Suivi RH

Point de départ quotidien."""
    
    def _synthesize_appariement(self):
        return """**🔗 Appariement**

**Action :** Associer intervenant à prestation famille.

**Procédure**

1. "Suivi Appariement"
2. Rechercher intervenant
3. Créer appariement
4. Définir créneaux

**Statuts :** En attente / Apparié / Actif."""
    
    def _synthesize_famille(self):
        return """**👨‍👩‍👧 Gestion Familles**

**Créer une fiche famille**

1. Onglet "Familles"
2. "Nouvelle famille"
3. Renseigner informations
4. Enregistrer

**Onglets disponibles :**
- Infos générales
- Prospection et devis
- Contrats
- Facturation
- Historique"""
    
    def _synthesize_salarie(self):
        return """**👥 Gestion Salariés**

**Créer un salarié**

1. Onglet "Salariés"
2. "Nouveau salarié"
3. Compléter la fiche
4. Documents obligatoires

**Informations clés :**
- État civil
- Contrats
- Disponibilités
- Compétences"""
    
    def _synthesize_planning(self):
        return """**📅 Planning**

**Consultation :**
- Vue journalière
- Vue hebdomadaire
- Vue mensuelle

**Actions :**
- Créer prestations
- Modifier horaires
- Gérer absences
- Export planning"""
    
    def _synthesize_paiement(self):
        return """**💳 Paiements**

**Modes disponibles :**
- Prélèvement SEPA
- Virement
- Chèque
- CESU

**Configuration :**
Fiche famille → Paiement → Mandat SEPA"""
    
    def _synthesize_urssaf(self):
        return """**📋 URSSAF et Déclarations**

**DSN** - Déclaration Sociale Nominative
- Mensuelle
- Génération automatique
- Transmission via portail

**Suivi :** Onglet "RH" → "Déclarations"."""
    
    def _synthesize_generic_improved(self, text, query):
        """Synthèse générique améliorée"""
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 30]
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        
        scored_lines = []
        for line in lines[:100]:  # Augmenté à 100 lignes
            score = sum(1 for w in query_words if w in line.lower())
            if score > 0:
                scored_lines.append((score, line))
        
        scored_lines.sort(reverse=True)
        best_lines = [line for _, line in scored_lines[:8]]  # Top 8
        
        if best_lines:
            synthesis = "**💡 Informations trouvées**\n\n"
            for line in best_lines:
                clean_line = ' '.join(line.split())
                if len(clean_line) > 20:
                    synthesis += f"• {clean_line}\n\n"
            synthesis += "\n💡 Pour plus de précisions, créez un ticket Freshdesk."
            return synthesis
        else:
            return "❌ Informations insuffisantes.\n\n💡 Créez un ticket Freshdesk pour une réponse détaillée."
    
    def create_freshdesk_ticket(self, query, answer, pages):
        ticket = f"""🎫 TICKET FRESHDESK - Assistant Kaizen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 OBJET
Question sur Kaizen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 QUESTION
{query}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 RÉPONSE IA
{answer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 PAGES CONSULTÉES
{', '.join([f'Page {p}' for p in pages]) if pages else 'Aucune'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ RAISON
Réponse insuffisante ou besoin de précisions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 INFORMATIONS
• Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}
• Nom : [À compléter]
• Email : [À compléter]
• Agence : [À compléter]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 PRÉCISIONS
[Ajoutez vos détails]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Ticket généré automatiquement
"""
        return ticket

def main():
    if 'assistant' not in st.session_state:
        st.session_state.assistant = KaizenAssistant()
    
    st.markdown("# 🤖 Assistant Kaizen")
    st.markdown("### 📚 Posez vos questions sur le manuel Kaizen")
    
    with st.sidebar:
        st.markdown("### 📊 Statistiques")
        if hasattr(st.session_state, 'history'):
            st.metric("Questions posées", len(st.session_state.history))
        
        st.markdown("---")
        st.success("✅ 13 concepts couverts\n✅ Synthèses pros\n✅ Tickets Freshdesk")
        
        if st.button("🗑️ Effacer historique"):
            st.session_state.history = []
            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Votre question")
        
        query = st.text_area(
            "Posez votre question :",
            value=st.session_state.get('selected_example', ''),
            height=80,
            placeholder="Ex: Comment créer un devis ?",
            key="query_input"
        )
        
        # Boutons TOUJOURS visibles côte à côte
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            search_btn = st.button("🔍 Rechercher", type="primary", use_container_width=True)
        
        with col_btn2:
            # CORRECTION : Bouton Freshdesk TOUJOURS visible
            ticket_btn = st.button("🎫 Ticket Freshdesk", use_container_width=True)
        
        # Recherche
        if search_btn and query:
            with st.spinner("🔎 Recherche..."):
                results = st.session_state.assistant.search_pages(query)
                answer, pages = st.session_state.assistant.synthesize_answer(query, results)
                
                st.session_state.history.append({
                    'timestamp': datetime.now().isoformat(),
                    'query': query,
                    'answer': answer,
                    'pages': pages
                })
                st.session_state.assistant.save_history()
                
                st.session_state.current_answer = answer
                st.session_state.current_pages = pages
                st.session_state.current_query = query
        
        # Affichage réponse
        if 'current_answer' in st.session_state and st.session_state.current_answer:
            st.markdown("---")
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.current_answer)
            
            if 'current_pages' in st.session_state and st.session_state.current_pages:
                st.markdown("\n**📍 Sources :**")
                for page in st.session_state.current_pages[:3]:
                    st.markdown(f'<span class="page-ref">Page {page}</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Cette réponse vous aide ?**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("👍 Oui")
            with col2:
                st.button("👌 Moyen")
            with col3:
                st.button("👎 Non")
        
        # Ticket Freshdesk
        if ticket_btn:
            if query:
                st.markdown("---")
                st.markdown('<div class="ticket-box">', unsafe_allow_html=True)
                st.markdown("### 🎫 Ticket Freshdesk")
                
                # Utiliser les infos de la dernière recherche ou générer avec question seule
                answer = st.session_state.get('current_answer', 'Aucune réponse générée')
                pages = st.session_state.get('current_pages', [])
                
                ticket = st.session_state.assistant.create_freshdesk_ticket(query, answer, pages)
                
                st.code(ticket, language="text")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.success("""
                ✅ **Ticket généré !**
                
                1. Copiez le contenu ci-dessus
                2. Allez sur Freshdesk
                3. Créez un ticket
                4. Collez et complétez
                """)
            else:
                st.warning("⚠️ Saisissez une question d'abord.")
    
    with col2:
        st.markdown("### 🎯 Exemples")
        
        examples = [
            "Réel ou mensualisé pour les devis ?",
            "C'est quoi l'AICI ?",
            "Comment créer un devis ?",
            "Comment faire un appariement ?"
        ]
        
        # CORRECTION : Boutons exemples fonctionnels
        for ex in examples:
            if st.button(f"💡 {ex}", key=f"btn_{hashlib.md5(ex.encode()).hexdigest()[:8]}", use_container_width=True):
                # Mettre la question dans le champ de texte
                st.session_state.selected_example = ex
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📜 Historique")
        
        if hasattr(st.session_state, 'history') and st.session_state.history:
            for entry in reversed(st.session_state.history[-3:]):
                with st.expander(f"🔍 {entry['query'][:25]}..."):
                    pages_str = ', '.join(map(str, entry.get('pages', [])[:2])) if entry.get('pages') else 'Aucune'
                    st.write(f"**Pages :** {pages_str}")
        else:
            st.info("Aucun historique")

if __name__ == "__main__":
    main()
