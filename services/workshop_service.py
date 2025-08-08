import requests

API_URL = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

def fetch_mod_details(mod_id):
    """Fetch mod title and update time from Steam Workshop. Returns dict or None."""
    try:
        payload = {
            "itemcount": 1,
            "publishedfileids[0]": str(mod_id)
        }
        resp = requests.post(API_URL, data=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        details = data.get("response", {}).get("publishedfiledetails", [])
        if not details:
            return None
        mod_info = details[0]
        if mod_info.get("result") != 1:
            return None
        return {
            "name": mod_info.get("title", f"Mod {mod_id}"),
            "updated": mod_info.get("time_updated", None)
        }
    except Exception as e:
        print(f"[workshop_service] Failed to fetch details for {mod_id}: {e}")
        return None
