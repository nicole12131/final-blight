# Data Management Module for RPG Character Manager - handles CSV export/import and data persistence

import csv
import os
import json
import sys
from datetime import datetime
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from character import Character, CharacterRoster

class DataManager:
    # Handles saving, loading, and exporting character data.
    
    def __init__(self, data_dir="character_data"):
        # Initialize data manager with data directory.
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        self.csv_file = os.path.join(data_dir, "characters.csv")
        self.backup_dir = os.path.join(data_dir, "backups")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def export_to_csv(self, roster, filename=None):
        # Export character roster to CSV file.
        #
        # Args:
        #     roster: CharacterRoster object
        #     filename: Optional custom filename
        #
        # Returns:
        #     Filename if successful, None otherwise
        if filename is None:
            filename = self.csv_file
        
        try:
            df = roster.get_dataframe()
            df.to_csv(filename, index=False)
            print(f"Roster exported to: {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def import_from_csv(self, filename=None):
        # Import characters from CSV file.
        #
        # Args:
        #     filename: CSV file to import from
        #
        # Returns:
        #     CharacterRoster object with imported characters
        if filename is None:
            filename = self.csv_file
        
        roster = CharacterRoster()
        
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return roster
        
        try:
            df = pd.read_csv(filename)
            
            for _, row in df.iterrows():
                # Extract basic info
                name = row['Name']
                race = row['Race']
                char_class = row['Class']
                level = int(row['Level'])
                
                # Extract attributes
                attributes = {}
                for col in df.columns:
                    if col not in ['Name', 'Race', 'Class', 'Level', 'skills_count']:
                        try:
                            attributes[col] = int(row[col])
                        except (ValueError, TypeError):
                            pass
                
                # Create character
                character = Character(name, race, char_class, level, attributes)
                roster.add_character(character)
            
            print(f" Imported {len(roster)} characters from: {filename}")
            return roster
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return roster
    
    def export_to_detailed_csv(self, roster, filename=None):
        # Export detailed character information including skills and inventory.
        #
        # Args:
        #     roster: CharacterRoster object
        #     filename: Optional custom filename
        #
        # Returns:
        #     Filename if successful, None otherwise
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.data_dir, f"characters_detailed_{timestamp}.csv")
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Name', 'Race', 'Class', 'Level', 'Skills', 'Total_Stats', 'Created_Date']
                fieldnames.extend(['MP', 'HP', 'Str', 'Atk', 'Def', 'Mag', 'Spr', 'Acc', 'Spd', 'Evs'])
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for character in roster:
                    row = {
                        'Name': character.name,
                        'Race': character.race,
                        'Class': character.char_class,
                        'Level': character.level,
                        'Skills': '; '.join(character.skills),
                        'Total_Stats': character.get_total_stats(),
                        'Created_Date': character.created_date.strftime('%Y-%m-%d'),
                    }
                    row.update(character.attributes)
                    writer.writerow(row)
            
            print(f"✓ Detailed roster exported to: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Error exporting detailed CSV: {e}")
            return None
    
    def export_to_json(self, roster, filename=None):
        # Export character roster to JSON format.
        #
        # Args:
        #     roster: CharacterRoster object
        #     filename: Optional custom filename
        #
        # Returns:
        #     Filename if successful, None otherwise
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.data_dir, f"characters_{timestamp}.json")
        
        try:
            data = {
                'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_characters': len(roster),
                'characters': []
            }
            
            for character in roster:
                char_data = {
                    'name': character.name,
                    'race': character.race,
                    'class': character.char_class,
                    'level': character.level,
                    'attributes': character.attributes,
                    'skills': list(character.skills),
                    'created_date': character.created_date.strftime('%Y-%m-%d %H:%M:%S')
                }
                data['characters'].append(char_data)
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"Roster exported to JSON: {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None
    
    def import_from_json(self, filename):
        # Import characters from JSON file.
        #
        # Args:
        #     filename: JSON file to import from
        #
        # Returns:
        #     CharacterRoster object with imported characters
        roster = CharacterRoster()
        
        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return roster
        
        try:
            with open(filename, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
            
            for char_data in data.get('characters', []):
                character = Character(
                    name=char_data['name'],
                    race=char_data['race'],
                    char_class=char_data['class'],
                    level=char_data['level'],
                    attributes=char_data.get('attributes', {}),
                    skills=set(char_data.get('skills', []))
                )
                roster.add_character(character)
            
            print(f"✓ Imported {len(roster)} characters from JSON: {filename}")
            return roster
        except Exception as e:
            print(f"✗ Error importing from JSON: {e}")
            return roster
    
    def create_backup(self, roster):
        # Create a timestamped backup of current roster.
        #
        # Args:
        #     roster: CharacterRoster to backup
        #
        # Returns:
        #     Path to backup file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
        return self.export_to_json(roster, backup_file)
    
    def list_backups(self):
        # List all available backup files.
        backups = []
        if os.path.exists(self.backup_dir):
            backups = sorted(os.listdir(self.backup_dir))
        return backups
    
    def restore_from_backup(self, backup_filename):
        # Restore roster from a backup file.
        #
        # Args:
        #     backup_filename: Name of backup file (not full path)
        #
        # Returns:
        #     CharacterRoster object restored from backup
        backup_path = os.path.join(self.backup_dir, backup_filename)
        return self.import_from_json(backup_path)
    
    def validate_character_data(self, character):
        # Validate character data integrity.
        #
        # Args:
        #     character: Character object to validate
        #
        # Returns:
        #     Tuple of (is_valid, error_message)
        errors = []
        
        if not character.name or not isinstance(character.name, str):
            errors.append("Invalid character name")
        
        if character.race not in ["Human", "Dragonborn", "Halfling", "Elf", "Ogre", "Dwarf", "Tiefling"]:
            errors.append("Invalid race")
        
        if character.char_class not in ["Black Mage", "Warrior", "Thief", "White Mage"]:
            errors.append("Invalid class")
        
        if not isinstance(character.level, int) or character.level < 1 or character.level > 99:
            errors.append("Invalid level (must be 1-99)")
        
        if not isinstance(character.attributes, dict):
            errors.append("Invalid attributes structure")
        
        return (len(errors) == 0, "; ".join(errors) if errors else "Valid")
    
    def export_analysis_report(self, roster, analyzer, filename=None):
        # Export statistical analysis report to text file.
        #
        # Args:
        #     roster: CharacterRoster object
        #     analyzer: StatisticalAnalyzer object
        #     filename: Optional custom filename
        #
        # Returns:
        #     Filename if successful, None otherwise
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.data_dir, f"analysis_report_{timestamp}.txt")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(analyzer.generate_statistical_report())
            
            print(f"✓ Analysis report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Error saving report: {e}")
            return None
