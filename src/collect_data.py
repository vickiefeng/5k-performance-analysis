import os
from datetime import datetime
import requests 
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("rsu_api_reg")
API_SECRET = os.getenv("X-RSU-API-REG-SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError(
        "Could not find RunSignup API credentials. Check .env file."
        )


def get_race_data(race_id):
    """
    Fetch metadata and event information for a RunSignup race.

    Args:
        race_id (int): RunSignup race identifier

    Returns:
        dict: Race metadata and associated event information
    """
    url = f"https://api.runsignup.com/rest/race/{race_id}"

    params = {
        "rsu_api_reg": API_KEY,
        "format": "json",
    }

    headers = {
        "X-RSU-API-REG-SECRET": API_SECRET
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    return data["race"]


def is_5k_distance(distance):
    """
    Check whether a race distance represents a 5K.

    Args:
        distance (str): Distance value reported by RunSignup

    Returns:
        bool: True if the distance represents a 5K, otherwise False
    """
    if not distance:
        return False
    
    distance = distance.strip().lower()

    return distance in ["5k", "3.1 miles", "3.11 miles"]


def get_completed_5k_events(events):
    """
    Filter race events to completed, in-person 5K running events.

    Args:
        events (list): Event records associated with a RunSignup race

    Returns:
        list: Completed 5K running events
    """
    completed_5ks = []

    for event in events:
        event_date = datetime.strptime(
            event["start_time"], "%m/%d/%Y %H:%M"
        )

        if (
            is_5k_distance(event["distance"])
            and event ["event_type"] == "running_race"
            and event_date < datetime.now()
        ):
            completed_event = event.copy()
            completed_event["event_date"] = event_date
            completed_5ks.append(completed_event)

    return completed_5ks


def get_race_results(race_id, event_id):
    """
    Fetch all available results for a RunSignup event using pagination.

    Args:
        race_id (int): RunSignup race identifier
        event_id (int): RunSignup event identifier

    Returns:
        list: Result records of participants across all available result pages
    """
    url = f"https://api.runsignup.com/rest/race/{race_id}/results/get-results"

    params = {
        "rsu_api_reg": API_KEY,
        "format": "json",
        "event_id": event_id,
        "page": 1,
        "results_per_page": 100,
        "include_total_finishers": "T"
    }

    headers = {
        "X-RSU-API-REG-SECRET": API_SECRET
    }

    all_results = []
    page = 1

    while True:
        params["page"] = page

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status

        data = response.json()

        if not data["individual_results_sets"]:
            return []
        
        result_set = data["individual_results_sets"][0]
        results = result_set["results"]

        all_results.extend(results)

        if len(results) < params["results_per_page"]:
            break

        page += 1

    return all_results