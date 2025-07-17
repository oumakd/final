import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Optimisation du Coffrage",
    page_icon="🧱",
    layout="centered",
    initial_sidebar_state="auto"
)

# Charger et afficher le logo TGCC 
url = "https://tgcc.ma/dataup/2021/11/Tgcc_fb.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img = img.resize((140, 70))  # Ajuster la taille si nécessaire
st.image(img, use_container_width=False)


# Titre
st.markdown(
    "<h1 style='text-align: center; color: #7d1a22;'>Optimisation du coffrage</h1>",
    unsafe_allow_html=True
)

st.markdown("Calcul du nombre optimal de jeux de coffrage selon la hauteur des piles, le délai max, la vitesse de bétonnage, et le temps de montage et démontage.")

# Entrées utilisateur
entree = st.text_area("Entrez les hauteurs des piles (en mètres), séparées par des espaces :", value="")
D = st.number_input("Entrez le délai maximal D (en jours) : ", min_value=0.0, value=0.0)
V = st.number_input("Entrez la vitesse de bétonnage V (en m/jour) : ", min_value=0.0, value=0.0)
Tm = st.number_input("Entrez le temps de montage et démontage (en jour) : ", min_value=0.0, value=0.0)

if st.button("Lancer le calcul"):
    try:
        hauteurs = list(map(float, entree.split()))
        if any(h <= 0 for h in hauteurs):
            st.error("Les hauteurs doivent être strictement positives.")
            st.stop()

        hauteurs.sort()
        n = len(hauteurs)

        st.subheader("Hauteurs triées :")
        st.write(hauteurs)

        meilleure_somme = 0
        meilleur_j = None

        st.subheader("Analyse des jeux possibles :")

        couleurs = ["#1f458c", "#1d3a70"]  # bleu et bleu foncé 

        for j in range(1, n + 1):
            somme = 0
            indices_utilises = []
            k = 0

            # Sélection des piles
            while True:
                index = n - 1 - j * k
                if index < 0:
                    break
                somme += hauteurs[index]
                indices_utilises.append(index)
                k += 1

            nb_hauteurs = len(indices_utilises)
            delai_total = D - Tm * nb_hauteurs
            capacite_max = delai_total * V

            couleur = couleurs[(j - 1) % 2]
            hauteurs_choisies = [hauteurs[i] for i in indices_utilises]

            st.markdown(f"<h4 style='color:{couleur};'>Jeu {j}</h4>", unsafe_allow_html=True)
            st.write(f"Somme = {somme:.2f} m | Délai total = {delai_total:.1f} jours | Capacité max = {capacite_max:.2f} m | Nb piles = {len(hauteurs_choisies)}")
            st.write(f"Hauteurs utilisées : {hauteurs_choisies}")

            if somme <= capacite_max and somme > meilleure_somme:
                meilleure_somme = somme
                meilleur_j = j
                st.success("-→ Meilleure somme trouvée")
            else:
                st.info("-→ Pas meilleure")

        st.markdown("## Résultat final")
        if meilleur_j is None:
            st.error("Aucune solution ne respecte les contraintes de délai.")
        else:
            # Calcul nombre piles utilisées pour le meilleur j
            nb_piles_meilleur = len([n - 1 - meilleur_j * k for k in range(n) if n - 1 - meilleur_j * k >= 0])

            st.markdown(
                f"""
                <div style="padding:15px;border-radius:10px;border:1px solid #CCC;">
                   <h3 style="color:#7d1a22;">Meilleure solution trouvée :</h3>
                   <p style="font-size:18px;"> <b>Jeu optimal </b> : <b style='color:#a88387;'> j = {meilleur_j}</b></p>
                   <p style="font-size:18px;"> <b>Nombre de piles utilisées </b> : <b style='color:#a88387;'> {nb_piles_meilleur}</b></p>
                   <p style="font-size:18px;"> <b>Hauteur totale utilisée </b> : <b style='color:#a88387;'> {meilleure_somme:.2f} m</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Erreur rencontrée : {e}")

# Signature 
st.markdown(
    """
    <p style="
        position: fixed;
        bottom: 10px;
        right: 70px;
        font-size: 12px;
        color: rgba(128, 128, 128, 0.4);
        ">
        Réalisé par KDAH Oumaima
    </p>
    """,
    unsafe_allow_html=True
)