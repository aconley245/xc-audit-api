from typing import Optional
from pydantic import BaseModel

class Namespace(BaseModel):
    name: str

class AppFirewall(BaseModel):
    name: str
    namespace: Namespace

class LoadBalancer(BaseModel):
    name: str
    namespace: Namespace
    app_firewall: Optional[AppFirewall] = None

class FirewallNamespace(BaseModel):
    name: Optional[str] = None

class GetAppFirewall(BaseModel):
    name: Optional[str] = None
    namespace: Optional[FirewallNamespace] = None

class GetLoadBalancer(BaseModel):
    name: str
    namespace: Namespace
    app_firewall: Optional[GetAppFirewall] = None

class GetWAF(BaseModel):
    name: str