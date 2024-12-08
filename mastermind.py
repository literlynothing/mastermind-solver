class MastermindSolver:
    def __init__(self, colors):
        self.colors = colors
        self.possible_codes = self._generate_all_possibilities()
        self.current_guess = None

    def _generate_all_possibilities(self):
        from itertools import product
        return list(product(self.colors, repeat=4))

    def make_guess(self):
        if not self.current_guess:
            # First guess strategy: use first two colors alternating
            self.current_guess = (self.colors[0], self.colors[1], self.colors[0], self.colors[1])
        else:
            # Choose first possible code as the next guess
            self.current_guess = self.possible_codes[0]
        return self.current_guess

    def process_feedback(self, feedback):
        """
        feedback should be a list of 4 values: 'G' for green, 'W' for white, 'B' for black
        """
        # Filter possibilities based on feedback
        self.possible_codes = [code for code in self.possible_codes 
                             if self._would_give_same_feedback(code, self.current_guess, feedback)]

    def _would_give_same_feedback(self, code, guess, target_feedback):
        feedback = ['B'] * 4
        code_counts = {}
        guess_counts = {}
        
        # Check for exact matches (greens)
        for i in range(4):
            if code[i] == guess[i]:
                feedback[i] = 'G'
            else:
                code_counts[code[i]] = code_counts.get(code[i], 0) + 1
                guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1

        # Check for color matches (whites)
        for color in guess_counts:
            if color in code_counts:
                white_count = min(guess_counts[color], code_counts[color])
                for _ in range(white_count):
                    for i in range(4):
                        if feedback[i] == 'B':
                            feedback[i] = 'W'
                            break

        return sorted(feedback) == sorted(target_feedback)

def play_mastermind():
    # Get available colors
    print("Enter the available colors (space-separated):")
    colors = input().strip().split()
    
    solver = MastermindSolver(colors)
    
    while True:
        # Make a guess
        guess = solver.make_guess()
        print("\nMy guess is:", guess)
        
        # Get feedback
        print("\nEnter feedback for each position (G for green, W for white, B for black):")
        print("Example: G W B B")
        feedback = input().strip().upper().split()
        
        if len(feedback) != 4 or not all(f in ['G', 'W', 'B'] for f in feedback):
            print("Invalid feedback! Please use G, W, or B for each position.")
            continue
            
        if all(f == 'G' for f in feedback):
            print("I won! The code was", guess)
            break
            
        solver.process_feedback(feedback)
        
        if not solver.possible_codes:
            print("Something went wrong - no possible codes remain. Please check your feedback.")
            break

if __name__ == "__main__":
    play_mastermind()
