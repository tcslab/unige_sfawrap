# specialized Xrn class for unigetestbed TB
import re
from sfa.util.xrn import Xrn

# temporary helper functions to use this module instead of namespace
def hostname_to_hrn (auth, testbed_name, hostname):
    return unigetestbedXrn(auth=auth+'.'+testbed_name,hostname=hostname).get_hrn()
def hostname_to_urn(auth, testbed_name, hostname):
    return unigetestbedXrn(auth=auth+'.'+testbed_name,hostname=hostname).get_urn()
def slicename_to_hrn (auth_hrn, slicename):
    return unigetestbedXrn(auth=auth_hrn,slicename=slicename).get_hrn()
def email_to_hrn (auth_hrn, email):
    return unigetestbedXrn(auth=auth_hrn, email=email).get_hrn()
def hrn_to_unigetestbed_slicename (hrn):
    return unigetestbedXrn(xrn=hrn,type='slice').unigetestbed_slicename()
def hrn_to_unigetestbed_authname (hrn):
    return unigetestbedXrn(xrn=hrn,type='any').unigetestbed_authname()
def xrn_to_hostname(hrn):
    return Xrn.unescape(PlXrn(xrn=hrn, type='node').get_leaf())

class unigetestbedXrn (Xrn):

    @staticmethod 
    def site_hrn (auth, testbed_name):
        return '.'.join([auth,testbed_name])

    def __init__ (self, auth=None, hostname=None, slicename=None, email=None, interface=None, **kwargs):
        #def hostname_to_hrn(auth_hrn, login_base, hostname):
        if hostname is not None:
            self.type='node'
            # keep only the first part of the DNS name
            #self.hrn='.'.join( [auth,hostname.split(".")[0] ] )
            # escape the '.' in the hostname
            self.hrn='.'.join( [auth,Xrn.escape(hostname)] )
            self.hrn_to_urn()
        #def slicename_to_hrn(auth_hrn, slicename):
        elif slicename is not None:
            self.type='slice'
            # split at the first _
            parts = slicename.split("_",1)
            self.hrn = ".".join([auth] + parts )
            self.hrn_to_urn()
        #def email_to_hrn(auth_hrn, email):
        elif email is not None:
            self.type='person'
            # keep only the part before '@' and replace special chars into _
            self.hrn='.'.join([auth,email.split('@')[0].replace(".", "_").replace("+", "_")])
            self.hrn_to_urn()
        elif interface is not None:
            self.type = 'interface'
            self.hrn = auth + '.' + interface
            self.hrn_to_urn()
        else:
            Xrn.__init__ (self,**kwargs)

    #def hrn_to_pl_slicename(hrn):
    def unigetestbed_slicename (self):
        self._normalize()
        leaf = self.leaf
        sliver_id_parts = leaf.split(':')
        name = sliver_id_parts[0]
        name = re.sub('[^a-zA-Z0-9_]', '', name)
        return name

    #def hrn_to_pl_authname(hrn):
    def unigetestbed_authname (self):
        self._normalize()
        return self.authority[-1]

    def interface_name(self):
        self._normalize()
        return self.leaf

    def unigetestbed_login_base (self):
        self._normalize()
        if self.type and self.type.startswith('authority'):
            base = self.leaf 
        else:
            base = self.authority[-1]
        
        # Fix up names of GENI Federates
        base = base.lower()
        base = re.sub('\\\[^a-zA-Z0-9]', '', base)

        if len(base) > 20:
            base = base[len(base)-20:]
        
        return base
