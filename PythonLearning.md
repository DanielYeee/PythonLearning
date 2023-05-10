## Python Learning Note

---
#### 列表
##### 1.创建
``` 
bicycles = ['trek', 'cannondale', 'rdline', 'specialized']
```

##### 2.访问
```
print(bicycles)
print(bicycles[0]) # python list start from 0
```

##### 3. 添加元素
* append(): 将元素追加到列表中，从0位置开始
* insert(position, value): 传入位置参数和值，将值插入到指定的位置
```
motocycles.append('ducati')
motocycles.insert(0, 'ducati')
```

##### 4. 删除元素
* del: 会直接删除列表中的元素，没有返回值
* pop(): 空值则会默认弹出列表末端的元素List[-1]作为返回值, 可提供位置参数弹出元素
* remove(): 删除一个指定值的元素，如果有多个重名的元素则删除第一个找到的元素，从左到右
```
#del//delete the one factor of the list straightly 
motocycles = ['honda', 'yamaha', 'suzuki']
del motocycles[1] #delete suzuki

#pop()//get last factor of the list by default
motocycles = ['honda', 'yamaha', 'suzuki']
print(motocycles)
popped_motocycle = motocycles.pop()

pop_one = motocycles.pop(0)

#remove()//remove the first one factor with certainly value
motocycles = ['honda', 'yamaha', 'suzuki', 'honda']
motocycles.remove('honda')
print(motocycles)
motocycles.remove('honda')
print(motocycles)
```
