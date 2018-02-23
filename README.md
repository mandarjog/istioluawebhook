Simple example of an istio pilot webhook
----------------------------------------

Steps
1. Create a service with 3 POST endpoints. 
   LDS, RDS and CDS
2. Update istio-pilot deployment by adding the following args to the "discovery" container
   --webhookEndpoint http://luawebhook:5000/
3. Deploy the webhook service by
   kubectl apply -n istio-system -f luawebhook.yaml
4. Use luawebhook config map to mount file.


Limitation
----------

At present the config is not refreshed automatically if you update the lua script.
Pilot maintains a cache of the generated config which is recalculated only when there is a change in the environment.
