import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
import json
import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from datetime import datetime
from streamlit_chat import message
import base64


# ---- Personnalisation CSS ----
def get_base64_image(image_path):
    """Convert image to base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

background_image_base64 = get_base64_image("aaa.jpg")
header_image_base64 = get_base64_image("WaterSense.png")

# ---- Page Configuration ----
st.set_page_config(
    page_title="WaterSense",      
    page_icon="💧",               
    layout="centered"
)

# ---- Function to Translate ----
def translate(fr, ar):
    return ar if st.session_state.lang == "العربية" else fr

# ---- Function to Change Language ----
def change_language():
    if st.session_state.lang == "Français":
        st.session_state.lang = "العربية"
    else:
        st.session_state.lang = "Français"
    st.rerun()

# ---- Session State Initialization ----
if "lang" not in st.session_state:
    st.session_state.lang = "Français"  # Default language
if st.session_state.lang == "العربية":
    direction = "rtl"
    text_align = "right"
    image_position = "left"  # Move image to the left for RTL
    text_position = "right"  # Move text to the right for RTL
else:
    direction = "ltr"
    text_align = "left"
    image_position = "right"  # Default position of image for LTR
    text_position = "left"  # Default position of text for LTR

if "visitors" not in st.session_state:
    st.session_state.visitors = 1
else:
    st.session_state.visitors += 1

# ---- Sidebar - Visitors and Time ----
def show_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    st.sidebar.markdown(f"**{translate('Current Time', 'الوقت الحالي')}**: {current_time}")

st.sidebar.markdown(f"**{translate('Visitors', 'الزوار')}**: {st.session_state.visitors}")
show_time()

# ---- Navigation Menu ----
menu_fr = ["Accueil", "Analyse de l'Eau", "Qualité de l'Eau", "Gestion de l'Eau",
           "Technologies et Innovations", "Impact Environnemental", "Quiz", "Dropbot", "À propos de nous"]

menu_ar = ["الرئيسية", "تحليل المياه", "جودة المياه", "إدارة المياه",
           "التقنيات والابتكارات", "الأثر البيئي", "اختبار", "دروب بوت", "معلومات عنا"]

menu = menu_ar if st.session_state.lang == "العربية" else menu_fr
choice = st.sidebar.radio(translate("**Navigation**", "**التنقل**"), menu)
st.session_state.page = choice

# ---- CSS for Different Pages ----
if choice in ["Accueil", "À propos de nous", "الرئيسية", "معلومات عنا"]:
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
            @media (max-width: 768px) {
        .header-text h1 {
            font-size: 2em !important;
        }
        .header-text p {
            font-size: 0.95em !important;
        }
        h1, h2, h3 {
            font-size: 1.2em !important;
        }
        body, p, span {
            font-size: 0.95em !important;
        }
        div[role="radiogroup"] > label {
            font-size: 0.95em !important;
        }
        .stButton>button {
            font-size: 0.95em !important;
            padding: 6px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)
# Apply dynamic CSS for layout changes
st.markdown(f"""
    <style>
        body {{
            direction: {direction};
            text-align: {text_align};
        }}
        .header-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            direction: {direction};
        }}
        .header-text {{
            text-align: {text_align};
            order: {text_position == 'right' and 2 or 1};  /* Swap order for RTL */
        }}
        .header-image {{
            order: {image_position == 'left' and 1 or 2}; /* Swap order for RTL */
        }}
    </style>
""", unsafe_allow_html=True)

# ---- Styling and Content ----
if choice in ["Accueil", "الرئيسية"]:
    st.markdown("""<style>.block-container {padding-top: 0rem;}</style>""", unsafe_allow_html=True)

    st.markdown("""<style>
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
        .language-button {
            position: absolute;
            top: 20px;
            left: 20px;
            background-color: white;
            color: #001D2F;
            border: none;
            padding: 10px 15px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            z-index: 10;
            transition: background-color 0.3s ease;
        }
        .language-button:hover {
            background-color: #001D2F;
            color: white;
        }
    </style>""", unsafe_allow_html=True)

    # ---- Language Button ----
    form = st.form(key="language_form")
    with form:
        lang_button_label = "Français" if st.session_state.lang == "العربية" else "العربية"
        change_lang_button = st.form_submit_button(lang_button_label)
    
    if change_lang_button:
        change_language()

    # ---- Header Section ----
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
                    {translate(
                        "L’eau est au cœur de la vie. Mais aujourd’hui, cette ressource vitale est menacée par la pollution, "
                        "le changement climatique, la surexploitation et l’inégalité d’accès. Ces défis exigent une prise de "
                        "conscience collective et une meilleure compréhension de l’importance de l’eau dans notre quotidien.<br><br>"
                        "Bienvenue sur WaterSense, une plateforme éducative et interactive qui t’aide à explorer, apprendre et agir "
                        "pour une gestion plus durable de l’eau.",
                        "الماء هو جوهر الحياة. لكنه اليوم مهدد بالتلوث، وتغير المناخ، والاستغلال المفرط، وعدم المساواة في الوصول إليه. "
                        "هذه التحديات تتطلب وعياً جماعياً وفهماً أفضل لأهمية الماء في حياتنا اليومية.<br><br>"
                        "مرحبًا بك في WaterSense، منصة تعليمية وتفاعلية تساعدك على الاستكشاف والتعلم والعمل من أجل إدارة مستدامة للماء."
                    )}
                </p>
            </div>
            <div class="header-image">
                <img src="data:image/png;base64,{header_image_base64}" alt="Water ripple"/>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif choice in ["À propos de nous", "معلومات عنا"]:
    col1, col2 = st.columns([2, 1])

    with col1:
        if st.session_state.lang == "العربية":
            st.markdown("""
            <div style="display: flex; align-items: center;">
                <div style="flex: 1; padding-right: 20px; text-align: justify;">
                    <h1>معلومات عنا</h1>
                    <p>
                        نحن فريق <strong>FikrCode</strong> من ثانوية ابن بطوطة في العرائش، مجموعة مكونة من أربعة طلاب شغوفين بالتكنولوجيا والبيئة: أمين الحافظي، ياسمينة بالحاج، سهام إدحسان، وإسماعيل الكركري. نحن تحت إشراف معلمتنا ومرشدتنا، فاتن أمهير، التي توجهنا في هذا المشروع الطموح.
                    </p>
                    <p>
                        تم تشكيل فريقنا حول هدف مشترك: زيادة الوعي حول حماية الماء، وهو مورد أساسي مهدد بشكل متزايد. على الرغم من أن الماء هو جوهر الحياة، إلا أنه يواجه العديد من التحديات مثل التلوث، الاستغلال المفرط، تغير المناخ، وعدم المساواة في الوصول إليه. نريد أن يدرك الجميع أهمية الحفاظ على هذه المورد، ليس فقط لأنفسنا، ولكن أيضًا من أجل الأجيال القادمة.
                    </p>
                    <p>
                        المشروع الذي طورناه فريد من نوعه. أنشأنا شات بوت تعليمي سهل الاستخدام يجيب على أسئلة الجمهور حول الماء، موضحًا مكوناته وخصائصه والتهديدات التي تواجهه. يعتمد هذا الشات بوت على أساليب الذكاء الاصطناعي البسيطة والمتاحة، مما يسمح لأي مستخدم بالحصول على معلومات دقيقة بنقرات قليلة. يهدف هذا المشروع إلى جعل المعرفة حول الماء أكثر سهولة ويشجع على العمل الجماعي من أجل إدارته بشكل مستدام.
                    </p>
                    <p>
                        منصتنا مخصصة بالكامل للجمهور العام. توفر مجموعة من الأدوات التفاعلية مثل الاختبارات، التحليلات، والمحتوى التعليمي. من خلال دمج المعلومات العلمية والحلول العملية، نريد أن نلهم المواطنين، وخاصة الشباب، لاعتماد ممارسات أكثر استدامة للحفاظ على الماء والبيئة بشكل عام.
                    </p>
                    <p>
                        نحن نؤمن بعالم أكثر استدامة، حيث يدرك كل فرد أهمية الماء، والمخاطر التي تهدده، ويعمل من أجل الحفاظ عليه. لهذا السبب نحن ملتزمون بشكل كامل بهذا المشروع، ليس فقط للإعلام، ولكن أيضًا لإحداث تغيير حقيقي في الطريقة التي نرى بها الماء ونستخدمه في حياتنا اليومية. معًا، يمكننا أن نحدث فرقًا ونسهم في إنشاء مستقبل يبقى فيه الماء موردًا متاحًا ومحفوظًا.
                    </p>
                    <p>
                        <strong>فريق FikrCode</strong>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)


        else:
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
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.image("eee.png", use_container_width=True)


# ---- Analyse de l'eau ----

# ---- Analyse de l'eau ----

# ---- Analyse de l'eau ----

if choice == translate("Analyse de l'Eau", "تحليل المياه"):

    def simulateur_qualite_eau():
        st.title("💧 " + translate("Simulateur de la qualité de l'eau", "محاكي جودة المياه"))

        # --- Entrée des paramètres ---
        ph = st.slider(translate("📏 Valeur du pH", "📏 قيمة الـ pH"), 0.0, 14.0, 7.0, key="ph_slider")
        turbidite = st.slider(translate("🌫 Turbidité (en NTU)", "🌫 العكارة (بـ NTU)"), 0.0, 10.0, 1.0, key="turbidite_slider")
        nitrates = st.slider(translate("🧪 Nitrates (mg/L)", "🧪 النترات (مغ/لتر)"), 0.0, 100.0, 20.0, key="nitrates_slider")
        bacteries = st.radio(
            translate("🦠 Y a-t-il des bactéries détectées ?", "🦠 هل تم اكتشاف بكتيريا؟"),
            [translate("Non", "لا"), translate("Oui", "نعم")],
            key="bacteries_radio",
            index=0 if st.session_state.lang == "Français" else 1
        )

        messages = []
        recommandations = []
        score = 100

        # --- Analyse des résultats ---
        if not (6.5 <= ph <= 8.5):
            messages.append(translate("❌ pH hors de la plage acceptable (6.5 - 8.5).", "❌ قيمة الـ pH خارج النطاق المقبول (6.5 - 8.5)."))
            recommandations.append(translate("✅ Ajuster le pH de l'eau avec des produits adaptés.", "✅ ضبط قيمة pH باستخدام مواد مناسبة."))
            score -= 25
        else:
            messages.append(translate("✅ pH dans la norme.", "✅ قيمة الـ pH ضمن النطاق المقبول."))

        if turbidite > 5:
            messages.append(translate("❌ Turbidité trop élevée (> 5 NTU).", "❌ العكارة مرتفعة (> 5 NTU)."))
            recommandations.append(translate("✅ Filtrer l'eau pour réduire la turbidité.", "✅ ترشيح المياه لتقليل العكارة."))
            score -= 25
        else:
            messages.append(translate("✅ Turbidité acceptable.", "✅ العكارة ضمن المستوى المقبول."))

        if nitrates > 50:
            messages.append(translate("❌ Nitrates élevés (> 50 mg/L).", "❌ النترات مرتفعة (> 50 مغ/لتر)."))
            recommandations.append(translate("✅ Traiter l'eau pour éliminer l'excès de nitrates.", "✅ معالجة المياه لإزالة فائض النترات."))
            score -= 25
        else:
            messages.append(translate("✅ Nitrates dans la norme.", "✅ النترات ضمن النطاق المقبول."))

        if bacteries == translate("Oui", "نعم"):
            messages.append(translate("❌ Présence de bactéries détectée.", "❌ تم اكتشاف بكتيريا."))
            recommandations.append(translate("✅ Désinfecter l'eau (par ex : par chloration ou UV).", "✅ تعقيم المياه (مثلاً بالتطهير بالكلور أو بالأشعة فوق البنفسجية)."))
            score -= 25
        else:
            messages.append(translate("✅ Aucune bactérie détectée.", "✅ لا توجد بكتيريا مكتشفة."))

        # --- Résultats simples ---
        st.subheader(translate("🔎 Résultat de l'analyse :", "🔎 نتيجة التحليل:"))
        for m in messages:
            st.write(m)

        if score >= 75:
            evaluation = translate("💧 Qualité de l'eau : BONNE", "💧 جودة المياه: جيدة")
            st.success(evaluation)
        elif 50 <= score < 75:
            evaluation = translate("⚠ Qualité de l'eau : MOYENNE", "⚠ جودة المياه: متوسطة")
            st.warning(evaluation)
        else:
            evaluation = translate("🚫 Qualité de l'eau : MAUVAISE", "🚫 جودة المياه: سيئة")
            st.error(evaluation)

        # --- Graphique Scatter (pH vs Turbidité) ---
        fig, ax = plt.subplots()
        ax.scatter(ph, turbidite, color='blue', s=150)
        ax.axvline(6.5, color='green', linestyle='--')
        ax.axvline(8.5, color='green', linestyle='--')
        ax.axhline(5, color='orange', linestyle='--')
        ax.set_title(translate("pH vs Turbidité", "pH ةﺭﺎﻜﻌﻟﺍ ﻞﺑﺎﻘﻣ"))
        ax.set_xlabel(translate("pH", "pH"))
        ax.set_ylabel(translate("Turbidité (NTU)", "ةﺭﺎﻜﻌﻟﺍ (NTU)"))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        ax.grid(True)
        st.pyplot(fig)

        # --- Graphique Radar ---
        import numpy as np

        labels = np.array([translate("pH", "pH"), translate("Turbidité", "ةﺭﺎﻜﻌﻟﺍ"), translate("Nitrates", "تﺍﺮﺘﻨﻟﺍ "), translate("Bactéries", "ﺎﻳﺮﻴﺘﻜﺒﻟﺍ")])
        valeurs = np.array([
            max(0, 100 - abs(ph - 7.5) * 20),
            max(0, 100 - (turbidite / 5) * 100),
            max(0, 100 - (nitrates / 50) * 100),
            0 if bacteries == translate("Oui", "نعم") else 100
        ])

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        valeurs = np.concatenate((valeurs, [valeurs[0]]))
        angles += angles[:1]

        fig2, ax2 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax2.fill(angles, valeurs, color='skyblue', alpha=0.5)
        ax2.plot(angles, valeurs, color='blue')
        ax2.set_yticklabels([])
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(labels)
        ax2.set_title(translate("Qualité globale de l'eau", "هﺎﻴﻤﻠﻟ ﺔﻣﺎﻌﻟﺍ ةﺩﻮﺠﻟﺍ"), size=15)
        st.pyplot(fig2)

        # --- Carte Récapitulative ---
        with st.container():
            st.markdown("---")
            st.subheader(translate("📋 Carte de Synthèse", "📋 بطاقة التلخيص"))

            st.info(f"{translate('Score Global', 'النقطة العامة')}: {score}/100")
            st.write(f"{translate('Évaluation', 'التقييم')}: {evaluation}")

            # --- Interprétation du radar ---
            valeurs_labels = dict(zip(labels, valeurs[:-1]))
            pire_parametre = min(valeurs_labels, key=valeurs_labels.get)
            pire_parametre1 = pire_parametre[::-1]
            interpretation = translate(
                f"🔎 Le paramètre le plus critique est : *{pire_parametre}*. Il nécessite une attention particulière.",
                f"🔎 المؤشر الأكثر خطورة هو: *{pire_parametre1}*. يتطلب اهتماماً خاصاً."
            )
            st.warning(interpretation)

            if recommandations:
                st.subheader(translate("🔧 Recommandations pour améliorer l'eau :", "🔧 توصيات لتحسين المياه:"))
                for reco in recommandations:
                    st.write("- " + reco)
            else:
                st.success(translate("👍 Aucune recommandation : l'eau est parfaite !", "👍 لا توجد توصيات: المياه ممتازة!"))

    simulateur_qualite_eau()
elif choice == translate("Qualité de l'Eau", "جودة المياه"):
    st.markdown(f"<h1 style='text-align:{text_align};'>{translate('Qualité de l\'Eau', 'جودة المياه')}</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate('L\'eau peut être contaminée par divers types de polluants, ayant des effets néfastes sur la santé humaine et l’environnement. Voici les principales catégories de polluants :', 
                   'المياه قد تتلوث بأنواع مختلفة من الملوثات التي تؤثر سلبًا على صحة الإنسان والبيئة. فيما يلي الفئات الرئيسية للملوثات:')}
    """)

    st.markdown(f"<h2 style='text-align:{text_align};'>{translate('Détection de Polluants', 'كشف الملوثات')}</h2>", unsafe_allow_html=True)
    st.markdown(f'''
        **{translate('Métaux lourds', 'المعادن الثقيلة')}** (plomb, mercure, arsenic) : {translate('Provoquent des maladies neurologiques et rénales.', 'تسبب أمراضًا عصبية وكلوية.')}
        
        **{translate('Pesticides et herbicides', 'المبيدات الحشرية والمبيدات العشبية')}** : {translate('Toxiques pour la faune aquatique et liés à des troubles hormonaux chez l\'homme.', 'سامة للحياة المائية وترتبط باضطرابات هرمونية لدى الإنسان.')}
        
        **{translate('Produits pharmaceutiques', 'المستحضرات الصيدلانية')}** : {translate('Affectent les organismes aquatiques et peuvent entraîner une résistance aux antibiotiques.', 'تؤثر على الكائنات المائية وقد تؤدي إلى مقاومة المضادات الحيوية.')}
    ''')
    
    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('1. Polluants biologiques', '1. الملوثات البيولوجية')}</h3>", unsafe_allow_html=True)
    st.markdown(f'''
        **{translate('Bactéries et virus', 'البكتيريا والفيروسات')}** (E. coli, choléra, hépatite A) : {translate('Responsables de maladies gastro-intestinales graves.', 'تسبب أمراضًا معوية خطيرة.')}
        
        **{translate('Parasites', 'الطفيليات')}** (Giardia, Cryptosporidium) : {translate('Peuvent causer des infections intestinales sévères.', 'قد تسبب التهابات معوية حادة.')}
    ''')

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('2. Polluants physiques', '2. الملوثات الفيزيائية')}</h3>", unsafe_allow_html=True)
    st.markdown(f'''
        **{translate('Microplastiques', 'الميكروبلاستيك')}** : {translate('Absorbent des toxines et peuvent s\'accumuler dans la chaîne alimentaire.', 'تمتص السموم ويمكن أن تتراكم في السلسلة الغذائية.')}
        
        **{translate('Sédiments en excès', 'الرواسب الزائدة')}** : {translate('Réduisent la clarté de l\'eau et perturbent l\'écosystème aquatique.', 'تقلل من وضوح المياه وتسبب اضطرابًا في النظام البيئي المائي.')}
    ''')

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('3. Impact sur la santé et l\'environnement', '3. التأثير على الصحة والبيئة')}</h3>", unsafe_allow_html=True)
    st.markdown(f'''
        **{translate('Problèmes de santé', 'مشاكل صحية')}** : {translate('Empoisonnement, maladies chroniques, troubles hormonaux.', 'التسمم، الأمراض المزمنة، اضطرابات هرمونية.')}
        
        **{translate('Dégradation de l\'écosystème', 'تدهور النظام البيئي')}** : {translate('Perte de biodiversité, contamination des ressources naturelles.', 'فقدان التنوع البيولوجي، تلوث الموارد الطبيعية.')}
        
        **{translate('Déséquilibres écologiques', 'الاختلالات البيئية')}** : {translate('Prolifération d\'algues nuisibles, acidification de l\'eau.', 'انتشار الطحالب الضارة، تحمض المياه.')}
    ''')

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('4. Solutions et prévention', '4. الحلول والوقاية')}</h3>", unsafe_allow_html=True)
    st.markdown(f'''
        - {translate('Surveillance et analyse régulière de la qualité de l\'eau.', 'مراقبة وتحليل جودة المياه بانتظام.')}
        
        - {translate('Technologies de filtration et de purification avancées.', 'تقنيات الفلترة والتطهير المتقدمة.')}
        
        - {translate('Sensibilisation et réglementation stricte pour limiter les rejets polluants.', 'التوعية والتنظيم الصارم للحد من انبعاثات الملوثات.')}
        
        {translate('L’identification et la réduction des polluants sont essentielles pour préserver la santé publique et protéger nos ressources en eau. 💧🌍', 'تحديد وتقليل الملوثات أمر أساسي للحفاظ على الصحة العامة وحماية مواردنا المائية. 💧🌍')}
    ''')

    video_url = "https://youtu.be/jkyZIpfrQnM?si=VqVo0zFCbevpG2ml"
    st.video(video_url)

    st.markdown(f"<h2 style='text-align:{text_align};'>{translate('Techniques de Purification de l’Eau', 'تقنيات تنقية المياه')}</h2>", unsafe_allow_html=True)

    st.markdown(f"""
        {translate('La purification de l’eau est essentielle pour éliminer les contaminants et garantir une eau propre et saine. Voici les principales méthodes utilisées, avec leurs avantages et limites.', 
                   'تنقية المياه أمر أساسي لإزالة الملوثات وضمان مياه نظيفة وصحية. فيما يلي الطرق الرئيسية المستخدمة، مع مزاياها وعيوبها.')}
    """)

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('1. Filtration Physique', '1. الفلترة الفيزيائية')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✔️ {translate('Filtres à sable et à charbon actif', 'فلاتر الرمال والفحم النشط')} : {translate('Retiennent les impuretés solides, les bactéries et les produits chimiques (chlore, pesticides).', 'تحتفظ بالشوائب الصلبة والبكتيريا والمواد الكيميائية (الكلور، المبيدات).')}  
        ➖ {translate('Peu efficace contre les virus et certains métaux lourds.', 'غير فعالة ضد الفيروسات وبعض المعادن الثقيلة.')}

        ✔️ {translate('Filtration par membranes', 'الفلترة عبر الأغشية')} ({translate('ultrafiltration', 'التصفية الفائقة')} / {translate('nanofiltration', 'التصفية النانوية')}) : {translate('Bloque les particules et les micro-organismes grâce à des pores extrêmement fins.', 'تمنع الجزيئات والكائنات الدقيقة باستخدام مسام دقيقة للغاية.')}  
        ➖ {translate('Peut nécessiter une pression élevée et un entretien régulier.', 'قد تتطلب ضغطًا عاليًا وصيانة منتظمة.')}
    """)

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('2. Traitement Chimique', '2. المعالجة الكيميائية')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✔️ {translate('Chloration', 'الكلورة')} : {translate('Désinfecte l’eau en éliminant bactéries et virus.', 'يتم تعقيم المياه عن طريق إزالة البكتيريا والفيروسات.')}  
        ➖ {translate('Peut produire des sous-produits nocifs et altérer le goût de l’eau.', 'قد تنتج عنها نواتج جانبية ضارة وتغير طعم المياه.')}

        ✔️ {translate('Ozonation', 'الأوزنة')} : {translate('Oxyde les contaminants organiques et tue les micro-organismes.', 'يؤكسد الملوثات العضوية ويقتل الكائنات الدقيقة.')}  
        ➖ {translate('Méthode coûteuse et l’ozone ne laisse pas de résidu protecteur.', 'طريقة مكلفة والأوزون لا يترك بقايا واقية.')}

        ✔️ {translate('Traitement aux UV', 'المعالجة بالأشعة فوق البنفسجية')} : {translate('Utilise la lumière ultraviolette pour détruire l’ADN des bactéries et virus.', 'يستخدم الضوء فوق البنفسجي لتدمير الحمض النووي للبكتيريا والفيروسات.')}  
        ➖ {translate('Inefficace contre les polluants chimiques et nécessite une eau claire.', 'غير فعالة ضد الملوثات الكيميائية وتتطلب ماءً صافياً.')}
    """)

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('3. Distillation', '3. التقطير')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✔️ {translate('Ébullition et condensation', 'الغليان والتكثيف')} {translate('de l’eau pour éliminer microbes, sels et métaux lourds.', 'من الماء لإزالة الميكروبات والأملاح والمعادن الثقيلة.')}  
        ➖ {translate('Processus lent et énergivore.', 'عملية بطيئة وتستهلك الطاقة.')}
    """)

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('4. Osmose Inverse', '4. التناضح العكسي')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✔️ {translate('Technique très efficace', 'تقنية فعالة للغاية')} {translate('qui utilise une membrane semi-perméable pour éliminer 99 % des contaminants (bactéries, virus, nitrates, métaux lourds).', 
                   'تستخدم غشاء شبه نفاذ لإزالة 99٪ من الملوثات (البكتيريا، الفيروسات، النترات، المعادن الثقيلة).')}  
        ➖ {translate('Nécessite une pression élevée, gaspille une partie de l’eau traitée.', 'تتطلب ضغطًا عاليًا وتضيع جزءًا من المياه المعالجة.')}
    """)

    st.markdown(f"<h3 style='text-align:{text_align};'>{translate('5. Quelle méthode choisir ?', '5. أي طريقة تختار؟')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        💧 {translate('Eau légèrement contaminée', 'ماء ملوث قليلاً')} : {translate('Filtration au charbon actif ou traitement UV.', 'الفلترة باستخدام الفحم النشط أو المعالجة بالأشعة فوق البنفسجية.')}
        
        💧 {translate('Eau polluée par des métaux lourds', 'ماء ملوث بالمعادن الثقيلة')} : {translate('Osmose inverse ou distillation.', 'التناضح العكسي أو التقطير.')}
        
        💧 {translate('Eau de surface avec bactéries et virus', 'ماء سطحي يحتوي على بكتيريا وفيروسات')} : {translate('Ozonation, chloration ou UV.', 'الأوزنة، الكلورة أو الأشعة فوق البنفسجية.')}
        
        {translate('L’association de plusieurs techniques permet souvent d’optimiser la purification pour garantir une eau potable de qualité. 💧✨', 
                   'غالبًا ما يسمح الجمع بين تقنيات متعددة بتحسين عملية التنقية لضمان مياه شرب عالية الجودة. 💧✨')}
    """)
    
    video_url2 = "https://youtu.be/2bTj-vo1tyU?si=-D_Ak60nqCSoWZhR"
    st.video(video_url2)
        
        
# ---- Gestion de l'Eau ----
elif choice == translate("Gestion de l'Eau","إدارة المياه"):

    st.markdown(f"<h1>{translate('Gestion de l\'Eau', 'إدارة المياه')}</h1>", unsafe_allow_html=True)

    st.markdown(f"<h2>{translate('Conservation de l’Eau : Astuces et Bonnes Pratiques 💧🌍', 'حفظ المياه: نصائح وممارسات جيدة 💧🌍')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
        La préservation de l’eau est essentielle pour lutter contre la pénurie et réduire notre empreinte écologique. Voici quelques conseils pratiques pour économiser l’eau à domicile et dans les industries.
    """, """
        الحفاظ على المياه أمر بالغ الأهمية لمكافحة النقص وتقليل بصمتنا البيئية. إليك بعض النصائح العملية لتوفير المياه في المنزل وفي الصناعات.
    """))
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

    st.markdown(f"""
    <table>
      <tr>
        <th>{translate('🏡 À la Maison', '🏡 في المنزل')}</th>
        <th>{translate('🏭 Dans les Industries', '🏭 في الصناعات')}</th>
      </tr>
      <tr>
        <td>
          <b>{translate('Réduction de la Consommation :', 'تقليل الاستهلاك :')}</b><br>
          ✔️ {translate('Fermer le robinet pendant le brossage des dents.', 'إغلاق الصنبور أثناء تنظيف الأسنان.')}<br>
          ✔️ {translate('Douches courtes au lieu de bains.', 'الاستحمام السريع بدلاً من الحمام.')}<br>
          ✔️ {translate('Utiliser des économiseurs d’eau.', 'استخدام موفرات المياه.')}
        </td>
        <td>
          <b>{translate('Amélioration des Procédés :', 'تحسين العمليات :')}</b><br>
          ✔️ {translate('Optimiser l’utilisation de l’eau.', 'تحسين استخدام المياه.')}<br>
          ✔️ {translate('Adopter des technologies propres.', 'اعتماد التكنولوجيا النظيفة.')}
        </td>
      </tr>
      <tr>
        <td>
          <b>{translate('Réutilisation et Recyclage :', 'إعادة الاستخدام وإعادة التدوير :')}</b><br>
          ✔️ {translate('Récupérer l’eau de pluie.', 'جمع مياه الأمطار.')}<br>
          ✔️ {translate('Réutiliser l’eau de cuisson.', 'إعادة استخدام مياه الطهي.')}<br>
          ✔️ {translate('Recycler les eaux grises.', 'إعادة تدوير المياه الرمادية.')}
        </td>
        <td>
          <b>{translate('Réutilisation & Traitement :', 'إعادة الاستخدام والمعالجة :')}</b><br>
          ✔️ {translate('Recycler les eaux industrielles.', 'إعادة تدوير المياه الصناعية.')}<br>
          ✔️ {translate('Systèmes de filtration & recyclage.', 'أنظمة الترشيح وإعادة التدوير.')}
        </td>
      </tr>
      <tr>
        <td>
          <b>{translate('Optimisation des Équipements :', 'تحسين الأجهزة :')}</b><br>
          ✔️ {translate('Choisir des appareils économes.', 'اختيار الأجهزة الاقتصادية.')}<br>
          ✔️ {translate('Réparer les fuites rapidement.', 'إصلاح التسريبات بسرعة.')}
        </td>
        <td>
          <b>{translate('Sensibilisation :', 'التوعية :')}</b><br>
          ✔️ {translate('Former le personnel.', 'تدريب الموظفين.')}<br>
          ✔️ {translate('Suivre la consommation avec capteurs.', 'مراقبة الاستهلاك باستخدام أجهزة الاستشعار.')}
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(f"<h4>{translate('Bénéfices de la Conservation de l’Eau', 'فوائد الحفاظ على المياه')}</h4>", unsafe_allow_html=True)
    st.markdown(translate("""
    ✅ Réduction des factures d’eau.  
    ✅ Protection des ressources naturelles.  
    ✅ Diminution de l’empreinte écologique.
    """, """
    ✅ تقليل فواتير المياه.  
    ✅ حماية الموارد الطبيعية.  
    ✅ تقليل البصمة البيئية.
    """))

    st.markdown(translate("""
    Chacun peut contribuer à la préservation de l’eau en adoptant des gestes simples mais efficaces ! 💙💦
    """, """
    يمكن لكل شخص أن يساهم في الحفاظ على المياه من خلال تبني عادات بسيطة ولكن فعّالة! 💙💦
    """))

    video_url3 = "https://youtu.be/HcMg3ghRfxY?si=kX040aCgkD8BJFgP"
    st.video(video_url3)

    st.markdown(f"<h2>{translate('Gestion Durable des Ressources en Eau 💧🌍', 'إدارة مستدامة للموارد المائية 💧🌍')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
    La gestion efficace de l’eau est essentielle pour préserver cette ressource précieuse face aux défis climatiques et
    à la croissance démographique. Voici des stratégies clés pour une utilisation durable de l’eau.
    """, """
    إن الإدارة الفعّالة للمياه أمر بالغ الأهمية للحفاظ على هذه المورد الثمين في مواجهة التحديات المناخية
    والنمو السكاني. إليك بعض الاستراتيجيات الأساسية للاستخدام المستدام للمياه.
    """))
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

    st.markdown(f"""
    <table>
      <tr>
        <th>{translate('🔹 Collecte et Utilisation des Eaux de Pluie ☔', '🔹 جمع واستخدام مياه الأمطار ☔')}</th>
        <th>{translate('🔹 Recyclage et Réutilisation des Eaux Usées 🔄', '🔹 إعادة تدوير وإعادة استخدام المياه المستعملة 🔄')}</th>
        <th>{translate('🔹 Gestion Intelligente et Optimisation de l’Irrigation 🌾', '🔹 الإدارة الذكية وتحسين الري 🌾')}</th>
        <th>{translate('🔹 Prévention du Gaspillage et Sensibilisation 🏡🏭', '🔹 منع الإسراف والتوعية 🏡🏭')}</th>
      </tr>
      <tr>
        <td>
          <b>{translate('Actions :', 'الإجراءات :')}</b><br>
          ✔ {translate('Installation de citernes et réservoirs pour récupérer l’eau de pluie.', 'تركيب خزانات لالتقاط مياه الأمطار.')}<br>
          ✔ {translate('Filtration et traitement pour un usage domestique (arrosage, lavage, chasse d’eau).', 'الترشيح والمعالجة للاستخدام المنزلي (الري، الغسيل، التخلص من المياه).')}<br>
          ✔ {translate('Intégration dans les bâtiments écologiques pour réduire la consommation d’eau potable.', 'التكامل في المباني البيئية لتقليل استهلاك المياه الصالحة للشرب.')}
        </td>
        <td>
          <b>{translate('Actions :', 'الإجراءات :')}</b><br>
          ✔ {translate('Traitement des eaux grises (eaux de douche, lave-linge) pour l’arrosage ou les toilettes.', 'معالجة المياه الرمادية (مياه الاستحمام، غسالات الملابس) للري أو المراحيض.')}<br>
          ✔ {translate('Réutilisation des eaux industrielles après filtration et purification.', 'إعادة استخدام المياه الصناعية بعد الترشيح والتنقية.')}<br>
          ✔ {translate('Systèmes de filtration avancés (membranes, UV, traitements biologiques).', 'أنظمة ترشيح متقدمة (أغشية، الأشعة فوق البنفسجية، المعالجات البيولوجية).')}
        </td>
        <td>
          <b>{translate('Actions :', 'الإجراءات :')}</b><br>
          ✔ {translate('Utilisation de l’irrigation goutte-à-goutte pour minimiser les pertes d’eau.', 'استخدام الري بالتنقيط لتقليل هدر المياه.')}<br>
          ✔ {translate('Capteurs d’humidité et systèmes automatisés pour ajuster l’arrosage aux besoins réels.', 'أجهزة استشعار الرطوبة وأنظمة آلية لضبط الري حسب الاحتياجات الفعلية.')}<br>
          ✔ {translate('Rotation des cultures et techniques agricoles durables pour préserver les nappes phréatiques.', 'دوران المحاصيل وتقنيات الزراعة المستدامة للحفاظ على المياه الجوفية.')}
        </td>
        <td>
          <b>{translate('Actions :', 'الإجراءات :')}</b><br>
          ✔ {translate('Campagnes de sensibilisation pour encourager une consommation responsable.', 'حملات التوعية لتشجيع الاستهلاك المسؤول.')}<br>
          ✔ {translate('Réglementations et incitations pour les entreprises adoptant des pratiques durables.', 'اللوائح والحوافز للشركات التي تعتمد ممارسات مستدامة.')}<br>
          ✔ {translate('Surveillance des réseaux d’eau pour détecter et réparer rapidement les fuites.', 'مراقبة شبكات المياه لاكتشاف وإصلاح التسريبات بسرعة.')}
        </td>
      </tr>
      <tr>
        <td>
          <b>{translate('✔ Avantages :', '✔ الفوائد :')}</b><br>
          ✔ {translate('Diminue la demande en eau potable et réduit les risques d’inondation urbaine.', 'يقلل من الطلب على المياه الصالحة للشرب ويقلل من مخاطر الفيضانات الحضرية.')}
        </td>
        <td>
          <b>{translate('✔ Avantages :', '✔ الفوائد :')}</b><br>
          ✔ {translate('Réduit le gaspillage et préserve les ressources en eau douce.', 'يقلل من الفاقد ويحافظ على الموارد المائية العذبة.')}
        </td>
        <td>
          <b>{translate('✔ Avantages :', '✔ الفوائد :')}</b><br>
          ✔ {translate('Économie d’eau et augmentation de la productivité agricole.', 'توفير المياه وزيادة الإنتاجية الزراعية.')}
        </td>
        <td>
          <b>{translate('✔ Avantages :', '✔ الفوائد :')}</b><br>
          ✔ {translate('Réduction des pertes d’eau et meilleure gestion des ressources disponibles.', 'تقليل هدر المياه وتحسين إدارة الموارد المتاحة.')}
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2>{translate('🌱Vers un Avenir Durable', '🌱 نحو مستقبل مستدام')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
    En combinant ces stratégies, nous pouvons assurer une gestion efficace de l’eau, protéger l’environnement et garantir un accès équitable à cette ressource essentielle pour les générations futures. 💙💦
    """, """
    من خلال دمج هذه الاستراتيجيات، يمكننا ضمان إدارة فعّالة للمياه، وحماية البيئة، وضمان الوصول العادل لهذه المورد الحيوي للأجيال القادمة. 💙💦
    """))

    video_url4 = "https://youtu.be/a56olKIMiiU?si=mTPxUz2Pt8c2sYqN"
    st.video(video_url4)

    st.markdown(f"<h2>{translate('Politiques et Régulations sur l’Eau 🌍💧', 'سياسات وتنظيمات المياه 🌍💧')}</h2>", unsafe_allow_html=True)

    # General Introduction
    st.markdown(f"""
        {translate("La gestion et la protection des ressources en eau sont encadrées par des régulations locales et internationales visant à garantir un accès équitable à l’eau potable, préserver l’environnement et promouvoir un usage durable.",
                   "إدارة وحماية الموارد المائية تخضع للتنظيمات المحلية والدولية التي تهدف إلى ضمان الوصول العادل إلى المياه الصالحة للشرب، والحفاظ على البيئة، وتعزيز الاستخدام المستدام.")}    
    """)    

    # International Regulations
    st.markdown(f"<h3>{translate('1. Régulations Internationales', '1. التنظيمات الدولية')}</h3>", unsafe_allow_html=True)

    # The UN's Sustainable Development Goals (SDGs)
    st.markdown(f"<h4>{translate('Les Objectifs de Développement Durable (ODD) de l’ONU', 'أهداف التنمية المستدامة (SDGs) للأمم المتحدة')}</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("L’**objectif n°6** vise un accès universel à l’eau potable et à l’assainissement d’ici 2030.",
                   "الهدف **رقم 6** يهدف إلى تحقيق الوصول العالمي إلى المياه الصالحة للشرب والصرف الصحي بحلول عام 2030.")}

        {translate("Encourage la gestion durable des ressources en eau et la réduction des pollutions.",
                   "يحث على الإدارة المستدامة للموارد المائية وتقليل التلوث.")} 
    """)

    # UN Water Convention
    st.markdown(f"<h4>{translate('La Convention de l’ONU sur l’Eau (1992)', 'اتفاقية الأمم المتحدة بشأن المياه (1992)')}</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Promeut la coopération entre pays partageant des ressources en eau transfrontalières.",
                   "تعزز التعاون بين البلدان التي تشترك في الموارد المائية عبر الحدود.")}

        {translate("Encourage la prévention des conflits liés à l’eau.", "تشجع على الوقاية من النزاعات المتعلقة بالمياه.")}  
    """)

    # EU Water Framework Directive
    st.markdown(f"<h4>{translate('La Directive-Cadre sur l’Eau (DCE) de l’Union Européenne (2000)', 'التوجيه الإطاري للمياه (DCE) من الاتحاد الأوروبي (2000)')}</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Vise la protection et la restauration des écosystèmes aquatiques.",
                   "يهدف إلى حماية واستعادة النظم البيئية المائية.")}

        {translate("Implique un suivi régulier de la qualité de l’eau et des restrictions sur les polluants.",
                   "يتطلب متابعة منتظمة لجودة المياه وفرض قيود على الملوثات.")}  
    """)

    # International Agreements and Treaties
    st.markdown(f"<h4>{translate('Accords et Traités Internationaux', 'الاتفاقيات والمعاهدات الدولية')}</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("**Protocole sur l’eau et la santé (OMS/ONU, 1999)** : Garantit l’accès à l’eau potable et à l’assainissement.",
                   "**بروتوكول المياه والصحة (منظمة الصحة العالمية/الأمم المتحدة، 1999)** : يضمن الوصول إلى المياه الصالحة للشرب والصرف الصحي.")}

        {translate("**Convention de Ramsar (1971)** : Protège les zones humides d’importance internationale.",
                   "**اتفاقية رامسار (1971)** : تحمي المناطق الرطبة ذات الأهمية الدولية.")}  
    """)

    # Local Regulations
    st.markdown(f"<h3>{translate('2. Régulations Locales', '2. التنظيمات المحلية')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Chaque pays adopte ses propres lois et règlements pour gérer l’eau. Voici quelques exemples :",
                   "كل بلد يتبنى قوانينه الخاصة لإدارة المياه. إليك بعض الأمثلة :")}

        - {translate("**Loi sur l’eau et l’assainissement** : Régit la distribution et la qualité de l’eau potable.",
                     "**قانون المياه والصرف الصحي** : ينظم توزيع وجودة المياه الصالحة للشرب.")}

        - {translate("**Normes de qualité de l’eau potable** : Fixent les seuils de contaminants autorisés.",
                     "**معايير جودة المياه الصالحة للشرب** : تحدد حدود الملوثات المسموح بها.")}

        - {translate("**Régulations sur le traitement des eaux usées** : Imposent aux industries et municipalités de traiter leurs rejets.",
                     "**التنظيمات المتعلقة بمعالجة مياه الصرف الصحي** : تفرض على الصناعات والبلديات معالجة تصريفاتهم.")}

        - {translate("**Politiques de tarification de l’eau** : Encouragent une consommation responsable par des tarifs progressifs.",
                     "**سياسات تسعير المياه** : تشجع على استهلاك مسؤول من خلال التعريفات التدريجية.")}

        {translate("Les gouvernements locaux peuvent aussi imposer des restrictions d’usage en cas de sécheresse ou promouvoir des incitations financières pour l’installation de systèmes d’économie d’eau.",
                   "يمكن للحكومات المحلية أيضًا فرض قيود على استخدام المياه في حالات الجفاف أو تعزيز الحوافز المالية لتركيب أنظمة لتوفير المياه.")} 
    """)

    # Impact of Regulations
    st.markdown(f"<h3>{translate('3. Impact des Régulations sur la Gestion de l’Eau', '3. تأثير التنظيمات على إدارة المياه')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✅ {translate('Protection de la santé publique en garantissant une eau potable conforme aux normes.',
                      'حماية الصحة العامة من خلال ضمان مياه صالحة للشرب وفقًا للمعايير.')}

        ✅ {translate('Préservation des ressources naturelles en limitant la pollution et la surexploitation.',
                      'حماية الموارد الطبيعية من خلال الحد من التلوث والاستغلال المفرط.')}

        ✅ {translate('Encouragement des innovations en matière de traitement et de recyclage des eaux.',
                      'تشجيع الابتكارات في معالجة المياه وإعادة تدويرها.')}

        ✅ {translate('Coopération internationale pour résoudre les conflits liés à l’eau.',
                      'التعاون الدولي لحل النزاعات المتعلقة بالمياه.')}

    """)

    # Global Commitment
    st.markdown(f"<h2>{translate('🌍 Un Engagement Mondial pour une Eau Saine et Durable', '🌍 التزام عالمي من أجل مياه صحية ومستدامة')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Les politiques et régulations jouent un rôle clé dans la gestion de l’eau. Il est essentiel de renforcer leur application et d’encourager les initiatives locales pour assurer un accès équitable et durable à cette ressource vitale. 💙💦",
                   "تلعب السياسات والتنظيمات دورًا أساسيًا في إدارة المياه. من الضروري تعزيز تطبيقها وتشجيع المبادرات المحلية لضمان الوصول العادل والمستدام إلى هذه المورد الحيوي. 💙💦")}
    """)

    # Video Link
    video_url5 = "https://youtu.be/PteEKDGEFfI?si=gykDmGRjkVBdeATs"
    st.video(video_url5)
    
# ---- Technologies et Innovations ----
elif choice == translate("Technologies et Innovations","التقنيات والابتكارات"):
    st.markdown(f"<h1>{translate('Technologies et Innovations', 'التقنيات والابتكارات')}</h1>", unsafe_allow_html=True)

    st.markdown(f"<h2>{translate('Technologies de Surveillance de l’Eau 💧🔬', 'تقنيات مراقبة المياه 💧🔬')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("La surveillance de la qualité de l’eau est essentielle pour détecter les polluants, prévenir les risques sanitaires et optimiser la gestion des ressources hydriques. Grâce aux avancées technologiques, de nouveaux outils permettent un suivi en temps réel et une analyse plus précise.",
                   "مراقبة جودة المياه أمر أساسي للكشف عن الملوثات، والوقاية من المخاطر الصحية، وتحسين إدارة الموارد المائية. بفضل التقدم التكنولوجي، توفر الأدوات الجديدة مراقبة في الوقت الفعلي وتحليلًا أكثر دقة.")}
    """)

    st.markdown(f"<h3>{translate('1. Capteurs Intelligents pour la Qualité de l’Eau', '1. أجهزة الاستشعار الذكية لجودة المياه')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Les capteurs modernes permettent de mesurer divers paramètres en temps réel, sans nécessiter d’analyse en laboratoire.",
                   "تتيح أجهزة الاستشعار الحديثة قياس مختلف المعايير في الوقت الفعلي دون الحاجة إلى تحليل في المختبر.")}

        ✔ {translate('Capteurs électrochimiques : Mesurent le pH, l’oxygène dissous, les nitrates et les métaux lourds.',
                      'أجهزة الاستشعار الكهروكيميائية: تقيس درجة الحموضة، والأوكسجين المذاب، والنترات، والمعادن الثقيلة.')}

        ✔ {translate('Capteurs optiques (fluorescence, spectroscopie UV-Vis) : Détectent les matières organiques, les hydrocarbures et les polluants chimiques.',
                      'أجهزة الاستشعار البصرية (التألق، الطيف الضوئي UV-Vis): تكشف عن المواد العضوية، والهيدروكربونات، والملوثات الكيميائية.')}

        ✔ {translate('Capteurs microbiologiques : Identifient la présence de bactéries et virus grâce à des biocapteurs spécifiques.',
                      'أجهزة الاستشعار الميكروبيولوجية: تحدد وجود البكتيريا والفيروسات باستخدام مستشعرات حيوية محددة.')}

        📌 {translate('Exemple d’innovation : Des capteurs autonomes à base de graphène, capables de détecter des contaminants à très faible concentration.',
                      'مثال على الابتكار: أجهزة استشعار مستقلة تعتمد على الجرافين، قادرة على اكتشاف الملوثات بتركيز منخفض للغاية.')}
    """)

    st.markdown(f"<h3>{translate('2. Surveillance en Temps Réel avec l’IoT et l’IA', '2. المراقبة في الوقت الفعلي باستخدام إنترنت الأشياء والذكاء الاصطناعي')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate('L’Internet des objets (IoT) et l’intelligence artificielle (IA) révolutionnent la gestion de l’eau en permettant une surveillance continue et automatisée.',
                   'تحدث تقنيات إنترنت الأشياء (IoT) والذكاء الاصطناعي (AI) ثورة في إدارة المياه من خلال تمكين المراقبة المستمرة والمتحكم بها.')}

        ✔ {translate('Stations de surveillance connectées : Collectent et transmettent les données en temps réel.',
                      'محطات المراقبة المتصلة: تجمع البيانات وتنقلها في الوقت الفعلي.')}

        ✔ {translate('Algorithmes d’IA : Analysent les tendances pour détecter rapidement une pollution.',
                      'الخوارزميات الذكية: تحلل الاتجاهات لاكتشاف التلوث بسرعة.')}

        ✔ {translate('Applications mobiles : Permettent aux gestionnaires d’eau de recevoir des alertes instantanées en cas de contamination.',
                      'التطبيقات المحمولة: تمكّن مديري المياه من تلقي التنبيهات الفورية في حالة التلوث.')}

        📌 {translate('Exemple d’innovation : Des drones équipés de capteurs capables de cartographier la pollution dans les rivières et les lacs.',
                      'مثال على الابتكار: طائرات مسيرة مزودة بمستشعرات قادرة على رسم خريطة للتلوث في الأنهار والبحيرات.')}
    """)

    st.markdown(f"<h3>{translate('3. Technologie de Télé-détection et Satellites', '3. تكنولوجيا الاستشعار عن بعد والأقمار الصناعية')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Les satellites et drones offrent une vue d’ensemble des ressources en eau et aident à la détection des anomalies.",
                   "تقدم الأقمار الصناعية والطائرات بدون طيار رؤية شاملة للموارد المائية وتساعد في اكتشاف الشوائب.")}

        ✔ {translate('Télédétection par satellite : Suivi des algues toxiques, pollution et niveau des nappes phréatiques.',
                      'الاستشعار عن بعد بواسطة الأقمار الصناعية: متابعة الطحالب السامة، التلوث، ومستوى المياه الجوفية.')}

        ✔ {translate('Drones aquatiques : Équipés de capteurs, ils analysent la qualité de l’eau dans des zones difficiles d’accès.',
                      'الطائرات المائية بدون طيار: مزودة بمستشعرات، تقوم بتحليل جودة المياه في المناطق التي يصعب الوصول إليها.')}

        ✔ {translate('Modélisation hydrologique : Utilise l’imagerie satellite pour prédire les sécheresses et les inondations.',
                      'النمذجة الهيدرولوجية: تستخدم التصوير الفضائي للتنبؤ بالجفاف والفيضانات.')}

        📌 {translate("Exemple d’innovation : Le satellite Sentinel-2 de l’ESA permet de surveiller la pollution des eaux en détectant les variations de couleur et de turbidité.",
                       "مثال على الابتكار: القمر الصناعي Sentinel-2 من وكالة الفضاء الأوروبية يسمح بمراقبة تلوث المياه من خلال اكتشاف التغيرات في اللون والعكارة.")}
    """)

    st.markdown(f"<h3>{translate('4. Avantages des Nouvelles Technologies', '4. فوائد التقنيات الجديدة')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
        ✔ {translate('Détection rapide et précoce des contaminants.',
                      'الكشف السريع والمبكر عن الملوثات.')}

        ✔ {translate('Réduction des coûts d’analyse en laboratoire.',
                      'تقليل تكاليف التحليل في المختبر.')}

        ✔ {translate('Optimisation de la gestion de l’eau pour prévenir les crises.',
                      'تحسين إدارة المياه لمنع الأزمات.')}

        ✔ {translate('Meilleure accessibilité aux données pour les gouvernements et le public.',
                      'تحسين الوصول إلى البيانات للحكومات والجمهور.')}
    """)

    st.markdown(f"<h2>{translate('🌍 Vers une Eau Plus Propre et Sécurisée', '🌍 نحو مياه أنظف وأكثر أمانًا')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Grâce aux avancées en capteurs intelligents, IoT et télédétection, la surveillance de l’eau devient plus efficace et accessible. Ces technologies permettent une gestion proactive des ressources en eau et contribuent à garantir une eau potable de qualité pour tous. 💙💦",
                   "بفضل التقدم في أجهزة الاستشعار الذكية، وإنترنت الأشياء، والاستشعار عن بُعد، أصبحت مراقبة المياه أكثر كفاءة وقابلية للوصول. هذه التقنيات تسمح بإدارة استباقية للموارد المائية وتساهم في ضمان مياه شرب ذات جودة للجميع. 💙💦")}
    """)

    video_url6 = "https://youtu.be/gBszA9CyH-I?si=nu9kX4fGDvWW1061"
    st.video(video_url6)

    st.markdown(f"<h2>{translate('Robots pour la Surveillance de l’Eau 🤖💧', 'الروبوتات لمراقبة المياه 🤖💧')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate("Les robots jouent un rôle de plus en plus important dans la surveillance de la qualité de l’eau. Grâce à leurs capteurs avancés et à leur capacité d’exploration autonome, ils permettent un suivi précis des rivières, lacs et réservoirs, contribuant ainsi à la protection des ressources en eau.",
                   "تتزايد أهمية الروبوتات في مراقبة جودة المياه. بفضل مستشعراتها المتقدمة وقدرتها على الاستكشاف الذاتي، توفر متابعة دقيقة للأنهار والبحيرات والخزانات، مما يساهم في حماية الموارد المائية.")}
    """)

    st.markdown(f"<h3>{translate('1. Types de Robots de Surveillance Aquatique', '1. أنواع الروبوتات لمراقبة المياه')}</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background-color: white;
    }}
    th, td {{
        border: 1px solid #cccccc;
        padding: 10px;
        text-align: left;
        vertical-align: top;
        font-size: 16px;
    }}
    th {{
        background-color: #e6f2ff;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <table>
      <tr>
        <th>🤖 {translate('Type de Robot', 'نوع الروبوت')}</th>
        <th>🛠 {translate('Description et Utilisations', 'الوصف والاستخدامات')}</th>
      </tr>
      <tr>
        <td><b>🔹 {translate('Robots Sous-marins (AUV)', 'روبوتات تحت الماء (AUV)')}</b><br>({translate('Autonomous Underwater Vehicles', 'المركبات تحت الماء الذاتية')})</td>
        <td>
          ✔️ {translate('Capables de plonger et d’analyser les eaux profondes.', 'قادرة على الغطس وتحليل المياه العميقة.')}<br>
          ✔️ {translate('Mesurent la température, la salinité, l’oxygène dissous et les polluants chimiques.', 'تقيس درجة الحرارة، والملوحة، والأوكسجين المذاب، والملوثات الكيميائية.')}<br>
          ✔️ {translate('Utilisés pour surveiller la pollution industrielle et les marées noires.', 'تستخدم لمراقبة التلوث الصناعي والتسربات النفطية.')}<br>
          📌 <b>{translate('Exemple', 'مثال')} :</b> {translate('Le robot "AquaBOT", utilisé pour détecter les fuites toxiques et la prolifération d’algues.', 'الروبوت "AquaBOT"، المستخدم لاكتشاف التسربات السامة وتكاثر الطحالب.')}
        </td>
      </tr>
      <tr>
        <td><b>🔹 {translate('Robots de Surface (ASV)', 'روبوتات السطح (ASV)')}</b><br>({translate('Autonomous Surface Vehicles', 'المركبات السطحية الذاتية')})</td>
        <td>
          ✔️ {translate('Naviguent à la surface des rivières et des lacs.', 'تبحر على سطح الأنهار والبحيرات.')}<br>
          ✔️ {translate('Équipés de capteurs pour analyser le pH, la turbidité, les nitrates et les hydrocarbures.', 'مجهزة بأجهزة استشعار لتحليل الرقم الهيدروجيني، العكارة، النترات والهيدروكربونات.')}<br>
          ✔️ {translate('Peuvent transmettre des données en temps réel via satellite ou Wi-Fi.', 'يمكنها إرسال البيانات في الوقت الفعلي عبر الأقمار الصناعية أو الواي فاي.')}<br>
          📌 <b>{translate('Exemple', 'مثال')} :</b> {translate('Le robot "Envirobot", développé pour détecter la pollution de l’eau grâce à des capteurs biochimiques.', 'الروبوت "Envirobot"، الذي تم تطويره لاكتشاف تلوث المياه باستخدام أجهزة استشعار بيولوجية كيميائية.')}
        </td>
      </tr>
      <tr>
        <td><b>🔹 {translate('Drones Aquatiques', 'الطائرات بدون طيار المائية')}</b></td>
        <td>
          ✔️ {translate('Volent au-dessus des plans d’eau pour cartographier la pollution.', 'تحلق فوق المسطحات المائية لرسم خرائط التلوث.')}<br>
          ✔️ {translate('Équipés de caméras thermiques et de capteurs optiques pour surveiller les algues toxiques.', 'مجهزة بكاميرات حرارية وأجهزة استشعار بصرية لمراقبة الطحالب السامة.')}<br>
          ✔️ {translate('Idéals pour les grandes surfaces, comme les réservoirs et les océans.', 'مثالية للأسطح الكبيرة مثل الخزانات والمحيطات.')}<br>
          📌 <b>{translate('Exemple', 'مثال')} :</b> {translate('Les drones de la NASA utilisés pour surveiller la qualité de l’eau des Grands Lacs aux États-Unis.', 'طائرات بدون طيار تابعة لناسا تستخدم لمراقبة جودة المياه في البحيرات الكبرى في الولايات المتحدة.')}
        </td>
      </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(f"<h3>2. {translate('Fonctionnement et Technologies Utilisées', 'آلية العمل والتقنيات المستخدمة')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
         ✔ {translate('Capteurs embarqués : Mesurent la qualité de l’eau en temps réel (métaux lourds, bactéries, pesticides).', 'أجهزة استشعار مدمجة: تقيس جودة المياه في الوقت الفعلي (المعادن الثقيلة، البكتيريا، المبيدات).')}

         ✔ {translate('Intelligence Artificielle (IA) : Analyse les données et détecte les anomalies.', 'الذكاء الصناعي (AI): يحلل البيانات ويكتشف الشذوذ.')}
         
         ✔ {translate('Systèmes autonomes : Les robots peuvent ajuster leur parcours en fonction des besoins.', 'الأنظمة الذاتية: يمكن للروبوتات تعديل مسارها حسب الحاجة.')}
         
         ✔ {translate('Communication en temps réel : Transmission des données aux chercheurs et autorités via des réseaux sans fil.', 'الاتصال في الوقت الفعلي: إرسال البيانات إلى الباحثين والسلطات عبر الشبكات اللاسلكية.')}
    """)

    st.markdown(f"<h3>3. {translate('Avantages de l’Utilisation des Robots', 'فوائد استخدام الروبوتات')}</h3>", unsafe_allow_html=True)
    st.markdown(f"""
     ✅ {translate('Surveillance continue : Fonctionnent 24h/24 sans intervention humaine.', 'مراقبة مستمرة: تعمل على مدار 24 ساعة يومياً دون تدخل بشري.')}

     ✅ {translate('Précision des mesures : Détection de polluants à très faible concentration.', 'دقة القياسات: اكتشاف الملوثات بتركيزات منخفضة جداً.')}

     ✅ {translate('Exploration des zones inaccessibles : Surveillance des eaux profondes et contaminées.', 'استكشاف المناطق التي يصعب الوصول إليها: مراقبة المياه العميقة والملوثة.')}

     ✅ {translate('Réduction des coûts : Moins de besoins en échantillonnage manuel et en analyses en laboratoire.', 'خفض التكاليف: الحاجة أقل إلى أخذ العينات يدوياً وتحليلها في المختبر.')}
    """)

    st.markdown(f"<h3>4. {translate('Applications Pratiques', 'التطبيقات العملية')}</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        {translate('Surveillance des marées noires : Détection des hydrocarbures et aide au nettoyage.', 'مراقبة التسربات النفطية: اكتشاف الهيدروكربونات والمساعدة في التنظيف.')}

        {translate('Contrôle de la pollution agricole : Mesure des nitrates et phosphates provenant des engrais.', 'مراقبة التلوث الزراعي: قياس النترات والفوسفات القادمة من الأسمدة.')}

        {translate('Prévention des crises sanitaires : Détection rapide de contaminants dangereux.', 'الوقاية من الأزمات الصحية: الكشف السريع عن الملوثات الضارة.')}

        {translate('Gestion des écosystèmes aquatiques : Suivi des populations de poissons et des niveaux d’oxygène.', 'إدارة النظم البيئية المائية: متابعة أعداد الأسماك ومستويات الأوكسجين.')}
    """)

    st.markdown(f"<h2>🌍 {translate('Vers une Surveillance de l’Eau Plus Intelligente', 'نحو مراقبة مياه أكثر ذكاء')}</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        {translate('L’utilisation de robots révolutionne la surveillance de l’eau, rendant les analyses plus rapides, précises et accessibles. Grâce à ces technologies, nous pouvons mieux protéger nos ressources en eau et réagir rapidement aux menaces environnementales. 💙🤖💦', 'استخدام الروبوتات يغير مراقبة المياه، مما يجعل التحليلات أسرع وأكثر دقة وقابلية للوصول. بفضل هذه التقنيات، يمكننا حماية مواردنا المائية بشكل أفضل والاستجابة بسرعة للتهديدات البيئية. 💙🤖💦')}
    """)

    video_url7 = "https://youtu.be/ljsuGRiz0As?si=h8kR0xfjCTGGtlfN"
    st.video(video_url7)

    video_url8 = "https://youtu.be/KfrtsR-MYl0?si=dbe5XIDVDsmtTJVH"
    st.video(video_url8)

    st.markdown(f"<h2>{translate('💡Projets Innovants dans le Domaine de l’Eau', '💡المشاريع المبتكرة في مجال المياه')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
        Face aux défis de la pénurie d’eau et de la pollution, plusieurs projets innovants ont été développés pour améliorer l’accès à une eau propre et potable. Voici quelques exemples inspirants de technologies révolutionnaires dans le domaine de l’eau. 💧
    """, """
        في مواجهة تحديات نقص المياه والتلوث، تم تطوير العديد من المشاريع المبتكرة لتحسين الوصول إلى مياه نظيفة وصالحة للشرب. إليكم بعض الأمثلة الملهمة للتقنيات الثورية في مجال المياه. 💧
    """))

    st.markdown(f"<h3>1. {translate('Systèmes de Désalinisation Avancés', 'أنظمة التحلية المتقدمة')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
        🔹 **The Solar Dome** *(Arabie Saoudite)*  
        Utilise l’énergie solaire pour désaliniser l’eau de mer de manière écologique.  
        Réduit de 30% les coûts énergétiques par rapport aux méthodes classiques.  
        Une solution prometteuse pour les pays arides.

        🔹 **Graphene-Based Desalination** *(MIT, États-Unis)*  
        Utilise des membranes de graphène pour filtrer le sel avec une efficacité accrue.  
        Réduit la consommation d’énergie par rapport aux techniques traditionnelles d’osmose inverse.  
        Peut fournir de l’eau potable aux régions côtières souffrant de sécheresse.
    """, """
        🔹 **The Solar Dome** *(السعودية)*  
        يستخدم الطاقة الشمسية لتحلية مياه البحر بشكل بيئي.  
        يقلل من التكاليف الطاقية بنسبة 30% مقارنة بالطرق التقليدية.  
        حل واعد للدول الجافة.

        🔹 **Graphene-Based Desalination** *(معهد ماساتشوستس للتكنولوجيا، الولايات المتحدة)*  
        يستخدم أغشية الجرافين لفصل الملح بفعالية أكبر.  
        يقلل من استهلاك الطاقة مقارنة بتقنيات التناضح العكسي التقليدية.  
        يمكنه توفير مياه شرب للمناطق الساحلية التي تعاني من الجفاف.
    """))

    st.markdown(f"<h3>2. {translate('Machines de Purification d’Eau Portables', 'أجهزة تنقية المياه المحمولة')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
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
    """, """
        🔹 **LifeStraw** *(سويسرا)*  
        مصاصة فلترية قادرة على القضاء على 99.9% من البكتيريا والطفيليات.  
        مثالية للمناطق الريفية وحالات الطوارئ.  
        تسمح للشخص بشرب ما يصل إلى 4000 لتر من المياه الملوثة بأمان.

        🔹 **The Drinkable Book** *(الولايات المتحدة)*  
        كتاب يحتوي على صفحات بها فلاتر مضادة للبكتيريا.  
        كل صفحة يمكنها تنقية 100 لتر من الماء، مما يعني أن الكتاب يكفي لمدة 4 سنوات من المياه الصالحة للشرب.  
        حل اقتصادي وتعليمي للسكان المحرومين.

        🔹 **Desolenator** *(المملكة المتحدة)*  
        وحدة تنقية تعمل بالطاقة الشمسية بنسبة 100%.  
        تحول مياه البحر إلى مياه شرب دون الحاجة إلى فلاتر مكلفة.  
        يمكنها إنتاج 15 لترًا من المياه النقية يوميًا، مما يجعلها مثالية للقرى المعزولة.
    """))

    st.markdown(f"<h3>3. {translate('Systèmes de Collecte et de Recyclage de l’Eau', 'أنظمة جمع وإعادة تدوير المياه')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
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
    """, """
        🔹 **Skywater** *(الولايات المتحدة)*  
        جهاز يحول الرطوبة في الهواء إلى مياه صالحة للشرب.  
        يمكنه إنتاج ما يصل إلى 5000 لتر من الماء يوميًا في المناخات الرطبة.  
        يُستخدم في الإغاثة الإنسانية والقواعد العسكرية في المناطق الجافة.

        🔹 **WaterSeer** *(الولايات المتحدة)*  
        جهاز مستقل يمسك الماء من الهواء باستخدام توربين هوائي.  
        يعمل بدون كهرباء ويمكنه توفير ما يصل إلى 37 لترًا من الماء يوميًا.  
        حل مستدام للمجتمعات الريفية.

        🔹 **Hydraloop** *(هولندا)*  
        نظام منزلي لإعادة تدوير المياه الرمادية (الدش، غسالات الملابس).  
        يقلل من استهلاك المياه بنسبة 45% في المنازل.  
        متوافق مع المنازل والمباني البيئية.
    """))

    st.markdown(f"<h3>4. {translate('Robots et Drones pour la Surveillance et le Nettoyage des Eaux', 'الروبوتات والطائرات بدون طيار لمراقبة وتنظيف المياه')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
        🔹 **WasteShark** *(Pays-Bas)*  
        Robot flottant capable de collecter les déchets plastiques dans les rivières et ports.  
        Fonctionne de manière autonome et réduit la pollution avant qu’elle n’atteigne les océans.

        🔹 **SEABIN Project** *(Australie)*  
        Une poubelle flottante qui aspire les déchets et les microplastiques à la surface de l’eau.  
        Déjà installée dans plus de 50 pays pour nettoyer les ports et marinas.

        🔹 **Nereus Drone** *(France)*  
        Drone sous-marin équipé de capteurs pour analyser la pollution des eaux en temps réel.  
        Utilisé pour la surveillance des rivières, lacs et stations d’épuration.
    """, """
        🔹 **WasteShark** *(هولندا)*  
        روبوت عائم قادر على جمع النفايات البلاستيكية في الأنهار والموانئ.  
        يعمل بشكل مستقل ويقلل من التلوث قبل أن يصل إلى المحيطات.

        🔹 **SEABIN Project** *(أستراليا)*  
        سلة مهملات عائمة تمتص النفايات والميكروبلاستيك على سطح المياه.  
        تم تركيبها في أكثر من 50 دولة لتنظيف الموانئ والمراسي.

        🔹 **Nereus Drone** *(فرنسا)*  
        طائرة بدون طيار تحت الماء مجهزة بأجهزة استشعار لتحليل تلوث المياه في الوقت الفعلي.  
        تستخدم لمراقبة الأنهار والبحيرات ومحطات معالجة المياه.
    """))

    st.markdown(f"<h2>{translate('🌍 Vers un Avenir Plus Durable', '🌍 نحو مستقبل أكثر استدامة')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
        Ces innovations montrent que la technologie peut jouer un rôle clé dans la préservation et l’accessibilité de l’eau. Grâce à ces projets, nous pouvons réduire la pollution, économiser les ressources et offrir de l’eau potable aux populations les plus vulnérables. 💙💦
    """, """
        تظهر هذه الابتكارات أن التكنولوجيا يمكن أن تلعب دورًا رئيسيًا في الحفاظ على المياه وجعلها في متناول الجميع. من خلال هذه المشاريع، يمكننا تقليل التلوث، وتوفير الموارد، وتقديم مياه صالحة للشرب للسكان الأكثر ضعفًا. 💙💦
    """))

    video_url9 = "https://youtu.be/zyjEX3MTcWw?si=tj6-XsvYmYFKt1xG"
    st.video(video_url9)
# ---- Impact Environnemental ----
elif choice == translate("Impact Environnemental",'الأثر البيئي'):
    st.markdown(f"<h1>{translate('Impact Environnemental', 'الأثر البيئي')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2>{translate('Effets du Changement Climatique sur l’Eau💧', 'آثار التغير المناخي على المياه💧')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
    Le changement climatique bouleverse les ressources en eau à travers le monde. Il modifie sa **disponibilité**, **sa qualité** et augmente la fréquence des **catastrophes hydriques**, avec de lourdes conséquences sur la santé, l’agriculture et les écosystèmes.
    """, """
    يغير التغير المناخي الموارد المائية حول العالم. إنه يعدل **توفرها** و **جودتها** ويزيد من تكرار **الكوارث المائية**، مما يؤدي إلى عواقب وخيمة على الصحة والزراعة والنظم البيئية.
    """))

    st.markdown(f"<h3>{translate('1. Réduction de la Disponibilité de l’Eau🚱', '1. تقليص توفر المياه🚱')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
    -**Sécheresses Plus Fréquentes et Intenses**  
    Hausse des températures = évaporation plus rapide + sols asséchés.  
    Baisse des nappes phréatiques, fleuves asséchés, moins d’eau potable.  
    *Exemple :* En **Californie**, l’agriculture souffre de sécheresses records.
    """, """
    -**الجفاف المتكرر والأكثر شدة**  
    زيادة درجات الحرارة = تبخر أسرع + تربة جافة.  
    انخفاض مستويات المياه الجوفية، الأنهار الجافة، مياه شرب أقل.  
    *مثال:* في **كاليفورنيا**، يعاني الزراعة من جفاف غير مسبوق.
    """))

    st.markdown(f"<h3>{translate('2. Inondations et Catastrophes Hydriques🌊🌪', '2. الفيضانات والكوارث المائية🌊🌪')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
    -**Précipitations Extrêmes et Crues Subites**  
    Plus de pluie + sols secs = inondations plus violentes.  
    Dommages aux infrastructures, contamination de l’eau.  
    📌 *Exemple :* En **Allemagne** et **Belgique** (2021), des pluies extrêmes ont causé des inondations dramatiques.
    """, """
    -**هطول الأمطار الغزيرة والفيضانات المفاجئة**  
    المزيد من الأمطار + التربة الجافة = فيضانات أكثر عنفًا.  
    تضرر البنية التحتية، تلوث المياه.  
    📌 *مثال:* في **ألمانيا** و **بلجيكا** (2021)، تسببت الأمطار الغزيرة في فيضانات كارثية.
    """))

    st.markdown(f"<h3>{translate('3. Dégradation de la Qualité de l’Eau🦠☣️', '3. تدهور جودة المياه🦠☣️')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
    -**Pollution Accrue des Sources d’Eau**  
    Températures + pollution = prolifération d’algues toxiques, égouts débordés.  
    Risques accrus de métaux lourds et bactéries.  
    📌 *Exemple :* Le **Lac Érié** (États-Unis) subit des pics d’algues toxiques.
    """, """
    -**التلوث المتزايد لمصادر المياه**  
    درجات الحرارة + التلوث = تكاثر الطحالب السامة، والصرف الصحي المتدفق.  
    زيادة مخاطر المعادن الثقيلة والبكتيريا.  
    📌 *مثال:* **بحيرة إيري** (الولايات المتحدة) تشهد ارتفاعات في الطحالب السامة.
    """))

    st.markdown(f"<h3>{translate('4. Impacts sur la Santé et l’Agriculture🌾', '4. التأثيرات على الصحة والزراعة🌾')}</h3>", unsafe_allow_html=True)
    st.markdown(translate("""
    -**Hausse des Maladies Liées à l’Eau**  
    Chaleur et humidité favorisent choléra, dysenterie, parasites.  
    Accès difficile à une eau potable saine.  
    📌 *Exemple :* En **Afrique de l’Ouest**, les épidémies de choléra sont en hausse.
    """, """
    -**زيادة الأمراض المتعلقة بالمياه**  
    الحرارة والرطوبة تعزز الكوليرا، الإسهال، والطفيليات.  
    صعوبة الوصول إلى مياه صالحة للشرب.  
    📌 *مثال:* في **غرب أفريقيا**، ترتفع حالات وباء الكوليرا.
    """))

    st.markdown(f"<h2>{translate('🌍Vers des Solutions Durables', '🌍نحو حلول مستدامة')}</h2>", unsafe_allow_html=True)
    st.markdown(translate("""
    ✅ Gestion plus efficace de l’eau (recyclage, irrigation goutte-à-goutte).
    
    ✅ Technologies de dessalement et purification pour compenser la raréfaction de l’eau douce.
    
    ✅ Politiques d’adaptation et d’atténuation pour limiter l’impact du changement climatique.
    
    ✅ Protection des écosystèmes aquatiques pour préserver les ressources naturelles.
    
    Le changement climatique transforme notre relation avec l’eau. Des actions rapides et innovantes sont nécessaires pour protéger cette ressource vitale pour l’avenir de l’humanité. 💙💦
    """, """
    ✅ إدارة المياه بشكل أكثر فعالية (إعادة التدوير، الري بالتنقيط).
    
    ✅ تقنيات تحلية المياه والتنقية لتعويض نقص المياه العذبة.
    
    ✅ سياسات التكيف والتخفيف للحد من تأثيرات التغير المناخي.
    
    ✅ حماية النظم البيئية المائية للحفاظ على الموارد الطبيعية.
    
    التغير المناخي يغير علاقتنا بالمياه. من الضروري اتخاذ إجراءات سريعة ومبتكرة لحماية هذه المورد الحيوي من أجل مستقبل الإنسانية. 💙💦
    """))

    st.video("https://youtu.be/LpSVRqYJP1g?si=swknl0Bp920Qfmbr")
    st.video("https://youtu.be/T4LVXCCmIKA?si=nazGSQJ0OHhVrjBc")

    st.markdown(translate(
        "<h2>Biodiversité Aquatique et Impacts de la Pollution de l’Eau 🌍🐟💧</h2>", 
        "<h2>التنوع البيولوجي المائي وتأثيرات تلوث المياه 🌍🐟💧</h2>"
    ), unsafe_allow_html=True)
    
    st.markdown(translate("""
        La biodiversité aquatique englobe l’ensemble des organismes vivants qui habitent les milieux aquatiques (rivières, lacs, océans, zones humides).  
        Ces écosystèmes jouent un rôle crucial dans le maintien de l’équilibre écologique, mais sont de plus en plus menacés par la pollution de l’eau.
    """, """
        يشمل التنوع البيولوجي المائي جميع الكائنات الحية التي تعيش في البيئات المائية (الأنهار، البحيرات، المحيطات، المناطق الرطبة).  
        تلعب هذه النظم البيئية دورًا حيويًا في الحفاظ على التوازن البيئي، ولكنها مهددة بشكل متزايد بسبب تلوث المياه.
    """), unsafe_allow_html=True)

    st.markdown(translate("<h3>1.La Biodiversité Aquatique 🌿🐠</h3>", "<h3>1.التنوع البيولوجي المائي 🌿🐠</h3>"), unsafe_allow_html=True)

    st.markdown("<h4>Les Écosystèmes Aquatiques</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - **Récifs Coralliens** : Habitats marins riches en biodiversité, abritant plus de 25% des espèces marines.
                          
        - **Zones Humides** : Cruciales pour la reproduction de nombreuses espèces d\'oiseaux, poissons et amphibiens.
                          
        - **Rivières et Lacs d’eau Douce** : Source d’eau potable et habitat pour de nombreuses espèces comme les poissons, insectes aquatiques et plantes.
    """, """
        - **الشعاب المرجانية**: بيئات بحرية غنية بالتنوع البيولوجي، تأوي أكثر من 25% من الأنواع البحرية.
        
        - **المناطق الرطبة**: ضرورية لتكاثر العديد من أنواع الطيور والأسماك والبرمائيات.
        
        - **الأنهار والبحيرات العذبة**: مصدر للمياه الصالحة للشرب وموائل للعديد من الأنواع مثل الأسماك والحشرات المائية والنباتات.
    """), unsafe_allow_html=True)

    st.markdown("<h4>Les Espèces Aquatiques</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - Poissons (exza. : saumons, thons, poissons tropicaux)
                          
        - Plantes aquatiques (ex. : nénuphars, algues)
                          
        - Invertébrés aquatiques (ex. : moules, crustacés, larves d’insectes)
                          
        - Mammifères marins (ex. : baleines, dauphins)
                          
        - Reptiles aquatiques (ex. : tortues marines)
                          
        Ces espèces sont essentielles à l’équilibre des chaînes alimentaires et à la régulation des cycles des nutriments.
    """, """
        - الأسماك (مثل: السلمون، التونة، الأسماك الاستوائية)
                          
        - النباتات المائية (مثل: زنابق الماء، الطحالب)
                          
        - اللافقاريات المائية (مثل: المحار، القشريات، يرقات الحشرات)
                          
        - الثدييات البحرية (مثل: الحيتان، الدلافين)
                          
        - الزواحف المائية (مثل: السلاحف البحرية)
                          
        هذه الأنواع أساسية في توازن السلاسل الغذائية وتنظيم دورات المغذيات.
    """), unsafe_allow_html=True)

    st.markdown(translate("<h3>2.Les Effets de la Pollution de l’Eau sur la Biodiversité Aquatique 🏭💔</h3>", "<h3>2.آثار تلوث المياه على التنوع البيولوجي المائي 🏭💔</h3>"), unsafe_allow_html=True)

    st.markdown("<h4>Pollution Chimique</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - **Bioaccumulation et biomagnification** : Les polluants s’accumulent et se concentrent à chaque niveau trophique.
        
        - **Intoxication et mortalité** : Affectent la reproduction, la croissance et la survie des espèces.
        
        📌 *Exemple :* Le **mercredi de Minamata** (Japon) – pollution au mercure causant malformations et décès.
    """, """
        - **التراكم الحيوي والتكبير البيولوجي**: تتراكم الملوثات وتزداد تركيزها في كل مستوى غذائي.
        
        - **التسمم والموت**: تؤثر على التكاثر والنمو وبقاء الأنواع.
        
        📌 *مثال*: **أربعاء ميناماتا** (اليابان) – تلوث بالزئبق يسبب التشوهات والوفيات.
    """), unsafe_allow_html=True)

    st.markdown("<h4>Pollution Organique (Dépôts de Nutriments)</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - **Zones mortes** : L’excès de nutriments provoque un manque d\’oxygène fatal à la vie aquatique.
        
        - **Perte de biodiversité** : Les algues toxiques étouffent la vie aquatique.
        
        📌 *Exemple :* Le **Golfe du Mexique** développe chaque été une vaste zone morte.
    """, """
        - **المناطق الميتة**: يؤدي الإفراط في المغذيات إلى نقص الأوكسجين القاتل للحياة المائية.
        
        - **فقدان التنوع البيولوجي**: الطحالب السامة تخنق الحياة المائية.
        
        📌 *مثال*: **خليج المكسيك** يطور كل صيف منطقة ميتة واسعة.
    """), unsafe_allow_html=True)

    st.markdown("<h4>Pollution Plastique</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - **Blocage des voies respiratoires** : Ingestion de plastiques par les animaux marins.
                          
        - **Perturbation hormonale** : Certains plastiques agissent comme perturbateurs endocriniens.
        
        📌 *Exemple :* Les **tortues marines** ingèrent des sacs plastiques confondus avec des méduses.
    """, """
        - **انسداد المجاري التنفسية**: ابتلاع الحيوانات البحرية للبلاستيك.
        
        - **اضطراب هرموني**: بعض البلاستيك يعمل كمؤثرات هرمونية.
        
        📌 *مثال*: **السلاحف البحرية** تبتلع أكياس بلاستيكية تعتقد أنها قناديل البحر.
    """), unsafe_allow_html=True)

    st.markdown("<h4>Pollution Thermique</h4>", unsafe_allow_html=True)
    
    st.markdown(translate("""
        - **Réduction de l’oxygène dissous** : L’eau chaude est moins oxygénée.
                          
        - **Migration des espèces** : Déplacement vers des eaux plus froides, perturbant l’équilibre.
                          
        📌 *Exemple :* Les **truites**, espèces sensibles, souffrent fortement de cette pollution.
    """, """
        - **تقليل الأوكسجين المذاب**: المياه الساخنة تحتوي على أوكسجين أقل.
                          
        - **هجرة الأنواع**: الانتقال إلى المياه الأكثر برودة، مما يعطل التوازن.
                          
        📌 *مثال*: **التروتة**، وهي أنواع حساسة، تعاني بشدة من هذا التلوث.
    """), unsafe_allow_html=True)

    st.markdown(translate("<h3>3.Solutions pour Protéger la Biodiversité Aquatique 🌱💦</h3>", "<h3>3.حلول لحماية التنوع البيولوجي المائي 🌱💦</h3>"), unsafe_allow_html=True)
    
    st.markdown(translate("""
        ✅ **Réduction de la Pollution** : Limiter les rejets industriels/agricoles, technologies écologiques.
        
        ✅ **Protection des Zones Sensibles** : Créer des réserves et zones protégées.
        
        ✅ **Restauration des Écosystèmes Aquatiques** : Réhabiliter zones humides, récifs coralliens.
        
        ✅ **Éducation et Sensibilisation** : Informer le public sur les dangers de la pollution de l’eau.
    """, """
        ✅ **تقليل التلوث**: الحد من الانبعاثات الصناعية والزراعية، واستخدام التقنيات البيئية.
        
        ✅ **حماية المناطق الحساسة**: إنشاء محميات ومناطق محمية.
        
        ✅ **إعادة تأهيل النظم البيئية المائية**: إعادة تأهيل المناطق الرطبة، الشعاب المرجانية.
        
        ✅ **التوعية والتعليم**: توعية الجمهور بمخاطر تلوث المياه.
    """), unsafe_allow_html=True)

    st.markdown(translate("<h2>🌍 Un Appel à la Protection de Nos Écosystèmes Aquatiques</h2>", "<h2>🌍 دعوة لحماية النظم البيئية المائية لدينا</h2>"), unsafe_allow_html=True)
    
    st.markdown(translate("""
        La biodiversité aquatique est cruciale pour la survie des humains et des espèces animales.  
        Agir contre la pollution, c’est préserver notre avenir commun. 💙🐟💧
    """, """
        التنوع البيولوجي المائي أمر حيوي لبقاء الإنسان والكائنات الحيوانية.  
        العمل ضد التلوث يعني الحفاظ على مستقبلنا المشترك. 💙🐟💧
    """), unsafe_allow_html=True)

    st.video("https://youtu.be/bIpmzuuyASY?si=iEi8aMqp7nvSuFUk")
# ---- Quiz ----
elif choice== translate("Quiz","اختبار"):
    questions_mcq = [
        {
            "question": translate("Quelle étape du cycle de l’eau correspond à la formation de nuages ?", "ما هي المرحلة من دورة المياه التي تتعلق بتشكل السحب؟"),
            "options": [translate("Infiltration", "التسلل"), translate("Condensation", "التكثف"), translate("Ruissellement", "الجريان السطحي"), translate("Évaporation", "التبخر")],
            "answer": translate("Condensation","التكثف")
        },
        {
            "question": translate("Quel usage consomme le plus d’eau à l’échelle mondiale ?", "أي استخدام يستهلك أكثر المياه على مستوى العالم؟"),
            "options": [translate("Domestique", "المنزلي"), translate("Industriel", "الصناعي"), translate("Agricole", "الزراعي"), translate("Énergétique", "الطاقة")],
            "answer": translate("Agricole","الزراعي")
        },
        {
            "question": translate("Quelle pratique permet d’économiser l’eau à la maison ?", "ما هي الممارسة التي تساعد في توفير المياه في المنزل؟"),
            "options": [translate("Arroser à midi", "الري في منتصف النهار"), translate("Utiliser un lave-vaisselle plein", "استخدام غسالة الصحون الممتلئة"), translate("Prendre des bains", "أخذ حمامات"), translate("Laver la voiture chaque semaine", "غسل السيارة كل أسبوع")],
            "answer": translate("Utiliser un lave-vaisselle plein","استخدام غسالة الصحون الممتلئة")
        }
    ]

    # ✅ Vrai ou Faux
    true_or_false_questions = [
        {"question": translate("L’évaporation transforme l’eau liquide en vapeur.", "التبخر يحول الماء السائل إلى بخار."), "answer": True},
        {"question": translate("L’infiltration renvoie l’eau directement dans l’atmosphère.", "التسلل يعيد الماء مباشرة إلى الغلاف الجوي."), "answer": False},
        {"question": translate("Les nappes phréatiques sont des réserves d’eau souterraines.", "المياه الجوفية هي خزانات للمياه تحت الأرض."), "answer": True},
        {"question": translate("L’industrie consomme plus d’eau que l’agriculture dans le monde.", "الصناعة تستهلك أكثر من المياه مقارنة بالزراعة في العالم."), "answer": False}
    ]

    # ✍ Questions ouvertes
    progressive_questions = [
        {"question": translate("Quelle étape du cycle de l’eau suit immédiatement les précipitations ?", "ما هي المرحلة التالية مباشرة بعد الأمطار في دورة المياه؟"), "answer": translate("Ruissellement","الجريان السطحي")},
        {"question": translate("Quel est le nom du processus par lequel l’eau passe du sol aux nappes souterraines ?", "ما هو اسم العملية التي ينتقل فيها الماء من التربة إلى المياه الجوفية؟"), "answer": translate("Infiltration","التسلل")},
        {"question": translate("Quel est le principal gaz responsable de la condensation dans le cycle de l’eau ?", "ما هو الغاز الرئيسي المسؤول عن التكثف في دورة المياه؟"), "answer": translate("Vapeur d’eau","بخار الماء")},
        {"question": translate("Cite une solution pour économiser l’eau dans un jardin ?", "اذكر حلاً لتوفير المياه في حديقة؟"), "answer": translate("Goutte-à-goutte","الري بالتنقيط")}
    ]

    # 🧪 Classement par usage d’eau (du plus au moins consommateur)
    usages = [
        {"method": translate("Agriculture", "الزراعة"), "efficiency": "Très élevé"},
        {"method": translate("Industrie", "الصناعة"), "efficiency": "Élevé"},
        {"method": translate("Usage domestique", "الاستخدام المنزلي"), "efficiency": "Moyen"},
        {"method": translate("Loisirs", "الترفيه"), "efficiency": "Faible"}
    ]

    # QCM
    def multiple_choice_game():
        st.title(translate("🧠 QCM - Cycle et usages de l’eau", "🧠 اختبار متعدد - دورة المياه واستخداماتها"))
        score = 0
        answers = []

        for i, q in enumerate(questions_mcq):
            st.subheader(f"{translate('Question', 'سؤال')} {i + 1}: {q['question']}")
            selected_option = st.radio(translate("Choisissez la bonne réponse :", "اختر الإجابة الصحيحة:"), q["options"], key=f"mcq_{i}")
            answers.append(selected_option == q["answer"])

        if st.button(translate("Afficher les résultats", "عرض النتائج"), key="btn_mcq"):
            for i, answer in enumerate(answers):
                if answer:
                    st.success(f"✅ {translate('Question', 'سؤال')} {i+1} : {translate('Bonne réponse !', 'إجابة صحيحة!')}")
                else:
                    st.error(f"❌ {translate('Question', 'سؤال')} {i+1} : {translate('Mauvaise réponse. La bonne réponse était :', 'إجابة خاطئة. الإجابة الصحيحة كانت:')} {questions_mcq[i]['answer']}")
            st.write(f"🎉 {translate('Score final', 'النتيجة النهائية')}: {sum(answers)} / {len(questions_mcq)}")

    # Vrai ou Faux
    def true_or_false_game():
        st.title(translate("🔍 Vrai ou Faux - Cycle de l’eau", "🔍 صح أم خطأ - دورة المياه"))
        answers = []

        for i, q in enumerate(true_or_false_questions):
            user_answer = st.radio(f"{translate('Question', 'سؤال')} {i + 1}: {q['question']}", [translate("Vrai", "صح"), translate("Faux", "خطأ")], key=f"tf_{i}")
            correct = (user_answer == translate("Vrai", "صح") and q["answer"]) or (user_answer == translate("Faux", "خطأ") and not q["answer"])
            answers.append(correct)

        if st.button(translate("Afficher les résultats", "عرض النتائج"), key="btn_tf"):
            for i, answer in enumerate(answers):
                correct = translate("Vrai", "صح") if true_or_false_questions[i]["answer"] else translate("Faux", "خطأ")
                if answer:
                    st.success(f"✅ {translate('Question', 'سؤال')} {i+1} : {translate('Bonne réponse !', 'إجابة صحيحة!')}")
                else:
                    st.error(f"❌ {translate('Question', 'سؤال')} {i+1} : {translate('La bonne réponse était :', 'الإجابة الصحيحة كانت:')} {correct}")
            st.write(f"🎉 {translate('Score final', 'النتيجة النهائية')}: {sum(answers)} / {len(true_or_false_questions)}")

    # Questions ouvertes
    def progressive_quiz():
        st.title(translate("🧠 Questions ouvertes - Cycle et gestion de l’eau", "🧠 أسئلة مفتوحة - دورة وإدارة المياه"))
        answers = []

        for i, q in enumerate(progressive_questions):
            user_answer = st.text_input(f"{translate('Question', 'سؤال')} {i + 1}: {q['question']}", key=f"pq_{i}")

            if user_answer.strip():
                similarity = fuzz.ratio(user_answer.strip().lower(), q["answer"].lower())
                correct = similarity >= 80  # نعتبر الإجابة صحيحة إذا كانت نسبة التشابه 80% أو أكثر
            else:
                correct = False
            
            answers.append(correct)

        if st.button(translate("Afficher les résultats", "عرض النتائج"), key="btn_pq"):
            for i, answer in enumerate(answers):
                if answer:
                    st.success(f"✅ {translate('Question', 'سؤال')} {i+1} : {translate('Bonne réponse !', 'إجابة صحيحة!')}")
                else:
                    st.error(f"❌ {translate('Question', 'سؤال')} {i+1} : {translate('La bonne réponse était :', 'الإجابة الصحيحة كانت:')} {progressive_questions[i]['answer']}")
            st.write(f"🎉 {translate('Score final', 'النتيجة النهائية')}: {sum(answers)} / {len(progressive_questions)}")

    # Classement
    def sorting_game():
        st.title(translate("📊 Classement des usages de l’eau selon la consommation", "📊 ترتيب استخدامات المياه حسب الاستهلاك"))
        st.write(translate("Classez les usages du plus grand au plus petit consommateur d’eau.", "صنف الاستخدامات من الأكثر إلى الأقل استهلاكًا للمياه."))

        usages_sorted = sorted(usages, key=lambda x: x["efficiency"], reverse=True)
        usage_names = [u["method"] for u in usages_sorted]

        ordered = st.multiselect(translate("Classez les usages :", "صنف الاستخدامات :"), options=[u["method"] for u in usages], key="sort")

        if ordered:
            if ordered == usage_names:
                st.success(translate("✅ Classement correct !", "✅ التصنيف صحيح!"))
            else:
                st.error(translate("❌ Classement incorrect. Essayez encore.", "❌ التصنيف غير صحيح. حاول مرة أخرى."))

    # Menu principal
    def main():
        st.sidebar.title(translate("💧 Quiz : Cycle et usages de l’eau", "💧 اختبار: دورة المياه واستخداماتها"))

        # الصفحات باللغتين
        page_fr = ["QCM", "Vrai ou Faux", "Questions ouvertes", "Classement des usages"]
        page_ar = ["أسئلة متعددة الاختيارات", "صح أم خطأ", "أسئلة مفتوحة", "ترتيب الاستعمالات"]

        # نحدد القائمة حسب اللغة
        menu = page_ar if st.session_state.lang == "العربية" else page_fr

        # نعرض القائمة الصحيحة
        choice = st.sidebar.radio(translate("Choisissez un jeu :", "اختر لعبة :"), menu)
        st.session_state.page = choice

        # الآن نتحقق من الاختيار حسب اللغة
        if st.session_state.lang == "العربية":
            if choice == "أسئلة متعددة الاختيارات":
                multiple_choice_game()
            elif choice == "صح أم خطأ":
                true_or_false_game()
            elif choice == "أسئلة مفتوحة":
                progressive_quiz()
            elif choice == "ترتيب الاستعمالات":
                sorting_game()
        else:
            if choice == "QCM":
                multiple_choice_game()
            elif choice == "Vrai ou Faux":
                true_or_false_game()
            elif choice == "Questions ouvertes":
                progressive_quiz()
            elif choice == "Classement des usages":
                sorting_game()
    if __name__ == "__main__":
        main()



# ---- Chatbot ----
elif choice == translate("Dropbot", "دروب بوت"):

    @st.cache_data
    def load_qa_data():
        if os.path.exists("qa_data.json"):
            with open("qa_data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_qa_data(data):
        with open("qa_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # === وظائف المساعدة ===

    def find_best_match(user_input, qa_pairs):
        best_match = process.extractOne(user_input, qa_pairs.keys())
        if best_match and best_match[1] > 80:
            return best_match[0], best_match[1]  # إرجاع السؤال الأكثر توافقًا والنسبة المئوية للتطابق
        return None, 0

    # === تحميل البيانات ===

    qa_pairs = load_qa_data()

    # === تهيئة الذاكرة ===

    if "history" not in st.session_state:
        st.session_state.history = []

    if "awaiting_answer" not in st.session_state:
        st.session_state.awaiting_answer = False

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = ""

    # === الواجهة ===

    st.title(translate("DropBot 💧", "دروب بوت 💧"))
    st.markdown(translate("Pose-moi une question sur l'eau", "اطرح عليّ سؤالاً حول الماء"))

    # === نموذج الإدخال ===

    with st.form("question_form", clear_on_submit=True):
        user_input = st.text_input(translate("Tape ta question :", "اكتب سؤالك :"), key="user_question")
        submitted = st.form_submit_button(translate("Envoyer", "إرسال"))

    # === معالجة السؤال ===

    if submitted and user_input:
        match, match_score = find_best_match(user_input, qa_pairs)
        st.session_state.history.append(("Toi", user_input))  # سجل السؤال أولاً
        
        if match and match_score == 100:
            best_answer = qa_pairs[match]
            bot_response = f"**{best_answer}**"
            st.session_state.history.append(("Bot", bot_response))
            st.session_state.awaiting_answer = False
            st.session_state.pending_question = ""
        else:
            st.session_state.awaiting_answer = True
            st.session_state.pending_question = user_input
            # عرض الإجابة مع التطابق جزئيًا
            if match:
                partial_answer = qa_pairs[match]
                bot_response = f"{partial_answer} (تطابق: {match_score}%)"
            else:
                bot_response = translate("Je n'ai pas pu trouver une réponse précise.","**لم أتمكن من إيجاد إجابة دقيقة.**")
            st.session_state.history.append(("Bot", bot_response))

    # === إذا البوت ينتظر إجابة من المستخدم ===

    if st.session_state.awaiting_answer:
        st.info(translate("Je n'ai pas trouvé de réponse exacte 😔. Peux-tu m'apprendre la bonne réponse ?", 
                          "لم أتمكن من إيجاد إجابة دقيقة 😔. هل يمكنك تعليمي الإجابة الصحيحة ؟"))
        with st.form("answer_form"):
            new_answer = st.text_input(translate("Ta réponse :", "إجابتك :"), key="new_answer")
            save_submitted = st.form_submit_button(translate("Sauvegarder la réponse", "حفظ الإجابة"))

        if save_submitted and new_answer:
            qa_pairs = load_qa_data()  # إعادة التحميل لضمان التحديث
            qa_pairs[st.session_state.pending_question] = new_answer
            save_qa_data(qa_pairs)
            
            bot_response = translate("**Merci ! J'ai appris une nouvelle réponse.**", "**شكراً! لقد تعلمت إجابة جديدة.**")
            st.session_state.history.append(("Bot", bot_response))
            
            st.session_state.awaiting_answer = False
            st.session_state.pending_question = ""
            st.success(translate("Merci ! J'ai appris une nouvelle réponse. Recharge la page pour continuer.", 
                                 "شكراً! لقد تعلمت إجابة جديدة. يرجى إعادة تحميل الصفحة للمتابعة."))

    # === عرض المحادثة مع الأفتارات ===

    for speaker, message in st.session_state.history:
        col1, col2 = st.columns([1, 9])
        with col1:
            if speaker == "Toi":
                st.image("https://cdn-icons-png.flaticon.com/512/1077/1077114.png", width=40)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/3558/3558977.png", width=40)
        with col2:
            if speaker == "Toi":
                st.markdown(f"**{translate('Toi :', 'أنت :')}** {message}")
            else:
                st.markdown(f"**{translate('DropBot 💧 :', 'دروب بوت 💧 :')}** {message}")
