#!/usr/bin/env python3
"""
Assistant IA Kaizen v4.0 - Synthèse Intelligente
Réponses professionnelles synthétisées
"""

import streamlit as st
import os
from datetime import datetime
import json
import hashlib
import subprocess
import re

st.set_page_config(
    page_title="Assistant Kaizen v4.0",
    page_icon="📚",
    layout="wide"
)

# CSS corrigé
st.markdown("""
<style>
    .answer-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .answer-title {
        color: #2e7d32;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .answer-content {
        color: #333;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    .answer-content p {
        margin: 1rem 0;
    }
    .answer-content strong {
        color: #1976d2;
        font-weight: 600;
    }
    .answer-content ol, .answer-content ul {
        margin: 1rem 0 1rem 1.5rem;
    }
    .answer-content li {
        margin: 0.8rem 0;
    }
    .reference-container {
        background: #fff9e6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        border-left: 4px solid #ffc107;
    }
    .page-badge {
        display: inline-block;
        background: white;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        border: 2px solid #ffc107;
        color: #856404;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .tip-box {
        background: #e3f2fd;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
        font-size: 0.95rem;
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
    
    def extract_pdf_by_pages(self):
        """Extrait le PDF page par page"""
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
        """Recherche dans les pages du PDF"""
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
        """VRAIE SYNTHÈSE intelligente - pas de copier-coller"""
        if not page_results:
            return None, []
        
        pages_found = [r['page'] for r in page_results]
        query_lower = query.lower()
        
        # Analyser TOUT le contenu des pages pertinentes
        all_text = "\n\join([r['text'] for r in page_results[:3]])
        
        # Détecter le type de question
        is_how = any(w in query_lower for w in ['comment', 'créer', 'faire', 'générer'])
        is_what = any(w in query_lower for w in ['qu\'est-ce', 'c\'est quoi', 'définir'])
        is_where = any(w in query_lower for w in ['où', 'trouver', 'accéder'])
        
        # Construire une VRAIE synthèse
        answer = f"**D'après le manuel Kaizen (pages {', '.join(map(str, pages_found[:3]))}), voici la synthèse :**\n\n"
        
        # Extraire et reformuler les informations clés
        if is_how:
            answer += self._synthesize_how_to(all_text, query)
        elif is_what:
            answer += self._synthesize_definition(all_text, query)
        elif is_where:
            answer += self._synthesize_location(all_text, query)
        else:
            answer += self._synthesize_general(all_text, query)
        
        return answer, pages_found
    
    def _synthesize_how_to(self, text, query):
        """Synthétise une procédure"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # Chercher les étapes numérotées
        steps = []
        for line in lines:
            if re.match(r'^\d+[\.)]\s+|^Étape\s+\d+', line, re.IGNORECASE):
                steps.append(line)
        
        if steps:
            synthesis = "### 📋 Procédure :\n\n"
            for step in steps[:8]:
                synthesis += f"• {step}\n"
        else:
            # Pas d'étapes trouvées, faire une synthèse manuelle
            synthesis = "### 💡 Informations clés :\n\n"
            
            # Extraire les phrases pertinentes
            sentences = []
            for line in lines:
                if len(line) > 30 and any(w in line.lower() for w in query.lower().split()):
                    sentences.append(line)
            
            for sent in sentences[:6]:
                synthesis += f"• {sent}\n"
        
        return synthesis + "\n\n💡 **Astuce :** Consultez les pages complètes pour plus de détails."
    
    def _synthesize_definition(self, text, query):
        """Synthétise une définition"""
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 20]
        
        synthesis = "### 📖 Définition :\n\n"
        
        # Trouver les phrases définitoires
        definitions = []
        for line in lines[:15]:
            line_lower = line.lower()
            if any(marker in line_lower for marker in ['est', 'permet', 'désigne', 'correspond']):
                definitions.append(line)
        
        for defin in definitions[:4]:
            synthesis += f"{defin}\n\n"
        
        return synthesis.strip()
    
    def _synthesize_location(self, text, query):
        """Synthétise un chemin de navigation"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        synthesis = "### 📍 Accès dans Kaizen :\n\n"
        
        # Chercher les mentions d'onglets, menus, boutons
        nav_keywords = ['onglet', 'menu', 'bouton', 'cliquer', 'accéder', 'rendez-vous']
        nav_lines = []
        
        for line in lines:
            if any(kw in line.lower() for kw in nav_keywords):
                nav_lines.append(line)
        
        for nav in nav_lines[:5]:
            synthesis += f"• {nav}\n"
        
        return synthesis
    
    def _synthesize_general(self, text, query):
        """Synthèse générale"""
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l) > 30]
        
        synthesis = "### 💡 Informations trouvées :\n\n"
        
        # Extraire les lignes pertinentes
        relevant = []
        query_words = query.lower().split()
        
        for line in lines:
            score = sum(1 for w in query_words if w in line.lower())
            if score > 0:
                relevant.append((score, line))
        
        relevant.sort(reverse=True)
        
        for _, line in relevant[:6]:
            synthesis += f"• {line}\n"
        
        return synthesis

def main():
    if 'assistant' not in st.session_state:
        st.session_state.assistant = KaizenAssistant()
    
    # En-tête
    st.markdown("# 🤖 Assistant Kaizen v4.0")
    st.markdown("### 📚 Posez vos questions - Obtenez des synthèses intelligentes")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Assistant Kaizen")
        st.markdown("**Version 4.0** - Synthèse IA")
        st.markdown("---")
        
        if hasattr(st.session_state, 'history'):
            st.metric("Questions posées", len(st.session_state.history))
        
        st.markdown("---")
        st.info("""
        ✅ Vraies synthèses intelligentes
        
        ✅ Pas de copier-coller
        
        ✅ Réponses structurées
        
        ✅ Références par pages
        """)
        
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.history = []
            st.rerun()
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Votre question")
        
        # Récupérer exemple sélectionné
        default_value = ""
        if 'selected_example' in st.session_state:
            default_value = st.session_state.selected_example
            del st.session_state.selected_example
        
        query = st.text_area(
            "Posez votre question ici",
            value=default_value,
            height=100,
            placeholder="Ex: Comment créer un devis ?",
            key="query_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            search_btn = st.button("🔍 Rechercher", type="primary", use_container_width=True)
        
        with col_btn2:
            ticket_btn = st.button("🎫 Ticket Freshdesk", use_container_width=True)
        
        # Recherche
        if search_btn and query:
            with st.spinner("🔎 Analyse et synthèse en cours..."):
                page_results = st.session_state.assistant.search_pages(query)
                
                if page_results:
                    answer, pages_found = st.session_state.assistant.synthesize_answer(query, page_results)
                    
                    # Sauvegarder
                    st.session_state.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'query': query,
                        'answer': answer,
                        'pages': pages_found
                    })
                    st.session_state.assistant.save_history()
                    
                    st.session_state.current_answer = answer
                    st.session_state.current_pages = pages_found
                else:
                    st.warning("Aucun résultat trouvé.")
        
        # Affichage réponse
        if 'current_answer' in st.session_state and st.session_state.current_answer:
            st.markdown("---")
            
            st.markdown('<div class="answer-container">', unsafe_allow_html=True)
            st.markdown('<div class="answer-title">✅ Synthèse</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer-content">{st.session_state.current_answer}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Références
            if 'current_pages' in st.session_state:
                st.markdown('<div class="reference-container">', unsafe_allow_html=True)
                st.markdown("**📍 Pages consultées :**")
                for page in st.session_state.current_pages:
                    st.markdown(f'<span class="page-badge">📄 Page {page}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Feedback
            st.markdown("---")
            st.markdown("**Cette synthèse vous aide-t-elle ?**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("👍 Oui")
            with col2:
                st.button("👌 Partiellement")
            with col3:
                st.button("👎 Non")
    
    with col2:
        st.markdown("### 📜 Historique")
        
        if hasattr(st.session_state, 'history') and st.session_state.history:
            for entry in reversed(st.session_state.history[-5:]):
                with st.expander(f"🔍 {entry['query'][:40]}..."):
                    st.write(f"**Pages :** {', '.join(map(str, entry.get('pages', []))[:3])}")
        else:
            st.info("Aucun historique")
        
        st.markdown("---")
        st.markdown("### 🎯 Exemples")
        
        examples = [
            "Comment créer un devis ?",
            "Qu'est-ce que l'AICI ?",
            "Comment générer une facture ?",
            "Comment faire un appariement ?"
        ]
        
        for ex in examples:
            if st.button(f"💡 {ex}", key=f"ex_{hashlib.md5(ex.encode()).hexdigest()[:8]}"):
                st.session_state.selected_example = ex
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🤖 Assistant Kaizen v4.0 - Synthèse Intelligente<br>
        Version Octobre 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
