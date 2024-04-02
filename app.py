import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster URL
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b6a887f8cfe6bf864f1fdd3f2ea8303d&languagad1ea1c76dd7d50575eeca54831ce166e=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender")
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set background image using CSS only before the button is pressed
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: url('https://assets.nflxext.com/ffe/siteui/vlv3/e89c9679-2f5f-491d-924c-c58924a8ee4b/8ec27a1d-02ce-4489-b320-a95106906f5d/IN-en-20221121-popsignuptwoweeks-perspective_alpha_website_medium.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dropdown box for movie selection
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

# Button to trigger recommendation
if st.button('Recommend'):
    # Clear background image CSS after button press
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"]{
            background: url('https://img.freepik.com/free-photo/popcorn-bucket-cup-popcorn-are-table-cinema_1340-34294.jpg?t=st=1698131688~exp=1698135288~hmac=d2e4e4267bde5fac6957b0da88902f061d276baebd629258738feb8db2fe1cca&w=740');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    try:
        names, posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i in range(len(names)):
            with cols[i]:
                # Display poster with title below it
                st.markdown(
                    f'<div class="movie-container">'
                    f'<a href="https://www.themoviedb.org/movie/{movies[movies["title"] == names[i]].iloc[0]["movie_id"]}" target="_blank">'
                    f'<div class="movie-poster" style="background-image: url({posters[i]});"></div>'
                    f'<div class="movie-title"><span style="background-color: black; opacity:80%; padding: 5px;">{names[i]}</span></div>'
                    f'</a>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    except IndexError:
        st.error("Movie not found. Please enter another movie.")

# Custom CSS for movie posters and button
st.markdown(
    """
    <style>
    .movie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .movie-poster {
        width: 220px;
        height: 320px;
        background-size: cover;
        background-position: center;
        cursor: pointer;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        position: relative;
    }
    .movie-title {
        font-weight: bold;
        margin-top: 50px;
        color: white;
    }
    .movie-poster:hover {
        transform: scale(1.3);
        z-index: 1;
    }
    .stButton>button {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

