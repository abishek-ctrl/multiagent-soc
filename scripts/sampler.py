# Balanced CICIDS Dataset Sampler
import pandas as pd
import json
import random
import math

def get_balanced_attack_samples(file: str, n_samples: int = 250, output_file: str = None) -> None:
    try:
        df = pd.read_csv(file)
        df = df.replace([float('inf'), float('-inf')], pd.NA).dropna(how='any')

        if 'Label' not in df.columns:
            print(json.dumps({"error": "CSV must contain a 'Label' column."}, indent=2))
            return

        labels = df['Label'].unique()
        n_labels = len(labels)
        samples_per_label = math.ceil(n_samples / n_labels)

        samples_list = []
        for label in labels:
            label_df = df[df['Label'] == label]
            num_to_sample = min(len(label_df), samples_per_label)
            if num_to_sample > 0:
                samples_list.append(label_df.sample(n=num_to_sample, random_state=42))

        balanced_df = pd.concat(samples_list).reset_index(drop=True)
        final_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True).head(n_samples)

        if output_file:
            final_df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"Successfully saved {len(final_df)} balanced samples to '{output_file}'")
        else:
            print(json.dumps(final_df.to_dict(orient='records'), indent=2, ensure_ascii=False))

    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {file}. Please ensure it's in the correct 'data' folder."}, indent=2))
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}, indent=2))

csv_file = "data/friday.csv"
output_sampled_csv = "friday_sampled.csv"
get_balanced_attack_samples(csv_file, n_samples=250, output_file=output_sampled_csv)