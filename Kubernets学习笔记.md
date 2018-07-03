#  Kubernets学习笔记

# 简介

​	一句话：k8s是一个完备的分布式系统支撑平台

​	Service是分布式集群架构的核心，拥有的特征：

1. 拥有一个唯一指定的名字，
2. 拥有一个虚拟IP和端口号（EndPoint)
3. 能够提供某种远程服务的能力
4. 被映射到提供这种服务能力的一组容器应用上。



# kubernets的结构图如下

![](D:\工作笔记\picture\kubernets_node.png)

如上图所示：

​	在运行项目时，我们有必要把为Service提供服务的进程放到容器中进行隔离。这里kubernets引入了Pod对象，将每个服务进程包装到相应的pod中，使其成为Pod中的一个容器。

​	建立关联关系Pod与  Service之间：

​		Pod -------->Label--------->name=mysql<------------Label Selector<------------Service



# 开始实践

