from flask import Flask
import math
app = Flask(__name__)

@app.route('/sqrt/calc/<int:num>')
def get_sqrt(num):
    return str(int(math.sqrt(num)))


if __name__ == "__main__":
    import sys
    port = sys.argv[1]
    app.config['DEBUG'] = True
    app.run(port=port)