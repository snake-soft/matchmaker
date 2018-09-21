""" filter (pipeable) """
from django import template


register = template.Library()


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
    if pov_team and match.firstteam is not pov_team:
        match.firstteam, match.secondteam = match.secondteam, match.firstteam

        match.firstteam_goals, match.secondteam_goals = \
            match.secondteam_goals, match.firstteam_goals
    return {
        'match': match, 'pov_team': pov_team,
        't1class': t1class, 't2class': t2class,
        't1show': t1show, 't2show': t2show,
        }


@register.inclusion_tag('core/match_details_badge.html')
def match_details_badge(match, pov_team=False, t1class='primary',
                        t2class='secondary', t1show=False, t2show=True):
    """ fdsf """
    if pov_team and match.firstteam is not pov_team:
        match.firstteam, match.secondteam = match.secondteam, match.firstteam

        match.firstteam_goals, match.secondteam_goals = \
            match.secondteam_goals, match.firstteam_goals

    return {
        'match': match, 'pov_team': pov_team,
        't1class': t1class, 't2class': t2class,
        't1show': t1show, 't2show': t2show,
        }