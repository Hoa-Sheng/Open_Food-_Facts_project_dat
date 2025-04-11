import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Charger la dataset
df = pd.read_csv('Dataset/df_nettoye.csv', sep=',', encoding='utf-8')  

# Configuration de la page
st.set_page_config(page_title="Dashboard Nutritionnel", page_icon="🍏", layout="wide")

# Style personnalisé
st.markdown(
    """
    <style>
    .css-1d391kg {background-color: #ff66b2; }
    .sidebar .sidebar-content {background-color: #ff66b2;}
    .css-16q5k9r {background-color: #ff66b2;}
    </style>
    """, unsafe_allow_html=True)

# Menu latéral
menu = st.sidebar.radio("Navigation", ["🏠 Accueil", "📊 Visualisations"])

# --- PAGE ACCUEIL ---
if menu == "🏠 Accueil":
    st.title("📌 Introduction au Nutri-Score et à notre étude")

    # Bloc définition stylisé
    st.markdown(""" 
    <div style="
        background-color: black;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid white;
        color: white;
        font-size: 16px;
        margin-bottom: 30px;
    ">
        <h3 style="color: #ff66b2;">🧠 Qu'est-ce que le Nutri-Score ?</h3>
        <p>
            Le <strong>Nutri-Score</strong> est un système d'étiquetage nutritionnel qui classe les aliments de A à E.
            Il repose sur un calcul prenant en compte :
        </p>
        <ul>
            <li><strong>Éléments négatifs :</strong> énergie, acides gras saturés, sucres, sel</li>
            <li><strong>Éléments positifs :</strong> fibres, protéines, fruits et légumes</li>
        </ul>
        <h4 style="color: #ff66b2;">❓ Problématique :</h4>
        <p>Le nutri score est il un outil fiable et quelles sont ces limites ?</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔢 Statistiques générales")

    col1, col2 = st.columns(2)

    # Bloc pour afficher le nombre total de produits
    with col1:
        st.markdown(f"""
            <div style="
                background-color: black;
                padding: 70px;
                border-radius: 15px;
                border: 2px solid white;
                text-align: center;
            ">
                <h2 style="color: #ff66b2;">📦 {df.shape[0]}</h2>
                <p style="color: white;">Nombre total de produits</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="
                background-color: black;
                padding: 70px;
                border-radius: 15px;
                border: 2px solid white;
                text-align: center;
                margin-top: 20px;
            ">
                <h2 style="color: #ff66b2;">📦 {df.shape[1]}</h2>
                <p style="color: white;">Nombre total de colonnes</p>
            </div>
        """, unsafe_allow_html=True)

    # Diagramme circulaire de la répartition par Nutri-Score
    with col2:
        st.subheader("🍽️ Répartition par Nutri-Score")
        grade_order = ['A', 'B', 'C', 'D', 'E']
        fig, ax = plt.subplots()

        # Obtenir les valeurs de Nutri-Score et réorganiser selon grade_order
        grade_counts = df['nutrition_grade_fr'].value_counts()
        grade_counts = grade_counts.reindex(grade_order, fill_value=0)  # Réorganiser et remplir les valeurs manquantes
        labels = grade_counts.index

        # Tracer le pie chart
        wedges, texts, autotexts = ax.pie(
            grade_counts,
            labels=None,  
            autopct='%1.1f%%',
            startangle=50,
            colors=["#61a37b", "#D4E157", "#FFF59D", "#FFCC80", "#EF9A9A"],
            
        )

        # Ajouter la légende à gauche
        ax.legend(
            wedges, labels, loc="center right",
            bbox_to_anchor=(0.7, 0, 0.5, 0.5), fontsize=10,
            title_fontsize='13', facecolor="#0e1117", labelcolor="white"
        )
        ax.set_ylabel("")
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117") 
        plt.setp(autotexts, size=13)   

        st.pyplot(fig)

    # Graphiques généraux
    col1, col2= st.columns(2)
    st.subheader('Répartition des catégories de produits')
    category_counts = df['categories_fr'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    category_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", color="white")
    ax.set_xlabel("Catégories de produits", color="white")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color="white")
    fig.patch.set_facecolor("#0e1117")  # Mettre le fond de la figure en noir
    ax.set_ylabel("Nombre de produits", color="white")
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117") 
    st.pyplot(fig)

    st.info("👉 Passez à l'onglet **Visualisations** pour explorer plus en détail les données.")

# --- PAGE VISUALISATIONS ---
elif menu == "📊 Visualisations":
    st.title("📊 Analyse des données nutritionnelles")

    # Sélection de l'option à afficher
    option = st.sidebar.selectbox(
        'Que souhaitez-vous visualiser ?',
        ['Répartition par grade nutritionnel',
         'Heatmap des corrélations',
         'Visualisation de boxplot par catégorie']  # Nouvelle option ajoutée
    )

    # Affichage de la répartition par grade nutritionnel
    if option == 'Répartition par grade nutritionnel':
        st.subheader('Répartition par grade nutritionnel')
        grade_counts = df['nutrition_grade_fr'].value_counts()
        grade_order = ['A', 'B', 'C', 'D', 'E']

        # Réorganiser les données selon l'ordre souhaité
        grade_counts = grade_counts.reindex(grade_order, fill_value=0)

        # Création du graphique avec matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor("#0e1117")  # Mettre le fond de la figure en noir
        grade_counts.plot(kind='bar', ax=ax, color='skyblue')

        # Mettre le fond de l'axe en noir
        ax.set_facecolor("#0e1117") 

        # Rotation des étiquettes des axes X et personnalisation des couleurs
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, color="white")
        ax.set_xlabel("Nutri-Score", color="white")
        ax.set_ylabel("Nombre de produits", color="white")
        ax.set_title("Répartition par grade nutritionnel", color="white")

        # Modifier la couleur des ticks et des bordures
        ax.tick_params(colors="white")
        ax.spines['bottom'].set_color("white")
        ax.spines['left'].set_color("white")

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
     
    elif option == 'Heatmap des corrélations':
        st.subheader("🔍 Heatmap des corrélations entre variables numériques")

        numeric_columns = df.select_dtypes(include=['float64', 'int64'])

        correlation_matrix = numeric_columns.corr()

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117") 
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            fmt='.2f',
            linewidths=0.5,
            ax=ax,
        )
            # Personnaliser les ticks et le titre
        ax.tick_params(colors="white")  # Couleur des ticks

        # Personnaliser les étiquettes des axes
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", color="white")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color="white")
        ax.set_title('Heatmap des corrélations', fontsize=16, color="white")
        st.pyplot(fig)
         
                

    # --- PAGE DE VISUALISATIONS PAR CATÉGORIE ---
    elif option == "Visualisation de boxplot par catégorie":
        category = st.sidebar.selectbox("Choisissez une catégorie :", df["categories_fr"].unique())
        st.subheader(f"Visualisation de boxplot par catégorie : {category}")

        # Filtrer les données selon la catégorie choisie
        df_category_filtered = df[df["categories_fr"] == category]
        
        # Sélectionner uniquement les colonnes numériques de type float64
        float_columns = df_category_filtered.select_dtypes(include=['float64'])

        # Liste des colonnes à tracer (en excluant 'additives_n' et 'nutrition-score-fr_100g')
        columns_to_plot = [col for col in float_columns.columns if col not in ['additives_n', 'nutrition-score-fr_100g']]

        if not columns_to_plot:
            st.warning("Aucune colonne numérique disponible pour tracer des boxplots.")
        else:
            # Calculer le nombre de lignes nécessaires pour afficher les boxplots
            columns_per_row = 3
            num_rows = math.ceil(len(columns_to_plot) / columns_per_row)

            # Créer les sous-graphes
            fig, axes = plt.subplots(num_rows, columns_per_row, figsize=(15, num_rows * 5))
            fig.patch.set_facecolor("#0e1117")

            # Aplatir les axes pour itérer plus facilement
            axes = axes.flatten()

            # Tracer les boxplots
            for i, column in enumerate(columns_to_plot):
                sns.boxplot(data=df_category_filtered, x=column, ax=axes[i], color='skyblue')
                axes[i].set_title(column, color="white")
                axes[i].tick_params(colors="white")
                axes[i].set_facecolor("#0e1117")

            # Supprimer les axes inutilisés (si le nombre de colonnes n'est pas un multiple de 3)
            for i in range(len(columns_to_plot), len(axes)):
                fig.delaxes(axes[i])

            # Ajuster l'affichage
            plt.tight_layout()
            st.pyplot(fig)