import re
p='C:/Users/mlrem/Desktop/MyProjects/GroceryStore/ui/order.html'
s=open(p,'r',encoding='utf-8').read()
pattern=re.compile(r'<(/?)([a-zA-Z0-9\-]+)([^>]*)>|<!--|-->',re.S)
self_closing=set(['br','img','input','meta','link','hr'])
stack=[]
for m in pattern.finditer(s):
    whole=m.group(0)
    if whole.startswith('<!--'):
        continue
    if m.group(2) is None:
        continue
    closing=m.group(1)=="/"
    tag=m.group(2).lower()
    attrs=m.group(3) or ''
    if closing:
        if stack and stack[-1]==tag:
            stack.pop()
        else:
            if tag in stack:
                while stack and stack[-1]!=tag:
                    print('Auto-closing tag:',stack.pop())
                stack.pop()
            else:
                print('Unmatched closing tag:',tag)
    else:
        if any(attr.strip().endswith('/') for attr in [attrs]):
            continue
        if tag in self_closing:
            continue
        stack.append(tag)
print('Remaining unclosed tags:',stack)
