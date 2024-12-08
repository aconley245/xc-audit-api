from xc_objects import XC_Namespace, XC_HTTP_LB, XC_Tenant
    
class XC_Functions:

    def get_all_lbs_for_ns (namespace, tenant, auth):
        queried_namespace = XC_Namespace(name=namespace, tenant=tenant, auth=auth)
        loadbalancers = []
        for loadbalancer in queried_namespace.get_loadbalancers():
            queried_lb = XC_HTTP_LB(namespace=namespace, name=loadbalancer["name"], tenant=tenant, auth=auth)
            loadbalancer["app_firewall"]=queried_lb.get_waf_policy()
            loadbalancer["waf_exclusions"]=queried_lb.get_waf_exclusions()
            loadbalancers.append(loadbalancer)
        return loadbalancers
    
    def get_all_lbs(tenant, auth):
        my_tenant = XC_Tenant(name=tenant, auth=auth)
        all_loadbalancers = []
        for ns in my_tenant.namespaces():
            ns_loadbalancers = XC_Functions.get_all_lbs_for_ns(namespace=ns["name"], tenant=tenant, auth=auth)
            if ns_loadbalancers:
                all_loadbalancers.extend(ns_loadbalancers)
        return all_loadbalancers
    
    def get_all_waf_policies_for_ns (namespace, tenant, auth):
        queried_namespace = XC_Namespace(name=namespace, tenant=tenant, auth=auth)
        waf_policies = queried_namespace.get_waf_policies()
        return waf_policies
    
