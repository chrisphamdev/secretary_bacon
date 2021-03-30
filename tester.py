import random
multiplier = 0
values = ['orange', 'banana', 'grape', 'coin']
emoji_dict = {'orange':'🍊', 'banana':'🍌', 'grape':'🍇', 'coin':'💰'}
output = []
for i in range(3):
 output += [random.choice(values)]
        
if output[0] == output[1] and output[0] == output[2]:
    if output[0] == 'coin':
        multiplier = 5
    else:
            multiplier = 3
elif output[0] == output[1] or output[1] == output[2] or output[0] == output[2]:
    if output.count('coin') == 2:
        multiplier = 2.5
    else:
        multiplier = 2
elif 'coin' in output:
    multiplier = 0.5
else:
    multiplier = 0


print(output)
for i in range(len(output)):
    output[i] = emoji_dict[output[i]]

print(output)
print(multiplier)

        