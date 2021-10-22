class State:
    pos = []
    f_value = 0
    g_cost = 0
    search = 0
    prev = None

    #default constructor that takes in the state's position
    def __init__(self, pos):
        self.pos = pos
    
    #create State object from a set containing raw State info
    def from_set(state_set):
        state = State(state_set[0])
        state.f_value = state_set[1]
        state.g_cost = state_set[2]
        state.search = state_set[3]
        state.prev = state_set[4]
        return state

    def to_set(self):
        return [self.pos, self.f_value, self.g_cost, self.search, self.prev]

    def to_string(self) -> str:
        return "[pos=" + str(self.pos) + ", f=" + str(self.f_value) + ", g=" + str(self.g_cost) + ", s=" + str(self.search) + "]"