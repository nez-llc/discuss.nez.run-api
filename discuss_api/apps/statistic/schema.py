from ninja import Schema


class StatisticsOut(Schema):
    agenda_count: int
    comment_count: int
    vote_count: int
