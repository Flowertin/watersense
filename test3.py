import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from datetime import datetime
from streamlit_chat import message
import base64
# Vider le cache des fonctions avec @st.cache_data
st.cache_data.clear()

# Vider le cache des fonctions avec @st.cache_resource
st.cache_resource.clear()
# ---- Personnalisation CSS ----
def get_base64_image(image_path):
    """Convert image to base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

background_image_base64 = get_base64_image("aaa.jpg")
header_image_base64 = get_base64_image("WaterSense.png")

# ---- Page Configuration ----
st.set_page_config(layout="centered")  # Default layout (centered)

# ---- Compteur de visiteurs ----
if "visitors" not in st.session_state:
    st.session_state.visitors = 1
else:
    st.session_state.visitors += 1

# ---- Horloge ----
def show_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    st.sidebar.markdown(f"**Heure actuelle** : {current_time}")

st.sidebar.markdown(f"**Visiteurs**: {st.session_state.visitors}")
show_time()

# ---- Navigation menu ----
menu = ["Accueil", "Analyse de l'Eau", "Qualité de l'Eau", "Gestion de l'Eau", "Technologies et Innovations",
        "Impact Environnemental", "Éducation et Sensibilisation", "Quiz", "Dropbot", "À propos de nous"]
choice = st.sidebar.radio("**Navigation**", menu)

# Save the current page choice to session_state
st.session_state.page = choice

# ---- Conditional Wide Mode CSS ----
if choice in ["Accueil", "À propos de nous"]:
    st.markdown("""
        <style>
        .block-container {
            max-width: 100% !important;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .block-container {
            max-width: 800px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# ---- Custom App CSS ----
st.markdown(
    f"""
    <style>
        [data-testid="stAppViewContainer"] {{
            background-color: white !important;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(to bottom, #001D2F, #015A86, #09759C) !important;
        }}
        h1, h2, h3 {{
            color: #015A86 !important;
        }}
        body, p, span {{
            color: black !important;
            font-size: 20px !important;
        }}
        div[role="radiogroup"] > label {{
            color: black !important;
        }}
        .stButton>button {{
            background-color: #015A86 !important;
            color: white !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 8px !important;
        }}
        .stButton>button:hover {{
            background-color: #77BDD9 !important;
        }}
        .header-section {{
            background-image: url('data:image/png;base64,{background_image_base64}');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: white;
            padding: 60px 5% 60px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}
        .header-text {{
            max-width: 50%;
        }}
        .header-text h1 {{
            font-size: 3em;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .header-text p {{
            font-size: 1.2em;
            line-height: 1.6em;
            text-align: justify;
        }}
        .header-image {{
            max-width: 40%;
            text-align: center;
        }}
        .header-image img {{
            width: 100%;
            border-radius: 12px;
            content: url('data:image/png;base64,{header_image_base64}');
        }}

        /* ---- Responsive Design for Mobile ---- */
        @media (max-width: 768px) {{
            .header-section {{
                flex-direction: column !important;
                text-align: center;
            }}
            .header-text, .header-image {{
                max-width: 100% !important;
            }}
            .header-text p {{
                text-align: justify;
            }}
            .header-image img {{
                width: 100% !important;
                margin-top: 20px;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        .css-1v0mbdj span {
            color: white !important;
        }
        .sidebar-text h4 {
            font-size: 16px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)



# ---- Page Content ----
if choice == "Accueil":
    st.markdown("""<style>.block-container {padding-top: 0rem;}</style>""", unsafe_allow_html=True)

    st.markdown("""
        <style>
            .cta-btn {
                color: #001D2F;
                background-color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            .cta-btn:hover {
                background-color: #001D2F;
                color: #fff;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <style>
            .header-text {{
                color: white !important;
            }}
            .header-text h1 {{
                color: white !important;
            }}
            .header-text p {{
                color: white !important;
            }}
        </style>

        <div class="header-section">
            <div class="header-text">
                <h1>WaterSense</h1>
                <p> 
                    L’eau est au cœur de la vie. Mais aujourd’hui, cette ressource vitale est menacée par la pollution, le changement
                    climatique, la surexploitation et l’inégalité d’accès. Ces défis exigent une prise de conscience collective et une meilleure
                    compréhension de l’importance de l’eau dans notre quotidien.<br><br>
                    Bienvenue sur WaterSense, une plateforme éducative et interactive qui t’aide à explorer, apprendre et agir pour une gestion
                    plus durable de l’eau. Grâce à des outils intelligents comme DropBot, des quiz, des analyses et des contenus pédagogiques, découvre
                    le monde de l’eau autrement et deviens acteur du changement.
                </p>
            </div>
            <div class="header-image">
                <img src="data:image/png;base64,{header_image_base64}" alt="Water ripple"/>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif choice == "À propos de nous":
    col1, col2 = st.columns([2, 1])  

    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="flex: 1; padding-right: 20px; text-align: justify;">
                <h1>À propos de nous</h1>
                <p>
                    Nous sommes l’équipe <strong>FikrCode</strong> du lycée Ibn Batouta à Larache, un groupe composé de quatre élèves passionnés par les technologies et l’environnement : Amine El Hafidi, Yasmina Belhaj, Siham Idhssain, et Ismail El Karkri. Nous sommes encadrés et supervisés par notre enseignante et mentor, Fatin M'hair, qui nous guide dans ce projet ambitieux.
                </p>
                <p>
                    Notre équipe a été formée autour d’un objectif commun : sensibiliser la communauté à la protection de l’eau, une ressource essentielle et de plus en plus menacée. L’eau, bien qu’elle soit au cœur de la vie, fait face à de nombreux défis tels que la pollution, la surexploitation, le changement climatique et l'inégalité d'accès. Nous souhaitons que chacun comprenne l'importance de préserver cette ressource, non seulement pour nous-mêmes, mais aussi pour les générations futures.
                </p>
                <p>
                    Le projet que nous avons développé est unique en son genre. Nous avons créé un chatbot éducatif simple à utiliser qui répond aux questions du public sur l’eau, en expliquant ses composants, ses propriétés et les menaces qui pèsent sur elle. Ce chatbot est alimenté par des méthodes d’intelligence artificielle simples et accessibles, permettant à tout utilisateur de trouver des informations précises en quelques clics. Ce projet vise à rendre la connaissance de l’eau plus accessible et à encourager l’action collective en faveur de sa gestion durable.
                </p>
                <p>
                    Notre plateforme est entièrement dédiée au grand public. Elle offre un ensemble d'outils interactifs tels que des quiz, des analyses, et des contenus éducatifs. En combinant des informations scientifiques et des solutions concrètes, nous souhaitons inspirer les citoyens, les jeunes en particulier, à adopter des pratiques plus durables pour préserver l’eau et l’environnement en général.
                </p>
                <p>
                    Nous croyons en un monde plus durable, où chaque individu prend conscience de l’importance de l’eau, des risques qui la menacent, et agit pour sa préservation. C’est pourquoi nous nous engageons pleinement dans ce projet, non seulement pour informer, mais aussi pour susciter un réel changement dans la manière dont nous percevons et utilisons l’eau au quotidien. Ensemble, nous pouvons faire la différence et contribuer à la création d’un avenir où l’eau reste une ressource accessible et protégée.
                </p>
                <p>
                    <strong>L’équipe FikrCode</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("eee.png", use_container_width=True)


# ---- Analyse de l'eau ----
elif choice == "Analyse de l'Eau":
    def simulateur_qualite_eau():
        st.title("💧 Simulateur de la qualité de l'eau")

        ph = st.slider("📏 Valeur du pH", 0.0, 14.0, 7.0, key="ph_slider")
        turbidite = st.slider("🌫️ Turbidité (en NTU)", 0.0, 10.0, 1.0, key="turbidite_slider")
        nitrates = st.slider("🧪 Nitrates (mg/L)", 0.0, 100.0, 20.0, key="nitrates_slider")
        bacteries = st.radio("🦠 Y a-t-il des bactéries détectées ?", ["Non", "Oui"], key="bacteries_radio")

        messages = []
        score = 100

        if not (6.5 <= ph <= 8.5):
            messages.append("❌ pH hors de la plage acceptable (6.5 - 8.5).")
            score -= 25
        else:
            messages.append("✅ pH dans la norme.")

        if turbidite > 5:
            messages.append("❌ Turbidité trop élevée (> 5 NTU).")
            score -= 25
        else:
            messages.append("✅ Turbidité acceptable.")

        if nitrates > 50:
            messages.append("❌ Nitrates élevés (> 50 mg/L).")
            score -= 25
        else:
            messages.append("✅ Nitrates dans la norme.")

        if bacteries == "Oui":
            messages.append("❌ Présence de bactéries détectée.")
            score -= 25
        else:
            messages.append("✅ Aucune bactérie détectée.")

        st.subheader("🔎 Résultat de l'analyse :")
        for m in messages:
            st.write(m)

        if score >= 75:
            st.success("💧 Qualité de l'eau : BONNE")
        elif 50 <= score < 75:
            st.warning("⚠️ Qualité de l'eau : MOYENNE")
        else:
            st.error("🚫 Qualité de l'eau : MAUVAISE")

        fig, ax = plt.subplots()
        ax.scatter(ph, turbidite, color='blue', s=150)
        ax.axvline(6.5, color='green', linestyle='--')
        ax.axvline(8.5, color='green', linestyle='--')
        ax.axhline(5, color='orange', linestyle='--')

        ax.set_title("pH vs Turbidité")
        ax.set_xlabel("pH")
        ax.set_ylabel("Turbidité (NTU)")
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        ax.grid(True)

        st.pyplot(fig)

    simulateur_qualite_eau()
elif choice=="Qualité de l'Eau":
    st.markdown("<h1>Qualité de l'Eau</h1>", unsafe_allow_html=True)
    st.markdown("""
        L'eau peut être contaminée par divers types de polluants, ayant des effets néfastes sur la santé humaine et l’environnement. Voici les principales catégories de polluants :
    """)
    st.markdown("<h2>Détection de Polluants</h2>", unsafe_allow_html=True)
    st.markdown('''
        **Métaux lourds** (plomb, mercure, arsenic) : Provoquent des maladies neurologiques et rénales.


        **Pesticides et herbicides** : Toxiques pour la faune aquatique et liés à des troubles hormonaux chez l'homme.


        **Produits pharmaceutiques** : Affectent les organismes aquatiques et peuvent entraîner une résistance aux antibiotiques.
    
    ''')
    st.markdown("<h3>1. Polluants biologiques</h3>", unsafe_allow_html=True)
    st.markdown('''
        **Bactéries et virus** (E. coli, choléra, hépatite A) : Responsables de maladies gastro-intestinales graves.


        **Parasites** (Giardia, Cryptosporidium) : Peuvent causer des infections intestinales sévères.

    ''')
    st.markdown("<h3>2. Polluants physiques</h3>", unsafe_allow_html=True)
    st.markdown('''
        **Microplastiques** : Absorbent des toxines et peuvent s’accumuler dans la chaîne alimentaire.


        **Sédiments en excès** : Réduisent la clarté de l'eau et perturbent l'écosystème aquatique.

    ''')
    st.markdown("<h3>3. Impact sur la santé et l’environnement</h3>", unsafe_allow_html=True)
    st.markdown('''
        **Problèmes de santé** : Empoisonnement, maladies chroniques, troubles hormonaux.


        **Dégradation de l’écosystème** : Perte de biodiversité, contamination des ressources naturelles.


        **Déséquilibres écologiques** : Prolifération d'algues nuisibles, acidification de l’eau.
        
    ''')
    st.markdown("<h3>4. Solutions et prévention</h3>", unsafe_allow_html=True)
    st.markdown('''
        -Surveillance et analyse régulière de la qualité de l’eau.


        -Technologies de filtration et de purification avancées.


        -Sensibilisation et réglementation stricte pour limiter les rejets polluants.
        
        L’identification et la réduction des polluants sont essentielles pour préserver la santé publique et protéger nos ressources en eau. 💧🌍

    ''')
    video_url = "https://youtu.be/jkyZIpfrQnM?si=VqVo0zFCbevpG2ml"
    st.video(video_url)
    st.markdown("<h2>Techniques de Purification de l’Eau</h2>", unsafe_allow_html=True)

    st.markdown("""
    La purification de l’eau est essentielle pour éliminer les contaminants et garantir une eau propre et saine. Voici les principales méthodes utilisées, avec leurs avantages et limites.
    """)

    st.markdown("<h3>1. Filtration Physique</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✔️ **Filtres à sable et à charbon actif** : Retiennent les impuretés solides, les bactéries et les produits chimiques (chlore, pesticides).  
        ➖ Peu efficace contre les virus et certains métaux lourds.

        ✔️ **Filtration par membranes** (ultrafiltration, nanofiltration) : Bloque les particules et les micro-organismes grâce à des pores extrêmement fins.  
        ➖ Peut nécessiter une pression élevée et un entretien régulier.
    """)

    st.markdown("<h3>2. Traitement Chimique</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✔️ **Chloration** : Désinfecte l’eau en éliminant bactéries et virus.  
        ➖ Peut produire des sous-produits nocifs et altérer le goût de l’eau.

        ✔️ **Ozonation** : Oxyde les contaminants organiques et tue les micro-organismes.  
        ➖ Méthode coûteuse et l’ozone ne laisse pas de résidu protecteur.

        ✔️ **Traitement aux UV** : Utilise la lumière ultraviolette pour détruire l’ADN des bactéries et virus.  
        ➖ Inefficace contre les polluants chimiques et nécessite une eau claire.
    """)

    st.markdown("<h3>3. Distillation</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✔️ **Ébullition et condensation** de l’eau pour éliminer microbes, sels et métaux lourds.  
        ➖ Processus lent et énergivore.
    """)

    st.markdown("<h3>4. Osmose Inverse</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✔️ **Technique très efficace** qui utilise une membrane semi-perméable pour éliminer 99 % des contaminants (bactéries, virus, nitrates, métaux lourds).  
        ➖ Nécessite une pression élevée, gaspille une partie de l’eau traitée.
    """)

    st.markdown("<h3>5. Quelle méthode choisir ?</h3>", unsafe_allow_html=True)
    st.markdown("""
        💧 **Eau légèrement contaminée** : Filtration au charbon actif ou traitement UV.
        
        💧 **Eau polluée par des métaux lourds** : Osmose inverse ou distillation.
        
        💧 **Eau de surface avec bactéries et virus** : Ozonation, chloration ou UV.

        L’association de plusieurs techniques permet souvent d’optimiser la purification pour garantir une eau potable de qualité. 💧✨
    """)
    video_url2 = "https://youtu.be/2bTj-vo1tyU?si=-D_Ak60nqCSoWZhR"
    st.video(video_url2)
        
# ---- Gestion de l'Eau ----
elif choice == "Gestion de l'Eau":

    st.markdown("<h1>Gestion de l'Eau</h1>", unsafe_allow_html=True)

    st.markdown("<h2>Conservation de l’Eau : Astuces et Bonnes Pratiques 💧🌍</h2>", unsafe_allow_html=True)
    st.markdown("""
        La préservation de l’eau est essentielle pour lutter contre la pénurie et réduire notre empreinte écologique. Voici quelques conseils pratiques pour économiser l’eau à domicile et dans les industries.
    """)
    st.markdown("""
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background-color: white;
    }
    th, td {
        border: 1px solid #cccccc;
        padding: 10px;
        text-align: left;
        vertical-align: top;
        font-size: 16px;
    }
    th {
        background-color: #e6f2ff;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table>
      <tr>
        <th>🏡 À la Maison</th>
        <th>🏭 Dans les Industries</th>
      </tr>
      <tr>
        <td>
          <b>Réduction de la Consommation :</b><br>
          ✔️ Fermer le robinet pendant le brossage des dents.<br>
          ✔️ Douches courtes au lieu de bains.<br>
          ✔️ Utiliser des économiseurs d’eau.
        </td>
        <td>
          <b>Amélioration des Procédés :</b><br>
          ✔️ Optimiser l’utilisation de l’eau.<br>
          ✔️ Adopter des technologies propres.
        </td>
      </tr>
      <tr>
        <td>
          <b>Réutilisation et Recyclage :</b><br>
          ✔️ Récupérer l’eau de pluie.<br>
          ✔️ Réutiliser l’eau de cuisson.<br>
          ✔️ Recycler les eaux grises.
        </td>
        <td>
          <b>Réutilisation & Traitement :</b><br>
          ✔️ Recycler les eaux industrielles.<br>
          ✔️ Systèmes de filtration & recyclage.
        </td>
      </tr>
      <tr>
        <td>
          <b>Optimisation des Équipements :</b><br>
          ✔️ Choisir des appareils économes.<br>
          ✔️ Réparer les fuites rapidement.
        </td>
        <td>
          <b>Sensibilisation :</b><br>
          ✔️ Former le personnel.<br>
          ✔️ Suivre la consommation avec capteurs.
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)


    st.markdown("<h4>Bénéfices de la Conservation de l’Eau</h4>", unsafe_allow_html=True)
    st.markdown("""
    ✅ Réduction des factures d’eau.  
    ✅ Protection des ressources naturelles.  
    ✅ Diminution de l’empreinte écologique.
    """)

    st.markdown("""
    Chacun peut contribuer à la préservation de l’eau en adoptant des gestes simples mais efficaces ! 💙💦
    """)

    video_url3 = "https://youtu.be/HcMg3ghRfxY?si=kX040aCgkD8BJFgP"
    st.video(video_url3)
    
    st.markdown("<h2>Gestion Durable des Ressources en Eau 💧🌍</h2>", unsafe_allow_html=True)
    st.markdown("""
    La gestion efficace de l’eau est essentielle pour préserver cette ressource précieuse face aux défis climatiques et
    à la croissance démographique. Voici des stratégies clés pour une utilisation durable de l’eau.

    """)
    st.markdown("""
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background-color: white;
    }
    th, td {
        border: 1px solid #cccccc;
        padding: 10px;
        text-align: left;
        vertical-align: top;
        font-size: 16px;
    }
    th {
        background-color: #e6f2ff;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table>
      <tr>
        <th>🔹 Collecte et Utilisation des Eaux de Pluie ☔</th>
        <th>🔹 Recyclage et Réutilisation des Eaux Usées 🔄</th>
        <th>🔹 Gestion Intelligente et Optimisation de l’Irrigation 🌾</th>
        <th>🔹 Prévention du Gaspillage et Sensibilisation 🏡🏭</th>
      </tr>
      <tr>
        <td>
          <b>Actions :</b><br>
          ✔ Installation de citernes et réservoirs pour récupérer l’eau de pluie.<br>
          ✔ Filtration et traitement pour un usage domestique (arrosage, lavage, chasse d’eau).<br>
          ✔ Intégration dans les bâtiments écologiques pour réduire la consommation d’eau potable.
        </td>
        <td>
          <b>Actions :</b><br>
          ✔ Traitement des eaux grises (eaux de douche, lave-linge) pour l’arrosage ou les toilettes.<br>
          ✔ Réutilisation des eaux industrielles après filtration et purification.<br>
          ✔ Systèmes de filtration avancés (membranes, UV, traitements biologiques).
        </td>
        <td>
          <b>Actions :</b><br>
          ✔ Utilisation de l’irrigation goutte-à-goutte pour minimiser les pertes d’eau.<br>
          ✔ Capteurs d’humidité et systèmes automatisés pour ajuster l’arrosage aux besoins réels.<br>
          ✔ Rotation des cultures et techniques agricoles durables pour préserver les nappes phréatiques.
        </td>
        <td>
          <b>Actions :</b><br>
          ✔ Campagnes de sensibilisation pour encourager une consommation responsable.<br>
          ✔ Réglementations et incitations pour les entreprises adoptant des pratiques durables.<br>
          ✔ Surveillance des réseaux d’eau pour détecter et réparer rapidement les fuites.
        </td>
      </tr>
      <tr>
        <td>
          <b>✔ Avantages :</b><br>
          ✔ Diminue la demande en eau potable et réduit les risques d’inondation urbaine.
        </td>
        <td>
          <b>✔ Avantages :</b><br>
          ✔ Réduit le gaspillage et préserve les ressources en eau douce.
        </td>
        <td>
          <b>✔ Avantages :</b><br>
          ✔ Économie d’eau et augmentation de la productivité agricole.
        </td>
        <td>
          <b>✔ Avantages :</b><br>
          ✔ Réduction des pertes d’eau et meilleure gestion des ressources disponibles.
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)


    st.markdown("<h2>🌱Vers un Avenir Durable</h2>", unsafe_allow_html=True)
    st.markdown("""
    En combinant ces stratégies, nous pouvons assurer une gestion efficace de l’eau, protéger l’environnement et garantir un accès équitable à cette ressource essentielle pour les générations futures. 💙💦

    """)

    video_url4 = "https://youtu.be/a56olKIMiiU?si=mTPxUz2Pt8c2sYqN"
    st.video(video_url4)
    st.markdown("<h2>Politiques et Régulations sur l’Eau 🌍💧</h2>", unsafe_allow_html=True)
    st.markdown("""
        La gestion et la protection des ressources en eau sont encadrées par des régulations locales et internationales visant à garantir un accès équitable à l’eau potable, préserver l’environnement et promouvoir un usage durable.
    """)    
    st.markdown("<h3>1. Régulations Internationales</h3>", unsafe_allow_html=True)
    st.markdown("<h4>Les Objectifs de Développement Durable (ODD) de l’ONU</h4>", unsafe_allow_html=True)
    st.markdown("""
        L’**objectif n°6** vise un accès universel à l’eau potable et à l’assainissement d’ici 2030.

        Encourage la gestion durable des ressources en eau et la réduction des pollutions.
    """)
    st.markdown("<h4>La Convention de l’ONU sur l’Eau (1992)</h4>", unsafe_allow_html=True)
    st.markdown("""
        Promeut la coopération entre pays partageant des ressources en eau transfrontalières.

        Encourage la prévention des conflits liés à l’eau.
    """)
    st.markdown("<h4>La Directive-Cadre sur l’Eau (DCE) de l’Union Européenne (2000)</h4>", unsafe_allow_html=True)
    st.markdown("""
        Vise la protection et la restauration des écosystèmes aquatiques.

        Implique un suivi régulier de la qualité de l’eau et des restrictions sur les polluants.
    """)
    st.markdown("<h4> Accords et Traités Internationaux</h4>", unsafe_allow_html=True)
    st.markdown("""
        **Protocole sur l’eau et la santé (OMS/ONU, 1999)** : Garantit l’accès à l’eau potable et à l’assainissement.

        **Convention de Ramsar (1971)** : Protège les zones humides d’importance internationale.

    """)
    st.markdown("<h3>2. Régulations Locales</h3>", unsafe_allow_html=True)
    st.markdown("""
        Chaque pays adopte ses propres lois et règlements pour gérer l’eau. Voici quelques exemples : Loi sur l’eau et l’assainissement : Régit la distribution et la qualité de l’eau potable.


        **Normes de qualité de l’eau potable** : Fixent les seuils de contaminants autorisés.


        **Régulations sur le traitement des eaux usées** : Imposent aux industries et municipalités de traiter leurs rejets.


        **Politiques de tarification de l’eau** : Encouragent une consommation responsable par des tarifs progressifs.


        Les gouvernements locaux peuvent aussi imposer des restrictions d’usage en cas de sécheresse ou promouvoir des incitations financières pour l’installation de systèmes d’économie d’eau.

    """)
    st.markdown("<h3>3. Impact des Régulations sur la Gestion de l’Eau</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✅ Protection de la santé publique en garantissant une eau potable conforme aux normes.
        
        ✅ Préservation des ressources naturelles en limitant la pollution et la surexploitation.
        
        ✅ Encouragement des innovations en matière de traitement et de recyclage des eaux.
        
        ✅ Coopération internationale pour résoudre les conflits liés à l’eau.

    """)
    st.markdown("<h2>🌍 Un Engagement Mondial pour une Eau Saine et Durable</h2>", unsafe_allow_html=True)
    st.markdown("""
        Les politiques et régulations jouent un rôle clé dans la gestion de l’eau. Il est essentiel de renforcer leur application et d’encourager les initiatives locales pour assurer un accès équitable et durable à cette ressource vitale. 💙💦
    """)
    video_url4 = "https://youtu.be/PteEKDGEFfI?si=gykDmGRjkVBdeATs"
    st.video(video_url4)

    
# ---- Technologies et Innovations ----
elif choice == "Technologies et Innovations":
    st.markdown("<h1>Technologies et Innovations</h1>", unsafe_allow_html=True)

    st.markdown("<h2>Technologies de Surveillance de l’Eau 💧🔬</h2>", unsafe_allow_html=True)
    st.markdown("""
        La surveillance de la qualité de l’eau est essentielle pour détecter les polluants, prévenir les risques sanitaires et optimiser la gestion des ressources hydriques. Grâce aux avancées technologiques, de nouveaux outils permettent un suivi en temps réel et une analyse plus précise.
    """)
    st.markdown("<h3>1. Capteurs Intelligents pour la Qualité de l’Eau</h3>", unsafe_allow_html=True)
    st.markdown("""
        Les capteurs modernes permettent de mesurer divers paramètres en temps réel, sans nécessiter d’analyse en laboratoire.

        ✔ **Capteurs électrochimiques** : Mesurent le pH, l’oxygène dissous, les nitrates et les métaux lourds.

        ✔ **Capteurs optiques (fluorescence, spectroscopie UV-Vis)** : Détectent les matières organiques, les hydrocarbures et les polluants chimiques.

        ✔ **Capteurs microbiologiques** : Identifient la présence de bactéries et virus grâce à des biocapteurs spécifiques.

        📌 **Exemple d’innovation** : Des capteurs autonomes à base de graphène, capables de détecter des contaminants à très faible concentration.
    """)
    st.markdown("<h3>2. Surveillance en Temps Réel avec l’IoT et l’IA</h3>", unsafe_allow_html=True)
    st.markdown("""
        L’**Internet des objets (IoT) et l’intelligence artificielle (IA)** révolutionnent la gestion de l’eau en permettant une surveillance continue et automatisée.
        
        ✔ **Stations de surveillance connectées** : Collectent et transmettent les données en temps réel.
        
        ✔ **Algorithmes d’IA** : Analysent les tendances pour détecter rapidement une pollution.
        
        ✔ **Applications mobiles** : Permettent aux gestionnaires d’eau de recevoir des alertes instantanées en cas de contamination.
        
        📌 **Exemple d’innovation** : Des drones équipés de capteurs capables de cartographier la pollution dans les rivières et les lacs.
    """)
    st.markdown("<h3>3. Technologie de Télé-détection et Satellites</h3>", unsafe_allow_html=True)
    st.markdown("""
        Les satellites et drones offrent une vue d’ensemble des ressources en eau et aident à la détection des anomalies.

        ✔ Télédétection par satellite : Suivi des algues toxiques, pollution et niveau des nappes phréatiques.

        ✔ Drones aquatiques : Équipés de capteurs, ils analysent la qualité de l’eau dans des zones difficiles d’accès.

        ✔ Modélisation hydrologique : Utilise l’imagerie satellite pour prédire les sécheresses et les inondations.

        📌 Exemple d’innovation : Le satellite Sentinel-2 de l’ESA permet de surveiller la pollution des eaux en détectant les variations de couleur et de turbidité.

    """)
    st.markdown("<h3>4. Avantages des Nouvelles Technologies</h3>", unsafe_allow_html=True)
    st.markdown("""
        ✔ Détection rapide et précoce des contaminants.
        
        ✔ Réduction des coûts d’analyse en laboratoire.
        
        ✔ Optimisation de la gestion de l’eau pour prévenir les crises.
        
        ✔ Meilleure accessibilité aux données pour les gouvernements et le public.

    """)
    st.markdown("<h2>🌍 Vers une Eau Plus Propre et Sécurisée</h2>", unsafe_allow_html=True)
    st.markdown("""
        Grâce aux avancées en capteurs intelligents, IoT et télédétection, la surveillance de l’eau devient plus efficace et accessible. Ces technologies permettent une gestion proactive des ressources en eau et contribuent à garantir une eau potable de qualité pour tous. 💙💦
    """)
    video_url5 = "https://youtu.be/gBszA9CyH-I?si=nu9kX4fGDvWW1061"
    st.video(video_url5)
    st.markdown("<h2>Robots pour la Surveillance de l’Eau 🤖💧</h2>", unsafe_allow_html=True)
    st.markdown("""
        Les robots jouent un rôle de plus en plus important dans la surveillance de la qualité de l’eau. Grâce à leurs capteurs avancés et à leur capacité d’exploration autonome, ils permettent un suivi précis des rivières, lacs et réservoirs, contribuant ainsi à la protection des ressources en eau.
    """)
    st.markdown("<h3>1. Types de Robots de Surveillance Aquatique</h3>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background-color: white;
    }
    th, td {
        border: 1px solid #cccccc;
        padding: 10px;
        text-align: left;
        vertical-align: top;
        font-size: 16px;
    }
    th {
        background-color: #e6f2ff;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <table>
      <tr>
        <th>🤖 Type de Robot</th>
        <th>🛠 Description et Utilisations</th>
      </tr>
      <tr>
        <td><b>🔹 Robots Sous-marins (AUV)</b><br>(Autonomous Underwater Vehicles)</td>
        <td>
          ✔️ Capables de plonger et d’analyser les eaux profondes.<br>
          ✔️ Mesurent la température, la salinité, l’oxygène dissous et les polluants chimiques.<br>
          ✔️ Utilisés pour surveiller la pollution industrielle et les marées noires.<br>
          📌 <b>Exemple :</b> Le robot <i>"AquaBOT"</i>, utilisé pour détecter les fuites toxiques et la prolifération d’algues.
        </td>
      </tr>
      <tr>
        <td><b>🔹 Robots de Surface (ASV)</b><br>(Autonomous Surface Vehicles)</td>
        <td>
          ✔️ Naviguent à la surface des rivières et des lacs.<br>
          ✔️ Équipés de capteurs pour analyser le pH, la turbidité, les nitrates et les hydrocarbures.<br>
          ✔️ Peuvent transmettre des données en temps réel via satellite ou Wi-Fi.<br>
          📌 <b>Exemple :</b> Le robot <i>"Envirobot"</i>, développé pour détecter la pollution de l’eau grâce à des capteurs biochimiques.
        </td>
      </tr>
      <tr>
        <td><b>🔹 Drones Aquatiques</b></td>
        <td>
          ✔️ Volent au-dessus des plans d’eau pour cartographier la pollution.<br>
          ✔️ Équipés de caméras thermiques et de capteurs optiques pour surveiller les algues toxiques.<br>
          ✔️ Idéals pour les grandes surfaces, comme les réservoirs et les océans.<br>
          📌 <b>Exemple :</b> Les drones de la <i>NASA</i> utilisés pour surveiller la qualité de l’eau des Grands Lacs aux États-Unis.
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("<h3>2. Fonctionnement et Technologies Utilisées</h3>", unsafe_allow_html=True)
    st.markdown("""
         ✔ Capteurs embarqués : Mesurent la qualité de l’eau en temps réel (métaux lourds, bactéries, pesticides).

         ✔ Intelligence Artificielle (IA) : Analyse les données et détecte les anomalies.

         ✔ Systèmes autonomes : Les robots peuvent ajuster leur parcours en fonction des besoins.

         ✔ Communication en temps réel : Transmission des données aux chercheurs et autorités via des réseaux sans fil.
    """)
    st.markdown("<h3>3. Avantages de l’Utilisation des Robots</h3>", unsafe_allow_html=True)
    st.markdown("""
     ✅ **Surveillance continue** : Fonctionnent 24h/24 sans intervention humaine.
     
     ✅ **Précision des mesures** : Détection de polluants à très faible concentration.
     
     ✅ **Exploration des zones inaccessibles** : Surveillance des eaux profondes et contaminées.
     
     ✅ **Réduction des coûts** : Moins de besoins en échantillonnage manuel et en analyses en laboratoire.

    """)
    st.markdown("<h3>4. Applications Pratiques</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        Surveillance des marées noires : Détection des hydrocarbures et aide au nettoyage.

        Contrôle de la pollution agricole : Mesure des nitrates et phosphates provenant des engrais.

        Prévention des crises sanitaires : Détection rapide de contaminants dangereux.

        Gestion des écosystèmes aquatiques : Suivi des populations de poissons et des niveaux d’oxygène.

    """)
    st.markdown("<h2>🌍 Vers une Surveillance de l’Eau Plus Intelligente</h2>", unsafe_allow_html=True)
    st.markdown("""
        L’utilisation de robots révolutionne la surveillance de l’eau, rendant les analyses plus rapides, précises et accessibles. Grâce à ces technologies, nous pouvons mieux protéger nos ressources en eau et réagir rapidement aux menaces environnementales. 💙🤖💦
    """)

    video_url7 = "https://youtu.be/ljsuGRiz0As?si=h8kR0xfjCTGGtlfN"
    st.video(video_url7)

    video_url8 = "https://youtu.be/KfrtsR-MYl0?si=dbe5XIDVDsmtTJVH"
    st.video(video_url8)


    st.markdown("<h2>💡Projets Innovants dans le Domaine de l’Eau</h2>", unsafe_allow_html=True)
    st.markdown("""
    Face aux défis de la pénurie d’eau et de la pollution, plusieurs projets innovants ont été développés pour améliorer l’accès à une eau propre et potable. Voici quelques exemples inspirants de technologies révolutionnaires dans le domaine de l’eau. 💧
    """)

    st.markdown("<h3>1. Systèmes de Désalinisation Avancés</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 **The Solar Dome** *(Arabie Saoudite)*  
    Utilise l’énergie solaire pour désaliniser l’eau de mer de manière écologique.  
    Réduit de 30% les coûts énergétiques par rapport aux méthodes classiques.  
    Une solution prometteuse pour les pays arides.

    🔹 **Graphene-Based Desalination** *(MIT, États-Unis)*  
    Utilise des membranes de graphène pour filtrer le sel avec une efficacité accrue.  
    Réduit la consommation d’énergie par rapport aux techniques traditionnelles d’osmose inverse.  
    Peut fournir de l’eau potable aux régions côtières souffrant de sécheresse.
    """)

    st.markdown("<h3>2. Machines de Purification d’Eau Portables</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 **LifeStraw** *(Suisse)*  
    Une paille filtrante capable d’éliminer 99,9% des bactéries et parasites.  
    Idéale pour les zones rurales et les situations d’urgence.  
    Permet à une personne de boire jusqu'à 4 000 litres d’eau contaminée sans danger.

    🔹 **The Drinkable Book** *(États-Unis)*  
    Un livre dont les pages contiennent un filtre antibactérien.  
    Chaque page peut purifier 100 litres d’eau, soit un livre pour 4 ans d’eau potable.  
    Une solution économique et éducative pour les populations défavorisées.

    🔹 **Desolenator** *(Royaume-Uni)*  
    Unité de purification alimentée à 100% par l’énergie solaire.  
    Transforme l’eau de mer en eau potable sans utiliser de filtres coûteux.  
    Peut produire 15 litres d’eau propre par jour, idéale pour les villages isolés.
    """)

    st.markdown("<h3>3. Systèmes de Collecte et de Recyclage de l’Eau</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 **Skywater** *(États-Unis)*  
    Machine qui transforme l’humidité de l’air en eau potable.  
    Peut produire jusqu’à 5 000 litres d’eau par jour dans des climats humides.  
    Utilisée pour les secours humanitaires et les bases militaires en zones arides.

    🔹 **WaterSeer** *(États-Unis)*  
    Appareil autonome qui capte l’eau de l’air grâce à une turbine éolienne.  
    Fonctionne sans électricité et peut fournir jusqu’à 37 litres d’eau par jour.  
    Une solution durable pour les communautés rurales.

    🔹 **Hydraloop** *(Pays-Bas)*  
    Système domestique de recyclage des eaux grises (douches, machines à laver).  
    Réduit la consommation d’eau de 45% dans les foyers.  
    Compatible avec les maisons et bâtiments écologiques.
    """)

    st.markdown("<h3>4. Robots et Drones pour la Surveillance et le Nettoyage des Eaux</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 **WasteShark** *(Pays-Bas)*  
    Robot flottant capable de collecter les déchets plastiques dans les rivières et ports.  
    Fonctionne de manière autonome et réduit la pollution avant qu’elle n’atteigne les océans.

    🔹 **SEABIN Project** *(Australie)*  
    Une poubelle flottante qui aspire les déchets et les microplastiques à la surface de l’eau.  
    Déjà installée dans plus de 50 pays pour nettoyer les ports et marinas.

    🔹 **Nereus Drone** *(France)*  
    Drone sous-marin équipé de capteurs pour analyser la pollution des eaux en temps réel.  
    Utilisé pour la surveillance des rivières, lacs et stations d’épuration.
    """)

    st.markdown("<h2>🌍 Vers un Avenir Plus Durable</h2>", unsafe_allow_html=True)
    st.markdown("""
    Ces innovations montrent que la technologie peut jouer un rôle clé dans la préservation et l’accessibilité de l’eau. Grâce à ces projets, nous pouvons réduire la pollution, économiser les ressources et offrir de l’eau potable aux populations les plus vulnérables. 💙💦
    """)

    video_url9 = "https://youtu.be/zyjEX3MTcWw?si=tj6-XsvYmYFKt1xG"
    st.video(video_url9)
# ---- Impact Environnemental ----
elif choice == "Impact Environnemental":
    st.markdown("<h1>Impact Environnemental</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Effets du Changement Climatique sur l’Eau💧</h2>", unsafe_allow_html=True)
    st.markdown("""
    Le changement climatique bouleverse les ressources en eau à travers le monde. Il modifie sa **disponibilité**, **sa qualité** et augmente la fréquence des **catastrophes hydriques**, avec de lourdes conséquences sur la santé, l’agriculture et les écosystèmes.
    """)

    st.markdown("<h3>1. Réduction de la Disponibilité de l’Eau🚱</h3>", unsafe_allow_html=True)
    st.markdown("""
    -**Sécheresses Plus Fréquentes et Intenses**  
    Hausse des températures = évaporation plus rapide + sols asséchés.  
    Baisse des nappes phréatiques, fleuves asséchés, moins d’eau potable.  
    *Exemple :* En **Californie**, l’agriculture souffre de sécheresses records.

    -**Fonte des Glaciers et Neiges Éternelles**  
    Les glaciers sont des réservoirs d’eau douce. Leur fonte diminue l’accès à l’eau.  
    Impact fort sur les régions alimentées par les rivières glaciaires.  
    📌 *Exemple :* L’**Himalaya** perd ses glaciers, menaçant le Gange, Yangtsé, etc.
    """)

    st.markdown("<h3>2. Inondations et Catastrophes Hydriques🌊🌪</h3>", unsafe_allow_html=True)
    st.markdown("""
    -**Précipitations Extrêmes et Crues Subites**  
    Plus de pluie + sols secs = inondations plus violentes.  
    Dommages aux infrastructures, contamination de l’eau.  
    📌 *Exemple :* En **Allemagne** et **Belgique** (2021), des pluies extrêmes ont causé des inondations dramatiques.

    -**Élévation du Niveau de la Mer et Intrusion Saline**  
    Les nappes phréatiques côtières sont envahies par l’eau salée.  
    Moins d’eau douce pour boire et irriguer.  
    📌 *Exemple :* Le **Bangladesh** subit une salinisation accrue de ses terres agricoles.
    """)

    st.markdown("<h3>3. Dégradation de la Qualité de l’Eau🦠☣️</h3>", unsafe_allow_html=True)
    st.markdown("""
    -**Pollution Accrue des Sources d’Eau**  
    Températures + pollution = prolifération d’algues toxiques, égouts débordés.  
    Risques accrus de métaux lourds et bactéries.  
    📌 *Exemple :* Le **Lac Érié** (États-Unis) subit des pics d’algues toxiques.

    -**Stress Hydrique et Conflits**  
    Moins d’eau = plus de tensions entre États et secteurs.  
    Risque de conflits et migrations massives.  
    📌 *Exemple :* Le **barrage du Nil** est source de tension entre l’Éthiopie, le Soudan et l’Égypte.
    """)

    st.markdown("<h3>4. Impacts sur la Santé et l’Agriculture🌾</h3>", unsafe_allow_html=True)
    st.markdown("""
    -**Hausse des Maladies Liées à l’Eau**  
    Chaleur et humidité favorisent choléra, dysenterie, parasites.  
    Accès difficile à une eau potable saine.  
    📌 *Exemple :* En **Afrique de l’Ouest**, les épidémies de choléra sont en hausse.

    -**Baisse des Rendements Agricoles**  
    Moins d’eau pour irriguer = moins de nourriture.  
    👉 Inflammations des prix et insécurité alimentaire.  
    📌 *Exemple :* Le **Sahel** subit une désertification et une chute de productivité.
    """)

    st.markdown("<h2>🌍Vers des Solutions Durables</h2>", unsafe_allow_html=True)
    st.markdown("""
    ✅ Gestion plus efficace de l’eau (recyclage, irrigation goutte-à-goutte).
    
    ✅ Technologies de dessalement et purification pour compenser la raréfaction de l’eau douce.
    
    ✅ Politiques d’adaptation et d’atténuation pour limiter l’impact du changement climatique.
    
    ✅ Protection des écosystèmes aquatiques pour préserver les ressources naturelles.
    
    Le changement climatique transforme notre relation avec l’eau. Des actions rapides et innovantes sont nécessaires pour protéger cette ressource vitale pour l’avenir de l’humanité. 💙💦

    """)

    st.video("https://youtu.be/LpSVRqYJP1g?si=swknl0Bp920Qfmbr")
    st.video("https://youtu.be/T4LVXCCmIKA?si=nazGSQJ0OHhVrjBc")

    st.markdown("<h2>Biodiversité Aquatique et Impacts de la Pollution de l’Eau 🌍🐟💧</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    La biodiversité aquatique englobe l’ensemble des organismes vivants qui habitent les milieux aquatiques (rivières, lacs, océans, zones humides).  
    Ces écosystèmes jouent un rôle crucial dans le maintien de l’équilibre écologique, mais sont de plus en plus menacés par la pollution de l’eau.
    """)

    st.markdown("<h3>1.La Biodiversité Aquatique 🌿🐠</h3>", unsafe_allow_html=True)

    st.markdown("<h4>Les Écosystèmes Aquatiques</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    - **Récifs Coralliens** : Habitats marins riches en biodiversité, abritant plus de 25% des espèces marines.  
    - **Zones Humides** : Cruciales pour la reproduction de nombreuses espèces d'oiseaux, poissons et amphibiens.  
    - **Rivières et Lacs d’eau Douce** : Source d’eau potable et habitat pour de nombreuses espèces comme les poissons, insectes aquatiques et plantes.
    """)

    st.markdown("<h4>Les Espèces Aquatiques</h4>", unsafe_allow_html=True)
    
    st.markdown("""

    - Poissons (exza. : saumons, thons, poissons tropicaux)
    
    - Plantes aquatiques (ex. : nénuphars, algues)
    
    - Invertébrés aquatiques (ex. : moules, crustacés, larves d’insectes)
    
    - Mammifères marins (ex. : baleines, dauphins)
    
    - Reptiles aquatiques (ex. : tortues marines)  

    Ces espèces sont essentielles à l’équilibre des chaînes alimentaires et à la régulation des cycles des nutriments.
    """)

    st.markdown("<h3>2.Les Effets de la Pollution de l’Eau sur la Biodiversité Aquatique 🏭💔</h3>", unsafe_allow_html=True)

    st.markdown("<h4>Pollution Chimique</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    - **Bioaccumulation et biomagnification** : Les polluants s’accumulent et se concentrent à chaque niveau trophique.  
    - **Intoxication et mortalité** : Affectent la reproduction, la croissance et la survie des espèces.  
    📌 *Exemple :* Le **mercredi de Minamata** (Japon) – pollution au mercure causant malformations et décès.
    """)

    st.markdown("<h4>Pollution Organique (Dépôts de Nutriments)</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    - **Zones mortes** : L’excès de nutriments provoque un manque d’oxygène fatal à la vie aquatique.  
    - **Perte de biodiversité** : Les algues toxiques étouffent la vie aquatique.  
    📌 *Exemple :* Le **Golfe du Mexique** développe chaque été une vaste zone morte.
    """)

    st.markdown("<h4>Pollution Plastique</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    - **Blocage des voies respiratoires** : Ingestion de plastiques par les animaux marins.  
    - **Perturbation hormonale** : Certains plastiques agissent comme perturbateurs endocriniens.  
    📌 *Exemple :* Les **tortues marines** ingèrent des sacs plastiques confondus avec des méduses.
    """)

    st.markdown("<h4>Pollution Thermique</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    - **Réduction de l’oxygène dissous** : L’eau chaude est moins oxygénée.  
    - **Migration des espèces** : Déplacement vers des eaux plus froides, perturbant l’équilibre.  
    📌 *Exemple :* Les **truites**, espèces sensibles, souffrent fortement de cette pollution.
    """)

    st.markdown("<h3>3.Solutions pour Protéger la Biodiversité Aquatique 🌱💦</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    ✅ **Réduction de la Pollution** : Limiter les rejets industriels/agricoles, technologies écologiques.  
    ✅ **Protection des Zones Sensibles** : Créer des réserves et zones protégées.  
    ✅ **Restauration des Écosystèmes Aquatiques** : Réhabiliter zones humides, récifs coralliens.  
    ✅ **Éducation et Sensibilisation** : Informer le public sur les dangers de la pollution de l’eau.
    """)

    st.markdown("<h2>🌍 Un Appel à la Protection de Nos Écosystèmes Aquatiques</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    La biodiversité aquatique est cruciale pour la survie des humains et des espèces animales.  
    Agir contre la pollution, c’est préserver notre avenir commun. 💙🐟💧
    """)

    st.video("https://youtu.be/bIpmzuuyASY?si=iEi8aMqp7nvSuFUk")
#----"Éducation et Sensibilisation"-----
elif choice=="Éducation et Sensibilisation":
    st.markdown("<h1>Éducation et Sensibilisation</h1>", unsafe_allow_html=True)
    st.markdown("<h2>🌊 Initiatives de Nettoyage des Océans et Réduction des Déchets Plastiques 🌍♻</h2>", unsafe_allow_html=True)

    st.markdown("""
    Les océans sont submergés par des milliards de tonnes de déchets, principalement plastiques.  
    Heureusement, plusieurs initiatives mondiales se battent pour restaurer la santé des océans.  
    Voici quelques-unes des plus remarquables.  
    """)

    st.markdown("<h3>1. The Ocean Cleanup (Pays-Bas)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Éliminer 90% du plastique flottant dans les océans d'ici 2040.  
    🔹 *Fonctionnement* : Dispositif flottant avec barrière + filet.  
    Utilisé dans les gyres océaniques (ex : Great Pacific Garbage Patch).  
    Le plastique est ensuite recyclé.  
    📌 Exemple : Des tonnes de plastique collectées dans le Pacifique.
    """)

    st.markdown("<h3>2. Plastic Bank (International)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Transformer les déchets plastiques en monnaie sociale.  
    🔹 *Fonctionnement* :  
    Collecte par des communautés défavorisées, échange contre crédits, énergie, produits.  
    Création d'une *économie circulaire*.  
    📌 Exemple : En Haïti, des familles échangent du plastique contre nourriture.
    """)

    st.markdown("<h3>3. Surfrider Foundation (International)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Protection des océans et plages.  
    🔹 *Fonctionnement* :  
    - Nettoyages de plages  
    - Sensibilisation (Rise Above Plastics)  
    - Lobbying contre les plastiques à usage unique  
    📌 Exemple : Événements mondiaux de nettoyage chaque année.
    """)

    st.markdown("<h3>4. Clean Seas (Programme ONU)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Réduction globale de la pollution plastique.  
    🔹 *Fonctionnement* :  
    - Collaboration avec les gouvernements  
    - Campagnes de sensibilisation  
    - Encouragement du recyclage et des alternatives durables  
    📌 Exemple : L'Indonésie, la Belgique, les Philippines agissent grâce à ce programme.
    """)

    st.markdown("<h3>5. Trash Isles (UK)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Créer un pays fictif dans le Pacifique pour *attirer l’attention* sur la pollution plastique.  
    🔹 *Fonctionnement* :  
    - Capitales, passeports symboliques  
    - Campagnes pour une reconnaissance à l’ONU  
    📌 Exemple : +200 000 signatures obtenues pour sensibiliser les médias.
    """)

    st.markdown("<h3>6. Parley for the Oceans (International)</h3>", unsafe_allow_html=True)
    st.markdown("""
    🔹 *Objectif* : Collaborer avec marques & créateurs pour transformer les plastiques marins en produits utiles.  
    🔹 *Fonctionnement* :  
    - Partenariat avec Adidas  
    - Création de vêtements à partir de plastique océanique recyclé  
    📌 Exemple : Chaussures Adidas en plastique recyclé.
    """)

    st.markdown("<h2>🌍 Un Appel à l’Action Collective</h2>", unsafe_allow_html=True)
    st.markdown("""
    La pollution plastique est un *défi mondial*.  
    Ces initiatives montrent qu’il est *possible d’agir*, mais un engagement **collectif** est essentiel.  
    Chaque geste compte pour *sauver nos océans*. 💙🌊♻
    """)

    st.video("https://youtu.be/W5atMhdq_gA?si=nYoZTggO86yd-rNp")

    
# ---- Quiz ----
elif choice == "Quiz":
    # 📚 Questions à choix multiples (QCM)
    questions_mcq = [
        {
            "question": "Quelle étape du cycle de l’eau correspond à la formation de nuages ?",
            "options": ["Infiltration", "Condensation", "Ruissellement", "Évaporation"],
            "answer": "Condensation"
        },
        {
            "question": "Quel usage consomme le plus d’eau à l’échelle mondiale ?",
            "options": ["Domestique", "Industriel", "Agricole", "Énergétique"],
            "answer": "Agricole"
        },
        {
            "question": "Quelle pratique permet d’économiser l’eau à la maison ?",
            "options": ["Arroser à midi", "Utiliser un lave-vaisselle plein", "Prendre des bains", "Laver la voiture chaque semaine"],
            "answer": "Utiliser un lave-vaisselle plein"
        }
    ]

    # ✅ Vrai ou Faux
    true_or_false_questions = [
        {"question": "L’évaporation transforme l’eau liquide en vapeur.", "answer": True},
        {"question": "L’infiltration renvoie l’eau directement dans l’atmosphère.", "answer": False},
        {"question": "Les nappes phréatiques sont des réserves d’eau souterraines.", "answer": True},
        {"question": "L’industrie consomme plus d’eau que l’agriculture dans le monde.", "answer": False}
    ]

    # ✍ Questions ouvertes
    progressive_questions = [
        {"question": "Quelle étape du cycle de l’eau suit immédiatement les précipitations ?", "answer": "Ruissellement"},
        {"question": "Quel est le nom du processus par lequel l’eau passe du sol aux nappes souterraines ?", "answer": "Infiltration"},
        {"question": "Quel est le principal gaz responsable de la condensation dans le cycle de l’eau ?", "answer": "Vapeur d’eau"},
        {"question": "Cite une solution pour économiser l’eau dans un jardin ?", "answer": "Goutte-à-goutte"}
    ]

    # 🧪 Classement par usage d’eau (du plus au moins consommateur)
    usages = [
        {"method": "Agriculture", "efficiency": "Très élevé"},
        {"method": "Industrie", "efficiency": "Élevé"},
        {"method": "Usage domestique", "efficiency": "Moyen"},
        {"method": "Loisirs", "efficiency": "Faible"}
    ]

    # QCM
    def multiple_choice_game():
        st.title("🧠 QCM - Cycle et usages de l’eau")
        score = 0
        answers = []

        for i, q in enumerate(questions_mcq):
            st.subheader(f"Question {i + 1}: {q['question']}")
            selected_option = st.radio("Choisissez la bonne réponse :", q["options"], key=f"mcq_{i}")
            answers.append(selected_option == q["answer"])

        if st.button("Afficher les résultats", key="btn_mcq"):
            for i, answer in enumerate(answers):
                if answer:
                    st.success(f"✅ Question {i+1} : Bonne réponse !")
                else:
                    st.error(f"❌ Question {i+1} : Mauvaise réponse. La bonne réponse était : {questions_mcq[i]['answer']}")
            st.write(f"🎉 Score final : {sum(answers)} / {len(questions_mcq)}")

    # Vrai ou Faux
    def true_or_false_game():
        st.title("🔍 Vrai ou Faux - Cycle de l’eau")
        answers = []

        for i, q in enumerate(true_or_false_questions):
            user_answer = st.radio(f"Question {i + 1}: {q['question']}", ["Vrai", "Faux"], key=f"tf_{i}")
            correct = (user_answer == "Vrai" and q["answer"]) or (user_answer == "Faux" and not q["answer"])
            answers.append(correct)

        if st.button("Afficher les résultats", key="btn_tf"):
            for i, answer in enumerate(answers):
                correct = "Vrai" if true_or_false_questions[i]["answer"] else "Faux"
                if answer:
                    st.success(f"✅ Question {i+1} : Bonne réponse !")
                else:
                    st.error(f"❌ Question {i+1} : Mauvaise réponse. La bonne réponse était : {correct}")
            st.write(f"🎉 Score final : {sum(answers)} / {len(true_or_false_questions)}")

    # Questions ouvertes
    def progressive_quiz():
        st.title("🧠 Questions ouvertes - Cycle et gestion de l’eau")
        answers = []

        for i, q in enumerate(progressive_questions):
            user_answer = st.text_input(f"Question {i + 1}: {q['question']}", key=f"pq_{i}")
            correct = user_answer.strip().lower() == q["answer"].lower()
            answers.append(correct)

        if st.button("Afficher les résultats", key="btn_pq"):
            for i, answer in enumerate(answers):
                if answer:
                    st.success(f"✅ Question {i+1} : Bonne réponse !")
                else:
                    st.error(f"❌ Question {i+1} : La bonne réponse était : {progressive_questions[i]['answer']}")
            st.write(f"🎉 Score final : {sum(answers)} / {len(progressive_questions)}")

    # Classement
    def sorting_game():
        st.title("📊 Classement des usages de l’eau selon la consommation")
        st.write("Classez les usages du plus grand au plus petit consommateur d’eau.")

        usages_sorted = sorted(usages, key=lambda x: x["efficiency"], reverse=True)
        usage_names = [u["method"] for u in usages_sorted]

        ordered = st.multiselect("Classez les usages :", options=[u["method"] for u in usages], key="sort")

        if ordered:
            if ordered == usage_names:
                st.success("✅ Classement correct !")
            else:
                st.error("❌ Classement incorrect. Essayez encore.")

    # Menu principal
    def main():
        st.sidebar.title("💧 Quiz : Cycle et usages de l’eau")
        page = st.sidebar.radio("Choisissez un jeu :", ["QCM", "Vrai ou Faux", "Questions ouvertes", "Classement des usages"])

        if page == "QCM":
            multiple_choice_game()
        elif page == "Vrai ou Faux":
            true_or_false_game()
        elif page == "Questions ouvertes":
            progressive_quiz()
        elif page == "Classement des usages":
            sorting_game()

    if __name__ == "__main__":
        main()



# ---- Chatbot ----
elif choice == "Dropbot":
    # === Load and cache model ===
    def preprocess_input(input_text):
        return input_text.lower().replace("quels sont", "").strip()

    @st.cache_resource
    def load_model():
        return SentenceTransformer('all-MiniLM-L6-v2')

    @st.cache_data
    def load_qa_data():
        with open("qa_data.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def encode_questions(model, questions):
        return model.encode(questions)

    def get_best_match_fuzzy(user_input, qa_pairs):
        best_match = process.extractOne(user_input, list(qa_pairs.keys()))
        return best_match

    # === Load data ===
    model = load_model()
    qa_pairs = load_qa_data()
    questions = list(qa_pairs.keys())

    # === Initialize memory ===
    if "history" not in st.session_state:
        st.session_state.history = []

    if "question_embeddings" not in st.session_state:
        st.session_state.question_embeddings = encode_questions(model, questions)

    # === Title ===
    st.title("DropBot 💧")
    st.markdown("Pose-moi une question sur l'eau")

    # === Form ===
    with st.form("my_form", clear_on_submit=True):
        user_input = st.text_input("Tape ta question :", key="user_question")
        submitted = st.form_submit_button("Envoyer")

    # === Handle response ===
    if submitted and user_input:
        user_input_clean = preprocess_input(user_input)
        user_embedding = model.encode([user_input_clean])
        similarities = cosine_similarity(user_embedding, st.session_state.question_embeddings)
        best_match_idx = np.argmax(similarities)
        confidence = similarities[0][best_match_idx]
        best_answer = qa_pairs[questions[best_match_idx]]

        if confidence < 0.5:
            fuzzy_match = get_best_match_fuzzy(user_input_clean, qa_pairs)
            best_answer = qa_pairs[fuzzy_match[0]]
            greeting = random.choice(["Bonjour 👋", "Salut !", "Coucou 😊"])
            bot_response = f"{greeting} Je ne suis pas totalement sûre, mais cela pourrait t'aider :\n\n**{best_answer}**"
        else:
            bot_response = f"**{best_answer}**"

        st.session_state.history.append(("Toi", user_input))
        st.session_state.history.append(("Bot", bot_response))

    # === Show chat with avatars ===
    for speaker, message in st.session_state.history:
        if speaker == "Toi":
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("https://cdn-icons-png.flaticon.com/512/1077/1077114.png", width=40)  # user avatar
            with col2:
                st.markdown(f"**Toi :** {message}")
        else:
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("https://cdn-icons-png.flaticon.com/512/3558/3558977.png", width=40)  # bot avatar
            with col2:
                st.markdown(f"**DropBot 💧 :** {message}")

