from src import app
import os


p = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(port=p)
