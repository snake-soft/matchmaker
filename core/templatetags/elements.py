""" filter (pipeable) """
from django import template


register = template.Library()


@register.inclusion_tag('core/player_details_badge.html')
def player_details_badge(player):
    """ get value from dict """
    return {'player': player}


@register.inclusion_tag('core/team_wdl_bar.html')
def team_wdl_bar(team):
    """ get value from dict """
    return {'team': team}


@register.inclusion_tag('core/team_wdl_bar.html')
def team_button(team):
    """ get value from dict """
    return {'team': team}
