# This file contains various functions for the basic and essential Elo calculations

# This function calculates the win probability of a head-to-head match given initial Elo
# values and the normalization factor
def win_prob(first_elo, second_elo, norm_factor=400):
    norm_factor = float(norm_factor)
    first_adjusted = 10 ** (first_elo / norm_factor)
    second_adjusted = 10 ** (second_elo / norm_factor)
    total = first_adjusted + second_adjusted
    first_rate = first_adjusted / total
    second_rate = second_adjusted / total
    return first_rate, second_rate

# This function calculates the change in Elo for two entities in a head on head match
# given a normalization factor, k-factor, and winner
def adjust_elo(first_elo, second_elo, winner, norm_factor=400, k_factor=32):
    first_wr, second_wr = win_prob(first_elo, second_elo, norm_factor)
    if winner == "first":
        adjustment = (1 - first_wr) * k_factor
        new_first = first_elo + adjustment
        new_second = second_elo - adjustment
    elif winner == "second":
        adjustment = (1 - second_wr) * k_factor
        new_first = first_elo - adjustment
        new_second = second_elo + adjustment
    elif winner == "tie":
        adjustment = (0.5 - first_wr) * k_factor
        new_first = first_elo + adjustment
        new_second = second_elo - adjustment
    else:
        print "Illegal winner in adjust_elo() of " + winner
        return  
    return new_first, new_second, abs(adjustment)

