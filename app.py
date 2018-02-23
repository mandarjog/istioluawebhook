from flask import Flask
from flask import request
from flask import jsonify
import threading
import os
import time

app = Flask(__name__)


# example
# /listeners/istio-proxy/sidecar~10.32.1.20~httpbin-57db476f4d-svs9h.default~default.svc.cluster.local
@app.route('/listeners/<cluster>/<node>', methods=['POST'])
def lds(cluster, node):
    print cluster
    print node
    op = insert_lua(request.json)
    return jsonify(op)

# example
# /clusters/istio-proxy/sidecar~10.32.1.20~httpbin-57db476f4d-svs9h.default~default.svc.cluster.local
@app.route('/clusters/<cluster>/<node>', methods=['POST'])
def cds(cluster, node):
    output = request.data
    return output

# example
# /routes/15003/istio-proxy/sidecar~10.32.1.20~httpbin-57db476f4d-svs9h.default~default.svc.cluster.local
@app.route('/routes/<name>/<cluster>/<node>', methods=['POST'])
def rds(name, cluster, node):
    output = request.data
    return output


"""
listeners:
- address: tcp://0.0.0.0:80
  bind_to_port: true
  filters:
  - name: http_connection_manager
    config:
      access_log:
      - path: /dev/stdout
      codec_type: auto
      filters:
      - name: mixer
        config: {}
      - name: lua
        config:
          inline_code: <code>

"""
#
# inserts lua as a filter in the http_connection_manager


def insert_lua(listeners):
    for l in listeners.get("listeners", []):
        for f in l.get("filters", []):
            if f["name"] != "http_connection_manager":
                continue

            ff = f["config"].get("filters", [])
            ff.insert(0, LUA_CONFIG)

    return listeners

last_check = 0


FILE_PATH = "scripts/webhook.lua"
LUA_SCRIPT = """
-- Called on the request path.
function envoy_on_request(request_handle)
  request_handle:headers():add("x-lua-header", "true")
end

-- Called on the response path.
function envoy_on_response(response_handle)
  response_handle:headers():add("x-lua-resp-header", "false")
end

"""
LUA_CONFIG = {"name": "lua", "config": {"inline_code": LUA_SCRIPT}}


# polls for file chage
class poller(object):

    def __init__(self):
        self.done = False

    def cancel(self):
        self.done = True

    def __call__(self):
        modtime = 0
        while not self.done:
            time.sleep(10)
            if not os.path.isfile(FILE_PATH):
                continue

            new_modtime = os.path.getmtime(FILE_PATH)
            if new_modtime == modtime:
                continue

            modtime = new_modtime
            with open(FILE_PATH, "rt") as fl:
                ls = fl.read()
                LUA_CONFIG["config"]["inline_code"] = ls

if __name__ == "__main__":
    p = poller()
    threading.Thread(target=p).start()
    app.run(host="0.0.0.0", port=5000)
    p.cancel()
