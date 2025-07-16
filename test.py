import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")

response = requests.get(
    "https://api.elevenlabs.io/v1/user",
    headers={"xi-api-key": api_key}
)
print(response.json())  # Should show your account info

voice_id = "IKne3meq5aSn9XLyUdCD"  # Test one ID
response = requests.get(
    f"https://api.elevenlabs.io/v1/voices/{voice_id}",
    headers={"xi-api-key": api_key}
)
print(response.json())  # Should show voice details