from django import template

from ..models import Game

#https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/


register = template.Library()

@register.filter
def my_index(values, i): #, *args, **kwargs):
    """return element of list by index

    Arguments:
        values {list} -- list
        i {int} - index

    Returns:
        int -- list value by index
    """
    return values[i]

@register.filter
def change_class(class_value, addition):
    """Change class

    Arguments:
        class_value {string} -- class to which should be added addition
        addition {int/str} -- what should be added to class_value

    Returns:
        string -- new class value
    """
    return class_value + str(addition)


@register.filter
def is_game_with_false_accepted_exist(player_1, player_2):
    """Check whether game with given players and is_accepted=False exists

    Arguments:
        player_1 {User} -- player_1
        player_2 {User} -- player_2

    Returns:
        bool -- whether game exists
    """
    games = Game.objects.filter(
        player_1=player_1,
        player_2=player_2,
        is_accepted=False,
        end_datetime=None
    )
    return bool(games)  # True if games else False

@register.filter
def get_game_status(game, request_user):
    """Return game status for user

    Arguments:
        game {Game} -- Game instance
        request_user {User} -- User

    Returns:
        str -- game status
    """
    return game.get_game_status(request_user)

@register.filter
def get_game_status_class(game, request_user):
    """Return game status for user in particular format

    Arguments:
        game {Game} -- Game instance
        request_user {User} -- User

    Returns:
        str -- game status in format (1 word, lowercase)
    """
    return game.get_game_status(request_user).split()[-1].lower()

@register.filter
def game_index(all_games, game):
    """Return index of game in all_games

    Arguments:
        all_games {QuerySet} -- QuerySet of all user's games
        game {Game} -- Game instance whose index will be returned

    Returns:
        int -- index of game. Index from the end
    """
    for index, item in enumerate(all_games):
        if item == game:
            return all_games.count() - index
    return 0

@register.filter
def get_ended_game_class(game):
    """Return end game class if game ended

    Arguments:
        game {Game} -- Game instance

    Returns:
        str -- ended game class
    """
    if game.winner:
        return " game-detail-map-ended"
    return ''

@register.filter
def get_player_ended_game_class(game, player):
    """Return end game class for patricular player

    Arguments:
        game {Game} -- Game instance
        player {User} -- player

    Returns:
        str -- ended game player class
    """
    if game.winner == player:
        return " player-3"
    return ''
