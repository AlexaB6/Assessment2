import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

CLIENT_ID = 'dc638f5aaa7a4476a12c1f46d7111381'
CLIENT_SECRET = '7641288fac914d28a92b321c60027513'
REDIRECT_URI = 'http://localhost:8888/callback'

SCOPE = 'user-library-read playlist-modify-public user-top-read user-read-recently-played'

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def print_granted_scopes(auth_manager):
    token_info = auth_manager.get_cached_token()
    if token_info and 'scope' in token_info:
        granted_scopes = token_info['scope']
        print(f"Granted Scopes: {granted_scopes}")
    else:
        print("No scopes granted.")

print_granted_scopes(auth_manager)

def print_user_profile(sp):
    try:
        user_profile = sp.current_user()
        print("\nAuthenticated User:")
        print(f"Username: {user_profile['display_name']}")
        print(f"User ID: {user_profile['id']}\n")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error while fetching user profile: {e}")

print_user_profile(sp)

def get_audio_features_batch(track_ids):
    features = []
    for i in range(0, len(track_ids), 50):  # Batch size of 50
        batch = track_ids[i:i+50]
        try:
            batch_features = sp.audio_features(batch)
            features.extend(batch_features)
            time.sleep(1)  # Delay between batches
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
            break
    return features

def get_mood_playlist(mood):
    mood_settings = {
        'happy': {'energy': (0.8, 1.0), 'valence': (0.8, 1.0)},  # More lively
        'sad': {'energy': (0.0, 0.3), 'valence': (0.0, 0.3)},  # More mellow
        'calm': {'energy': (0.0, 0.4), 'valence': (0.3, 0.5)},  # More mellow
        'energetic': {'energy': (0.7, 1.0), 'valence': (0.5, 1.0)}  # More upbeat
    }

    if mood not in mood_settings:
        print("Invalid mood. Choose from: happy, sad, calm, energetic")
        return

    print(f"\nFetching user liked songs for mood: {mood}")

    track_ids = []
    limit = 50
    offset = 0

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results or not results['items']:
            break
        for item in results['items']:
            track = item['track']
            if track and track['id']:
                track_ids.append(track['id'])
        offset += limit

    print(f"Total liked songs fetched: {len(track_ids)}")

    if not track_ids:
        print("No liked songs found for the user.")
        return

    features = get_audio_features_batch(track_ids)
    if not features:
        print("No audio features found for the fetched tracks.")
        return

    energy_min, energy_max = mood_settings[mood]['energy']
    valence_min, valence_max = mood_settings[mood]['valence']

    filtered_tracks = []
    for feature in features:
        if feature is None:
            continue
        energy = feature.get('energy', 0)
        valence = feature.get('valence', 0)
        if (energy_min <= energy <= energy_max) and (valence_min <= valence <= valence_max):
            filtered_tracks.append(feature['id'])

    print(f"Number of tracks matching the mood '{mood}': {len(filtered_tracks)}")

    if not filtered_tracks:
        print(f"No tracks matched the mood '{mood}'.")
        return

    filtered_tracks = filtered_tracks[:8]  # Limit to 8 songs

    try:
        user_id = sp.current_user()['id']
        playlist_name = f"{mood.capitalize()} Playlist"
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        print(f"Created playlist: {playlist_name}")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error while creating playlist: {e}")
        return

    try:
        sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=filtered_tracks)
        print(f"Added {len(filtered_tracks)} tracks to '{playlist_name}'.\n")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error while adding tracks to playlist: {e}")

if __name__ == "__main__":
    mood = input("Enter the mood (happy, sad, calm, energetic): ").lower()
    get_mood_playlist(mood)