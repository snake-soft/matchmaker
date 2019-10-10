""" filter (pipeable) """
from django import template

from match.models import Match


register = template.Library()


@register.filter
def match_close(match_or_list_of_matches):
    """ returns if match is close or list of close matches from list """
    def is_close(match):
        return match.firstteam_goals - match.secondteam_goals in [-1, 1]

    if isinstance(match_or_list_of_matches, Match):
        return is_close(match_or_list_of_matches)

    if isinstance(match_or_list_of_matches, list):
        return ([match for match in match_or_list_of_matches
                 if is_close(match)])
