from flask import Flask, request
import py_compile
import os
import time
import signal

app = Flask(__name__)

def generate(uuid_str):
    timeout = 2
    def handler(signum, frame):
        print "timeout"
        raise TimeoutError("timeout")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        f = open(uuid_str+'.txt', "w")
        f.close()
        py_compile.compile("%s.py" % uuid_str)
        print "compile ok"
        os.system("./pythonvm %s.pyc >> %s.txt" % (uuid_str, uuid_str))
        signal.alarm(0)
        print "exec ok"
        with open(uuid_str+'.txt', "r") as f:
            res = f.read()
        return res, 200, {'Access-Control-Allow-Origin': "*"}
    except:
        return "timeout", 200, {'Access-Control-Allow-Origin': "*"}


@app .route('/code_api', methods=["POST"])
def code_api():
    res = request.get_data()
    uuid_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    with open("%s.py" % uuid_str, "w") as f:
        f.write(res)
    res = generate(uuid_str)
    os.remove(uuid_str+'.txt')
    os.remove(uuid_str+'.py')
    os.remove(uuid_str+'.pyc')
    return res


if __name__ == '__main__':
    app.run(threaded=False)