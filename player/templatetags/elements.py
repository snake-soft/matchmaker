""" filter (pipeable) """
from django import template


register = template.Library()


@register.inclusion_tag('core/badge/player_details.html')
def player_details_badge(player):
    """ get value from dict """
    return {'player': player}


@register.inclusion_tag('core/bar/team_wdl.html')
def team_wdl_bar(team):
    """ get value from dict """
    return {'team': team}
