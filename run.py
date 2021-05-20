from zembil import create_app, db

app = create_app()
# uncomment the following 2 lines, if database doesn't exist.
with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)