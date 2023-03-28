import pickle
import requests

with open("playlist_artists.pickle", "rb") as f:
    playlist_artists = pickle.load(f)


def get_artist_id(api_key, artist_name):
    url = f"https://api.setlist.fm/rest/1.0/search/artists?artistName={artist_name}&p=1&sort=relevance"
    headers = {"Accept": "application/json", "x-api-key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["total"] > 0:
        return data["artist"][0]["mbid"]
    else:
        return None


def get_upcoming_concerts(api_key, artist_id):
    url = f"https://api.setlist.fm/rest/1.0/artist/{artist_id}/setlists"
    headers = {"Accept": "application/json", "x-api-key": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["total"] > 0:
        events = [
            {
                "title": event["eventDate"],
                "date": event["eventDate"],
                "venue": event["venue"]["name"],
                "location": f"{event['venue']['city']['name']}, {event['venue']['city']['country']['code']}",
            }
            for event in data["setlist"]
        ]
        return events
    else:
        return []


def main():
    artist_name = input("Enter artist name: ")
    api_key = "YOUR_SETLIST_FM_API_KEY"

    artist_id = get_artist_id(api_key, artist_name)

    if artist_id:
        concerts = get_upcoming_concerts(api_key, artist_id)
        if concerts:
            print(f"Upcoming concerts for {artist_name}:")
            for concert in concerts:
                print(
                    f"{concert['title']} - {concert['date']} - {concert['venue']} - {concert['location']}"
                )
        else:
            print(f"No upcoming concerts found for {artist_name}.")
    else:
        print(f"Artist {artist_name} not found.")


if __name__ == "__main__":
    main()
