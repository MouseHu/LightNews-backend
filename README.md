# PKUReader-backend
backend for PKUReader 



## Deployment by docker-compose:

为了方便i在不同环境下的部署与调试，使用了docker来搭建统一的运行环境。另外，为了方便调试，采取了动态的代码加载方法，即在构建docker镜像时不加载代码，而是在运行容器时以volume的形式加载代码。

django仍然运行在debug模式下（自动重新加载代码），方便调试。

数据库的5432的端口暴露在主机上，方便其他程序（如爬虫）调用

1. 安装 docker-ce and docker-compose

   - https://docs.docker.com/install/linux/docker-ce/ubuntu/
   - https://github.com/docker/compose

2. ```bash
   docker-compose build # 搭建docker容器
   docker-compose up # 运行docker容器 （ctrl-C即可停止容器）

   打开另一个shell
   docker container ls #查看正在运行的容器，记下运行django的编号前几位
   docker exec -it <Container ID> bash 

   在打开的bash中运行：
   python manage.py makemigrations core reader
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic

## crawler usage:
````
	import crawler2
	crawler2.craw()
```
you can also specify the source:
```
	import crawler2
	chinadaily=crawler2.ChinaDailyCrawler()
	chinadaily.craw()
```
