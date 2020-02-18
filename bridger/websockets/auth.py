from channels.sessions import CookieMiddleware

from bridger.websockets.middleware import JWTAuthMiddleware


def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(JWTAuthMiddleware(inner))
