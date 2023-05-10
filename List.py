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

motocycles.insert(0, 'ducati')

# use del to delete the factor of the list
del motocycles[0]#delete first ducati
print(motocycles)


del motocycles[1]#delete suzuki
print(motocycles)

# get last factor of the list
motocycles = ['honda', 'yamaha', 'suzuki']
print(motocycles)
popped_motocycle = motocycles.pop()
print(popped_motocycle)
print(motocycles)

# pop any factor with certain position
pop_one = motocycles.pop(0)
print(pop_one)

motocycles = ['honda', 'yamaha', 'suzuki', 'honda']
motocycles.remove('honda')
print(motocycles)
motocycles.remove('honda')
print(motocycles)





