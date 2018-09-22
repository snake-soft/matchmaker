""" filter (pipeable) """
from django import template


register = template.Library()


@register.inclusion_tag('core/bar.html')
def bar(add_class, val_dict):
    """  NOT FINISHED
    :param add_class: additional classes for progressbar
    :param val_dict: [{'percent': 0, 'text': 'bla']}
    """
    return {'add_class': add_class, 'val_dict': val_dict}


@register.inclusion_tag('core/player_details_badge.html')
def player_details_badge(player, player_realtime=False):
    """ get value from dict """
    return {'player': player, 'player_realtime': player_realtime}


@register.inclusion_tag('core/player_badge.html')
def player_badge(player, player_realtime=False):
    """ get value from dict """
    return {'player': player, 'player_realtime': player_realtime}


@register.inclusion_tag('core/team_wdl_bar.html')
def team_wdl_bar(team, team_realtime=False):
    """ get value from dict """
    return {'team': team, 'team_realtime': team_realtime}


@register.inclusion_tag('core/team_details_badge.html')
def team_details_badge(team, team_realtime=False, linkclass=False):
    """ get value from dict """
    return {'team': team, 'team_realtime': team_realtime,
            'linkclass': linkclass}


@register.inclusion_tag('core/team_badge.html')
def team_badge(team, team_realtime=False, linkclass=False):
    """ get value from dict """
    return {'team': team, 'team_realtime': team_realtime,
            'linkclass': linkclass}


@register.inclusion_tag('core/match_badge.html')
def match_badge(match, pov_team=False, t1class='primary',
                t2class='secondary', t1show=False, t2show=True):
    """ sf """
    return {
        'match': match.pov(pov_team) if pov_team else match,
        'pov_team': pov_team,
        't1class': t1class, 't2class': t2class,
        't1show': t1show, 't2show': t2show,
        }


@register.inclusion_tag('core/match_details_badge.html')
def match_details_badge(match, pov_team=False, t1class='primary',
                        t2class='secondary', t1show=False, t2show=True):
    """ fdsf """
    return {
        'match': match.pov(pov_team) if pov_team else match,
        'pov_team': pov_team,
        't1class': t1class, 't2class': t2class,
        't1show': t1show, 't2show': t2show,
        }