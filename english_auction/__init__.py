from otree.api import *

import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'english_auction'
    players_per_group = 3
    num_rounds = 3
    timeout_seconds = 120


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    L_highest_bidder = models.IntegerField(initial=0)
    L_highest_bid = models.CurrencyField(initial=0)
    L_winner = models.IntegerField(initial=0)
    R_highest_bidder = models.IntegerField(initial=0)
    R_highest_bid = models.CurrencyField(initial=0)
    R_winner = models.IntegerField(initial=0)
    treatment = models.StringField()


class Player(BasePlayer):
    value = models.CurrencyField()
    L_bid = models.CurrencyField(initial=0)
    L_is_winner = models.BooleanField()
    L_price = models.CurrencyField()
    R_bid = models.CurrencyField(initial=0)
    R_is_winner = models.BooleanField()
    R_price = models.CurrencyField()
# FUNCTIONS


def creating_session(subsession):
    if subsession.round_number == 1 or subsession.round_number == 6:
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)

    for p in subsession.get_players():
        p.value = random.random()*100
        p.L_is_winner = False
        p.R_is_winner = False
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0
            p.participant.vars['finished'] = False

    for g in subsession.get_groups():
        order = ["A", "B", "C"]
        for r in range(1, subsession.round_number):
            prior_group = g.in_round(r)
            order.remove(prior_group.treatment)
        g.treatment = random.sample(order, 1)[0]


def auction_outcome(g: Group):

    # Get the set of players in the group
    players = g.get_players()

    # Get the set of bids from the players
    bids = [p.bid for p in players if p.bid >= 0]

    # Sort the bids in descending order
    bids.sort(reverse=True)

    # Set the highest
    # (Python uses 0-based arrays...)
    g.L_highest_bid = bids[0]

# PAGES
class MyPage(Page):

    @property
    def vars_for_template(player: Player):
        g = player.group
        if g.treatment == 'A':
            left_pic = 'TB.jpg'
            right_pic = 'BTB.jpeg'
            left_description =
            right_description =

        elif g.treatment == 'B':
            left_pic = 'CF.jpg'
            right_pic = 'WE.jpeg'
            left_description =
            right_description =

        elif g.treatment == 'C':
            left_pic = 'FC.jpeg'
            right_pic = 'NC.jpeg'
            left_description =
            right_description =

        return dict(
            left_image_file=left_pic,
            right_image_file=right_pic,
            left_description_file=left_description,
            right_description_file=right_description

        )


    def live_method(player, data):
        print(data)

        group = player.group
        bidder_id = player.id_in_group
        auction = data['auction']
        bid = data['bid']
        if auction == 'L':
            player.L_bid = data['bid']
            if player.L_bid > group.L_highest_bid:
                group.L_highest_bid = player.L_bid
                group.L_highest_bidder = bidder_id
                response = dict(highest_bidder=bidder_id, highest_bid=bid, auction=auction)
                return {0: response}
        if auction == 'R':
            player.R_bid = data['bid']
            if player.R_bid > group.R_highest_bid:
                group.R_highest_bid = player.R_bid
                group.R_highest_bidder = bidder_id
                response = dict(highest_bidder=bidder_id, highest_bid=bid, auction=auction)
                return {0: response}

    def get_timeout_seconds(player):
        return Constants.timeout_seconds  # in seconds

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]

