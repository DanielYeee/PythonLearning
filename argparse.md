## Python参数解析工具argparse.ArgumentParser()
<br>

```
argparse是一个Python模块：命令行选项、参数和子命令解析器。

通过命令行运行Python脚本时，可以通过ArgumentParser来高效地接受并解析命令行参数。
```

### 使用流程


新建一个ArgumentParser类对象，然后来添加若干个参数选项，最后通过parse_args()方法解析并获得命令行传来的参数。即主要有三个步骤：
* 创建 ArgumentParser() 对象
* 调用 add_argument() 方法添加参数
* 使用 parse_args() 解析添加的参数


```
import argparser

parser = argparser.ArgumentParser()
parser.add_argument('--param', type = str, default = 'DEFAULT_VALUE', help = 'parameter help message')

parser.parse_args()
```

### 添加参数选项

使用add_argument()来添加参数选项

`parser.add_argument("-v", "--verbosity", help="...", type=int, choices=[0, 1, 2]， default=0)`

* 在使用add_argument来添加参数选项的时候，首先要指定参数的名字argument_name这个属性，可选参数有长短两个名称；
* 在命令行指定位置参数时直接传值，指定可选参数时，先注明长短名称，然后在后面接值；
* help提示参数的作用，type规定了参数的取值类型，choices以列表的形式规定了值域，default规定了参数的默认值

<br><br>
注：
https://www.cnblogs.com/happystudyeveryday/p/16590921.html