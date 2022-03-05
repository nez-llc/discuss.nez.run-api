from ninja import Router

from discuss_api.apps.agenda.models import Agenda, Comment, Vote
from discuss_api.apps.statistic.schema import StatisticsOut


api = Router()


@api.get('/', response=StatisticsOut)
def agenda_list_by_tag(request):
    agenda_count = Agenda.objects.all().count()
    comment_count = Comment.objects.count()
    vote_count = Vote.objects.count()

    statistics_out = StatisticsOut(agenda_count=agenda_count, comment_count=comment_count, vote_count=vote_count)
    return statistics_out
