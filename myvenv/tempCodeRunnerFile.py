from Ignosis import app, db
from Ignosis.models import User

if __name__=='__main__':
    with app.app_context():
        user=User.query.first()
        print(user) 
    app.run()

 