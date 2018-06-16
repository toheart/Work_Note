# shell的一些使用

## 变量=    中间不能加空格

## echo 

​	-e   提供转义功能，如果需要打印格式，那么推荐使用print

​	-n 关闭自动换行

## wc

​	-l  统计文本行数，

​	-w 统计字数

## xargs 的使用

​	find -name "*.sh" | xargs grep ""

​	这样使用可以打印出文件名

## eval

​	可读取一连串的参数，然后再依参数本身的特性来执行 



## 每行读取文件

   cat ./config/cfg_dir_authority | while read paraa parab parac
   do 
        eval chmod $paraa $parab $parac
   done



## 截取字符串

​	${file#*xxxx}



## awk

​	ls -l | awk '{print $}'

​	ls -l | awk '{cmd="xxxx";system(cmd)}' 执行命令



