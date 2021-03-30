import random
values = ['orange', 'banana', 'grape', 'coin']
output = []
for i in range(3):
    output += [random.choice(values)]

print(output)
print(output.count('coin'))
        