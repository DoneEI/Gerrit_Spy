# 1. Info
This is a tool for collecting data related to code review process from projects of communities, such as code changes and corresponding review comments. Note that the code review process of communities must be supported by Gerrit since the data collection is based on Gerrit API.
# 2. Usage
The following code comes from Demo.py, which can be founded in the repository.
```python
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
```
You could get more detailed information from the source code comments.

# 3. Customization
## 3.1 Query Parameters
When querying for code changes, parameters could be set to limit the range of the results. To make sure the parameters are all valid, they are predefined in the __queryProperties in class CodeChangeSpy. Users could customize their parameters by following the style of the default parameters in __queryProperties (see class QueryProperty for detailed info).
## 3.2 Data Info Items
Users could also limit the data info items (i.e., code changes and review comments) by setting param info for CodeChangeSpy and ReviewCommentSpy, otherwise default info would be used (see \_\_init__ function of CodeChangeSpy and ReviewCommentSpy for detailed info). 
## 3.3 Output Approach
The results of CodeChangeSpy and ReviewCommentSpy are both a list of dict items. Users could output and save the results by the dafault apporoach (i.e., writing into a excel file by using SavingUtils.writeExcel). Users could also customize their own output approaches based on the structure of results.
