class StateMachine:
    def __init__(self):
        self.current_state = "neutral"
        self.move_buffer = []
        
    def update_state(self, moves):
        self.move_buffer.append(moves)
        if len(self.move_buffer) > 5:
            self.move_buffer.pop(0)
        
        if "Punch" in moves:
            self.current_state = "punching"
        elif "Block" in moves:
            self.current_state = "blocking"
        elif "Kick" in moves:
            self.current_state = "kicking"
        else:
            self.current_state = "neutral"
        
        # Add more complex state transitions here if needed