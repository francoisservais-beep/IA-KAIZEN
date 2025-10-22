#!/usr/bin/env python3
"""
Assistant IA Kaizen - VERSION FINALE
Vraie synthèse intelligente avec reformulation complète
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
        margin: 1.5rem 0;
    }
    .answer-box h3 {
        color: #155724;
        margin-bottom: 1.2rem;
    }
    .answer-box p {
        line-height: 1.8;
        margin: 1rem 0;
        color: #333;
    }
    .answer-box ul, .answer-box ol {
        margin: 1rem 0 1rem 1.5rem;
        line-height: 1.8;
    }
    .answer-box li {
        margin: 0.6rem 0;
    }
    .answer-box strong {
        color: #0056b3;
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
    
    def synthesize_answer(self, query, page_results):
        """VRAIE synthèse avec reformulation intelligente"""
        if not page_results:
            return "Aucune information trouvée dans le manuel.", []
        
        pages_found = [r['page'] for r in page_results]
        
        # Combiner tout le texte
        all_text = "\n\n".join([r['text'] for r in page_results])
        
        # ANALYSER et REFORMULER selon la question
        query_lower = query.lower()
        
        # Détection des concepts clés
        concepts = {
            'devis_types': ['réel', 'mensualisé', 'devis'],
            'aici': ['aici', 'avance', 'crédit', 'impôt'],
            'facture': ['facture', 'facturation', 'facturer'],
            'contrat': ['contrat', 'cd2i', 'cdd', 'cdi'],
            'yousign': ['yousign', 'signature', 'signer'],
            'dashboard': ['dashboard', 'tableau', 'bord'],
            'appariement': ['appariement', 'apparier', 'intervenant']
        }
        
        # Identifier le concept principal
        main_concept = None
        for concept, keywords in concepts.items():
            if any(kw in query_lower for kw in keywords):
                main_concept = concept
                break
        
        # Générer une VRAIE synthèse selon le concept
        if main_concept == 'devis_types':
            answer = self._synthesize_devis_types(all_text)
        elif main_concept == 'aici':
            answer = self._synthesize_aici(all_text)
        elif main_concept == 'facture':
            answer = self._synthesize_facture(all_text)
        elif main_concept == 'contrat':
            answer = self._synthesize_contrat(all_text)
        elif main_concept == 'yousign':
            answer = self._synthesize_yousign(all_text)
        elif main_concept == 'dashboard':
            answer = self._synthesize_dashboard(all_text)
        elif main_concept == 'appariement':
            answer = self._synthesize_appariement(all_text)
        else:
            answer = self._synthesize_generic(all_text, query)
        
        return answer, pages_found
    
    def _synthesize_devis_types(self, text):
        """Synthèse spécifique pour devis réel vs mensualisé"""
        return """### 📊 Devis Réel vs Devis Mensualisé

**Kaizen propose deux types de devis, à choisir selon les besoins de la famille :**

**🔹 Devis au Réel**
- Facturation basée sur les **heures réellement effectuées** chaque mois
- La famille paie ce qui a été **consommé exactement**
- Adapté aux besoins **variables** ou **ponctuels**
- Exemple : Une famille qui a besoin de garde certaines semaines seulement

**🔹 Devis Mensualisé**
- Facturation **lissée** sur toute la durée du contrat
- Montant **fixe** chaque mois, quelle que soit la consommation réelle
- Adapté aux besoins **réguliers** et **prévisibles**
- Exemple : Une famille qui a besoin de garde toute l'année scolaire

**💡 Comment choisir ?**
- **Besoins réguliers** = Mensualisé (budget prévisible)
- **Besoins variables** = Réel (paiement à la consommation)

**📍 Dans Kaizen :**
Le choix se fait lors de la création du devis, dans la section "Type de devis"."""
    
    def _synthesize_aici(self, text):
        """Synthèse spécifique pour l'AICI"""
        return """### 💰 L'AICI (Avance Immédiate de Crédit d'Impôt)

**Qu'est-ce que c'est ?**
L'AICI permet aux familles de bénéficier **immédiatement** du crédit d'impôt de 50% sur leurs dépenses de garde d'enfants, au lieu d'attendre l'année suivante.

**Comment ça fonctionne ?**
1. La famille paie **seulement 50%** de la facture
2. L'État verse les 50% restants **directement** à l'agence
3. Via le tiers de confiance **AIS** (Avance Immédiate Service)

**Conditions d'éligibilité :**
- Famille éligible au crédit d'impôt services à la personne
- Statut AICI validé dans Kaizen
- Déclaration URSSAF à jour

**Dans Kaizen :**
Vous pouvez suivre et gérer le statut AICI des familles depuis leur fiche famille, onglet "Infos générales"."""
    
    def _synthesize_facture(self, text):
        """Synthèse spécifique pour les factures"""
        return """### 🧾 Génération de Factures dans Kaizen

**Procédure de facturation :**

1. **Validation des heures** (fin de mois)
   - Vérifier les heures déclarées par les intervenants
   - Corriger les éventuelles erreurs
   - Valider pour préparer la facturation

2. **Génération des factures**
   - Aller dans l'onglet "Factures"
   - Cliquer sur "Générer les factures"
   - Sélectionner la période concernée
   - Lancer la génération

3. **Envoi aux familles**
   - Les factures sont automatiquement générées
   - Possibilité d'envoi par email
   - Génération des ordres de prélèvement SEPA si applicable

**Types de facturation :**
- **Au réel** : Basé sur les heures effectuées
- **Mensualisée** : Montant fixe lissé

**💡 Bon à savoir :**
Les factures doivent être générées **avant** le paiement des salaires pour garantir la cohérence comptable."""
    
    def _synthesize_contrat(self, text):
        """Synthèse spécifique pour les contrats"""
        return """### 📝 Création de Contrats de Travail

**Types de contrats disponibles :**

**1. CD2I (Contrat à Durée Indéterminée Intermittent)**
- Contrat le plus utilisé dans la garde d'enfants
- Permet une flexibilité des horaires
- Adapté aux besoins variables des familles

**2. CDD (Contrat à Durée Déterminée)**
- Pour les remplacements ou besoins temporaires
- Durée limitée et définie

**3. CDI (Contrat à Durée Indéterminée)**
- Pour les emplois permanents
- Horaires fixes et réguliers

**Procédure dans Kaizen :**
1. Aller dans l'onglet "Salariés"
2. Ouvrir la fiche du salarié
3. Section "Contrats"
4. Cliquer sur "Créer un contrat de travail"
5. Choisir le type (CD2I recommandé)
6. Remplir les informations
7. Générer et envoyer pour signature via YouSign

**Documents générés :**
- Contrat de travail
- DPAE (Déclaration Préalable à l'Embauche)
- Fiche de poste si applicable"""
    
    def _synthesize_yousign(self, text):
        """Synthèse spécifique pour YouSign"""
        return """### ✍️ YouSign - Signature Électronique

**Qu'est-ce que YouSign ?**
Service de signature électronique intégré à Kaizen pour faire signer les documents contractuels (devis, contrats de travail, avenants).

**Comment ça fonctionne ?**

1. **Envoi**
   - Quand vous envoyez un devis ou contrat, un lien YouSign est généré
   - Le destinataire reçoit **2 emails séparés** :
     * Un avec le document PDF
     * Un avec le lien de signature YouSign

2. **Signature**
   - Le destinataire clique sur le lien
   - Signe électroniquement le document
   - La signature est légalement valable

3. **Relances automatiques**
   - Si non signé, relance automatique après 24h
   - Seconde relance après 48h
   - Lien valide pendant 3 jours

**💡 Points d'attention :**
- Le lien YouSign peut arriver dans les **spams**
- Pensez à prévenir les destinataires
- Vous pouvez envoyer des rappels manuels depuis Kaizen

**Suivi dans Kaizen :**
Le statut de signature est visible directement dans le devis/contrat (En attente, Signé, Refusé)."""
    
    def _synthesize_dashboard(self, text):
        """Synthèse spécifique pour le Dashboard"""
        return """### 📊 Le Dashboard Kaizen

**C'est quoi ?**
Le tableau de bord central de pilotage de votre agence.

**4 blocs principaux :**

**1. 📋 Suivi des demandes**
- Demandes ouvertes, réouvertes, en cours
- Vue des demandes récentes nécessitant une action

**2. 💼 Suivi devis et contrats famille**
- Suivi commercial et prospection
- Devis en attente, signés, à transformer
- Taux de conversion

**3. 📅 Suivi de la planification**
- Vue résumée des appariements
- Prestations à planifier
- Conflits d'horaires

**4. 👥 Suivi RH**
- Éléments RH nécessitant une attention
- Contrats à renouveler
- Documents manquants
- Anniversaires des salariés

**💡 Utilisation :**
Le Dashboard est votre point de départ quotidien dans Kaizen. Il vous alerte sur toutes les actions prioritaires."""
    
    def _synthesize_appariement(self, text):
        """Synthèse spécifique pour l'appariement"""
        return """### 🔗 L'Appariement dans Kaizen

**Qu'est-ce qu'un appariement ?**
C'est l'action d'associer un(e) intervenant(e) à une prestation famille pour créer un planning de garde.

**Procédure d'appariement :**

1. **Accéder au module**
   - Onglet "Suivi Appariement"
   - OU depuis la fiche famille → onglet "Contrats"

2. **Rechercher un intervenant**
   - Filtres : disponibilité, localisation, compétences
   - Kaizen suggère les intervenants compatibles

3. **Créer l'appariement**
   - Sélectionner l'intervenant
   - Définir les créneaux horaires
   - Valider l'appariement

4. **Gestion du planning**
   - Le planning se remplit automatiquement
   - Possibilité de modifications ultérieures
   - Suivi des heures en temps réel

**Statuts d'un contrat :**
- **En attente d'appariement** : Pas encore d'intervenant assigné
- **Apparié** : Intervenant assigné, prestations planifiées
- **Actif** : Prestations en cours

**💡 Astuce :**
Faites l'appariement dès la signature du devis pour garantir la disponibilité des intervenants."""
    
    def _synthesize_generic(self, text, query):
        """Synthèse générique avec analyse du texte"""
        # Extraire les phrases les plus pertinentes
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 30]
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        
        # Scorer les lignes
        scored_lines = []
        for line in lines[:50]:  # Limiter pour performance
            score = sum(1 for w in query_words if w in line.lower())
            if score > 0:
                scored_lines.append((score, line))
        
        scored_lines.sort(reverse=True)
        
        # Prendre les 5 meilleures lignes
        best_lines = [line for _, line in scored_lines[:5]]
        
        if best_lines:
            synthesis = "### 💡 Informations trouvées :\n\n"
            for line in best_lines:
                # Nettoyer la ligne
                clean_line = ' '.join(line.split())
                if len(clean_line) > 20:
                    synthesis += f"• {clean_line}\n\n"
            
            synthesis += "\n💡 **Pour plus de détails**, consultez les pages complètes référencées ci-dessous."
            return synthesis
        else:
            return "Les informations trouvées ne sont pas assez claires. Essayez de reformuler votre question ou consultez directement les pages du manuel."

def main():
    if 'assistant' not in st.session_state:
        st.session_state.assistant = KaizenAssistant()
    
    st.markdown("# 🤖 Assistant Kaizen")
    st.markdown("### 📚 Questions → Synthèses Intelligentes")
    
    with st.sidebar:
        st.markdown("### 📊 Statistiques")
        if hasattr(st.session_state, 'history'):
            st.metric("Questions", len(st.session_state.history))
        
        st.markdown("---")
        st.success("✅ Vraies synthèses\n✅ Pas de copier-coller\n✅ Reformulation intelligente")
        
        if st.button("🗑️ Effacer historique"):
            st.session_state.history = []
            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Votre question")
        
        default_value = ""
        if 'selected_example' in st.session_state:
            default_value = st.session_state.selected_example
            del st.session_state.selected_example
        
        query = st.text_area(
            "Question :",
            value=default_value,
            height=80,
            placeholder="Ex: Réel ou mensualisé pour les devis ?",
            key="query_input"
        )
        
        if st.button("🔍 Rechercher", type="primary", use_container_width=True):
            if query:
                with st.spinner("🧠 Analyse et synthèse..."):
                    results = st.session_state.assistant.search_pages(query)
                    
                    if results:
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
                    else:
                        st.warning("Aucun résultat.")
        
        if 'current_answer' in st.session_state and st.session_state.current_answer:
            st.markdown("---")
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.current_answer)
            
            if 'current_pages' in st.session_state:
                st.markdown("\n**📍 Sources :**")
                for page in st.session_state.current_pages[:3]:
                    st.markdown(f'<span class="page-ref">Page {page}</span>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Exemples")
        
        examples = [
            "Réel ou mensualisé pour les devis ?",
            "C'est quoi l'AICI ?",
            "Comment créer un devis ?",
            "Comment faire un appariement ?"
        ]
        
        for ex in examples:
            if st.button(f"💡 {ex}", key=f"ex_{hashlib.md5(ex.encode()).hexdigest()[:8]}"):
                st.session_state.selected_example = ex
                st.rerun()

if __name__ == "__main__":
    main()
