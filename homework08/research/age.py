import datetime as dt
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    ages = []
    for friend in (get_friends(user_id, fields=["bdate"])).items:
        if "bdate" in friend:  # type: ignore
            birthday = friend["bdate"]  # type: ignore
            try:
                ages.append(dt.date.today().year - int(birthday[-4:]))
            except ValueError:
                pass
    if ages:
        return sum(ages) / len(ages)
    else:
        return None
