
from edu.internet2.middleware.grouper.rules import RuleUtils
from edu.internet2.middleware.grouper.rules import RuleCheckType
from edu.internet2.middleware.grouper.rules import RuleIfConditionEnum
from edu.internet2.middleware.grouper.rules import RuleThenEnum
from edu.internet2.middleware.grouper import SubjectFinder
import jython_grouper
import java.lang.RuntimeException


def cascadeRemoval(session, primaryGroup, targetGroup):
    """
    Add a rule to `primaryGroup` so that if a member leaves that group,
    that subject is also removed from `targetGroup`.
    """
    actAs = SubjectFinder.findRootSubject()
    attribAssign = targetGroup.getAttributeDelegate().addAttribute(RuleUtils.ruleAttributeDefName()).getAttributeAssign()
    attribValueDelegate = attribAssign.getAttributeValueDelegate()
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectSourceIdName(), actAs.getSourceId())
    attribValueDelegate.assignValue(RuleUtils.ruleActAsSubjectIdName(), actAs.getId())
    attribValueDelegate.assignValue(RuleUtils.ruleCheckOwnerIdName(), primaryGroup.getId())
    attribValueDelegate.assignValue(RuleUtils.ruleCheckTypeName(), RuleCheckType.membershipRemove.name())
    attribValueDelegate.assignValue(
        RuleUtils.ruleIfConditionEnumName(),
        RuleIfConditionEnum.thisGroupHasImmediateEnabledMembership.name())
    attribValueDelegate.assignValue(
        RuleUtils.ruleThenEnumName(),
        RuleThenEnum.removeMemberFromOwnerGroup.name())
    isValidString = attribValueDelegate.retrieveValueString(RuleUtils.ruleValidName())
    if not isValidString == "T":
        raise java.lang.RuntimeException(isValidString)

