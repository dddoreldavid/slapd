import ldap
import ldap.modlist as modlist
username='cn=admin,dc=ldap,dc=com'
password='admin'
ldap_url='ldap://10.0.0.16:389'
client_name='ddd'

"""create, search, delete"""
class my_ldap(object):
    """initialize connection to server"""
    def __init__(self, ldap_url):
        self.ldap_server = ldap.initialize(ldap_url)
    
    """login to server""" 
    def login(self, username, password):
        return self.ldap_server.simple_bind_s(username, password)    

 
#cn is an attribute in which we search in the value client_name
#[] is the result attribute that I want to see
#I want to see all the attributes and their values of 'cn'
    def finds_attrs(self, dn):
        try:
            lis_attr = self.ldap_server.search_s(dn,
                                      ldap.SCOPE_SUBTREE,
                                      'cn='+client_name,
                                      [])
            return lis_attr
        except Exception ,e:
            print e 

    def search(self, dc, client_name):
        #searching"""
        try:
            result = self.ldap_server.search_s(dc,
                                      ldap.SCOPE_SUBTREE,
                                      'cn='+client_name,
                                      ['audio'])
            #cn is an attribute in which we search in the value client_name
            #audio of is the result attribute that I want to see
            return result

        except Exception ,e:
            print e 
            
    def create(self, dn):

        #attributes of the new user:
        """dn: cn=new_user,cn=sales_group,ou=sales,cn=admin,dc=ldap,dc=com"""
        attrs = {}
        attrs['cn']='user_two'
        attrs['gidNumber'] = '500'
        attrs['homeDirectory'] = '/home/users/user_two'
        attrs['objectClass'] = ['inetOrgPerson','posixAccount','top']
        attrs['sn'] = 'ddd'
        #add_s function accept modlist type. this function changing dictionary to  mod list
        ldif = modlist.addModlist(attrs)

        try:
        #adding to the ldap 
            self.ldap_server.add_s(dn,ldif)
            print 'User added'
        except Exception, e:
            print e #cannot connect to server or user is not exist
    
    """ delete dn"""
    def delete_dn(self, dn):
        try:
            self.ldap_server.delete_s(dn)
            print 'User deleted'
        except Exception, e:
            print e #cannot connect to server or user is not exist
                    
           
    def close(self):
            #closing the connection to the server
        try:
            self.ldap_server.unbind_s()
        except Exception ,e:
            print e