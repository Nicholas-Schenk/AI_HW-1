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
    def from_set(State):
        state = State(State[0])
        state.f_value = State[1]
        state.g_cost = State[2]
        state.search = State[3]
        state.prev = State[4]
        return state

    def to_set(self):
        return [self.pos, self.f_value, self.g_cost, self.search, self.prev]

    def to_string(self):
        return "[" + str(self.pos) + ", " + str(self.f_value) + ", " + str(self.g_cost) + ", " + str(self.search) + ", " + str(self.prev) + "]"