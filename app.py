import streamlit as st
import pickle
with open('movie_pkl.pkl','rb') as f:
    movies=pickle.load(f)
with open('similarity_matrix.pkl', 'rb') as f:    
    sim=pickle.load(f)
 
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