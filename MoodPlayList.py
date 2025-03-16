import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
from textblob import TextBlob

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="client_id here",  # Replace with your Spotify client ID
    client_secret="client_secret here"  # Replace with your Spotify client secret
))

# Expanded dataset for emotion classification
data = [
    ("I am feeling very happy today!", "happy"),
    ("I'm so sad and lonely.", "sad"),
    ("This is such a relaxing evening.", "relaxed"),
    ("I'm full of energy!", "energetic"),
    ("I feel amazing!", "happy"),
    ("I'm feeling very down right now.", "sad"),
    ("What a chill day it has been.", "relaxed"),
    ("Let's party all night!", "energetic"),
    ("Feeling great to be alive!", "happy"),
    ("I feel tired and upset.", "sad"),
    ("I am frustrated with everything!", "frustrated"),
    ("I feel annoyed and angry.", "frustrated"),
    ("I feel calm and peaceful.", "relaxed"),
    ("Let's dance and have fun!", "energetic"),
    ("I feel so energetic and excited!", "energetic"),
]

# Preprocess data
texts, labels = zip(*data)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = labels

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
print("Emotion Classifier Accuracy:", accuracy_score(y_test, y_pred))


# Function to classify emotion using the trained ML model with custom rules
def classify_emotion_ml(user_input):
    user_input = user_input.lower()
    print(f"Debug: Input received: {user_input}")  # Debugging input
    
    # Custom rule for frustration and annoyance
    if "frustrated" in user_input or "annoyed" in user_input:
        return "frustrated"
    if "angry" in user_input or "mad" in user_input:
        return "frustrated"

    # Sentiment analysis for general cases
    analysis = TextBlob(user_input)
    polarity = analysis.sentiment.polarity
    print(f"Debug: Sentiment polarity: {polarity}")  # Debugging polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    else:
        return "relaxed"


# Function to fetch random songs for emotion
def get_random_songs_for_emotion(emotion):
    print(f"Searching for random songs that match the emotion: {emotion}")
    
    # Define broad queries for each emotion
    emotion_queries = {
        'happy': ['happy', 'joy', 'celebration', 'upbeat', 'positive'],
        'sad': ['sad', 'melancholy', 'heartbreak', 'blue', 'emotional'],
        'relaxed': ['relax', 'chill', 'peaceful', 'calm', 'serene'],
        'energetic': ['energy', 'workout', 'dance', 'high-energy', 'party'],
        'frustrated': ['intense', 'angsty', 'frustration', 'raw emotions']
    }
    
    # Choose a random query for the emotion
    query = random.choice(emotion_queries.get(emotion, [emotion]))
    
    # Use a wide offset range to fetch random results
    offset = random.randint(0, 1000)
    
    try:
        # Fetch songs from Spotify
        results = sp.search(q=query, type='track', limit=10, offset=offset)
        songs = []
        seen = set()  # To track unique song names and artists

        for track in results['tracks']['items']:
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            song_url = track['external_urls']['spotify']

            # Ensure uniqueness by checking the combination of song name and artist
            unique_key = (song_name.lower(), artist_name.lower())
            if unique_key not in seen:
                seen.add(unique_key)
                songs.append(f"{song_name} by {artist_name} ({song_url})")

        # Shuffle songs for further randomness
        random.shuffle(songs)
        return songs if songs else ["No songs found for this mood."]
    except Exception as e:
        return [f"Error fetching songs: {str(e)}"]


# Main program loop
if __name__ == "__main__":
    print("Welcome to MoodTunes!")
    print("Type how you're feeling, and I'll suggest some songs!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nHow are you feeling today? ")

        if user_input.lower() == 'exit':
            print("Goodbye! Enjoy your tunes!")
            break

        # Classify the emotion using ML
        detected_emotion = classify_emotion_ml(user_input)
        print(f"Detected emotion: {detected_emotion}")

        # Fetch random songs for the detected emotion
        songs = get_random_songs_for_emotion(detected_emotion)

        # Display songs
        print("\nHere are some random songs for your mood:")
        for song in songs:
            print(f"- {song}")
