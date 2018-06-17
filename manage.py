import os
from app import create_app
from flask_script import Manager

# Select production mode or development mode
app = create_app(os.getenv("FLASK_CONFIG") or "development")
manager = Manager(app)

if __name__ == '__main__':
	# Start application
	manager.run()