import fileinput

# dictionary of card ranks
rank = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

hands = [];


def sort_input_arr():
    hands_converted = []
    for hand in hands:
        cards = [];
        is_same_suit = 0
        # loop through the 3 cards in each hand
        for i in range(1, 4):
            # convert card value to integers
            cards.append(rank[hand[i][0]])
            # sort the hands in ascending order
            cards.sort()
        if hand[i][1] == hand[2][1] and hand[2][1] == hand[3][1] and hand[3][1] == hand[1][1]:
            is_same_suit = 1  # 1 represents True is the same hand
        # [3, 4, 5, 1, 0]  card1, card2, card3, is_same_suit, player #
        cards.append(is_same_suit)
        player_num = int(hand[0])
        cards.append(player_num)
        hands_converted.append(cards)
    return hands_converted


def is_straight_flush(cards):
    is_same = cards[3]
    default_a_value_fourteen = (is_straight(cards) and is_same == 1)
    # A-2-3
    # Q-K-A
    # A can be low or high
    if cards[2] == rank['A']:
        # check also if A to value of 1
        return default_a_value_fourteen or (cards[0] + 1 == cards[1] and cards[0] - 1 == 1 and is_same == 1)
    else:
        return default_a_value_fourteen


def is_three_of_a_kind(cards):
    return cards[0] == cards[1] and cards[1] == cards[2]


def is_straight(cards):
    return cards[0] + 1 == cards[1] and cards[1] + 1 == cards[2]


def is_flush(cards):
    is_same_suit = cards[3]
    return is_same_suit


def is_pair(cards):
    return cards[0] == cards[1] or cards[1] == cards[2]


def find_winner_rules(converted_hands):
    winner = {}
    for converted_cards in converted_hands:
        highest_card = converted_cards[2]
        second_highest = converted_cards[1]
        third_highest = converted_cards[0]
        player_num = converted_cards[4]
        if is_straight_flush(converted_cards):
            points = 6
        elif is_three_of_a_kind(converted_cards):
            points = 5
        elif is_straight(converted_cards):
            points = 4
        elif is_flush(converted_cards):
            points = 3
        elif is_pair(converted_cards):
            points = 2
        else:
            points = 1
        winner[player_num] = [points, highest_card, second_highest, third_highest]
    return winner


def tie_breaker(curr_winner, player_key, player_points):
    winner_array = curr_winner
    #  compare the first card, if equal compare the second , if equal compare third, if equal add both to the winner[]
    curr_winner_key = curr_winner[0]
    player_points_arr = player_points.get(player_key)
    curr_winner_arr = player_points.get(curr_winner_key)
    if player_points.get(curr_winner_key)[0] != 2:
        if curr_winner_arr[1] < player_points_arr[1]:
            winner_array[0] = player_key
        if curr_winner_arr[1] == player_points_arr[1]:
            if curr_winner_arr[2] < player_points_arr[2]:
                winner_array[0] = player_key
            if curr_winner_arr[2] == player_points_arr[2]:
                if curr_winner_arr[3] < player_points_arr[3]:
                    winner_array[0] = player_key
                if curr_winner_arr[3] == player_points_arr[3]:
                    winner_array.append(player_key)
    else:
        # new rules for checking pairs: use the middle card because always in the pair
        # if pair is less than
        if curr_winner_arr[2] < player_points_arr[2]:
            winner_array[0] = player_key
            # if pair is equal check the third card for highest
        elif curr_winner_arr[2] == player_points_arr[2]:
            if curr_winner_arr[3] < player_points_arr[3]:
                winner_array[0] = player_key
            # if all is equal there are two winners
            elif curr_winner_arr[3] == player_points_arr[3]:
                winner_array.append(player_key)
    return winner_array


def get_winner(all_player_points):
    player_list = list(all_player_points.keys())
    curr_winner = []
    for player_key in player_list:
        if not curr_winner:
            curr_winner.append(player_key)
        else:
            curr_winner_points = all_player_points.get(curr_winner[0])[0]
            curr_player_points = all_player_points.get(player_key)[0]
            if curr_winner_points < curr_player_points:
                curr_winner[0] = player_key
            if curr_winner_points == curr_player_points:
                curr_winner = tie_breaker(curr_winner, player_key, all_player_points)
    return curr_winner


if __name__ == "__main__":
    for line in fileinput.input():
        # split the line by spaces
        input_arr = line.split()
        # if line is length of 4: n player, card1, card2, card3
        if len(input_arr) == 4:
            # check if the cards are in the correct form of length 2: suit and value
            if len(input_arr[1]) == 2 and len(input_arr[2]) == 2 and len(input_arr[3]) == 2:
                hands.append(input_arr)
    converted_hands = sort_input_arr()
    player_points = find_winner_rules(converted_hands)
    winner_arr = get_winner(player_points)
    print(*winner_arr, sep=", ")

