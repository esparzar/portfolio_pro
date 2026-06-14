"""Application error handlers."""

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

ErrorResponse = tuple[str, int]


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found_error(error: object) -> ErrorResponse:
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error: object) -> ErrorResponse:
        app.logger.error("Server error: %s", error)
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error: object) -> ErrorResponse:
        return render_template("errors/403.html"), 403

    @app.errorhandler(429)
    def too_many_requests_error(error: object) -> ErrorResponse:
        return render_template("errors/429.html"), 429

    @app.errorhandler(400)
    def bad_request_error(error: object) -> ErrorResponse:
        return render_template("errors/404.html"), 400

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error: object) -> ErrorResponse:
        return render_template("errors/csrf.html"), 400

    @app.errorhandler(401)
    def unauthorized_error(error: object) -> ErrorResponse:
        return render_template("errors/404.html"), 401
