import json
import os

class GameLogic:
    def __init__(self, save_file='savegame.json'):
        self.save_file = save_file
        self.eggs = 0
        self.load()

    def click(self):
        self.eggs += 1
        self.save()

    def save(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump({'eggs': self.eggs}, f)
        except Exception as e:
            print(f"Error saving: {e}")

    def load(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.eggs = data.get('eggs', 0)
            except Exception as e:
                print(f"Error loading: {e}")
                self.eggs = 0
        else:
            self.eggs = 0
