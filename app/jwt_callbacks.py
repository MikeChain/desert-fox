from flask import jsonify
from flask_jwt_extended import JWTManager


def init_jwt(app, redis_client):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_block_list(jwt_header, jwt_payload):
        return redis_client.sismember("jwt:blocklist", jwt_payload["jti"])

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has expired", "error": "token_expired"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(error):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "invalid_token",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification failed.",
                    "error": "invalid_token",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
