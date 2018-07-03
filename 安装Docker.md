## 安装Docker

1. sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys  36A1D7869245yumC8950F966E92D8576A8BA88D21E9
2. sudo bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
3. sudo apt-get update
4.  sudo apt-get install -y lxc-docker



## 镜像相关

1、下载镜像

`sudo docker pull ubuntu`

​	默认从Docker HUb 上下载

2、查看当前已有的镜像

`sudo docker images`

3、查看镜像文件的详细信息

`sudo docker inspect  id`

4、搜寻镜像

`docker search `

5、删除镜像

`docker rmi <标签、ID>`

只是删除其一个标签，只剩下最后一个标签的时候就会删除镜像文件。

6、创建镜像

`sudo docker commit -m "message" -a "author" ID  名称`

7、基于本地模板导入

`sudo cat xxx.tar.gz | docker import - ubuntu`

8、存出镜像

`sudo docker save -o xxx.tar <镜像名称`

9、载入镜像

`sudo docker load --input <镜像tar包>`

10、上传镜像

`sudo docker push xxx/xxx:lastest`



## 容器相关

1、新建容器

`sudo docker create -ti ubuntu`

2、创建并启动

`sudo docker -t -i ubuntu /bin/bash`

3、守护态运行容器

`sudo docker run -d ubuntu /bin/bash -c ""`

4、打印容器的输出信息

`sudo docker logs id`

5、终止一个容器

`sudo docker stop id`

6、查看终止状态的容器ID

`sudo docker ps -a  -q`

7、启动容器

`sudo docker start id`

8、重启容器

`sudo docker restart id`

9、进入容器

`sudo docker attach NAME `    #多个窗口attach 一个容器，所有窗口会同步显示

10、进入容器 2

`sudo docker exec -ti id  /bin/bash`

11、删除容器

`sudo docker rm xxx`

12、导出容器

`sudo docker export ce5 > text_for_run.tar`

13、导入容器

`cat test_for_run.tar | sudo docker import - test/ubuntu:v1.0`



## 仓库相关

1、在仓库 中查找镜像文件

`sudo docker search centos`

2、下拉镜像文件

`sudo docker pull centos`

3、自动下载并启动一个registry容器

`sudo docker run -d -p 5000:5000 registry`



## 数据卷

类似于挂载效果

`sudo docker run -d -P --name web -v /webapp training/webapp python app.py`

使用一个training/webapp镜像创建一个web容器，并创建一个数据卷挂载到容器/webapp上

### 挂载一个主机目录作为数据卷

`sudo docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py`

-P 允许外部访问容器需要暴露端口

-v 挂载数据卷选项

/src/webapp 主机路径

: 表明挂载

/opt/webapp  容器路径

training/webapp 镜像文件

python app.py 容器运行命令，这是运行flask 网站

还可以挂载文件

### 数据卷容器

创建容器

`sudo docker run -it -v /dbdata --name=dbdata ubuntu`

其他容器挂载数据卷容器

`sudo docker run -itd --volumes-from dbdata --name=db1 ubuntu`

 --volumes-from dbdata     挂载dbdata数据卷容器

`docker run -itd --net=host --name=ubuntu -v /src:/opt/webapp ubuntu`

数据卷迁移数据

`sudo docker run --volumes-from dbdata -v $(pwd):/backup --name=work ubuntu`



## 网络基础配置

​	启动创建容器的时候，如果不指定对应的参数，在容器外是无法通过网络来访问容器内的网络应用和服务的。

1、动态分配端口

​	`sudo docker run -d -P xxxxx `

2、查看容器是否使用端口

​	`sudo docker ps -l`

3、映射所有接口地址

​	`docker run -d -p 5000:5000 xxx xxxx`

​					主机端口：容器端口

 	映射多个端口出来

​	`docker run -d -p 5000:5000 -p 3000:80 xxx` 

​	多次使用-p就行

4、映射指定的地址到指定的端口

​	`docker run -d -p 127.0.0.1:5000:5000 xx`

​	将127.0.0.1地址的5000端口给容器使用

5、映射到指定地址的任意端口

​	`docker run -d -p 127.0.0.1::5000`

6、查看映射端口配置

​	`sudo docker port xxxx 5000`



## Dockfile的使用

快速创建自定义的镜像。

四部分：基础镜像信息，维护者信息，镜像操作指令， 容器启动执行指令。

注释：#

基础镜像信息：

​	FROM xxx

维护者信息：

​	MAINTAINER     author     email

镜像操作指令：

​	RUN   xxxxx   #shell 命令 进行相关的安装指令



### 指令

#### FROM

​	指定镜像

#### MAINTAINER

​	指定维护者信息

#### RUN

​	使用shell命令，完成初始化安装

#### CMD

​	容器启动时执行。如果用户指定了运行命令，则覆盖掉CMD指定命令

#### EXPOSE

 	容器暴露的端口号

#### ENV

​	设置docker中镜像的环境变量

#### ADD

​	即copy命令，ADD  主机源文件   docker目的路径

#### COPY

​	与ADD 相似，推荐使用

#### ENTRYPOINT

#### VOLUME

​	创建本机的挂载点

#### USER

​	指定容器运行的用户。

#### WORKDIR

​	配置工作目录

#### ONBUILD

​	\#todo

### 创建镜像

​	`docker build -t 生成的镜像标签   指定dockerfile所在的路径`



 



## 遇到的问题

### get D-Bus connection: Operation not permitted

 解决办法：

` docker run --privileged -itd --net=host -v /virus:/virus --name=centos docker.io/centos /usr/sbin/init` 

 















