import json

def get_unique_attack_pattern_names(json_file_path):
    """
    Reads a JSON file, extracts all unique 'name' values
    specifically for objects with "type": "attack-pattern",
    and returns them along with their count.

    Args:
        json_file_path (str): The path to the enterprise-attack.json file.

    Returns:
        tuple: A tuple containing:
               - count (int): The number of unique 'name' values for attack-pattern objects.
               - unique_names (set): A set of all unique 'name' values for attack-pattern objects.
    """
    unique_names = set()

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "objects" in data and isinstance(data["objects"], list):
            for obj in data["objects"]:
                if obj.get("type") == "attack-pattern" and "name" in obj:
                    unique_names.add(obj["name"])

    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{json_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return len(unique_names), unique_names

if __name__ == "__main__":
    file_path = "data\enterprise-attack.json" # Make sure this file is in the same directory as your script

    count, names = get_unique_attack_pattern_names(file_path)

    print(f"Number of unique names under 'type': 'attack-pattern': {count}")
    print("\n--- Unique Attack Pattern Names ---")
    if names:
        for name in sorted(list(names)):
            print(name)
    else:
        print("No attack pattern names found.")