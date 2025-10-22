#!/usr/bin/env python3
"""
Assistant IA Kaizen v4.0 - Version avec VRAIE synthèse
- Affichage corrigé (pas de markdown brut)
- Synthèse intelligente du contenu
- Reformulation claire et structurée
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

# CSS amélioré
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class KaizenAssistant:
    """Assistant IA avec synthèse intelligente"""
    
    def __init__(self):
        if os.path.exists("Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "Kaizen_-_Manuel_ope_ratoire.pdf"
        elif os.path.exists("/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"
        else:
            self.pdf_path = None
            
        self.history_file = "chat_history.json"
        self.pdf_text_cache = None
        self.load_history()
        
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    st.session_state.history = json.load(f)
            else:
                st.session_state.history = []
        except:
            st.session_state.history = []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def extract_pdf_text(self):
        """Extrait le texte du PDF page par page"""
        if self.pdf_text_cache:
            return self.pdf_text_cache
            
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            return None
        
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', self.pdf_path, '-'],
                capture_output=True,
                text=True,
                check=True
            )
            
            pages = result.stdout.split('\f')
            self.pdf_text_cache = {}
            
            for i, page_text in enumerate(pages, 1):
                if page_text.strip():
                    self.pdf_text_cache[i] = page_text.strip()
            
            return self.pdf_text_cache
            
        except Exception as e:
            st.error(f"Erreur lors de l'extraction du PDF : {str(e)}")
            return None
    
    def search_in_pdf_by_pages(self, query):
        """Recherche dans le PDF par pages"""
        pdf_pages = self.extract_pdf_text()
        
        if not pdf_pages:
            return []
        
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 2]
        
        results = []
        
        for page_num, page_text in pdf_pages.items():
            page_lower = page_text.lower()
            score = 0
            
            for word in query_words:
                count = page_lower.count(word)
                if count > 0:
                    score += count
            
            if score > 0:
                results.append({
                    'page': page_num,
                    'score': score,
                    'text': page_text
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:3]  # Top 3 pages
    
    def synthesize_answer(self, query, page_results):
        """
        VRAIE SYNTHÈSE INTELLIGENTE
        Analyse le contenu et crée une réponse structurée
        """
        if not page_results:
            return None, []
        
        # Combiner le texte des meilleures pages
        combined_text = "\n\n".join([r['text'] for r in page_results])
        pages_found = [r['page'] for r in page_results]
        
        # Analyser le type de question
        query_lower = query.lower()
        is_how = any(w in query_lower for w in ['comment', 'créer', 'faire', 'générer'])
        is_what = any(w in query_lower for w in ['qu\'est-ce', 'c\'est quoi', 'définition'])
        is_where = any(w in query_lower for w in ['où', 'trouver', 'accéder', 'onglet'])
        
        # SYNTHÈSE INTELLIGENTE
        synthesis = []
        
        # Extraire les informations clés
        if is_how:
            # Pour les "comment", extraire les étapes
            steps = self._extract_procedure(combined_text)
            if steps:
                synthesis.append("**Procédure :**")
                for i, step in enumerate(steps, 1):
                    synthesis.append(f"{i}. {step}")
            else:
                # Si pas d'étapes claires, faire un résumé
                synthesis.append(self._summarize_procedure(combined_text))
        
        elif is_what:
            # Pour les "qu'est-ce", faire une définition
            definition = self._extract_definition(combined_text, query)
            synthesis.append(f"**Définition :**")
            synthesis.append(definition)
        
        elif is_where:
            # Pour les "où", extraire la navigation
            navigation = self._extract_navigation(combined_text)
            synthesis.append("**Navigation :**")
            synthesis.append(navigation)
        
        else:
            # Réponse générale : résumé intelligent
            summary = self._create_summary(combined_text, query)
            synthesis.append(summary)
        
        # Ajouter les points clés
        key_points = self._extract_key_points(combined_text, query)
        if key_points:
            synthesis.append("\n**Points importants :**")
            for point in key_points:
                synthesis.append(f"• {point}")
        
        answer = "\n".join(synthesis)
        
        return answer, pages_found
    
    def _extract_procedure(self, text):
        """Extrait les étapes d'une procédure"""
        steps = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Chercher les lignes qui commencent par un numéro ou "Étape"
            if re.match(r'^\d+[\.)]\s+', line):
                step = re.sub(r'^\d+[\.)]\s+', '', line)
                if len(step) > 10:  # Filtrer les étapes trop courtes
                    steps.append(step)
            elif re.match(r'^[•\-]\s+', line):
                step = re.sub(r'^[•\-]\s+', '', line)
                if len(step) > 10:
                    steps.append(step)
        
        return steps[:8]  # Max 8 étapes
    
    def _summarize_procedure(self, text):
        """Résume une procédure quand pas d'étapes claires"""
        # Prendre les phrases importantes
        sentences = re.split(r'[.!?]\s+', text)
        important = []
        
        for sent in sentences:
            if len(sent) > 30 and any(word in sent.lower() for word in ['cliquer', 'aller', 'sélectionner', 'ouvrir', 'créer']):
                important.append(sent.strip())
        
        return ' '.join(important[:3]) + '.'
    
    def _extract_definition(self, text, query):
        """Extrait une définition"""
        # Chercher la première occurrence du terme dans le texte
        sentences = re.split(r'[.!?]\s+', text)
        
        # Extraire le terme cherché
        query_words = query.lower().split()
        main_term = [w for w in query_words if len(w) > 3]
        
        definition_sentences = []
        for sent in sentences:
            if len(sent) > 20 and any(term in sent.lower() for term in main_term):
                definition_sentences.append(sent.strip())
                if len(definition_sentences) >= 3:
                    break
        
        if definition_sentences:
            return ' '.join(definition_sentences)
        else:
            return sentences[0] if sentences else text[:200]
    
    def _extract_navigation(self, text):
        """Extrait les informations de navigation"""
        lines = text.split('\n')
        nav_lines = []
        
        for line in lines:
            line_lower = line.lower()
            if any(word in line_lower for word in ['onglet', 'menu', 'cliquez', 'rendez-vous', 'accéder']):
                if len(line.strip()) > 10:
                    nav_lines.append(line.strip())
        
        return ' '.join(nav_lines[:4])
    
    def _create_summary(self, text, query):
        """Crée un résumé général"""
        sentences = re.split(r'[.!?]\s+', text)
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        
        relevant = []
        for sent in sentences:
            sent_lower = sent.lower()
            score = sum(1 for word in query_words if word in sent_lower)
            if score > 0 and len(sent) > 30:
                relevant.append((score, sent.strip()))
        
        relevant.sort(reverse=True, key=lambda x: x[0])
        
        summary_parts = [sent for score, sent in relevant[:4]]
        return ' '.join(summary_parts)
    
    def _extract_key_points(self, text, query):
        """Extrait les points clés"""
        lines = text.split('\n')
        key_points = []
        
        for line in lines:
            line = line.strip()
            # Chercher les lignes importantes (bullets, warnings, notes)
            if re.match(r'^[•\-]\s+', line) or 'important' in line.lower() or 'attention' in line.lower():
                point = re.sub(r'^[•\-]\s+', '', line)
                if 10 < len(point) < 150:
                    key_points.append(point)
        
        return key_points[:4]  # Max 4 points

def main():
    """Fonction principale"""
    
    if 'assistant' not in st.session_state:
        st.session_state.assistant = KaizenAssistant()
    
    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = None
    
    if 'page_results' not in st.session_state:
        st.session_state.page_results = []
    
    # En-tête
    st.markdown('<h1 class="main-header">🤖 Assistant IA Kaizen</h1>', unsafe_allow_html=True)
    st.markdown("### 📚 Posez vos questions sur le manuel opératoire Kaizen")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Assistant Kaizen")
        st.markdown("**Version 4.0** - Synthèse intelligente")
        st.markdown("---")
        
        st.markdown("### 📊 Statistiques")
        if hasattr(st.session_state, 'history'):
            total = len(st.session_state.history)
            st.markdown(f'<div class="stats-card"><h3>{total}</h3><p>Questions posées</p></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        st.success("""
        **✨ Version 4.0**
        
        ✅ Vraie synthèse intelligente
        
        ✅ Affichage corrigé
        
        ✅ Réponses structurées
        
        ✅ Points clés extraits
        """)
        
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.history = []
            st.session_state.assistant.save_history()
            st.rerun()
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Posez votre question")
        
        default_value = ""
        if 'selected_example' in st.session_state:
            default_value = st.session_state.selected_example
            del st.session_state.selected_example
        
        query = st.text_area(
            "Que voulez-vous savoir sur Kaizen ?",
            value=default_value,
            height=100,
            placeholder="Ex: Comment créer un devis ? Qu'est-ce que l'AICI ?",
            key="query_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            search_clicked = st.button("🔍 Rechercher", type="primary", use_container_width=True)
        
        with col_btn2:
            ticket_clicked = st.button("🎫 Créer un ticket", use_container_width=True)
        
        # Recherche
        if search_clicked and query:
            with st.spinner("🔎 Analyse du manuel en cours..."):
                page_results = st.session_state.assistant.search_in_pdf_by_pages(query)
                st.session_state.page_results = page_results
                
                if page_results:
                    answer, pages_found = st.session_state.assistant.synthesize_answer(query, page_results)
                    
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'query': query,
                        'answer': answer,
                        'pages': pages_found
                    })
                    st.session_state.assistant.save_history()
                    
                    st.session_state.current_answer = answer
                    st.session_state.current_pages = pages_found
                    st.session_state.current_extracts = page_results
                else:
                    st.error("❌ Aucune information trouvée dans le manuel.")
        
        # Affichage de la réponse
        if st.session_state.current_answer:
            st.markdown("---")
            
            # Réponse dans un container Streamlit (pas markdown brut)
            with st.container():
                st.success("✅ Réponse")
                
                # Afficher la réponse ligne par ligne (pour éviter le markdown brut)
                answer_lines = st.session_state.current_answer.split('\n')
                for line in answer_lines:
                    if line.strip():
                        if line.startswith('**') and line.endswith('**'):
                            # Titres
                            st.markdown(f"### {line.strip('*')}")
                        elif line.startswith('•'):
                            # Bullets
                            st.markdown(line)
                        elif re.match(r'^\d+\.', line):
                            # Étapes numérotées
                            st.markdown(line)
                        else:
                            # Texte normal
                            st.write(line)
            
            # Références
            if 'current_pages' in st.session_state and st.session_state.current_pages:
                st.info(f"📄 **Sources :** Pages {', '.join(map(str, st.session_state.current_pages))}")
            
            # Extraits
            if 'current_extracts' in st.session_state and st.session_state.current_extracts:
                st.markdown("---")
                st.markdown("### 📖 Consulter les extraits")
                
                for extract in st.session_state.current_extracts:
                    with st.expander(f"📄 Page {extract['page']}", expanded=False):
                        st.text(extract['text'][:800])
            
            # Feedback
            st.markdown("---")
            st.markdown("**Cette réponse vous aide-t-elle ?**")
            col_fb1, col_fb2, col_fb3 = st.columns(3)
            with col_fb1:
                if st.button("👍 Oui, parfait"):
                    st.success("Merci !")
            with col_fb2:
                if st.button("👌 Partiellement"):
                    st.info("Reformulez pour plus de précision.")
            with col_fb3:
                if st.button("👎 Non"):
                    st.warning("Créez un ticket pour une aide personnalisée.")
    
    with col2:
        st.markdown("### 📜 Historique")
        
        if hasattr(st.session_state, 'history') and st.session_state.history:
            for entry in reversed(st.session_state.history[-5:]):
                with st.expander(f"🔍 {entry['query'][:40]}...", expanded=False):
                    st.markdown(f"**Date :** {entry['timestamp'][:19]}")
                    if 'pages' in entry:
                        st.markdown(f"**Pages :** {', '.join(map(str, entry['pages']))}")
        else:
            st.info("Aucune recherche")
        
        st.markdown("---")
        st.markdown("### 🎯 Exemples")
        
        examples = [
            "Comment créer un devis ?",
            "Qu'est-ce que l'AICI ?",
            "Comment générer une facture ?",
            "Où trouver le Dashboard ?",
            "Comment faire un appariement ?"
        ]
        
        for ex in examples:
            if st.button(f"💡 {ex}", key=f"ex_{hashlib.md5(ex.encode()).hexdigest()[:8]}", 
                        use_container_width=True):
                st.session_state.selected_example = ex
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem 0;'>
        <p>🤖 Assistant Kaizen v4.0 - Synthèse Intelligente</p>
        <p style='font-size: 0.8rem;'>Octobre 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
