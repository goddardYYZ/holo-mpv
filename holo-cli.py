import requests
import subprocess

# Your Holodex API key
HOLODEX_API_KEY = "64eac75c-d7dd-44fc-b6b1-addbe3961b10"

# Holodex API endpoint for live streams
HOLODEX_API_URL = "https://holodex.net/api/v2/live"

# Headers including API key for authentication
HEADERS = {
    "X-APIKEY": HOLODEX_API_KEY,
    "User-Agent": "Mozilla/5.0"
}

def get_live_hololive_streams():
    """Fetch live Hololive VTuber streams."""
    params = {"org": "Hololive", "limit": 20, "status": "live"}
    response = requests.get(HOLODEX_API_URL, params=params, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ ERROR: {response.status_code} - {response.text}")
        return []

    streams = response.json()
    return [(stream["channel"]["name"], stream["id"], stream["title"]) for stream in streams if stream["status"] == "live"]

def open_in_mpv(video_id):
    """Open live stream in MPV."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    subprocess.run(["mpv", url])

def main():
    live_streams = get_live_hololive_streams()

    if not live_streams:
        print("⚠️ No live Hololive VTubers at the moment.")
        return

    print("\n🎥 Live Hololive VTubers:\n")
    for idx, (name, _, title) in enumerate(live_streams, start=1):
        print(f"{idx}. {name} - {title}")

    choice = input("\nEnter the number of the stream to open (or press Enter to exit): ")
    
    if not choice.isdigit():
        print("🚪 Exiting...")
        return
    
    choice = int(choice)
    if 1 <= choice <= len(live_streams):
        _, video_id, _ = live_streams[choice - 1]
        print(f"🎬 Opening {live_streams[choice - 1][0]}'s stream...")
        open_in_mpv(video_id)
    else:
        print("❌ Invalid selection!")

if __name__ == "__main__":
    main()
