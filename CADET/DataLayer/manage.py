import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from cadetapi.models import db, Comment, Course, Instructor, Dataset, Result

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show_urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Comment=Comment, Course=Course,
            Instructor=Instructor, Dataset=Dataset, Result=Result)

@manager.command
def setup_db():
    pass

if __name__ == '__main__':
    manager.run()
