# import pickle
# import streamlit as st
# import requests
# import time
#
#
# API_KEY = "bce5b0ed7eac7effcdb4f69222003972"
#
#
# def fetch_poster(movie_id):
#
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}"
#
#     params = {
#         "api_key": API_KEY,
#         "language": "en-US"
#     }
#
#     try:
#         session = requests.Session()
#
#         response = session.get(
#             url,
#             params=params,
#             timeout=(10, 60),
#             headers={
#                 "User-Agent": "Mozilla/5.0",
#                 "Accept": "application/json"
#             }
#         )
#
#         response.raise_for_status()
#
#         data = response.json()
#
#         poster_path = data.get("poster_path")
#
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"
#
#         return None
#
#     except Exception as e:
#         print(f"Movie {movie_id} failed: {e}")
#         return None
#
#
# def recommend(movie):
#
#     index = movies[movies["title"] == movie].index[0]
#
#     distances = sorted(
#         list(enumerate(similarity[index])),
#         reverse=True,
#         key=lambda x: x[1]
#     )
#
#     recommended_movie_names = []
#     recommended_movie_posters = []
#
#     for i in distances[1:6]:
#
#         movie_id = movies.iloc[i[0]].movie_id
#
#         st.write(
#             movies.iloc[i[0]].title,
#             "→ TMDB ID:",
#             movie_id)
#
#         recommended_movie_names.append(
#             movies.iloc[i[0]].title
#         )
#
#         recommended_movie_posters.append(
#             fetch_poster(movie_id)
#         )
#
#     return recommended_movie_names, recommended_movie_posters
#
#
# st.header("Movie Recommender System")
#
# movies = pickle.load(open("movies.pkl", "rb"))
# similarity = pickle.load(open("similarity.pkl", "rb"))
#
# movie_list = movies["title"].values
#
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )
#
# if st.button("Show Recommendation"):
#
#     names, posters = recommend(selected_movie)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     for col, name, poster in zip(
#             [col1, col2, col3, col4, col5],
#             names,
#             posters
#     ):
#         with col:
#             st.write(name)
#             st.write(poster)
#
#             if poster:
#                 st.image(poster)
#             else:
#                 st.warning("Poster not available")
import pickle
import streamlit as st
import requests

API_KEY = "bce5b0ed7eac7effcdb4f69222003972"


def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except requests.exceptions.RequestException as e:
        print(f"Movie {movie_id} failed: {e}")
        return None


def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        st.write(
            movies.iloc[i[0]].title,
            "→ TMDB ID:",
            movie_id
        )

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movie_names, recommended_movie_posters


st.header("Movie Recommender System")

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    for col, name, poster in zip(
        [col1, col2, col3, col4, col5],
        names,
        posters
    ):
        with col:

            st.write(name)

            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.warning("Poster not available")