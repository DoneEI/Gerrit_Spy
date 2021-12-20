# a demo for how to use the tool
from base import SavingUtils
from spy.CodeChangeSpy import CodeChangeSpy
from spy.ReviewCommentSpy import ReviewCommentSpy

community = 'openstack'
project = 'nova'

codeChangeSpy = CodeChangeSpy(community, project, {
    'after': '2020-01-01',
    'before': '2021-01-01',
    'status': 'closed'
})

# run codeChangeSpy to get code changes
codeChanges = codeChangeSpy.run()

reviewCommentSpy = ReviewCommentSpy(codeChanges)

# run reviewComments to get review comments of the above code changes
reviewComments = reviewCommentSpy.run()

# output the results
SavingUtils.writeExcel('code changes', 'code changes - %s - %s.xls' % (project, community), codeChanges)
SavingUtils.writeExcel('review comments', 'review comments - %s - %s.xls' % (project, community), reviewComments)
