# ONCatQuery
An interim tool to query the ONCat database

In order to use, contact Peter Parker to obtain the credentials, which must be added to lines 8 and 9.

Instructions are included in the script. Users should edit inputs only (between lines 15 and 48)

Filtering uses filter objects that are defined in ONCatTools. They take the format:

obj = FilterObj('thing to test', 'condition', 'value')

Where: 

'thing to test' is a variable stored in oncat (e.g. an item in metadata such as a pv). it is a string
'condition' is a logical represented by a string (e.g. '>','==')
'value' is the value to compare with. can be a string integer or float

Note: the condition '~=', only applies floats and requires an additional value specifying a tolerance

e.g. 

filterObj('daslogs.bl3:det:th:bl:frequency','~=',60.0,0.1)

will be True if daslogs.bl3:det:th:bl:frequency has a value between 59.9 and 60.1

Any filter Objects added to the list `filters` will be tested and all must be true for output to be generated.


