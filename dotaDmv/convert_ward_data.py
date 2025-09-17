# Query used for fetching wards data
# replace the $matchID for real value
"""
query {
  match(id: $matchID){
    id
    playbackData{
      wardEvents {
        indexId
        time
        positionX
        positionY
        fromPlayer
        wardType
        action
        playerDestroyed
      }
    }
  }
}
"""

import json
import csv
import os
from pathlib import Path

def process_ward_events(json_file_path, csv_writer):
    """Process ward events from a JSON file and write to CSV."""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract match ID from the data
    match_id = data['data']['match']['id']
    
    # Extract ward events
    ward_events = data['data']['match']['playbackData']['wardEvents']
    
    # Process each ward event
    for event in ward_events:
        # Replace null values with 'NULL' string
        processed_event = {}
        for key, value in event.items():
            if value is None:
                processed_event[key] = 'NULL'
            else:
                processed_event[key] = value
        
        # Add match_id column
        processed_event['match_id'] = match_id
        
        # Add isRadiant column (True if fromPlayer is between 0-4)
        processed_event['isRadiant'] = 0 <= event['fromPlayer'] <= 4 if event['fromPlayer'] is not None else False
        
        # Write to CSV
        csv_writer.writerow(processed_event)

def main():
    # Directory containing JSON files
    json_dir = Path('ward-data/ti2025-xg-falcon')
    
    # Output CSV file
    output_file = 'ward_events.csv'
    
    # Get all JSON files in the directory
    json_files = list(json_dir.glob('*.json'))
    
    if not json_files:
        print("No JSON files found in the directory.")
        return
    
    # Collect all unique field names to ensure consistent CSV columns
    all_fieldnames = {'match_id', 'isRadiant'}  # Start with our added fields
    
    # First pass: collect all possible field names
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            ward_events = data['data']['match']['playbackData']['wardEvents']
            for event in ward_events:
                all_fieldnames.update(event.keys())
    
    # Convert to sorted list for consistent column ordering
    fieldnames = sorted(list(all_fieldnames))
    
    # Second pass: write data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each JSON file
        for json_file in json_files:
            print(f"Processing {json_file}...")
            process_ward_events(json_file, writer)
    
    print(f"Successfully processed {len(json_files)} files.")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()