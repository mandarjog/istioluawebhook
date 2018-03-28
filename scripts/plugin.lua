-- local base64 = require "base64"

-- Called on the request path.
function envoy_on_request(request_handle)
  auth = request_handle:headers():get("authorization")
  request_handle:headers():add("x-lua-header", "true")
  if auth == nil or auth == '' then
    request_handle:respond(
      {{[":status"] = "401", ["Content-Type"] = "text/plain", ["WWW-Authenticate"] = "Basic realm=luawebhook"}},
           "authenticate-{nodeid}\nAny username is ok")
  end
end

-- Called on the response path.
function envoy_on_response(response_handle)
  response_handle:headers():add("x-lua-resp-header", "{nodeid}")
end
