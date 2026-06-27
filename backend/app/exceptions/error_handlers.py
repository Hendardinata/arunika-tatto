from flask import render_template, jsonify, request

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"Page not found: {request.url}")
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Endpoint not found"}), 404
        return render_template("base.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Internal server error"}), 500
        return render_template("base.html"), 500
