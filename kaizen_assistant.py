#!/usr/bin/env python3
"""
Assistant IA Kaizen - Documentation intelligente
Permet de poser des questions sur le manuel Kaizen et créer des tickets Freshdesk
"""

import streamlit as st
import os
from datetime import datetime
import json
import hashlib

# Configuration de la page
st.set_page_config(
    page_title="Assistant Kaizen",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin: 1rem 0;
    }
    .answer-box {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .reference-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    .ticket-box {
        background-color: #ffe6e6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF5252;
        margin: 1rem 0;
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
    """Assistant IA pour la documentation Kaizen"""
    
    def __init__(self):
        # Chemins adaptés pour Streamlit Cloud
        # Chercher d'abord dans le répertoire courant, puis dans uploads
        if os.path.exists("Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "Kaizen_-_Manuel_ope_ratoire.pdf"
        elif os.path.exists("/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"):
            self.pdf_path = "/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf"
        else:
            self.pdf_path = None
            
        if os.path.exists("Documentation_Utilisateur_KAIZEN.pdf"):
            self.user_doc_path = "Documentation_Utilisateur_KAIZEN.pdf"
        elif os.path.exists("/mnt/user-data/uploads/Documentation_Utilisateur_KAIZEN.pdf"):
            self.user_doc_path = "/mnt/user-data/uploads/Documentation_Utilisateur_KAIZEN.pdf"
        else:
            self.user_doc_path = None
        
        # Utiliser un chemin temporaire accessible sur Streamlit Cloud
        self.history_file = "chat_history.json"
        self.load_history()
        
    def load_history(self):
        """Charge l'historique des conversations"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                st.session_state.history = json.load(f)
        else:
            st.session_state.history = []
    
    def save_history(self):
        """Sauvegarde l'historique des conversations"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            # Si l'écriture échoue, on continue sans sauvegarder
            st.warning(f"Impossible de sauvegarder l'historique : {str(e)}")
            pass
    
    def search_in_pdf(self, query):
        """Recherche dans le PDF en utilisant pdftotext"""
        import subprocess
        
        # Vérifier que le PDF existe
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            st.error("❌ Le fichier PDF du manuel Kaizen n'a pas été trouvé.")
            st.info("💡 Assurez-vous que 'Kaizen_-_Manuel_ope_ratoire.pdf' est dans le même dossier que l'application.")
            return []
        
        try:
            # Extraire le texte complet
            result = subprocess.run(
                ['pdftotext', self.pdf_path, '-'],
                capture_output=True,
                text=True,
                check=True
            )
            full_text = result.stdout
            
            # Recherche simple par mots-clés
            query_lower = query.lower()
            query_words = query_lower.split()
            
            # Découper le texte en sections
            lines = full_text.split('\n')
            relevant_sections = []
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                # Si la ligne contient des mots de la requête
                matches = sum(1 for word in query_words if word in line_lower)
                if matches > 0:
                    # Capturer le contexte (5 lignes avant et après)
                    start = max(0, i - 5)
                    end = min(len(lines), i + 6)
                    context = '\n'.join(lines[start:end])
                    relevant_sections.append({
                        'text': context,
                        'score': matches,
                        'line': i
                    })
            
            # Trier par pertinence
            relevant_sections.sort(key=lambda x: x['score'], reverse=True)
            
            return relevant_sections[:5]  # Top 5 résultats
            
        except Exception as e:
            st.error(f"Erreur lors de la recherche : {str(e)}")
            return []
    
    def generate_answer(self, query, context_sections):
        """Génère une réponse basée sur les sections trouvées"""
        if not context_sections:
            return None, "Aucune information trouvée dans le manuel."
        
        # Construire le contexte
        context = "\n\n---\n\n".join([s['text'] for s in context_sections])
        
        # Réponse basée sur le contexte
        answer = f"""D'après le manuel Kaizen, voici les informations pertinentes :

{context_sections[0]['text'][:500]}...

💡 **Conseil** : Pour plus de détails, consultez la section complète du manuel.
"""
        
        references = [f"Section trouvée (ligne ~{s['line']})" for s in context_sections[:3]]
        
        return answer, references
    
    def create_freshdesk_ticket_summary(self, query, search_results):
        """Crée un résumé pour un ticket Freshdesk"""
        summary = f"""📋 RÉSUMÉ DE LA RECHERCHE KAIZEN

🔍 Question posée :
{query}

📊 Résultats de recherche :
"""
        if search_results:
            summary += f"- {len(search_results)} sections pertinentes trouvées\n"
            summary += "- Extraits trouvés :\n"
            for i, result in enumerate(search_results[:3], 1):
                summary += f"\n{i}. {result['text'][:200]}...\n"
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
✅ Ticket créé automatiquement par l'Assistant Kaizen IA
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
    
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    
    # En-tête
    st.markdown('<h1 class="main-header">🤖 Assistant IA Kaizen</h1>', unsafe_allow_html=True)
    st.markdown("### 📚 Posez vos questions sur le manuel opératoire Kaizen (261 pages)")
    
    # Sidebar - Informations et statistiques
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1E88E5/ffffff?text=KAIZEN", use_container_width=True)
        st.markdown("---")
        
        st.markdown("### 📊 Statistiques")
        
        if hasattr(st.session_state, 'history'):
            total_questions = len(st.session_state.history)
            st.markdown(f'<div class="stats-card"><h3>{total_questions}</h3><p>Questions posées</p></div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ℹ️ À propos")
        st.info("""
        Cet assistant utilise l'IA pour vous aider à naviguer dans le manuel Kaizen.
        
        **Fonctionnalités :**
        - 🔍 Recherche intelligente
        - 💡 Réponses contextuelles
        - 🎫 Création de tickets Freshdesk
        - 📝 Historique des recherches
        """)
        
        st.markdown("---")
        st.markdown("### 🛠️ Actions")
        
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.history = []
            st.session_state.assistant.save_history()
            st.success("Historique effacé !")
            st.rerun()
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Posez votre question")
        
        # Zone de saisie de la question
        query = st.text_area(
            "Que voulez-vous savoir sur Kaizen ?",
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
            with st.spinner("🔎 Recherche en cours dans le manuel Kaizen..."):
                # Recherche dans le PDF
                search_results = st.session_state.assistant.search_in_pdf(query)
                st.session_state.search_results = search_results
                
                # Génération de la réponse
                answer, references = st.session_state.assistant.generate_answer(query, search_results)
                
                # Sauvegarder dans l'historique
                history_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'query': query,
                    'answer': answer,
                    'references': references,
                    'results_found': len(search_results)
                }
                st.session_state.history.append(history_entry)
                st.session_state.assistant.save_history()
                
                st.session_state.current_query = query
                st.session_state.current_answer = answer
                st.session_state.current_references = references
        
        # Affichage de la réponse
        if st.session_state.current_answer:
            st.markdown("---")
            st.markdown("### ✅ Réponse")
            
            st.markdown(f'<div class="answer-box">{st.session_state.current_answer}</div>', 
                       unsafe_allow_html=True)
            
            if st.session_state.current_references:
                st.markdown("**📍 Références dans le manuel :**")
                for ref in st.session_state.current_references:
                    st.markdown(f"- {ref}")
            
            # Feedback
            st.markdown("---")
            st.markdown("**Cette réponse vous a-t-elle été utile ?**")
            col_fb1, col_fb2, col_fb3 = st.columns(3)
            with col_fb1:
                if st.button("👍 Oui, parfait"):
                    st.success("Merci pour votre retour !")
            with col_fb2:
                if st.button("👌 Partiellement"):
                    st.info("Essayez de reformuler votre question ou créez un ticket.")
            with col_fb3:
                if st.button("👎 Non"):
                    st.warning("Créez un ticket Freshdesk pour obtenir une aide personnalisée.")
        
        # Création de ticket Freshdesk
        if ticket_clicked and query:
            st.markdown("---")
            st.markdown("### 🎫 Créer un ticket Freshdesk")
            
            ticket_summary = st.session_state.assistant.create_freshdesk_ticket_summary(
                query,
                st.session_state.search_results
            )
            
            st.markdown('<div class="ticket-box">', unsafe_allow_html=True)
            st.markdown("**Résumé du ticket à créer :**")
            st.code(ticket_summary, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.info("""
            📋 **Prochaines étapes :**
            1. Copiez le résumé ci-dessus
            2. Rendez-vous sur votre portail Freshdesk
            3. Créez un nouveau ticket
            4. Collez le résumé dans la description
            5. Complétez les informations manquantes
            
            ℹ️ L'intégration automatique avec Freshdesk nécessite une configuration API.
            """)
            
            if st.button("📋 Copier le résumé", use_container_width=True):
                st.success("✅ Résumé copié dans le presse-papier ! (fonctionnalité à implémenter)")
    
    with col2:
        st.markdown("### 📜 Historique des recherches")
        
        if hasattr(st.session_state, 'history') and st.session_state.history:
            # Afficher les 5 dernières recherches
            for entry in reversed(st.session_state.history[-5:]):
                with st.expander(f"🔍 {entry['query'][:50]}...", expanded=False):
                    st.markdown(f"**Date :** {entry['timestamp'][:19]}")
                    st.markdown(f"**Résultats :** {entry['results_found']} sections trouvées")
                    if st.button(f"Revoir cette recherche", key=f"reload_{entry['timestamp']}"):
                        st.session_state.current_query = entry['query']
                        st.session_state.current_answer = entry['answer']
                        st.session_state.current_references = entry['references']
                        st.rerun()
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
                st.session_state.query_input = example
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>🤖 Assistant IA Kaizen - Développé pour Kangourou Kids</p>
        <p>📚 Basé sur le Manuel Opératoire Kaizen (261 pages)</p>
        <p style='font-size: 0.8rem;'>Version 1.0 - Octobre 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
