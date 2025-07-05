import json
import os
import threading
import time
from rebirth import Rebirth  # add this import

class GameLogic:
    def __init__(self, save_file='savegame.json'):
        self.save_file = save_file
        self.eggs = 0
        self.autoclickers = 0
        self.autoclicker_cost = 10
        self.click_power = 1
        self.click_upgrade_cost = 15
        self.autoclicker_running = False
        self.tutorial_completed = False
        self.rebirth = Rebirth()  # add rebirth object
        self.load()

    def click(self):
        # Multiply eggs gained by rebirth multiplier
        self.eggs += self.click_power * self.rebirth.get_multiplier()
        self.save()

    def buy_autoclicker(self):
        if self.eggs >= self.autoclicker_cost:
            self.eggs -= self.autoclicker_cost
            self.autoclickers += 1
            self.autoclicker_cost = int(self.autoclicker_cost * 1.5)
            self.save()
            if not self.autoclicker_running:
                self.start_autoclicker()
            return True
        return False

    def buy_click_upgrade(self):
        if self.eggs >= self.click_upgrade_cost:
            self.eggs -= self.click_upgrade_cost
            self.click_power += 1
            self.click_upgrade_cost = int(self.click_upgrade_cost * 2)
            self.save()
            return True
        return False

    def rebirth_purchase(self):
        if self.eggs >= 500:
            # Reset progress
            self.eggs = 0
            self.autoclickers = 0
            self.autoclicker_cost = 10
            self.click_power = 1
            self.click_upgrade_cost = 15
            # Apply rebirth multiplier doubling and increment count
            self.rebirth.apply_rebirth()
            self.save()
            if not self.autoclicker_running:
                self.start_autoclicker()
            return True
        return False

    def reset_all_progress(self):
        self.eggs = 0
        self.autoclickers = 0
        self.autoclicker_cost = 10
        self.click_power = 1
        self.click_upgrade_cost = 15
        self.tutorial_completed = False
        self.rebirth = Rebirth()  # reset rebirth count & multiplier
        self.save()

    def start_autoclicker(self):
        self.autoclicker_running = True
        thread = threading.Thread(target=self._autoclick_loop, daemon=True)
        thread.start()

    def _autoclick_loop(self):
        while True:
            time.sleep(1)
            # Autoclicker also multiplied by rebirth multiplier
            self.eggs += self.autoclickers * self.rebirth.get_multiplier()
            self.save()

    def save(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump({
                    'eggs': self.eggs,
                    'autoclickers': self.autoclickers,
                    'autoclicker_cost': self.autoclicker_cost,
                    'click_power': self.click_power,
                    'click_upgrade_cost': self.click_upgrade_cost,
                    'tutorial_completed': self.tutorial_completed,
                    'rebirth_multiplier': self.rebirth.get_multiplier(),  # save multiplier
                    'rebirth_count': self.rebirth.get_count()             # save count
                }, f)
        except Exception as e:
            print(f"Error saving: {e}")

    def load(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.eggs = data.get('eggs', 0)
                    self.autoclickers = data.get('autoclickers', 0)
                    self.autoclicker_cost = data.get('autoclicker_cost', 10)
                    self.click_power = data.get('click_power', 1)
                    self.click_upgrade_cost = data.get('click_upgrade_cost', 15)
                    self.tutorial_completed = data.get('tutorial_completed', False)
                    multiplier = data.get('rebirth_multiplier', 1)
                    count = data.get('rebirth_count', 0)
                    self.rebirth = Rebirth(multiplier, count)
            except Exception as e:
                print(f"Error loading: {e}")
                self.eggs = 0
                self.autoclickers = 0
                self.autoclicker_cost = 10
                self.click_power = 1
                self.click_upgrade_cost = 15
                self.tutorial_completed = False
                self.rebirth = Rebirth()
        else:
            self.eggs = 0
            self.autoclickers = 0
            self.autoclicker_cost = 10
            self.click_power = 1
            self.click_upgrade_cost = 15
            self.tutorial_completed = False
            self.rebirth = Rebirth()

        if self.autoclickers > 0:
            self.start_autoclicker()
