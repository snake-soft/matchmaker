""" Default context """
from datetime import date, datetime
from calendar import monthrange
from django.contrib.auth.forms import AuthenticationForm

from player.forms import PlayerCreateForm
from team.forms import TeamCreateForm
from .forms import TimeRangeForm


def date_to_str(date_obj):
    """ return date as str """
    return str(date_obj)


def str_to_date(date_str):
    """ return datestring as string """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def default(request):
    """ Default context """
    if "from" not in request.session:
        request.session["from"] = date_to_str(date.today().replace(day=1))
    if "to" not in request.session:
        request.session["to"] = date_to_str(
            date.today().replace(day=monthrange(
                date.today().year,
                date.today().month)[1]))
    context = {
        'time_range_form': TimeRangeForm(
            initial={
                'frm': request.session["from"],
                'to': request.session['to'],
                }
            ),
        'from': str_to_date(request.session['from']),
        'to': str_to_date(request.session['to']),
        'login_form': AuthenticationForm,
        'new_player_form': PlayerCreateForm,
        'new_team_form': TeamCreateForm(request=request),
        }
    return context
