-- Called on the request path.
function envoy_on_request(request_handle)
  request_handle:headers():add("x-lua-header", "true")
end

-- Called on the response path.
function envoy_on_response(response_handle)
  response_handle:headers():add("x-lua-resp-header", "{nodeid}")
end
