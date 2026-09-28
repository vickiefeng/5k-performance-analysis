import pandas as pd

from src.collect_data import (
    get_race_data,
    get_completed_5k_events,
    get_race_results,
)
from src.clean_data import clean_race_results


def build_5k_dataset(race_ids):
    """
    Build datasets from selected RunSignup races.

    Args:
        race_ids (list): RunSignup race identifiers to include

    Returns:
        tuple: Three pandas DataFrames containing race metadata,
        event metadata, and cleaned participant results
    """
    race_records = []
    event_records = []
    result_dfs = []

    for race_id in race_ids:
        # Race metadata
        race = get_race_data(race_id)
        events = race["events"]
        address = race["address"]

        race_records.append({
            "race_id": race["race_id"],
            "race_name": race["name"],
            "city": address["city"],
            "state": address["state"],
            "country_code": address["country_code"],
            "timezone": race["timezone"]
        })

        # Find completed 5k events
        completed_5ks = get_completed_5k_events(events)

        for event in completed_5ks:
            event_id = event["event_id"]
            results = get_race_results(race_id, event_id)

            # Skip events with no RunSignup results
            if not results:
                continue

            event_records.append({
                "event_id": event_id,
                "race_id": race_id,
                "event_name": event["name"],
                "event_date": event["event_date"],
                "distance_km": 5.0
            })

            # Runner results
            cleaned_df = clean_race_results(results, race_id, event_id)
            result_dfs.append(cleaned_df)

    races_df = pd.DataFrame(race_records)
    events_df = pd.DataFrame(event_records)
    results_df = pd.concat(result_dfs, ignore_index=True)

    return races_df, events_df, results_df