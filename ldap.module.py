import ldap
import ldap.modlist as modlist
from getpass import getpass
username = 'cn=admin,dc=ldap,dc=com'
password = getpass()
IP = raw_input("Enter a ip address of ldap server (slapd): ")
ldap_url = 'ldap://'+IP+':389'
dn = 'dc=ldap,dc=com'

class my_ldap(object):
    """Create, search, delete"""
    def __init__(self, ldap_url):
        """Initialize connection to server"""
        self.ldap_server = ldap.initialize(ldap_url)
    
    
    def login(self, username, password):
        """login to server""" 
        return self.ldap_server.simple_bind_s(username, password)    

    
    def search(self, dn):       
        """Searching"""
        #dn = Search path
        client_name = raw_input('enter a client name that you want to search : ')
        try:
            result = self.ldap_server.search_s(dn,
                                      ldap.SCOPE_SUBTREE,
                                      'cn='+client_name, #Cn is an attribute in which we search in the value client_name
                                      )
            return result

        except ldap.LDAPError ,e:
            print e 
            
    def create(self):
        """Create object"""
        dn_object = raw_input('Enter the dn that you want to add: ') #New dn, parent folder should be set
        """
        Example:
        Values in the atmosphere of the Mondial
        Attributes of the new ou = Lio
        dn_object = "ou=Lio,dc=ldap,dc=com"
        """
        attrs = {}
        attrs["objectclass"]=["top", "organizationalRole", "simpleSecurityObject"]
        attrs["cn"] = "Argentina"
        attrs["userPassword"] = password
       
        ldif = modlist.addModlist(attrs) #This function changing dictionary to  mod list
        
        try:
            self.ldap_server.add_s(dn_object,ldif) #Add_s function adding to the ldap 
            print 'Ou/User added'
        except ldap.LDAPError, e:
            print e #Cannot connect to server or user is not exist
    
    def create_user(self):
        """create user """
        dn_user = raw_input('Enter the dn that you want to add: ')
        """
        Example: Add user to Lio object
        dn_user = "cn=Messi,ou=Lio,dc=ldap,dc=com"
        """
        attrs = {}
        attrs["objectclass"]=["top", "posixGroup"]
        attrs["gidNumber"] =  raw_input("Enter a gidNumber: ")
        attrs["cn"] = "Argentina"
        attrs["userPassword"] = raw_input("Enter a user password: ")
        ldif = modlist.addModlist(attrs)
        self.ldap_server.add_s(dn_user, ldif)

    def delete_dn(self, dn):
        """Delete dn"""
        try:
            self.ldap_server.delete_s(dn) #dn = Path to delete
            print 'User deleted'
        except ldap.LDAPError, e:
            print e #Cannot connect to server or user is not exist
                    
           
    def close(self):
        """Closing the connection to the server"""
        try:
            self.ldap_server.unbind_s()
        except ldap.LDAPError ,e:
            print e
