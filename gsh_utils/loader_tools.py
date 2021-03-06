
import jython_grouper
from edu.internet2.middleware.grouper.app.loader.ldap import LoaderLdapUtils
from edu.internet2.middleware.grouper.app.loader import GrouperLoader
from edu.internet2.middleware.grouper import GroupTypeFinder       

def connect_group_to_sql_source(session, group_name, db_id, query, **kwds):
    """
    :param `session`: A Grouper session.
    :param `group_name`: A grouper group name.
    :param `db_id`: The database identifier from `grouper-loader.properties`.
    :param `query`: SQL query with result columns `subject_id` and `subject_source_id`. 
    :param `cron`: Optional Quartz cron schedule.  Default: '0 0 0 * * ?'.

    Returns the Grouper group that was connected to the SQL source.
    """
    cron = kwds.get("cron", "0 0 0 * * ?")
    g = jython_grouper.getGroup(session, group_name)
    t = GroupTypeFinder.find("grouperLoader", True)
    g.addType(t)
    g.setAttribute("grouperLoaderDbName", db_id)
    g.setAttribute("grouperLoaderQuartzCron", cron)
    g.setAttribute("grouperLoaderQuery", query)
    g.setAttribute("grouperLoaderScheduleType", "CRON")                                            
    g.setAttribute("grouperLoaderType", "SQL_SIMPLE")  
    return g

def edit_group_sql_source(session, group_name, **kwds):
    """
    Edit the properties of a SQL connected group.

    :param `session`: A Grouper session.
    :param `group_name`: A grouper group name.
    :param `db_id`: Optional.  The database identifier from `grouper-loader.properties`.
    :param `query`: Optional.  SQL query with result columns `subject_id` and `subject_source_id`. 
    :param `cron`:  Optional Quartz cron schedule.
    """
    cron = kwds.get("cron", None)
    db_id = kwds.get("db_id", None)
    query = kwds.get("query", None)
    g = jython_grouper.getGroup(session, group_name)
    if db_id is not None:
        g.setAttribute("grouperLoaderDbName", db_id)
    if cron is not None:
        g.setAttribute("grouperLoaderQuartzCron", cron)
    if query is not None:
        g.setAttribute("grouperLoaderQuery", query)
    return g

def connect_group_to_ldap_source(session, group_name, ldap_base_dn, ldap_group_filter, **kwds):
    """
    :param `session`: A Grouper session.
    :param `group_name`: A grouper group name.
    :param `ldap_base_dn`: The base DN from which to search for the LDAP group.
    :param `ldap_group_filter`: An LDAP filter that will result in a single group being returned. 
    :param `cron`: Optional Quartz cron schedule.  Default: '0 0 0 * * ?'.
    :param `server_id`: Optional LDAP server ID.  Default: 'personLdap'.
    :param `subj_attrib_name`: Optional subject attribute name.  Default: 'member'.
    :param `subj_id_type`: Optional subject ID type.  Default: 'subjectIdentifier'.

    Returns the Grouper group that was connected to LDAP.
    """
    server_id = kwds.get("server_id", "personLdap")
    subj_attrib_name = kwds.get("subj_attrib_name", "member")
    subj_id_type = kwds.get("subj_id_type", "subjectIdentifier")
    cron = kwds.get("cron", "0 0 0 * * ?")
    
    group = jython_grouper.getGroup(session, group_name)

    attrib_delegate = group.getAttributeDelegate()
    attr_def_name = LoaderLdapUtils.grouperLoaderLdapAttributeDefName() 
    result = attrib_delegate.assignAttribute(attr_def_name)
    attrib_assign = result.getAttributeAssign()
    attr_value_delegate = attrib_assign.getAttributeValueDelegate()
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapTypeName(), "LDAP_SIMPLE")
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapFilterName(), ldap_group_filter)   
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapQuartzCronName(), cron) 
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSearchDnName(), ldap_base_dn)
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapServerIdName(), server_id) 
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectAttributeName(), subj_attrib_name)    
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectIdTypeName(), subj_id_type)
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapErrorUnresolvableName(), "false")            
    attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectExpressionName(), '''${loaderLdapElUtils.convertDnToSpecificValue(subjectId)}''')
    return group

def run_loader_for_group(session, group):
    """
    Run the Grouper Loader once for a connected group.

    :param `session`: A Grouper session.
    :param `group`: A grouper group object.
    """
    GrouperLoader.runJobOnceForGroup(session, group)

def edit_group_ldap_source(session, group_name, **kwds):
    """
    :param `session`: A Grouper session.
    :param `group_name`: A grouper group name.
   
    Optional Parameters: 
    :param `ldap_type`: "LDAP_SIMPLE", etc.
    :param `server_id`:
    :param `subj_attrib_name`:
    :param `subj_id_type`: One of "subjectIdentifier", "subjectId".
    :param `ldap_group_filter`: LDAP filter that selects the group.
    :param `ldap_base_dn`: LDAP base DN to which filter is applied.
    :param `cron`: Quartz cron schedule string (e.g. "0 0 0 * * ?").
    :param `error_on_unresolvable_name`: Boolean.
    :param `subj_expr_name`: Jexl expression for extracting subject name.

    Returns the Grouper group that was connected to LDAP.
    """
    ldap_type = kwds.get("ldap_type", None)
    server_id = kwds.get("server_id", "personLdap")
    subj_attrib_name = kwds.get("subj_attrib_name", "member")
    subj_id_type = kwds.get("subj_id_type", "subjectIdentifier")
    cron = kwds.get("cron", None)
    error_on_unresolvable_name = kwds.get("error_on_unresolvable_name", None)
    subj_expr_name = kwds.get("subj_expr_name", None)
    ldap_group_filter = kwds.get('ldap_group_filter', None)
    ldap_base_dn = kwds.get('ldap_base_dn', None)
 
    group = jython_grouper.getGroup(session, group_name)

    attrib_delegate = group.getAttributeDelegate()
    attr_def_name = LoaderLdapUtils.grouperLoaderLdapAttributeDefName() 
    result = attrib_delegate.assignAttribute(attr_def_name)
    attrib_assign = result.getAttributeAssign()
    attr_value_delegate = attrib_assign.getAttributeValueDelegate()
    if ldap_type is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapTypeName(), "LDAP_SIMPLE")
    if ldap_group_filter is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapFilterName(), ldap_group_filter)   
    if cron is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapQuartzCronName(), cron) 
    if ldap_base_dn is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSearchDnName(), ldap_base_dn)
    if server_id is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapServerIdName(), server_id) 
    if subj_attrib_name is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectAttributeName(), subj_attrib_name)    
    if subj_id_type is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectIdTypeName(), subj_id_type)
    if error_on_unresolvable_name is not None:
        if error_on_unresolvable_name:
            value = "true"
        else:
            value = "false"
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapErrorUnresolvableName(), false)            
    if subj_expr_name is not None:
        attr_value_delegate.assignValue(LoaderLdapUtils.grouperLoaderLdapSubjectExpressionName(), subj_expr_name)

    return group

