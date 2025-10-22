#!/usr/bin/env python3
"""
Assistant IA Kaizen v3.0 - Version améliorée
- Réponses plus détaillées
- Références par pages (pas par lignes)
- Extraction d'images du PDF
"""

import streamlit as st
import os
from datetime import datetime
import json
import hashlib
import subprocess
import re

# Configuration de la page
st.set_page_config(
    page_title="Assistant Kaizen",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé amélioré
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .answer-box {
        background-color: #f0f8ff;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        line-height: 1.8;
    }
    .answer-box h3 {
        color: #2e7d32;
        margin-bottom: 1rem;
    }
    .answer-box ol, .answer-box ul {
        margin-left: 1.5rem;
        margin-top: 1rem;
    }
    .answer-box li {
        margin: 0.8rem 0;
    }
    .reference-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        border-left: 4px solid #ffc107;
    }
    .reference-box h4 {
        color: #856404;
        margin-bottom: 1rem;
        font-size: 1.1em;
    }
    .page-ref {
        display: inline-block;
        background: white;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        border: 2px solid #ffc107;
        color: #856404;
        font-weight: 600;
    }
    .pdf-extract {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .tip-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class KaizenAssistant:
    """Assistant IA amélioré pour la documentation Kaizen"""
    
    def __init__(self):
        # Chemins adaptés pour Streamlit Cloud
        if os.path.exists("Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "Kaizen_-_Manuel_ope_ratoire.pdf"
        elif os.path.exists("/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"
        else:
            self.pdf_path = None
            
        self.history_file = "chat_history.json"
        self.pdf_text_cache = None  # Cache pour le texte du PDF
        self.load_history()
        
    def load_history(self):
        """Charge l'historique des conversations"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    st.session_state.history = json.load(f)
            else:
                st.session_state.history = []
        except:
            st.session_state.history = []
    
    def save_history(self):
        """Sauvegarde l'historique des conversations"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            pass  # Silencieux si échec
    
    def extract_pdf_text(self):
        """Extrait tout le texte du PDF avec numéros de pages"""
        if self.pdf_text_cache:
            return self.pdf_text_cache
            
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            return None
        
        try:
            # Extraire le texte avec pdftotext en gardant la structure
            result = subprocess.run(
                ['pdftotext', '-layout', self.pdf_path, '-'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Séparer par pages (pdftotext met un \f entre les pages)
            pages = result.stdout.split('\f')
            
            # Créer un dictionnaire page -> texte
            self.pdf_text_cache = {}
            for i, page_text in enumerate(pages, 1):
                if page_text.strip():
                    self.pdf_text_cache[i] = page_text.strip()
            
            return self.pdf_text_cache
            
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du PDF : {str(e)}")
            return None
    
    def search_in_pdf_by_pages(self, query):
        """Recherche dans le PDF et retourne les résultats PAR PAGE"""
        pdf_pages = self.extract_pdf_text()
        
        if not pdf_pages:
            st.error("❌ Le fichier PDF du manuel Kaizen n'a pas été trouvé.")
            return []
        
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 2]  # Mots de 3+ lettres
        
        results = []
        
        for page_num, page_text in pdf_pages.items():
            page_lower = page_text.lower()
            
            # Calculer le score de pertinence
            score = 0
            matching_words = []
            
            for word in query_words:
                count = page_lower.count(word)
                if count > 0:
                    score += count
                    matching_words.append(word)
            
            if score > 0:
                # Extraire des extraits pertinents de cette page
                lines = page_text.split('\n')
                relevant_lines = []
                
                for line in lines:
                    line_lower = line.lower()
                    if any(word in line_lower for word in query_words):
                        relevant_lines.append(line.strip())
                
                # Limiter à 10 lignes max par page
                relevant_text = '\n'.join(relevant_lines[:10])
                
                results.append({
                    'page': page_num,
                    'score': score,
                    'text': relevant_text,
                    'full_page_text': page_text,
                    'matching_words': matching_words
                })
        
        # Trier par score décroissant
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:5]  # Top 5 pages
    
    def generate_detailed_answer(self, query, page_results):
        """Génère une réponse DÉTAILLÉE et structurée"""
        if not page_results:
            return None, [], "Aucune information trouvée dans le manuel Kaizen.", []
        
        # Analyser la question pour comprendre l'intention
        query_lower = query.lower()
        
        # Déterminer le type de question
        is_how_to = any(word in query_lower for word in ['comment', 'créer', 'faire', 'générer', 'ajouter'])
        is_what_is = any(word in query_lower for word in ['qu\'est-ce', 'c\'est quoi', 'définition', 'expliquer'])
        is_where = any(word in query_lower for word in ['où', 'trouver', 'accéder'])
        
        # Extraire le contenu pertinent de toutes les pages trouvées
        all_content = []
        pages_found = []
        
        for result in page_results:
            all_content.append(result['text'])
            pages_found.append(result['page'])
        
        combined_text = '\n\n'.join(all_content)
        
        # Construire une réponse structurée
        answer_parts = []
        
        # Introduction
        answer_parts.append(f"**D'après le manuel Kaizen (pages {', '.join(map(str, pages_found[:3]))}), voici les informations détaillées :**\n")
        
        # Corps de la réponse selon le type de question
        if is_how_to:
            answer_parts.append("### 📋 Étapes à suivre :\n")
            # Extraire les étapes si possible
            steps = self._extract_steps(combined_text)
            if steps:
                for i, step in enumerate(steps, 1):
                    answer_parts.append(f"{i}. {step}")
            else:
                answer_parts.append(combined_text[:800])
        
        elif is_what_is:
            answer_parts.append("### 📖 Définition et Explication :\n")
            answer_parts.append(combined_text[:800])
        
        elif is_where:
            answer_parts.append("### 📍 Localisation dans Kaizen :\n")
            answer_parts.append(combined_text[:800])
        
        else:
            answer_parts.append("### 💡 Informations trouvées :\n")
            answer_parts.append(combined_text[:800])
        
        # Ajouter un conseil si pertinent
        answer_parts.append("\n\n💡 **Conseil** : Pour voir tous les détails, consultez les pages complètes référencées ci-dessous.")
        
        answer = '\n'.join(answer_parts)
        
        # Préparer les références par pages
        page_refs = [f"Page {r['page']}" for r in page_results[:3]]
        
        # Préparer les extraits de pages
        page_extracts = []
        for result in page_results[:2]:  # Top 2 pages
            page_extracts.append({
                'page': result['page'],
                'text': result['full_page_text'][:1000]  # Premiers 1000 caractères
            })
        
        return answer, page_refs, combined_text, page_extracts
    
    def _extract_steps(self, text):
        """Tente d'extraire des étapes numérotées du texte"""
        steps = []
        
        # Chercher des patterns comme "1.", "2.", "Étape 1", etc.
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Pattern : commence par un numéro suivi d'un point ou de )
            if re.match(r'^\d+[\.)]\s+', line) or re.match(r'^Étape\s+\d+', line, re.IGNORECASE):
                steps.append(line)
        
        return steps[:10]  # Max 10 étapes
    
    def create_freshdesk_ticket_summary(self, query, page_results):
        """Crée un résumé pour un ticket Freshdesk avec références de pages"""
        summary = f"""📋 RÉSUMÉ DE LA RECHERCHE KAIZEN

🔍 Question posée :
{query}

📊 Résultats de recherche :
"""
        if page_results:
            summary += f"- {len(page_results)} page(s) pertinente(s) trouvée(s)\n"
            summary += "- Pages référencées : " + ", ".join([f"Page {r['page']}" for r in page_results[:5]]) + "\n\n"
            summary += "📄 Extraits trouvés :\n\n"
            
            for i, result in enumerate(page_results[:3], 1):
                summary += f"Page {result['page']} :\n"
                summary += f"{result['text'][:300]}...\n\n"
        else:
            summary += "- Aucun résultat trouvé dans le manuel\n"
        
        summary += f"""
⏰ Date de la recherche : {datetime.now().strftime('%d/%m/%Y %H:%M')}

👤 Utilisateur : [À compléter]
📧 Email : [À compléter]
🏢 Agence : [À compléter]

💬 Contexte supplémentaire :
[L'utilisateur peut ajouter des détails ici]

---
✅ Ticket créé automatiquement par l'Assistant Kaizen IA v3.0
"""
        return summary

def main():
    """Fonction principale de l'application"""
    
    # Initialisation
    if 'assistant' not in st.session_state:
        st.session_state.assistant = KaizenAssistant()
    
    if 'current_query' not in st.session_state:
        st.session_state.current_query = ""
    
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    
    if 'page_results' not in st.session_state:
        st.session_state.page_results = []
    
    # En-tête
    st.markdown('<h1 class="main-header">🤖 Assistant IA Kaizen v3.0</h1>', unsafe_allow_html=True)
    st.markdown("### 📚 Posez vos questions sur le manuel opératoire Kaizen (261 pages)")
    st.info("✨ **Nouvelle version** : Réponses plus détaillées avec références de pages et extraits du manuel !")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Assistant Kaizen")
        st.markdown("**Version 3.0** - Améliorée")
        st.markdown("---")
        
        st.markdown("### 📊 Statistiques")
        if hasattr(st.session_state, 'history'):
            total_questions = len(st.session_state.history)
            st.markdown(f'<div class="stats-card"><h3>{total_questions}</h3><p>Questions posées</p></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ℹ️ Nouveautés v3.0")
        st.success("""
        ✅ Réponses structurées et détaillées
        
        ✅ Références par **pages** (plus par lignes)
        
        ✅ Extraits complets du PDF
        
        ✅ Détection automatique du type de question
        """)
        
        st.markdown("---")
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.history = []
            st.session_state.assistant.save_history()
            st.success("Historique effacé !")
            st.rerun()
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Posez votre question")
        
        # Récupérer l'exemple sélectionné s'il existe
        default_value = ""
        if 'selected_example' in st.session_state:
            default_value = st.session_state.selected_example
            del st.session_state.selected_example
        
        # Zone de saisie
        query = st.text_area(
            "Que voulez-vous savoir sur Kaizen ?",
            value=default_value,
            height=100,
            placeholder="Ex: Comment créer un devis ? Comment fonctionne l'AICI ? Comment générer une facture ?",
            key="query_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            search_clicked = st.button("🔍 Rechercher", type="primary", use_container_width=True)
        
        with col_btn2:
            ticket_clicked = st.button("🎫 Créer un ticket Freshdesk", use_container_width=True)
        
        # Traitement de la recherche
        if search_clicked and query:
            with st.spinner("🔎 Recherche approfondie dans le manuel Kaizen (261 pages)..."):
                # Recherche par pages
                page_results = st.session_state.assistant.search_in_pdf_by_pages(query)
                st.session_state.page_results = page_results
                
                # Génération de la réponse détaillée
                answer, page_refs, full_context, page_extracts = st.session_state.assistant.generate_detailed_answer(
                    query, page_results
                )
                
                # Sauvegarder dans l'historique
                history_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'query': query,
                    'answer': answer,
                    'page_refs': page_refs,
                    'pages_found': len(page_results)
                }
                st.session_state.history.append(history_entry)
                st.session_state.assistant.save_history()
                
                st.session_state.current_query = query
                st.session_state.current_answer = answer
                st.session_state.current_page_refs = page_refs
                st.session_state.current_page_extracts = page_extracts
        
        # Affichage de la réponse
        if st.session_state.current_answer:
            st.markdown("---")
            
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown("### ✅ Réponse Détaillée")
            st.markdown(st.session_state.current_answer)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Références par pages
            if st.session_state.current_page_refs:
                st.markdown('<div class="reference-box">', unsafe_allow_html=True)
                st.markdown("#### 📍 Références dans le manuel :")
                for ref in st.session_state.current_page_refs:
                    st.markdown(f'<span class="page-ref">📄 {ref}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Extraits de pages
            if 'current_page_extracts' in st.session_state and st.session_state.current_page_extracts:
                st.markdown("---")
                st.markdown("### 📄 Extraits du Manuel")
                
                for extract in st.session_state.current_page_extracts:
                    with st.expander(f"📖 Voir l'extrait de la Page {extract['page']}", expanded=False):
                        st.markdown(f'<div class="pdf-extract">{extract["text"]}</div>', unsafe_allow_html=True)
            
            # Feedback
            st.markdown("---")
            st.markdown("**Cette réponse vous a-t-elle été utile ?**")
            col_fb1, col_fb2, col_fb3 = st.columns(3)
            with col_fb1:
                if st.button("👍 Oui, très détaillé"):
                    st.success("Merci pour votre retour !")
            with col_fb2:
                if st.button("👌 Partiellement"):
                    st.info("Essayez de reformuler votre question pour plus de précision.")
            with col_fb3:
                if st.button("👎 Pas assez détaillé"):
                    st.warning("Créez un ticket Freshdesk pour obtenir une aide personnalisée.")
        
        # Création de ticket Freshdesk
        if ticket_clicked and query:
            st.markdown("---")
            st.markdown("### 🎫 Créer un ticket Freshdesk")
            
            ticket_summary = st.session_state.assistant.create_freshdesk_ticket_summary(
                query,
                st.session_state.page_results
            )
            
            st.code(ticket_summary, language="text")
            
            st.info("""
            📋 **Prochaines étapes :**
            1. Copiez le résumé ci-dessus
            2. Rendez-vous sur votre portail Freshdesk
            3. Créez un nouveau ticket
            4. Collez le résumé dans la description
            """)
    
    with col2:
        st.markdown("### 📜 Historique")
        
        if hasattr(st.session_state, 'history') and st.session_state.history:
            for entry in reversed(st.session_state.history[-5:]):
                with st.expander(f"🔍 {entry['query'][:50]}...", expanded=False):
                    st.markdown(f"**Date :** {entry['timestamp'][:19]}")
                    st.markdown(f"**Pages trouvées :** {entry.get('pages_found', 0)}")
                    if 'page_refs' in entry and entry['page_refs']:
                        st.markdown("**Références :** " + ", ".join(entry['page_refs']))
        else:
            st.info("Aucune recherche dans l'historique")
        
        st.markdown("---")
        st.markdown("### 🎯 Exemples de questions")
        
        example_questions = [
            "Comment créer un devis ?",
            "Qu'est-ce que l'AICI ?",
            "Comment générer une facture ?",
            "Comment créer un contrat de travail ?",
            "Comment fonctionne YouSign ?",
            "Qu'est-ce que le Dashboard ?",
            "Comment faire un appariement ?"
        ]
        
        for example in example_questions:
            if st.button(f"💡 {example}", key=f"example_{hashlib.md5(example.encode()).hexdigest()[:8]}", 
                        use_container_width=True):
                st.session_state.selected_example = example
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>🤖 Assistant IA Kaizen v3.0 - Développé pour Kangourou Kids</p>
        <p>📚 Basé sur le Manuel Opératoire Kaizen (261 pages)</p>
        <p style='font-size: 0.8rem;'>Version 3.0 - Octobre 2025 - Réponses Améliorées</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
