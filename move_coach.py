class MoveCoach:
    def generate_advice(self, moves):
        advice = []
        for move in moves:
            if move == "Jab":
                advice.append("Move right and parry left. Counter with right cross.")
            elif move == "Cross":
                advice.append("Slip left, block with right hand. Counter with left hook.")
            elif move == "Hook":
                advice.append("Duck down and right. Counter with right uppercut.")
            elif move == "Uppercut":
                advice.append("Step back and push opponent's arm down. Counter with straight right.")
            elif move == "Front Kick":
                advice.append("Step left and parry kick down with right hand. Counter with left cross.")
            elif move == "Roundhouse Kick":
                advice.append("Step in and block with left arm. Counter with right low kick.")
        
        if not advice:
            advice.append("Stay alert, keep guard up, and look for openings.")
        
        return " | ".join(advice)