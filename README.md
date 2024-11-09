# Assessment2

Install the required dependencies:
Copy
pip install spotipy



Obtain Spotify API credentials:
Create a Spotify Developer account and register a new application.
Copy the CLIENT_ID and CLIENT_SECRET values from the application dashboard.
Set the REDIRECT_URI to http://localhost:8888/callback.


Usage
Run the script:
Copy
python spotify_mood_playlist.py


Enter the desired mood when prompted (happy, sad, calm, or energetic).
The script will create a new public playlist with 8 songs that match the specified mood.


Code Structure
The script is organized as follows:

Imports the necessary libraries and sets up the Spotify API credentials.
Defines functions to print the granted scopes, retrieve the user's profile, fetch audio features in batches, and create a mood-based playlist.
The main part of the script prompts the user for a mood and calls the get_mood_playlist() function.


Original Code Contribution
All the code in this project is my original work, with the exception of the Spotipy library, which is a third-party library used to interact with the Spotify API.

Project Journal and Reflection
I have maintained a detailed project journal throughout the development of this prototype, documenting my learnings, challenges, and insights. I have referenced key entries from the journal in my written reflection, which demonstrates how this project has developed my code literacy.

Future Improvements
Potential areas for future improvement include:

Allowing users to customise the mood settings or create their own mood profiles.
Integrating machine learning algorithms to improve the accuracy of the mood-based playlist generation.
Expanding the functionality to allow users to save or share their generated playlists.


References and Acknowledgments
Spotipy library: https://spotipy.readthedocs.io/en/2.19.0/
Spotify Web API documentation: https://developer.spotify.com/documentation/web-api/
