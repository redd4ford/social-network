from django.core.exceptions import ValidationError


class ObjectDoesNotExistError(ValidationError):
    def __init__(self, obj_type, obj_id: str, code=None, params=None):
        message = f'{obj_type.get_verbose()} object with id={obj_id} does not exist.'
        super().__init__(message=message, code=code, params=params)


class UserNotAuthorizedError(ValidationError):
    def __init__(self, code=None, params=None):
        message = 'You are not allowed to perform this action.'
        super().__init__(message=message, code=code, params=params)


class LikeAlreadyExistsError(ValidationError):
    def __init__(self, code=None, params=None):
        message = f'You have already liked this post.'
        super().__init__(message=message, code=code, params=params)


class LikeDoesNotExistError(ValidationError):
    def __init__(self, code=None, params=None):
        message = f'You have not liked this post.'
        super().__init__(message=message, code=code, params=params)
