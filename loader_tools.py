
import jython_grouper
from edu.internet2.middleware.grouper.app.loader.ldap import LoaderLdapUtils
from edu.internet2.middleware.grouper.app.loader import GrouperLoader

def connect_group_to_ldap_source(session, group_name, ldap_base_dn, ldap_group_filter, **kwds):
    """
    :param:`session`: A Grouper session.
    :param:`group_name`: A grouper group name.
    :param:`ldap_base_dn`: The base DN from which to search for the LDAP group.
    :param:`ldap_group_filter`: An LDAP filter that will result in a single group being returned. 

    Returns the Grouper group that was connected to LDAP.
    """
    server_id = kwds.get("server_id", "personLdap")
    subj_attrib_name = kwds.get("subj_attrib_name", "member")
    subj_id_type = kwds.get("subj_id_type", "subjectIdentifier")
    
    group = jython_grouper.getGroup(session, group_name)

    attrib_delegate = group.getAttributeDelegate()
    attr_def_name = LoaderLdapUtils.grouperLoaderLdapAttributeDefName() 
    result = attrib_delegate.assignAttribute(attr_def_name)
    attrib_assign = result.getAttributeAssign()
    attr_value_delegate = attrib_assign.getAttributeValueDelegate()
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapTypeName(), "LDAP_SIMPLE")
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapFilterName(), ldap_group_filter)   
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapQuartzCronName(), "* * * * * ?") 
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSearchDnName(), ldap_base_dn)
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapServerIdName(), server_id) 
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectAttributeName(), subj_attrib_name)    
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectIdTypeName(), subj_id_type)
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapErrorUnresolvableName(), "false")            
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectExpressionName(), '''${loaderLdapElUtils.convertDnToSpecificValue(subjectId)}''')
    return group

def run_loader_for_group(session, group):
    """
    """
    GrouperLoader.runJobOnceForGroup(session, group)

