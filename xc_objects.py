import json
from api_functions import API_Functions

class XC_Tenant:
    def __init__(self, name, auth):
        self.name = name
        self.auth = auth

    def namespaces (self):
        api_endpoint = f'https://{self.name}.console.ves.volterra.io/api/web/namespaces'
        status, bulk_namespaces = API_Functions.api_call(method='get', url=api_endpoint, headers=self.auth)
        namespaces = []
        for namespace in bulk_namespaces.json()["items"]:
            namespaces.append({"name": namespace["name"]})
        self.namespaces = namespaces
        return self.namespaces

class XC_Namespace:
    def __init__(self, name, tenant, auth):
        self.name = name
        self.auth = auth
        self.tenant = tenant
    
    def get_loadbalancers(self):
        api_endpoint = f'https://{self.tenant}.console.ves.volterra.io/api/config/namespaces/{self.name}/http_loadbalancers'
        status, bulk_loadbalancers = API_Functions.api_call(method='get', url=api_endpoint, headers=self.auth)
        loadbalancers =[]
        for loadbalancer in bulk_loadbalancers.json()["items"]:
            loadbalancers.append({"name": loadbalancer["name"], "namespace": {"name": self.name}})
        self.loadbalancers = loadbalancers
        return self.loadbalancers
    
    def get_waf_policies(self):
        api_endpoint = f'https://{self.tenant}.console.ves.volterra.io/api/config/namespaces/{self.name}/app_firewalls'
        status, bulk_waf_policies = API_Functions.api_call(method='get', url=api_endpoint, headers=self.auth)
        waf_policies =[]
        for waf_policy in bulk_waf_policies.json()["items"]:
            waf_policies.append({"name": waf_policy["name"], "namespace": {"name": waf_policy["namespace"]}})
        self.waf_policies = waf_policies
        return self.waf_policies


class XC_HTTP_LB:
    def __init__(self, name, namespace, tenant, auth):
        self.name = name
        self.namespace = namespace
        self.auth = auth
        self.api_endpoint = f'https://{tenant}.console.ves.volterra.io/api/config/namespaces/{namespace}/http_loadbalancers/{name}'

    def __str__(self):
        return f'The HTTP LoadBalancer {self.name} exists in the namespace {self.namespace}'
    
    def get_attributes(self):
        '''Queries the XC API to get the name of the Application Firewall applied to the HTTP LB'''
        status, response = API_Functions.api_call("get", self.api_endpoint, headers=self.auth)
        return response
        
    def get_waf_policy(self):
        '''Queries the LB attributes to get the name of the Application Firewall applied to the HTTP LB'''
        attributes = self.get_attributes()
        if 'app_firewall' in attributes.json()["spec"] and 'name' in attributes.json()["spec"]["app_firewall"]:
            self.waf_policy = {"name": attributes.json()["spec"]["app_firewall"]["name"], "namespace" : {"name": attributes.json()["spec"]["app_firewall"]["namespace"] }}
        else:
            self.waf_policy = {"name": None, "namespace": {"name": None}}
        return self.waf_policy
    
    def get_waf_exclusions(self):
        '''Queries the LB attributes to get any WAF exclusion rules'''
        attributes = self.get_attributes()
        if 'waf_exclusion_rules' in attributes.json()["spec"]: #and len(attributes.json()["spec"]["waf_exclusion_rules"]) > 0:
            waf_exclusions = []
            for waf_exclusion in attributes.json()["spec"]["waf_exclusion_rules"]:
                waf_exclusions.append({"name": waf_exclusion["metadata"]["name"], "data": waf_exclusion})
            self.waf_exclusions = waf_exclusions
        else:
            self.waf_exclusions = None
        return self.waf_exclusions
        
