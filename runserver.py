from app import app
import logging

if __name__ == '__main__':
    app.logger.setLevel(logging.CRITICAL)
    app.run(host='0.0.0.0', port=80, debug=False)