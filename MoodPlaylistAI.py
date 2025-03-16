import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
import random

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="client_id here",  # Replace with your Spotify client ID
    client_secret="client_secret here"  # Replace with your Spotify client secret
))

# Set up OpenAI API Key
openai.api_key = "openai_api_key" # Replace with your OpenAI API key

# Function to detect mood using OpenAI GPT
def detect_mood_with_openai(user_input):
    try:
        # Send the user's input to OpenAI's API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mood detector. Analyze the user's input and determine their mood."},
                {"role": "user", "content": user_input}
            ]
        )
        # Extract the mood from the response
        mood = response['choices'][0]['message']['content'].strip().lower()
        print(f"Debug: OpenAI detected mood: {mood}")  # Debugging output
        return mood
    except Exception as e:
        print(f"Error detecting mood with OpenAI: {str(e)}")
        return "neutral"  # Default to neutral if OpenAI fails


# Function to fetch random songs for emotion
def get_random_songs_for_emotion(emotion):
    print(f"Searching for random songs that match the emotion: {emotion}")
    
    # Define broad queries for each emotion
    emotion_queries = {
        'happy': ['happy', 'joy', 'celebration', 'upbeat', 'positive'],
        'sad': ['sad', 'melancholy', 'heartbreak', 'blue', 'emotional'],
        'relaxed': ['relax', 'chill', 'peaceful', 'calm', 'serene'],
        'energetic': ['energy', 'workout', 'dance', 'high-energy', 'party'],
        'frustrated': ['intense', 'angsty', 'frustration', 'raw emotions'],
        'neutral': ['general music', 'popular hits', 'trending now']
    }
    
    # Choose a random query for the emotion
    query = random.choice(emotion_queries.get(emotion, ['general music']))
    
    # Use a wide offset range to fetch random results
    offset = random.randint(0, 1000)
    
    try:
        # Fetch songs from Spotify
        results = sp.search(q=query, type='track', limit=10, offset=offset)
        tracks = []
        seen = set()  # To track unique song names and artists

        for track in results['tracks']['items']:
            song_name = track['name']
            artist_name = track['artists'][0]['name']
            song_url = track['external_urls']['spotify']

            # Ensure uniqueness by checking the combination of song name and artist
            unique_key = (song_name.lower(), artist_name.lower())
            if unique_key not in seen:
                seen.add(unique_key)
                tracks.append(f"{song_name} by {artist_name} ({song_url})")

        # Shuffle tracks for further randomness
        random.shuffle(tracks)

        return tracks if tracks else ["No songs found for this mood."]
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

        # Detect mood using OpenAI
        detected_mood = detect_mood_with_openai(user_input)
        print(f"Detected mood: {detected_mood}")

        # Fetch random songs for the detected emotion
        songs = get_random_songs_for_emotion(detected_mood)

        # Display songs
        print("\nHere are some random songs for your mood:")
        for song in songs:
            print(f"- {song}")