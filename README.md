# jupyter-server

- 这个repository为什么存在？

这个repository用来存放`jupyter server`上的全部`jupyter notebook`文件。

- jupyter server是什么意思？

[jupyter server](http:/47.100.52.214:8888)是我本人使用`阿里云ECS`(Elastic Compute Service)搭建的一个远程`jupyter notebook`程序，仅供个人使用。

# 一、搭建jupyter server

## 1、购买阿里云的ECS云服务器
官网是[阿里云](https://www.aliyun.com/),系统我选择了CentOS 8.4，配置则是乞丐版，一个月￥9。
## 2、配置ECS的ssh，以便远程访问

首先安装openssh-server

```bash
 yum install openssh-server -y
```

然后配置OpenSSH服务（不配置也是可以正常工作的

```bash
vi /etc/ssh/sshd_config
```

常见配置选项：

```text
Port=22  设置SSH的端口号是22(默认端口号为22)

Protocol 2  启用SSH版本2协议

ListenAddress 192.168.0.222  设置服务监听的地址

DenyUsers   user1 user2 foo  拒绝访问的用户(用空格隔开)

AllowUsers  root osmond vivek  允许访问的用户(用空格隔开)

PermitRootLogin  yes  允许root用户登陆

PermitEmptyPasswords no  用户登陆需要密码认证

PasswordAuthentication  yes  启用口令认证方式
```

最后重启openssh

```bash
  service sshd restart
```

本节内容参考自[博客](https://www.cnblogs.com/lvfeilong/p/324343dfadsfds.html)

## 3、用ssh客户端连接ECS，配置jupyter notebook环境

使用命令行连接：

```bash
ssh root@hostIP
例如
ssh root@192.168.0.0
```

也可以使用Xshell之类的工具连接。

*注意ECS的实例密码（也就是服务器root账户的密码）和账号密码是独立的，需要单独设置*

连接之后

### a、安装anaconda，下载清华镜像的安装包，并安装

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```
安装的过程中，遇到初始化conda的选项选择yes

### b、刷新PATH

```bash
source ~/.bashrc
```

### c、更新conda

```bash
conda update conda
```

### d、生成jupyter配置文件，并编辑

在那之前，生成一个密钥，在python中

```python
>>> from notebook.auth import passwd
>>> passwd() # 下面输入两次同样的密码，会返回一个密钥
Enter password:
Verify password:
'argon2:*******'
```

*网上常见的''sha1:xxxx'密钥只是加密算法不同，如果要使用sha1算法加密也可以做如下操作*

```python
>>> from notebook.auth import passwd
>>> p = '' # 你的密码 
>>> passwd(p,'sha1') # 下面输入两次同样的密码，会返回一个密钥
Enter password:
Verify password:
'sha1:*******'
```

```bash
jupyter notebook --generate-config
vim ~/.jupyter/jupyter_notebook_config.py
```

常用配置

```python
c.NotebookApp.allow_remote_access = True   # 允许外部访问
c.NotebookApp.password = u'sha1:xxxxx'  # 刚才生成的密钥
c.NotebookApp.ip = '*' #所有绑定服务器的IP都能访问，若想只在特定ip访问，输入ip地址即可
c.NotebookApp.port = 8888 #将端口设置为自己喜欢的吧，默认是8888
c.NotebookApp.open_browser = False #我们并不想在服务器上直接打开Jupyter Notebook，所以设置成False
c.NotebookApp.notebook_dir = 'xxxx' #这里是设置Jupyter的根目录，若不设置将默认root的根目录，不安全
c.NotebookApp.allow_root = True # 为了安全，Jupyter默认不允许以root权限启动jupyter 
```

## 4、在ECS控制台开放端口

在ECS安全组配置中开放上面设置的端口，然后就可以在浏览器中访问`ip:port`来使用远程的jupyter notebook了！

## 5、后台运行jupyter notebook

```bash
nohup jupyter notebook --allow-root > jupyter.log 2>&1 &
```

`nohup`表示no hang up, 就是不挂起, 于是这个命令执行后即使终端退出, 也不会停止运行

`&`让命令后台允许，另外把日志信息写到jupyter.log中

本命令参考自[博客](https://blog.csdn.net/weixin_42561002/article/details/85382922)

## 7、玩点花样

### a、修改jupyter网页的css，实现自定义字体等

```bash
vi ~/anaconda3/lib/python3.9/site-packages/notebook/static/components/codemirror/lib/codemirror.css
```

这个文件就是jupyter notebook的css，只修改如下的内容就可以实现字体、字号等内容：

复杂的俺也就不会了，懂css的老哥可以自己发挥

```css
.CodeMirror pre.CodeMirror-line-like {
  /* Reset some styles that the rest of the page might have set */
  -moz-border-radius: 0; -webkit-border-radius: 0; border-radius: 0;
  border-width: 0;
  background: transparent;
  font-family: inherit;
  font-size: 20px;
  margin: 0;
  white-space: pre;
  word-wrap: normal;
  line-height: 110%;
  color: inherit;
  z-index: 2;
  position: relative;
  overflow: visible;
  -webkit-tap-highlight-color: transparent;
  -webkit-font-variant-ligatures: contextual;
  font-variant-ligatures: contextual;
}
```

### b、使用juyter notebook的插件

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
```

### c、安装其他的kernel

…………

## 6、配置git

远程服务器可以用git来上传文件（当然也可以用scp等服务

安装git

```bash
 yum install git
```

基本配置

```bash
git config --global user.name "yourusername"
git config --global user.email yourmail@xxx.com
```

然后就可以快乐使用云端的jupyter notebook了~

# 二、安装Rstudio server

先安装R

然后安装Rstudio server

https://www.rstudio.com/products/rstudio/download-server/redhat-centos/

使用

# 三、安装codeserver

安装参考

https://augists.top/SELF/SHARING/STUDY/Code-Server-on-ECS/

服务配置文件：

```bash
vi /etc/systemd/system/code-server.service
```

修改设置：

```bash
vi  ~/.config/code-server/config.yaml
```

后台运行：

```bash
nohup code-server --allow-root > codeserver.log 2>&1 &
```



# 四、安装vue开发环境

使用conda创建nodejs虚拟环境

```bash
conda create -n node nodejs
```

# 五、使用docker搭建镜像

使用一键安装命令

```bash
curl -sSL https://get.daocloud.io/docker | sh
```

启动服务

```bash
systemctl start docker
```

