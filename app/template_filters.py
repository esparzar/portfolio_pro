import json
import os

from flask import current_app, url_for

PROJECT_IMAGE_ALIASES = {
    "portfolio-home.png": "homepage-hero.png",
    "portfolio-admin-dashboard.png": "admin-dashboard.png",
    "portfolio-about.png": "projects-section.png",
}


def register_template_filters(app):
    @app.context_processor
    def inject_year():
        from datetime import datetime

        return {"current_year": datetime.utcnow().year}

    @app.template_filter("from_json")
    def from_json_filter(value):
        """Convert JSON strings or comma-separated values to a list."""
        if not value:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            if isinstance(value, str) and "," in value:
                return [item.strip() for item in value.split(",")]
            return [value] if value else []

    @app.template_filter("static_image")
    def static_image_filter(path):
        """Resolve a static image path or external URL for use in img src."""
        if path is None:
            return ""

        path = str(path).strip()
        if not path:
            return ""

        lower = path.lower()
        if lower.startswith(("http://", "https://")):
            return path

        path = path.lstrip("/")
        if lower.endswith(".pn") and not lower.endswith(".png"):
            path = path[:-3] + ".png"

        static_root = os.path.join(current_app.root_path, "static")
        initial = [path] if path.startswith("images/") else [f"images/{path}"]
        if not path.startswith("images/") and "/" not in path:
            initial.append(f"images/project/{path}")

        candidates = []
        seen = set()
        for rel_path in initial:
            if rel_path not in seen:
                seen.add(rel_path)
                candidates.append(rel_path)
            mapped = PROJECT_IMAGE_ALIASES.get(os.path.basename(rel_path).lower())
            if mapped:
                alias = f"images/project/{mapped}"
                if alias not in seen:
                    seen.add(alias)
                    candidates.append(alias)

        for filename in candidates:
            if os.path.isfile(os.path.join(static_root, filename)):
                return url_for("static", filename=filename)

        return url_for("static", filename=candidates[0])
