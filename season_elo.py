import elo

# This class is designed to take in a fixed set of teams, a CSV of initial Elo values,
# a CSV of match results with listed scores. This class will output a CSV with Elo values
# for all teams after each match.

# This class contains information for a single match with winner team name, losing team
# name, and winning margin. This class does not have any information 
class Match:
    def __init__(self, team1, team1_score, team2, team2_score):
        self.team1 = team1
        self.team1_score = team1_score
        self.team2 = team2
        self.team2_score = team2_score

        if team1_score > team2_score:
            self.winner = team1
            self.loser = team2
            self.winner_score = team1_score
            self.loser_score = team2_score
            self.wm = team1_score - team2_score
            self.tie = False
        elif team1_score < team2_score:
            self.winner = team2
            self.loser = team1
            self.winner_score = team2_score
            self.loser_score = team1_score
            self.wm = team1_score - team2_score
            self.tie = False
        else:
            self.winner = None
            self.loser = None
            self.winner_score = None
            self.loser_score = None
            self.wm = 0
            self.tie = True


    def is_tie(self):
        return self.tie

    def get_winner(self):
        return self.winner

    def get_loser(self):
        return self.loser
    
    def get_team1(self):
        return self.team1

    def get_team2(self):
        return self.team2

    def get_wm(self):
        return self.wm

    def to_string(self):
        if self.tie:
            return str(self.team1) + " tied with " + str(self.team2) + " " + str(self.team1_score) + " to " + str(self.team2_score)
        else:
            return str(self.winner) + " beat " + str(self.loser) + " " + str(self.winner_score) + " to "  + str(self.loser_score)

# This method takes in a dictionary of initial elo values and a list of Match objects
# and runs each match while calculating and adjusting Elo. Output for this method 
# appears in a CSV with matches, new Elos, winrates. Additionally, final Elo values are
# returned as a dictionary.
# Elo Methodology:
#  - Ignore scores
#  - Report wins/losses as single games with results of 0 or 1
#  - Report ties as single game with results of 0.5
#
# Format of output file is: match_number, team1, team2, winner, win_prob, elo_adj, new_winner_Elo, new_loser_elo
def run_season(initial_elos, matches, output=None, final_elos_loc=None):
    if output != None:
        output_file = open(output, "w")

    if final_elos_loc != None:
        final_elos_file = open(final_elos_loc, "w")

    elos = initial_elos
    for team in elos:
        print str(team) + " starting with initial Elo of " + str(elos[team])

    for i in range(len(matches)):
        match = matches[i]
        if not match.is_tie():
            winner = match.get_winner()
            loser = match.get_loser()
            new_winner_elo, new_loser_elo, adj, prob = elo.adjust_elo(elos[winner], elos[loser], "first")
            elos[winner] = new_winner_elo
            elos[loser] = new_loser_elo
            output_file.write(str(i) + "," + match.get_team1() + "," + match.get_team2() + "," + winner + "," + str(prob) + "," + str(adj) + "," + str(new_winner_elo) + "," + str(new_loser_elo) + "\n") 
        else:
            team1 = match.get_team1()
            team2 = match.get_team2()
            new_team1_elo, new_team2_elo, adj, prob = elo.adjust_elo(elos[team1], elos[team2], "tie")
            elos[team1] = new_team1_elo
            elos[team2] = new_team2_elo
            output_file.write(str(i) + "," + str(match.get_team1()) + "," + str(match.get_team2()) + ",tie," + str(prob) + "," + str(adj) + "," + str(new_winner_elo) + "," + str(new_loser_elo) + "\n")
    
    for team in elos:
        final_elos_file.write(team + "," + str(elos[team]) + "\n")
        print str(team) + " ending with final Elo of " + str(elos[team])
    
    output_file.close()
    final_elos_file.close()
    return elos

# Loads a CSV of matches into a list of Match objects
# Format for the CSV should be team1, team1_score, team2, team2_score
def load_match_csv(input_loc):
    input_file = open(input_loc, "r")
    matches_as_lines = input_file.read().splitlines()
    matches = []

    for match_line in matches_as_lines:
        match_data = match_line.split(",")
        match = Match(match_data[0], float(match_data[1]), match_data[2], float(match_data[3]))
        matches.append(match)
    
    """
    print "Loaded the following mathces:"
    for match in matches:
        print match.to_string()
    """

    return matches

# Loads a CSV of teams and Elo values
# Format for the CSV should be team, elo
def load_elo_csv(input_loc):
    input_file = open(input_loc, "r")
    teams_as_lines = input_file.read().splitlines()

    elos = {}
    for team_line in teams_as_lines:
        team_data = team_line.split(",")
        elos[team_data[0]] = float(team_data[1])
    return elos

# Calls the run_season method but takes in CSVs instead of native objects
def run_season_csvs(input_elos, input_matches, output_matches, output_elos=None):
    matches = load_match_csv(input_matches)
    elos = load_elo_csv(input_elos)
    end_elos = run_season(elos, matches, output_matches, output_elos)

run_season_csvs("elos_input.csv", "input.csv", "output.csv", "output_elos.csv")
