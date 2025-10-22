#!/usr/bin/env python3
"""
Script de configuration de l'Assistant Kaizen
Configure l'accès aux APIs et vérifie l'installation
"""

import os
import sys
from pathlib import Path

def print_header():
    """Affiche l'en-tête du script"""
    print("=" * 60)
    print("🤖 ASSISTANT KAIZEN - CONFIGURATION")
    print("=" * 60)
    print()

def check_python_version():
    """Vérifie la version de Python"""
    print("🔍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} détecté")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} détecté")
        print("⚠️  Python 3.8 ou supérieur requis")
        return False

def check_dependencies():
    """Vérifie les dépendances Python"""
    print("\n🔍 Vérification des dépendances...")
    
    dependencies = {
        'streamlit': 'Streamlit (interface web)',
        'requests': 'Requests (API HTTP)',
    }
    
    missing = []
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description}")
            missing.append(package)
    
    return missing

def check_pdf_files():
    """Vérifie la présence des fichiers PDF"""
    print("\n🔍 Vérification des fichiers PDF...")
    
    files = {
        '/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf': 'Manuel opératoire Kaizen',
        '/mnt/user-data/uploads/Documentation_Utilisateur_KAIZEN.pdf': 'Documentation utilisateur'
    }
    
    all_found = True
    for filepath, description in files.items():
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✅ {description} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {description} - NON TROUVÉ")
            all_found = False
    
    return all_found

def configure_freshdesk():
    """Configure l'intégration Freshdesk"""
    print("\n" + "=" * 60)
    print("📋 CONFIGURATION FRESHDESK (OPTIONNEL)")
    print("=" * 60)
    print()
    print("L'intégration Freshdesk permet la création automatique de tickets.")
    print("Si vous ne souhaitez pas l'activer maintenant, appuyez sur Entrée.")
    print()
    
    configure = input("Voulez-vous configurer Freshdesk maintenant ? (o/N) : ").lower()
    
    if configure == 'o':
        print("\n🔧 Configuration de Freshdesk...")
        
        domain = input("Domaine Freshdesk (ex: kangourou.freshdesk.com) : ").strip()
        api_key = input("Clé API Freshdesk : ").strip()
        
        if domain and api_key:
            env_content = f"""# Configuration Freshdesk
FRESHDESK_DOMAIN={domain}
FRESHDESK_API_KEY={api_key}
"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("\n✅ Configuration Freshdesk sauvegardée dans .env")
            
            # Test de connexion
            try:
                from freshdesk_integration import test_connection
                result = test_connection(domain, api_key)
                if result['success']:
                    print(f"✅ {result['message']}")
                else:
                    print(f"⚠️  {result['message']}")
                    print("Vérifiez vos identifiants Freshdesk")
            except Exception as e:
                print(f"⚠️  Impossible de tester la connexion : {e}")
        else:
            print("⚠️  Configuration annulée")
    else:
        print("⏭️  Configuration Freshdesk ignorée")

def install_dependencies(packages):
    """Installe les dépendances manquantes"""
    if not packages:
        return True
    
    print(f"\n📦 Installation de {len(packages)} package(s) manquant(s)...")
    
    for package in packages:
        print(f"\n📥 Installation de {package}...")
        exit_code = os.system(f"pip install {package} -q")
        
        if exit_code == 0:
            print(f"✅ {package} installé avec succès")
        else:
            print(f"❌ Erreur lors de l'installation de {package}")
            return False
    
    return True

def create_launch_script():
    """Crée un script de lancement rapide"""
    print("\n🚀 Création du script de lancement...")
    
    script_content = """#!/bin/bash
# Script de lancement de l'Assistant Kaizen

echo "🚀 Lancement de l'Assistant Kaizen..."
echo ""

# Vérifier si Streamlit est installé
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit n'est pas installé"
    echo "Installation en cours..."
    pip install streamlit
fi

# Lancer l'application
streamlit run kaizen_assistant.py

# Si l'application se ferme avec une erreur
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ L'application s'est fermée avec une erreur"
    echo "Consultez les logs ci-dessus pour plus de détails"
    read -p "Appuyez sur Entrée pour fermer..."
fi
"""
    
    with open('launch_kaizen.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('launch_kaizen.sh', 0o755)
    print("✅ Script de lancement créé : launch_kaizen.sh")

def main():
    """Fonction principale"""
    print_header()
    
    # Vérifications
    python_ok = check_python_version()
    if not python_ok:
        print("\n❌ Configuration interrompue - Mettez à jour Python")
        return
    
    missing_deps = check_dependencies()
    pdf_ok = check_pdf_files()
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 60)
    
    if not missing_deps and pdf_ok:
        print("✅ Tous les prérequis sont satisfaits !")
    else:
        if missing_deps:
            print(f"⚠️  {len(missing_deps)} dépendance(s) manquante(s)")
        if not pdf_ok:
            print("⚠️  Fichiers PDF manquants")
    
    # Installation des dépendances manquantes
    if missing_deps:
        install = input("\n📦 Installer les dépendances manquantes ? (O/n) : ").lower()
        if install != 'n':
            if install_dependencies(missing_deps):
                print("\n✅ Toutes les dépendances sont installées !")
            else:
                print("\n❌ Erreur lors de l'installation")
                return
    
    # Configuration Freshdesk
    configure_freshdesk()
    
    # Création du script de lancement
    create_launch_script()
    
    # Instructions finales
    print("\n" + "=" * 60)
    print("✅ CONFIGURATION TERMINÉE")
    print("=" * 60)
    print()
    print("🚀 Pour lancer l'Assistant Kaizen :")
    print()
    print("   Option 1 (recommandé) :")
    print("   ./launch_kaizen.sh")
    print()
    print("   Option 2 :")
    print("   streamlit run kaizen_assistant.py")
    print()
    print("📚 L'application sera accessible à : http://localhost:8501")
    print()
    print("📖 Consultez README.md pour plus d'informations")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
