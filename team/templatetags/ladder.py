""" filter (pipeable) """
from django import template

from team.models import Team


register = template.Library()


@register.inclusion_tag('team/team_list_realtime.html')
def ladder(request):
    """ includes realtime list of teams """
    Team.set_from_to(request.session['from'], request.session['to'])
    return {
        'object_list': Team.objects.filter(owner=request.user),
        'max_score': max([x.team_score for x in Team.objects.filter(
            owner=request.user)])}
