import random
import ascii_art

#Main menu function for the game
def menu():
    # Display ASCII welcome message and menu options
    print(ascii_art.welcome_message)
    print("1. Start a New Game")
    print(ascii_art.start_game_art)
    print("2. View Scorecard")
    print(ascii_art.view_scorecard_art)
    print("3. Exit")
    print(ascii_art.exit_art)
    

    #Input loop for choices in the menu
    while True:
        try:
            choice = int(input("\n🔹 Enter your choice (1, 2, or 3): "))
            if choice in (1, 2, 3):
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#In-game menu for actions during a game
def in_game_menu():
    while True:
        print(ascii_art.in_game_menu)
        print("1. roll dice")
        print("2. View scorecard")
        print("3. Rules")
        print("4. Exit game")

        #choice loop for in-game choices
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice in (1, 2, 3, 4):
                return choice
            else:
                print("Invalid choice, please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 4.")

#Function for ASCII art for each dice roll
def dice_graphics(dice):
    """Displays the ASCII art for each dice based on its value."""
    dice_art = [ascii_art.get_dice_face(die) for die in dice]
    for line in range(5):
        print(" ".join(die.splitlines()[line] for die in dice_art))

#Global variables to track the game state
players = []  # List of player names
scores = {}  # Dictionary to store scores
current_player = 0  # Index for the current player
rolls_left = 3  # Number of rolls left for every turn
dice = [0] * 5  #setting the dice to 0 for the start

#Yatzy scoring categories
upper_section = {
    "Ones": None,
    "Twos": None,
    "Threes": None,
    "Fours": None,
    "Fives": None,
    "Sixes": None
}

lower_section = {
    'One Pairs': None, 
    'Two Pairs': None,
    'Three of a Kind': None,
    'Four of a Kind': None,
    'Full House': None,
    'Small Straight': None,
    'Large Straight': None,
    'Chance': None,
    'Yatzy': None
}

#Function to display the rules of Yatzy
def display_rules():
    print("\nYatzy Rules:")
    print("1. The game consists of 13 rounds, each round you roll 5 dice up to 3 times.")
    print("2. You can hold dice and re-roll others.")
    print("3. At the end of your turn, you must choose a category to score.")
    print("4. Upper Section: Ones to Sixes; Lower Section: Combos like Full House, Yatzy, etc.")
    print("5. Score 63+ in the Upper Section for a 50-point bonus!")
    input("\nPress Enter to continue...")

#Function to start a new game
def start_game():
    global players, scores, current_player

    #Input loop for number of players
    while True:
        try:
            player_count = int(input("Enter number of players: "))
            if player_count > 0:
                break
            else:
                print("Please enter a positive number of players.") #handles errors if a neghative integer is added
        except ValueError:
            print("Invalid input. Please enter an integer.") #handles errors if a integer isnt added

    #Setting player names and scores
    players.clear()
    scores.clear()
    
    for i in range(player_count):
        
        player_name = input(f"Enter player name {i + 1}: ") #updates the player count, ex: player 1, player 2
        players.append(player_name)
        scores[player_name] = {
            "upper": upper_section.copy(),
            "lower": lower_section.copy()
        }

    print("Loading new game...")
    play_game()  # Call function to begin the game

#Main gameplay loop
def play_game():
    
    global current_player  #make the current player a free variable making it flow better in the code
    while True:
       #choices for in game actions
        current_player_name = players[current_player]  
        print(f"\nCurrent player: {current_player_name}")
        choice = in_game_menu()
        
        if choice == 1:    
            play_turn()
        
        elif choice == 2:
            display_scorecard()
        
        elif choice == 3:
            display_rules()
       
        elif choice == 4:
            print("Exiting current game...")
            break
            
        else:
            print("Error: Invalid input. Choose between (1-4).")
        
        #Switch to next player
        current_player = (current_player + 1) % len(players)

#Function to roll five dice
def rolling_dice():
    return [random.randint(1, 6) for _ in range(5)]

#Function to handle holding and re-rolling dice
def hold_and_reroll(dice):
    print(f"Current dice:")
    dice_graphics(dice)

    #input/output for holding dice
    held_dice_status = ["H" if held else "R" for held in held_dice]
    print("Held dice status: ", " ".join(held_dice_status))

    #input handling for holding dice
    hold_input = input("Enter the indexes (1-5) of the dice you want to hold, separated by spaces (or press Enter to roll all): ")
    hold_indexes = list(set(int(i) - 1 for i in hold_input.split() if i.isdigit()))

    #Update dice based on held indexes
    for i in range(len(held_dice)):
        held_dice[i] = i in hold_indexes

    # Re-roll dice that are not held
    for i in range(len(dice)):
        if not held_dice[i]:
            dice[i] = random.randint(1, 6)

    return dice

#Function to display player scorecard
def display_scorecard():
    for player in players:
        print(f"\nScoreCard for {player}:")

        #Calculate and display upper section score
        print("\nUpper Section:")
        upper_score = sum(score for score in scores[player]['upper'].values() if score is not None)
        for category, score in scores[player]['upper'].items():
            print(f"{category}: {score if score is not None else '-'}")

        #Calculate the 63+ bonus
        bonus = 50 if upper_score >= 63 else 0
        print(f"Sum: {upper_score}")
        print(f"Bonus (63+): {bonus}")

        #Calculate and display lower section score
        print("\nLower Section:")
        for category, score in scores[player]['lower'].items():
            print(f"{category}: {score if score is not None else '-'}")

        #Calculate total score including the bonus
        total_score = upper_score + bonus + sum(score for score in scores[player]["lower"].values() if score is not None)
        print(f"Total score for {player}: {total_score}")


#Function to calculate scores for the upper section
def calculate_upper_score(dice, category):
    category_values = {
        "Ones": 1,
        "Twos": 2,
        "Threes": 3,
        "Fours": 4,
        "Fives": 5,
        "Sixes": 6
    }
    value = category_values.get(category)
    return sum(die for die in dice if die == value) if value else 0

def calculate_lower_score(dice, category):
    if category == "One Pairs":
        #Find all dice values that appear at least twice
        pairs = [die for die in set(dice) if dice.count(die) >= 2]
        if pairs:
            return max(pairs) * 2  #Return the sum of the highest pair
        return 0  #Return 0 if no valid pair found

   
    elif category == "Two Pairs":
        pairs = [die for die in set(dice) if dice.count(die) >= 2]
        return sum(die * 2 for die in sorted(pairs, reverse=True)[:2]) if len(pairs) >= 2 else 0

    elif category == "Three of a Kind":
        #Sum only the three matching dice
        for die in set(dice):
            if dice.count(die) >= 3:
                return die * 3
        return 0  #Return 0 if no valid "Three of a Kind"

    elif category == "Four of a Kind":
        #Sum only the four matching dice 
        for die in set(dice):
            if dice.count(die) >= 4:
                return die * 4
        return 0  #Return 0 if no valid "Four of a Kind"

    elif category == "Full House":
        # Check for a pair and a three-of-a-kind
        unique_counts = [dice.count(die) for die in set(dice)]
        if sorted(unique_counts) == [2, 3]:
            return sum(dice)  #Full house scores the sum of all dice
        return 0  #No valid full house

    elif category == "Small Straight":
        #Check for a small straight 
        if sorted(dice) == [1, 2, 3, 4, 5]:
            return 15
        return 0  #No valid small straight

    elif category == "Large Straight":
        #Check for a large straight 
        if sorted(dice) == [2, 3, 4, 5, 6]:
            return 20
        return 0  #No valid large straight

    elif category == "Chance":
        return sum(dice)


    elif category == "Yatzy":
        #Yatzy scores 50 points if all dice are the same
        return 50 if len(set(dice)) == 1 else 0

    return 0



#Function to update the scorecard
def update_scorecard(dice, category, section):
    player = players[current_player]
    
    #Convert the category input to lowercase for case-insensitive comparison
    category = category.lower()

    #Check if the category exists in the section (upper or lower) 
    if section == "upper":
        # Convert keys to lowercase 
        valid_categories = {key.lower(): key for key in upper_section.keys()}
        if category in valid_categories:
            actual_category = valid_categories[category]  #Get the category name from the uppercase
            if scores[player]['upper'][actual_category] is None:
                score = calculate_upper_score(dice, actual_category)
                scores[player]['upper'][actual_category] = score
                print(f"Score for {actual_category}: {score}")
            else:
                print(f"{actual_category} has already been scored.")
        else:
            print("Invalid category in the upper section.")
            
    elif section == "lower":
        #Convert keys to lowercase for case-insensitive comparison
        valid_categories = {key.lower(): key for key in lower_section.keys()}
        if category in valid_categories:
            actual_category = valid_categories[category]  # Get category name from the uppercase
            if scores[player]['lower'][actual_category] is None:
                score = calculate_lower_score(dice, actual_category)
                scores[player]['lower'][actual_category] = score
                print(f"Score for {actual_category}: {score}")
            else:
                print(f"{actual_category} has already been scored.")
        else:
            print("Invalid category in the lower section.")

#Function to handle a player's turn
def play_turn():
    global rolls_left, dice, held_dice
    rolls_left = 3
    dice = rolling_dice()
    held_dice = [False] * 5  #Reset held dice for a new turn

    while rolls_left > 0:
        print(f"Roll {4 - rolls_left}:")
        dice_graphics(dice)
        dice = hold_and_reroll(dice)
        rolls_left -= 1

        if rolls_left == 0:
            print("\nChoose a category to score this roll:")
            print("Upper Section:", list(upper_section.keys()))  #using keys to be able to make the category choices arent case sensitive 
            print("Lower Section:", list(lower_section.keys()))
            
            category = input("\nEnter category name (as written in choose category): ").strip().lower()  #Convert input to lowercase 
            #identifying where the input is and using error hanling to determine what should happen if he input is invalid
            if category in [letter.lower() for letter in upper_section]:
                section = "upper"
            elif category in [letter.lower() for letter in lower_section]:
                section = "lower"
            else: 
                print("Invalid entry, choose a valid category.")
                return
            
            update_scorecard(dice, category, section)
            print("The scores have been updated!")



#Function to save high scores to a file
def loading_high_score_data():
    input_filename = "Scoreboard.txt"  #Giving our file that saves the scores a title for when it is generated
    scores = {}   #dictionary that collects highscores
    current_player = None
    current_section = None  # Track the current section being read (upper or lower)

    try:
        with open(input_filename, "r") as file:  
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                
                #Skip headers or separators
                if line.startswith("High Scores") or line.startswith("=" * 20):
                    continue
               
                elif line.endswith(":") and "Section" not in line:  # Player's name
                    current_player = line[:-1]
                    scores[current_player] = {"upper": {}, "lower": {}}
                
                elif "Upper Section" in line:
                    current_section = "upper"
                
                elif "Lower Section" in line:
                    current_section = "lower"
                
                elif current_player and current_section:
                    # Process category and score only if player and section are set
                    if ":" in line:
                        category, score = line.split(":")
                        category = category.strip()
                        score = score.strip()
                        
                        # Handle missing scores and convert to appropriate type
                        if score == '-':
                            scores[current_player][current_section][category] = None
                        else:
                            # Convert score to float if it contains a decimal, otherwise to int
                            scores[current_player][current_section][category] = float(score) if '.' in score else int(score)
    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
    except Exception as e:
        print(f"Error loading scores: {e}")

    return scores




#function for formating the highscores in the scoreboard.txt file

def load_HighScores():
    output_file_name = "Scoreboard.txt"
    
    with open(output_file_name, "w") as outputfile:
        outputfile.write("High Scores\n")
        outputfile.write("====================\n")
       
        #Sorting players by their total score in descending order
        def calculate_total_score(player):
            upper_score = sum(score for score in scores[player]["upper"].values() if score is not None)
            lower_score = sum(score for score in scores[player]["lower"].values() if score is not None)
            return upper_score / lower_score

        sorted_players = sorted(players, key=calculate_total_score, reverse=True)

        # Writing high scores to the file
        for player in sorted_players:
            outputfile.write(f"{player}:\n")
            outputfile.write("Upper Section:\n")
           #score format for upper score
            for category, score in scores[player]["upper"].items():
                outputfile.write(f"  {category}: {score if score is not None else '-'}\n") # write "-" if score is left empty
            upper_sum = sum(score for score in scores[player]["upper"].values() if score is not None)
            outputfile.write("Sum: " + str(upper_sum) + "\n")
            outputfile.write("Lower Section:\n")
            #score format for lower score
            for category, score in scores[player]["lower"].items():
                outputfile.write(f"  {category}: {score if score is not None else '-'}\n") # write "-" if score is left empty
            total_score = upper_sum / sum(score for score in scores[player]["lower"].values() if score is not None)
            outputfile.write(f"Total score for {player}: {total_score}\n")
        
        outputfile.write("====================\n")
    
    print(f"New high scores saved in {output_file_name}") #tells user where scores are saved in output

    return scores




