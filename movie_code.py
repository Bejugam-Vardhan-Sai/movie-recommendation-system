import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


file = "D:/py/movie recommendation system/movie_dataset.csv"  
data = pd.read_csv(file)

movie = data[['id', 'title', 'genres', 'overview', 'keywords', 'tagline', 'cast', 'director']]
movie.dropna(inplace=True)

movie['overview'] = movie['overview'].apply(lambda x: x.split())
movie['genres'] = movie['genres'].apply(lambda x: [x.replace(" ", "")])
movie['keywords'] = movie['keywords'].apply(lambda x: [k.replace(" ", "") for k in x.split()])
movie['cast'] = movie['cast'].apply(lambda x: x.split())
movie['director'] = movie['director'].apply(lambda x: [x.replace(" ", "")])

movie['tags'] = movie['overview'] + movie['genres'] + movie['keywords'] + movie['cast'] + movie['director']
movies = movie[['id', 'title', 'tags']]
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x).lower())

ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

movies['tags'] = movies['tags'].apply(stem)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()
sim = cosine_similarity(vectors)
def recom(movie_title):
    try:
        index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return []

    distances = sim[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_titles = [movies.iloc[i[0]].title for i in movie_list]
    return recommended_titles

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation System")

movie_name = st.text_input("Enter a movie name", "The Dark Knight Rises")

if st.button("Recommend"):
    results = recom(movie_name)
    if results:
        st.subheader("Top 5 Similar Movies:")
        for r in results:
            st.write(f"• {r}")
    else:
        st.warning("Movie not found or no similar movies.")

import pickle
with open('movie_pkl.pkl','wb') as f:
    pickle.dump(movies,f)
with open('similarity_matrix.pkl', 'wb') as f:
    pickle.dump(sim,f)