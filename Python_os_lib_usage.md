## Python常用标准库之os

**os模块的主要功能：系统相关、目录及文件操作、执行命令和管理进程**

在使用os模块的时候，如果出现了问题，会抛出OSError异常，表明无效的路径名或文件名，或者路径名(文件名)无法访问，或者当前操作系统不支持该操作。

<br><br>

### 系统相关

```
os.name  #查看当前操作系统的名称。windows平台下返回'nt'，Linux则返回'posix'。
os.environ  #获取系统环境变量
os.sep  #当前平台的路径分隔符。在windows下，为'\'，在POSIX系统中，为'/'。
os.altsep  #可替代的路径分隔符，在Windows中为'/'。
os.extsep   #文件名和文件扩展名之间分隔的符号，在Windows下为'.'。
os.pathsep  #PATH环境变量中的分隔符，在POSIX系统中为':'，在Windows中为';'。
os.linesep  #行结束符。在不同的系统中行尾的结束符是不同的，例如在Windows下为'\r\n'。
os.devnull  #在不同的系统上null设备的路径，在Windows下为'nul'，在POSIX下为'/dev/null'。
os.defpath  #当使用exec函数族的时候，如果没有指定PATH环境变量，则默认会查找os.defpath中的值作为子进程PATH的值。
```
<br>

### 文件和目录操作

```
os.getcwd() #获取当前工作目录，即当前python脚本工作的目录路径
os.chdir("dirname") #改变当前脚本工作目录；相当于shell下cd
os.curdir   #返回当前目录: ('.')
os.pardir   #获取当前目录的父目录字符串名：('..')
os.makedirs('dir1/dir2')    #可生成多层递归目录
os.removedirs(‘dirname1’)   #递归删除空目录（要小心）
os.mkdir('dirname') #生成单级目录
os.rmdir('dirname') #删除单级空目录，若目录不为空则无法删除并报错
os.listdir('dirname')   #列出指定目录下的所有文件和子目录，包括隐藏文件
os.remove('filename')   #删除一个文件
os.rename("oldname","new")  #重命名文件/目录
os.stat('path/filename')    #获取文件/目录信息
os.path.abspath(path)   #返回path规范化的绝对路径
os.path.split(path) #将path分割成目录和文件名二元组返回
os.path.dirname(path)   #返回path的目录。其实就是os.path.split(path)的第一个元素
os.path.basename(path)  #返回path最后的文件名。如果path以／或\结尾，那么就会返回空值。
os.path.exists(path或者file)  #如果path存在，返回True；如果path不存在，返回False
os.path.isabs(path) #如果path是绝对路径，返回True
os.path.isfile(path)    #如果path是一个存在的文件，返回True。否则返回False
os.path.isdir(path) #如果path是一个存在的目录，则返回True。否则返回False
os.path.join(path1[, path2[, ...]]) #将多个路径组合后返回，第一个绝对路径之前的参数将被忽略
os.path.getatime(path)  #返回path所指向的文件或者目录的最后存取时间
os.path.getmtime(path)  #返回path所指向的文件或者目录的最后修改时间
os.path.getsize(filename)   #返回文件包含的字符数量
```




注：
https://www.jianshu.com/p/eb3d65879a90 Python常用标准库之os