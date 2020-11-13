import re
p = re.compile('.*\.(jpg|png)$')
print(p.match('foshgfs.jpg').group(0))
#     print('yes')
# else:
#     print('no')