""" filter (pipeable) """
from django import template

from match.models import Match


register = template.Library()


@register.filter
def match_close(match_or_list_of_matches):
    """ returns if match is close or list of close matches from list """
    def is_close(match):
        return match.firstteam_goals - match.secondteam_goals in [-1, 1]

    if type(match_or_list_of_matches) is Match:
        return is_close(match_or_list_of_matches)
    elif type(match_or_list_of_matches) is list:
        return ([match for match in match_or_list_of_matches
                 if is_close(match)])
