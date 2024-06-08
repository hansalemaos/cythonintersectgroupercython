from fragmentparser import get_all_activity_elements

d = get_all_activity_elements(as_pandas=False)
for e in d:
    for ee in e:
        print(ee)
