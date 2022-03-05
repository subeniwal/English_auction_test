from otree.api import *

import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'english_auction'
    players_per_group = 3
    num_rounds = 3
    timeout_seconds = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bidder = models.IntegerField(initial=0)
    highest_bid = models.CurrencyField(initial=0)
    winner = models.IntegerField(initial=0)
    treatment = models.StringField()


class Player(BasePlayer):
    value = models.CurrencyField()
    bid = models.CurrencyField(initial=0)
    is_winner = models.BooleanField()
    price = models.CurrencyField()

# FUNCTIONS


def creating_session(subsession):
    if subsession.round_number == 1 or subsession.round_number == 6:
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)

    for p in subsession.get_players():
        p.value = random.random()*100
        p.is_winner = False
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
    g.highest_bid = bids[0]

# PAGES
class MyPage(Page):
    def live_method(player, bid):
        player.bid = bid
        group = player.group
        my_id = player.id_in_group
        if bid > group.highest_bid:
            group.highest_bid = bid
            group.highest_bidder = my_id
            response = dict(id_in_group=my_id, bid=bid)
            return {0: response}

    def get_timeout_seconds(player):
        return Constants.timeout_seconds  # in seconds

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]

