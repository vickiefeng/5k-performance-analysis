from src.build_dataset import build_5k_dataset
from src.build_database import build_database


def main():
    """Run the complete data pipeline and build the SQLite database."""  
    race_ids = [60883, 105951, 151599, 44857, 38168, 62492]

    race_df, events_df, results_df = build_5k_dataset(race_ids)

    conn = build_database(
        race_df, events_df, results_df,
        "data/processed/5k_performance.db")

    conn.close()

if __name__ == "__main__":
    main()