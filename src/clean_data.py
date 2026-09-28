import pandas as pd


def time_to_seconds(time):
    """
    Convert a finish-time string to total seconds.

    Args:
        time (str): Finish time in MM:SS or HH:MM:SS format

    Returns:
        float or None: Finish time in seconds, or None if the input is missing
    """
    if pd.isna(time):
        return None
    
    parts = time.split(":")

    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return (int(hours) * 3600 + int(minutes) * 60 + float(seconds))
    
    return None


def clean_race_results(results, race_id, event_id):
    """
    Clean raw RunSignup results for a single 5K event.

    Args:
        results (list): Raw participant result records from the RunSignup API
        race_id (int): RunSignup identifier for the parent race
        event_id (int): RunSignup identifier for the specific 5K event

    Returns:
        pandas.DataFrame: Cleaned event results with standardized missing
        values, numeric finish times, numeric age percentages, and race/event 
        identifiers
    """
    df = pd.DataFrame(results)

    analysis_df = df[[
        "result_id", 
        "place",
        "gender",
        "age",
        "chip_time",
        "pace",
        "age_percentage"
    ]].copy()

    # Convert empty strings to missing values
    analysis_df["chip_time"] = (
        analysis_df["chip_time"].replace("", pd.NA))

    analysis_df["age_percentage"] = (
        analysis_df["age_percentage"]).replace("", pd.NA)
    
    # Convert finish times to seconds and minutes
    analysis_df["chip_time_seconds"] = (
        analysis_df["chip_time"].apply(time_to_seconds))
    
    analysis_df["chip_time_minutes"] = (
        analysis_df["chip_time_seconds"] / 60)
    
    # Convert age percentage from strings to numeric
    analysis_df["age_percentage_numeric"] = pd.to_numeric(
        analysis_df["age_percentage"].str.rstrip("%"),
        errors="coerce")
    
    # Standardize numeric columns as nullable floats to preserve missing 
    # values.
    analysis_df["chip_time_seconds"] = (
        analysis_df["chip_time_seconds"].astype("Float64")
    )

    analysis_df["chip_time_minutes"] = (
        analysis_df["chip_time_minutes"].astype("Float64")
    )

    analysis_df["age_percentage_numeric"] = (
        analysis_df["age_percentage_numeric"].astype("Float64")
    )

    # Treat identified invalid/placeholder ages as missing
    invalid_age = analysis_df["age"].isin([99, 125])

    analysis_df.loc[invalid_age, [
        "age", "age_percentage", "age_percentage_numeric"]] = pd.NA
    
    analysis_df["race_id"] = race_id
    analysis_df["event_id"] = event_id

    return analysis_df