from flask import Blueprint, render_template

error = Blueprint('error', __name__)

# 400
@error.app_errorhandler(400)
def error400(e):
    return render_template('error-pages/400.html'), 400

# 401
@error.app_errorhandler(401)
def error401(e):
    return render_template('error-pages/401.html'), 401

# 403
@error.app_errorhandler(403)
def error403(e):
    return render_template('error-pages/403.html'), 403

# 404
@error.app_errorhandler(404)
def error404(e):
    return render_template('error-pages/404.html'), 404

# 500
@error.app_errorhandler(500)
def error500(e):
    return render_template('error-pages/500.html'), 500

# 503
@error.app_errorhandler(503)
def error503(e):
    return render_template('error-pages/503.html'), 503