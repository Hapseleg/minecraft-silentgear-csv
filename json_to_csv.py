import json
import csv
import os

def json_to_csv(json_dir, csv_file):
    """Loads JSON files, extracts properties, and writes to CSV."""

    all_data = []

    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(json_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    if isinstance(data, list):
                        for item in data:
                            extracted_data = extract_properties(item)
                            if extracted_data:
                                all_data.append(extracted_data)
                    elif isinstance(data, dict):
                        extracted_data = extract_properties(data)
                        if extracted_data:
                            all_data.append(extracted_data)
                    else:
                        print(f"Warning: JSON in {filename} is not a list or dictionary. Skipping.")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {filename}: {e}")
            except Exception as e:
                print(f"An error occurred processing {filename}: {e}")

    if all_data:
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = all_data[0].keys() if all_data else []
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)
            print(f"Data from JSON files written to {csv_file}")
        except Exception as e:
            print(f"Error writing to CSV: {e}")
    else:
        print("No valid JSON data found in the directory.")


def extract_properties(data):
    """Extracts properties, including 'translate', 'tag', splits 'traits' and 'categories'."""
    try:
        availability = data.get("availability", {})
        stats = data.get("stats", {}).get("main", {})
        rod_stats = data.get("stats", {}).get("rod", {})
        name = data.get("name", {})
        traits = data.get("traits", {}).get("main", [])
        rod_traits = data.get("traits", {}).get("rod", [])
        categories = availability.get("categories", [])
        crafting_items = data.get("crafting_items", {}).get("main", {})

        extracted = {
            "name": name.get("translate"),
            "tier": availability.get("tier"),
            "rarity": stats.get("rarity"),
            "crafting_items": crafting_items.get("tag"),
            "charging_value": stats.get("charging_value"),
            "durability": stats.get("durability"),
            "armor": stats.get("armor"),
            "armor_durability": stats.get("armor_durability"),
            "enchantment_value": stats.get("enchantment_value"),
            "harvest_level": stats.get("harvest_level"),
            "harvest_speed": stats.get("harvest_speed"),
            "melee_damage": stats.get("melee_damage"),
            "magic_damage": stats.get("magic_damage"),
            "attack_speed": stats.get("attack_speed"),
            "armor/helmet": stats.get("armor/helmet"),
            "armor/chestplate": stats.get("armor/chestplate"),
            "armor/leggings": stats.get("armor/leggings"),
            "armor/boots": stats.get("armor/boots"),
            "armor_toughness": stats.get("armor_toughness"),
            "ranged_damage": stats.get("ranged_damage"),
            "ranged_speed": stats.get("ranged_speed"),
            "rod_durability_multiplier": rod_stats.get("durability", {}).get("mul2"),
            "rod_rarity": rod_stats.get("rarity"),
            "rod_ranged_damage_multiplier": rod_stats.get("ranged_damage", {}).get("mul2"),

        }

        # Replace "material.silentgear." in "translate"
        if extracted.get("name"):
            extracted["name"] = extracted["name"].replace("material.silentgear.", "")

        max_traits = 3  # Adjust if needed
        for i in range(max_traits):
            trait_name = traits[i].get("name") if i < len(traits) else None
            trait_level = traits[i].get("level") if i < len(traits) else None
            extracted[f"main_trait_{i+1}"] = trait_name
            extracted[f"main_trait_level_{i+1}"] = trait_level

        max_categories = 2  # Adjust if needed
        for i in range(max_categories):
            category_name = categories[i] if i < len(categories) else None
            extracted[f"main_category_{i+1}"] = category_name
        

        max_rod_traits = 3  # Adjust if needed
        for i in range(max_rod_traits):
            trait_name = rod_traits[i].get("name") if i < len(rod_traits) else None
            trait_level = rod_traits[i].get("level") if i < len(rod_traits) else None
            extracted[f"rod_trait_{i+1}"] = trait_name
            extracted[f"rod_trait_level_{i+1}"] = trait_level

        return extracted
    except Exception as e:
        print(f"Error extracting properties: {e}")
        return None


# Example usage:
json_directory = "C:/Users/Hapse/Documents/vsc/python/files/json_to_csv/"  # Replace with the actual path
output_csv = "output.csv"  # Replace with the desired output CSV file name
json_to_csv(json_directory, output_csv)