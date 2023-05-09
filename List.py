bicycles = ['trek', 'cannondale', 'rdline', 'specialized']
print(bicycles)
print(bicycles[0])
# python list start from 0

print(bicycles[1].title())
print(bicycles[-1])
print("my bicycle is a" + bicycles[3].upper())

motocycles = ['honda', 'yamaha', 'suzuki']
print(motocycles[0])

motocycles[0] = 'ducati'
print(motocycles[0])

print(motocycles)
motocycles.append('ducati')
print(motocycles)

# use del to delete the factor of the list
del motocycles[0]#delete first ducati
print(motocycles)


del motocycles[1]#delete suzuki
print(motocycles)

# get last factor of the list
popped_motocycle = motocycles.pop()
print(popped_motocycle)

