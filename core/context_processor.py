from datetime import date, datetime, timedelta
from calendar import monthrange

from .forms import TimeRangeForm


def date_to_str(date):
    return str(date)


def str_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def default(request):
    if "from" not in request.session:
        request.session["from"] = date_to_str(date.today().replace(day=1))
    if "to" not in request.session:
        request.session["to"] = date_to_str(
            date.today().replace(day=monthrange(
                date.today().year,
                date.today().month)[1]
            ))
    return {
        'time_range_form': TimeRangeForm(
            initial={
                'frm': request.session["from"],
                'to': request.session['to'],
                }
            ),
        'from': str_to_date(request.session['from']),
        'to': str_to_date(request.session['to']),
    }

            #===================================================================
            # to = datetime.strptime(
            #     self.request.session['to'], '%Y-%m-%d').date()
            # to += timedelta(days=1)
            #===================================================================