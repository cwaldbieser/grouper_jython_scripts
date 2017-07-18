from edu.internet2.middleware.grouper.rules import RuleApi
from edu.internet2.middleware.grouper.rules import RuleUtils
from edu.internet2.middleware.grouper import SubjectFinder
from edu.internet2.middleware.grouper.rules import RuleCheckType                                               
from edu.internet2.middleware.grouper.rules import RuleIfConditionEnum
from edu.internet2.middleware.grouper.rules import RuleThenEnum
import jython_grouper
from java.text import SimpleDateFormat


def makeEphemeral(session, groupName, numDays):
    """
    Add a rule to group so that new members automatically have an end date
    set `numDays` days in the future.
    
    :param session:`Grouper root session`
    :param groupName:`The fully qualified group name`
    :param numDays:`An integer representing the number of days in the future for new memberships to expire`
    """
    actAs = SubjectFinder.findRootSubject()
    group = jython_grouper.getGroup(session, groupName)
    attribAssign = group.getAttributeDelegate().addAttribute(RuleUtils.ruleAttributeDefName()).getAttributeAssign()
    attribValueDelegate = attribAssign.getAttributeValueDelegate()
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectSourceIdName(), actAs.getSourceId())
    attribValueDelegate.assignValue(RuleUtils.ruleRunDaemonName(), "F")
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectIdName(), actAs.getId())            
    attribValueDelegate.assignValue(RuleUtils.ruleCheckTypeName(), RuleCheckType.membershipAdd.name())
    attribValueDelegate.assignValue(RuleUtils.ruleIfConditionEnumName(), RuleIfConditionEnum.thisGroupHasImmediateEnabledNoEndDateMembership.name())
    attribValueDelegate.assignValue(RuleUtils.ruleThenEnumName(), RuleThenEnum.assignMembershipDisabledDaysForOwnerGroupId.name())
    attribValueDelegate.assignValue(RuleUtils.ruleThenEnumArg0Name(), str(numDays))                                                   
    attribValueDelegate.assignValue(RuleUtils.ruleThenEnumArg1Name(), "T")   

def setMembershipTime(session, groupName, memberName, enable_str=None, expire_str=None):
    """
    Set the expiration date for a group member.

    :param session:`The grouper session`
    :param groupName:`The fully qualified group name`
    :param memberName:`The fully qualified member name`
    :param enable_str:`The enable date/time in yyyy-mm-dd HH:MM:SS format`
    :param expire_str:`The expiration date/time in yyyy-mm-dd HH:MM:SS format`
    """
    sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
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

def trigger_temp_membership(session, intakeGroupName, triggeredGroupName, numDays):
    """
    Add a rule to group so that when new members are added to an intake group,
    they are added to the triggered group for `numDays` days.
    
    :param session:`Grouper root session`
    :param intakeGroupName:`The fully qualified group name for the intake group.`
    :param triggeredGroupName:`The fully qualified group name for the group that will have a transient membership.`
    :param numDays:`An integer representing the number of days in the future for new memberships to expire.`
    """
    actAs = SubjectFinder.findRootSubject()
    group = jython_grouper.getGroup(session, triggeredGroupName)
    # Add to triggered group when added to intake.
    attribAssign = group.getAttributeDelegate().addAttribute(RuleUtils.ruleAttributeDefName()).getAttributeAssign()
    attribValueDelegate = attribAssign.getAttributeValueDelegate()
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectSourceIdName(), actAs.getSourceId())
    attribValueDelegate.assignValue(RuleUtils.ruleRunDaemonName(), "F")
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectIdName(), actAs.getId())
    attribValueDelegate.assignValue(RuleUtils.ruleCheckOwnerNameName(), intakeGroupName)
    attribValueDelegate.assignValue(RuleUtils.ruleCheckTypeName(), RuleCheckType.membershipAdd.name())
    attribValueDelegate.assignValue(RuleUtils.ruleThenEnumName(), RuleThenEnum.addMemberToOwnerGroup.name())
    # Make membership transient for triggered group.
    makeEphemeral(session, triggeredGroupName, numDays)

