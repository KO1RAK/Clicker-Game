class Goal:
    def __init__(self, initial_goal=500):
        self.current_goal = initial_goal

    def double_goal(self):
        self.current_goal *= 2

    def reset_goal(self):
        self.current_goal = 500

    def get_goal(self):
        return self.current_goal

    def to_dict(self):
        return {"goal_target": self.current_goal}

    def load_from_dict(self, data):
        self.current_goal = data.get("goal_target", 500)
