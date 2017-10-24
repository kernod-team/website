from flask_security import login_required

from app.main import main


@main.route('/')
@login_required
def index():
    return 'hello, world'
