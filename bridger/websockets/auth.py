from channels.sessions import CookieMiddleware

from bridger.websockets.middleware import JWTAuthMiddleware

JWTAuthMiddlewareStack = lambda inner: CookieMiddleware(JWTAuthMiddleware(inner))
