#Spawn point configuration manager.
#Allows editing of spawn locations for the player and other entities.

import json
import os


class SpawnConfig:
    #Manages spawn point configuration for the game.#
    
    DEFAULT_CONFIG = {
        "player": {
            "x": 180,
            "y": 120,
            "name": "Player spawn point"
        },
        "world": {
            "width": 15360,
            "height": 8640,
            "name": "World dimensions"
        },
        "layers": {
            "ground": {
                "enabled": True,
                "parallax_factor": 1.0
            },
            "wall": {
                "enabled": True,
                "parallax_factor": 1.0
            },
            "misc": {
                "enabled": True,
                "parallax_factor": 1.0
            },
            "skybox": {
                "enabled": True,
                "parallax_factor": 0
            }
        }
    }
    
    def __init__(self, config_path=None):
        #Initialize spawn config from file or use defaults.
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'spawn_config.json')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        #Load config from file or create new one with defaults.
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Error loading config from {self.config_path}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create config file with defaults
            self.save_config()
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        #Save current config to file.
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Config saved to {self.config_path}")
        except IOError as e:
            print(f"Error saving config to {self.config_path}: {e}")
    
    def get_player_spawn(self):
        #Get player spawn point.
        spawn = self.config.get("player", self.DEFAULT_CONFIG["player"])
        return spawn.get("x", 180), spawn.get("y", 120)
    
    def set_player_spawn(self, x, y):
        #Set player spawn point.
        if "player" not in self.config:
            self.config["player"] = {}
        self.config["player"]["x"] = x
        self.config["player"]["y"] = y
        self.save_config()
    
    def get_world_size(self):
        #Get world dimensions.
        world = self.config.get("world", self.DEFAULT_CONFIG["world"])
        return world.get("width", 15360), world.get("height", 8640)
    
    def get_layer_config(self, layer_name):
        #Get configuration for a specific layer.
        layers = self.config.get("layers", self.DEFAULT_CONFIG["layers"])
        return layers.get(layer_name, {"enabled": True, "parallax_factor": 1.0})
