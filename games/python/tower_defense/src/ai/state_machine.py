class State:
    def enter(self, owner):
        pass

    def update(self, owner, dt):
        pass

    def exit(self, owner):
        pass


class StateMachine:
    def __init__(self, owner):
        self.owner = owner
        self.states = []
        self.current_state = None

    def push_state(self, state):
        if self.current_state:
            self.current_state.exit(self.owner)
        self.states.append(state)
        self.current_state = state
        self.current_state.enter(self.owner)

    def pop_state(self):
        if self.current_state:
            self.current_state.exit(self.owner)
        if self.states:
            self.states.pop()
        self.current_state = self.states[-1] if self.states else None
        if self.current_state:
            self.current_state.enter(self.owner)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(self.owner, dt)
