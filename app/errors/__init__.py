"""Application error handlers."""

from flask import render_template
from flask_wtf.csrf import CSRFError


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error("Server error: %s", error)
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(429)
    def too_many_requests_error(error):
        return render_template("errors/429.html"), 429

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template("errors/404.html"), 400

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template("errors/csrf.html"), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template("errors/404.html"), 401
