import dataclasses
import time
import typing as tp

from vkapi import Session, config

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    access_token = config.VK_CONFIG["access_token"]
    version = config.VK_CONFIG["version"]
    fields = ", ".join(fields) if fields else "" # type: ignore
    GetUrl = Session(config.VK_CONFIG["domain"]).get(
        f"friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&offset={offset}&count={count}&v={version}"
    )
    try:
        response = FriendsResponse(GetUrl.json()["response"]["count"], GetUrl.json()["response"]["items"])
    except KeyError:
        response = GetUrl.json()
        print(response)
    return response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    access_token = config.VK_CONFIG["access_token"]
    version = config.VK_CONFIG["version"]
    results_of_requests = []

    if target_uids:
        for i in range(0, len(target_uids), 100):
            try:
                friends = Session(config.VK_CONFIG["domain"]).get(
                    f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uids={','.join(map(str, target_uids[i: i + 100]))}&count={count}&offset={i}&v={version}"
                )
                results_of_requests.extend(
                    [
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                        for friend in friends.json()["response"]
                    ]
                )
            except KeyError:
                pass
            time.sleep(0.3)
        return results_of_requests

    try:
        friends = Session(config.VK_CONFIG["domain"]).get(
            f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&count={count}&offset={offset}&v={version}"
        )
        results_of_requests.extend(friends.json()["response"])
    except:
        pass

    return results_of_requests


if __name__ == "__main__":
    friends_response = get_friends(user_id=233463303, fields=["nickname"])
    active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]  # type: ignore
    mutual_friends = get_mutual(source_uid=233463303, target_uid=88506163, count=len(active_users))
    print("Number of active friends is:", len(active_users))
    print("Number of mutual friends is:", len(mutual_friends))
    print("List of IDs of mutual friends is:", mutual_friends)
