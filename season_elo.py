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
def run_season(initial_elos, matches, output=None):
    if output != None:
        output_file = open(output, "w")

    elos = initial_elos
    for team in elos:
        print str(team) + " starting with initial Elo of " + str(elos[team])

    for i in range(len(matches)):
        match = matches[i]
        print match.to_string()
        if not match.is_tie():
            winner = match.get_winner()
            loser = match.get_loser()
            new_winner_elo, new_loser_elo, adj = elo.adjust_elo(elos[winner], elos[loser], "first")
            elos[winner] = new_winner_elo
            elos[loser] = new_loser_elo 
        else:
            team1 = match.get_team1()
            team2 = match.get_team2()
            new_team1_elo, new_team2_elo, adj = elo.adjust_elo(elos[team1], elos[team2], "tie")
            elos[team1] = new_team1_elo
            elos[team2] = new_team2_elo

    for team in elos:
        print str(team) + " ending with final Elo of " + str(elos[team])
        

elos = {"A":1500, "B":1640, "C": 1350}

match_sample = Match("A", 3, "B", 2)
match_sample2 = Match("C", 4, "A", 1)
match_sample3 = Match("A", 1, "B", 3)
match_sample4 = Match("B", 5, "C", 1)
match_sample5 = Match("B", 1, "C", 1)
matches = [match_sample, match_sample2, match_sample3, match_sample4, match_sample5]

run_season(elos, matches)
