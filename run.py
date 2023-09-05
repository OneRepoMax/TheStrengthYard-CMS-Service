from app import app
from scheduler import app as scheduler_app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    scheduler_app.run()
