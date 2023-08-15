from flask import Blueprint, current_app, send_from_directory
import os

bp = Blueprint("media",__name__,url_prefix="/media")


# @bp.get("/<path:filename>")
# def media_file(filename):
#   return os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"),filename)

@bp.get("/<path:filename>")
def media_file(filename):
    return send_from_directory(current_app.config.get("UPLOAD_IMAGE_PATH"), filename)
