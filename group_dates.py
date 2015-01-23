
import jython_grouper
from java.text import SimpleDateFormat

def setMembershipTime(session, groupName, memberName, enable_str=None, expire_str=None):
    """
    Set the expiration date for a group member.

    :param session:`The grouper session`
    :param groupName:`The fully qualified group name`
    :param memberName:`The fully qualified member name`
    :param enable_str:`The enable date/time in yyyy-mm-dd HH:MM:SS format`
    :param expire_str:`The expiration date/time in yyyy-mm-dd HH:MM:SS format`
    """
    sdf = SimpleDateFormat("yyy-MM-dd HH:mm:ss")
    if enable_str is not None:
        ts = sdf.parse(enable_str)
        enable_millis = ts.getTime()
    else:
        enable_millis = None
    if expire_str is not None:
        ts = sdf.parse(expire_str)
        expire_millis = ts.getTime()
    else:
        expire_millis = None
    grp = jython_grouper.getGroup(session, groupName) 
    memberships = grp.memberships.toArray()
    for m in memberships:
        member = m.member
        if member.name == memberName:
            m.enabledTimeDb = enable_millis
            m.disabledTimeDb = expire_millis
            m.update()
            return True
    else:
        return False
            
