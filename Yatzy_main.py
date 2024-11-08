from functions import * 

def main_loop():
    while True:
        try:
            choice = menu()
            if choice == 1:
                high_scores = loading_high_score_data()
                if high_scores:
                    print("\nThe High Scores:")
                    for player, score_data in high_scores.items():
                        total_score = sum(float(score) for score in score_data["upper"].values() if score is not None) + \
                                      sum(float(score) for score in score_data["lower"].values() if score is not None)
                        # Print the score as an integer if it's a whole number, otherwise keep it as a float
                        print(f"{player}'s high score: {int(total_score) if total_score.is_integer() else total_score} points")
                    print("=" * 20)
                else:
                    print("\nNo highscore. Be the first to break it!")
                start_game()
            elif choice == 2:
                display_scorecard()
            elif choice == 3:
                # Check if load_HighScores is defined in globals and call it if it exists1
        
                if 'load_HighScores' in globals():
                    load_HighScores()
                print("Exiting the game...")
                break
            else:
                print("Error: Invalid input, choose between 1 and 3.")
        except ValueError:
            print("Error: Invalid input. Enter a number.")
        except Exception as e:
            print(f"Unexpected error: {e}")

main_loop()