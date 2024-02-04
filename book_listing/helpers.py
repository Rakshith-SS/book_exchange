from users.models import User


def get_user_id_dict(user_ids):
    """
        pass a bunch of user ids
        and a get a list of dictionary resp
        Example: [{"rakshith": 2}, {"sagar": 6} ]
    """
    output = []
    for user_id in user_ids:
        user = User.objects.filter(id=user_id).first()
        if user is not None:
            data = {user.username: user.id}
            output.append(data)

    return output
