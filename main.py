from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import Namespace, GetLoadBalancer, AppFirewall
from xc_functions import XC_Functions
from xc_objects import XC_Tenant

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/namespaces')
async def get_namespaces(auth: str = Header(None), tenant: str = Header(None)) -> list[Namespace]:
    if auth == "":
        raise HTTPException(status_code=401, detail="No API Token Received")
    headers = {'Authorization': auth}
    tenant = tenant
    my_tenant = XC_Tenant(name=tenant, auth=headers)
    return my_tenant.namespaces()

@app.get('/api/namespace_loadbalancers/{namespace}')
async def get_namespace_load_balancers(namespace: str, auth: str = Header(None), tenant: str = Header(None)) -> list[GetLoadBalancer]:
    if auth == "":
        raise HTTPException(status_code=401, detail="No API Token Received")
    headers = {'Authorization': auth}
    tenant = tenant
    loadbalancers = XC_Functions.get_all_lbs_for_ns(namespace=namespace, tenant=tenant, auth=headers)
    return loadbalancers

@app.get('/api/all_loadbalancers')
async def get_all_load_balancers(auth: str = Header(None), tenant: str = Header(None)) -> list[GetLoadBalancer]:
    if auth == "":
        raise HTTPException(status_code=401, detail="No API Token Received")
    headers = {'Authorization': auth}
    tenant = tenant
    loadbalancers = XC_Functions.get_all_lbs(tenant=tenant, auth=headers)
    return loadbalancers

@app.get('/api/namespace_waf_policies/{namespace}')
async def get_namespace_waf_policies(namespace: str, auth: str = Header(None), tenant: str = Header(None)) -> list[AppFirewall]:
    if auth == "":
        raise HTTPException(status_code=401, detail="No API Token Received")
    headers = {'Authorization': auth}
    tenant = tenant
    waf_policies = XC_Functions.get_all_waf_policies_for_ns(namespace=namespace, tenant=tenant, auth=headers)
    return waf_policies