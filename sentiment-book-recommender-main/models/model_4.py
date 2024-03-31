import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from scipy.sparse import hstack
from sklearn.decomposition import TruncatedSVD




def load_user_feedback(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['user_id', 'book_id', 'user_rating'])

#preprocessing for overview data
def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    # Tokenization
    tokens = nltk.word_tokenize(text)
    
    # Lowercasing
    tokens = [word.lower() for word in tokens]
    
    # Removing punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [word.translate(table) for word in tokens]
    
    # Removing non-alphabetic tokens
    words = [word for word in stripped if word.isalpha()]
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    
    return ' '.join(lemmatized)


#*********************************
#********LOAD THE DATASET*********
#*********************************
program_path = os.path.dirname(__file__)

relative_cleaned_dataset_path = '../data/processed/cleaned_dataset.csv'
full_cleaned_dataset_path = os.path.join(program_path, relative_cleaned_dataset_path)
relative_feedback_path = '../data/User_Feedback.csv'
full_feedback_path = os.path.join(program_path, relative_feedback_path)

dataset = pd.read_csv(full_cleaned_dataset_path)
user_feedback = load_user_feedback(full_feedback_path)
    

#*********************************
#*******CONTENT FILTERING*********
#*********************************

#datasets to be used in content filtering
dataset['overview_processed'] = dataset['overview'].apply(preprocess_text)
dataset['genres'].fillna('', inplace=True)
dataset['overview_processed'].fillna('', inplace=True)

tfidf_vectorizer = TfidfVectorizer(stop_words='english')

#matrices for genres and overview separately, to prevent dilution of genres
tfidf_matrix_genres = tfidf_vectorizer.fit_transform(dataset['genres'])
tfidf_matrix_overview = tfidf_vectorizer.fit_transform(dataset['overview_processed'])

svd = TruncatedSVD(n_components=50)  
tfidf_matrix_overview_reduced = svd.fit_transform(tfidf_matrix_overview)

#give more weight to genres, more direct correlation
weight_for_genres = 0.85 
weight_for_overview = 0.15 
tfidf_matrix_genres_weighted = tfidf_matrix_genres * weight_for_genres
tfidf_matrix_overview_reduced_weighted = tfidf_matrix_overview_reduced * weight_for_overview
# Combine the weighted matrices
combined_tfidf_matrix = hstack([tfidf_matrix_genres_weighted, tfidf_matrix_overview_reduced_weighted])
#get content similarity
content_similarity = linear_kernel(combined_tfidf_matrix, combined_tfidf_matrix)


#*********************************
#******USER BASED FILTERING*******
#*********************************

user_features = ['book_id', 'ratings_count', 'average_rating']
# Calculate user similarity matrix
user_similarity = 1 - pairwise_distances(dataset[user_features].fillna(0), metric='cosine')


#used to test mean and median ranges of similarity statistics during dev
def calculate_similarity_statistics(similarity_scores):
    # Ensure the input is a 1D array (flattened, if it was 2D)
    if similarity_scores.ndim > 1:
        similarity_scores = similarity_scores.flatten()

    # Remove the self-similarity score if it's included (similarity score of 1)
    similarity_scores = similarity_scores[similarity_scores < 1]

    # Calculate the mean and median
    mean_score = np.mean(similarity_scores)
    median_score = np.median(similarity_scores)

    return mean_score, median_score


#Use user feedback to adjust model 
def adjust_ratings_with_feedback(user_id, similarity_threshold=0.5):
    adjusted_ratings = dataset.copy()
    user_specific_feedback = user_feedback[user_feedback['user_id'] == user_id]

    for index, feedback in user_specific_feedback.iterrows():
        book_id = feedback['book_id']
        user_rating = feedback['user_rating']

        # Find the index of the book in the dataset
        book_idx = adjusted_ratings.index[adjusted_ratings['book_id'] == book_id].tolist()
        if not book_idx:
            continue
        book_idx = book_idx[0]

        # Find and adjust ratings for similar books
        similar_books_indices = np.where(content_similarity[book_idx] >= similarity_threshold)[0]
        # The similarity scores for all similar books
        similar_books_similarity_scores = content_similarity[book_idx][similar_books_indices]
        
        for idx, similar_book_idx in enumerate(similar_books_indices):

            similarity_score = similar_books_similarity_scores[idx] 
            # Scale the impact by the similarity score
            impact = (user_rating - adjusted_ratings.loc[similar_book_idx, 'average_rating']) * similarity_score
            # Update the average rating of similar books
            adjusted_ratings.loc[similar_book_idx, 'average_rating'] += impact

    return adjusted_ratings


# Function to recalculate user similarity matrix
def recalculate_user_similarity(user_id):
    global user_similarity, dataset, user_feedback
    adjusted_ratings = adjust_ratings_with_feedback(user_id)
    user_similarity = 1 - pairwise_distances(adjusted_ratings[user_features].fillna(0), metric='cosine')

# Function to update user feedback
def update_user_feedback(user_id, book_id, user_rating):
    global user_feedback
    new_feedback = pd.DataFrame({'user_id': [user_id], 'book_id': [book_id], 'user_rating': [user_rating]})
    user_feedback = pd.concat([user_feedback, new_feedback], ignore_index=True)
    recalculate_user_similarity(user_id)
    save_user_feedback()

def format_and_print_recommendations(recommendations):
    pd.set_option('display.max_colwidth', 40)
    pd.set_option('display.precision', 3)
    pd.set_option('display.width', None)  # Adjust the total width of the output display

    # Strip leading and trailing spaces from 'title' and 'authors'
    recommendations['title'] = recommendations['title'].str.strip().apply(lambda x: (x[:40] + '...') if len(x) > 30 else x)
    recommendations['authors'] = recommendations['authors'].str.strip().apply(lambda x: (x[:25] + '...') if len(x) > 25 else x)

    # Round the 'hybrid_rating' to three decimal places
    recommendations['hybrid_rating'] = recommendations['hybrid_rating'].round(3)

    # Print recommendations without the index
    print(recommendations.to_string(index=False, justify='middle'))

#function to normalize the scores of content and collaborative, to combine into hybrid
def normalize_scores(scores):
    min_score = np.min(scores)
    max_score = np.max(scores)
    if max_score == min_score:
        return np.zeros_like(scores) if min_score == 0 else np.ones_like(scores)
    normalized_scores = (scores - min_score) / (max_score - min_score)
    return normalized_scores


def hybrid_recommendation(movie_title, user_id, k=5, alpha=0.5, beta=0.5):

    recalculate_user_similarity(user_id)
    
    # Find index of the movie title for content-based recommendation
    movie_idx = dataset.index[dataset['movie_title'].str.contains(movie_title, case=False, na=False)].tolist()
    if not movie_idx:
        return None
    movie_idx = movie_idx[0]

    # Get content-based similarity scores for all books against the movie
    movie_similarities = content_similarity[movie_idx]

    # Adjust dataset based on user feedback to reflect collaborative filtering
    adjusted_ratings = adjust_ratings_with_feedback(user_id)

    # Prepare the entire dataset with hybrid ratings
    all_books = adjusted_ratings.copy()
    all_books['content_score'] = movie_similarities
    normalized_collaborative_scores = normalize_scores(all_books['average_rating'].values)
    normalized_content_scores = normalize_scores(all_books['content_score'].values)

    all_books['hybrid_rating'] = np.nan

    # Calculate hybrid rating for each book
    for idx in all_books.index:
        collaborative_score = normalized_collaborative_scores[idx]
        content_score = normalized_content_scores[idx]

        hybrid_rating = alpha * collaborative_score + beta * content_score
        all_books.at[idx, 'hybrid_rating'] = hybrid_rating

    # Sort all books based on the hybrid score and select the top k recommendations
    final_columns = ['book_id', 'title', 'authors', 'average_rating', 'ratings_count', 'hybrid_rating']
    top_recommendations = all_books.sort_values(by='hybrid_rating', ascending=False)[final_columns].head(k)

    print(f"\nBook recommendations based on '{movie_title}':\n")
    return format_and_print_recommendations(top_recommendations)


# Function for dynamic user feedback input
def input_user_feedback():
    try:
        user_id = int(input("Enter your user ID: "))
        book_id = int(input("Enter book ID to rate: "))
        user_rating = float(input("Enter your rating for the book (1-5): "))
        update_user_feedback(user_id, book_id, user_rating)
        print("Feedback updated.")
    except ValueError:
        print("Invalid input. Please try again.")

def save_user_feedback():
    global user_feedback
    user_feedback.to_csv(full_feedback_path, index=False)

# Function to compute recall
def compute_recall(predictions, threshold=3.5):
    # Consider a recommendation as successful if the predicted rating is above the threshold
    relevant_items = sum((prediction.est >= threshold) for prediction in predictions)
    # Count all items that are actually relevant
    total_relevant_items = sum((prediction.r_ui >= threshold) for prediction in predictions)
    # Avoid division by zero
    return relevant_items / total_relevant_items if total_relevant_items > 0 else 0

# Function to compute F1 score
def compute_f1(predictions, threshold=3.5):
    # Convert predictions to binary values (1 if >= threshold, 0 otherwise)
    predicted_labels = [1 if prediction.est >= threshold else 0 for prediction in predictions]
    # Convert actual ratings to binary values (1 if >= threshold, 0 otherwise)
    actual_labels = [1 if prediction.r_ui >= threshold else 0 for prediction in predictions]
    # Compute F1 score
    return compute_f1(actual_labels, predicted_labels)


def main_menu():
     # After user feedback is collected
    user_feedback_data = load_user_feedback(full_feedback_path)
    while True:

        print("\nMain Menu:")
        print("1. Rate a Book")
        print("2. Get Book Recommendations from a Movie Title")
        print("3. Save Feedback and Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            input_user_feedback()
            user_feedback_given = True
        elif choice == '2':
            movie_title = input("Enter a movie title for book recommendations: ")
            user_id = int(input("Enter your user ID: "))
            recommendations = hybrid_recommendation(movie_title, user_id, k=5, alpha=0.5, beta=0.5)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()
save_user_feedback()

