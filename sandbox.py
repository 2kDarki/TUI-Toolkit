from tuikit import listools

nested = [1, [2, 3, [4, 5, 6], [7], 8], [9]]
print(listools.flatten(nested, to=tuple))