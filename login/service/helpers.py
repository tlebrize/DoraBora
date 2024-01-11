import httpx, functools


def api_error_logger(func):
    """tries to log json reponse error bodies"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as exc:
            try:  # response.json() might fail
                print(f"Http error : {exc.response.json()}")
            except:  # noqa E722 - Already in a scoped except.
                print(f"Http error : {exc.response.body}")
                raise exc
            finally:
                raise exc

    return wrapper
