class IsPost:
    publ = 'PUBL'
    news = 'NEWS'

    names = [
        (publ, 'Новость'),
        (news, 'Статья')
    ]


class ChangeRate:
    @staticmethod
    def make_like(rate):
        rate += 1 if rate < 10 else 10
        return rate

    @staticmethod
    def make_dislike(rate):
        rate -= 1 if rate > 0 else 0
        return rate