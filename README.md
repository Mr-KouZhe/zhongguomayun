 **导语：** 一直没有时间开放个人对人脸识别技术的研究成果，目前自己的工作出现了空挡期，与大家分享一下自己业余时间研究的人脸技术相关的知识，希望能给和我一样对人工智能这个高逼格的学科感兴趣的朋友一些帮助.因为是后期的文档可能有些在研究中间遇到的怪异的问题，没有记录，所以中间大家如果遇到什么错误，可以联系我。日后会不断的更新，与君共勉。

 >  **windows下安装人脸技术相关的环境** 

-  **下载并安装anaconda** 

Anaconda是一个用于科学计算的Python发行版，支持 Linux, Mac, Windows系统，提供了包管理与环境管理的功能，可以很方便地解决多版本python并存、切换以及各种第三方包安装问题。Anaconda利用工具/命令conda来进行package和environment的管理，并且已经包含了Python和相关的配套工具。

这里先解释下conda、anaconda这些概念的差别。conda可以理解为一个工具，也是一个可执行命令，其核心功能是包管理与环境管理。包管理与pip的使用类似，环境管理则允许用户方便地安装不同版本的python并可以快速切换。Anaconda则是一个打包的集合，里面预装好了conda、某个版本的python、众多packages、科学计算工具等等，所以也称为Python的一种发行版。其实还有Miniconda，顾名思义，它只包含最基本的内容——python与conda，以及相关的必须依赖项，对于空间要求严格的用户，Miniconda是一种选择。

进入下文之前，说明一下conda的设计理念——conda将几乎所有的工具、第三方包都当做package对待，甚至包括python和conda自身！因此，conda打破了包管理与环境管理的约束，能非常方便地安装各种版本python、各种package并方便地切换。

 **Anaconda的安装** 

Anaconda的下载页参见[官网](https://www.anaconda.com/download/)下载，Linux、Mac、Windows均支持。

大家在下载的时候请注意一下版本的问题，（为什么哪，因为python2和python3有着很多的差别，语法上等等，所以看看自己喜欢那个版本的python开发就因人而异吧。）
![输入图片说明](https://gitee.com/uploads/images/2017/1216/125950_daa9ec40_1007473.png "YXVVQZ(CIBV%YVBMZ%O9((A.png")
因为anaconda是国外的吧，大家都明白哈，速度不咋地，不过我们大清华有完美快速的镜像：[清华大学开源软件镜像站](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)不在赘述配置，请前去参考吧！

 **- 安装dlib资源** 

下载 [dlib-18.17.100-cp35-none-win_amd64.whl](https://pypi.org/project/dlib/18.17.100/#files)
打开conda的命令行工具，![输入图片说明](https://gitee.com/uploads/images/2018/0515/095846_302aa977_1007473.png "屏幕截图.png")
命令：pip install dlib-18.17.100-cp35-none-win_amd64.whl,然后就成功了。
更改pycharm的python.exe，为conda中的python.exe,这样就可以使用conda管理的三方库了,包括刚才安装的dlib，就可以使用了
![输入图片说明](https://gitee.com/uploads/images/2018/0515/100147_0ceedded_1007473.png "屏幕截图.png")

 **- 安装opencv资源** 

版本问题：我安装的是python3.6所以对应的opencv也是3

根据安装python的版本下载相应的opencv *.whl文件，笔者是python3.6，所以对应的是opencv_python‑3.2.0‑cp36‑cp36m‑win_amd64.whl这个文件，下载网址是：[http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

下载好后把文件拷贝到D:\Program Files\Anaconda3\Lib\site-packages文件夹下（anaconda安装路径，每个人的不一样，要根据自己的安装路径更改），在该文件下按住Shift建+鼠标右键，出来一个对话框，选择‘在此处打开命令窗口’即可打开doc 窗口，之后执行pip install opencv_python‑3.2.0‑cp36‑cp36m‑win_amd64.whl 安装opencv3，执行完，显示成功安装 opencv-python‑3.2.0，就应该没问题

>  **安装的过程可能有些错误** 

pip安装报错：is not a supported wheel on this platform

[https://www.cnblogs.com/nice-forever/p/5371906.html](https://www.cnblogs.com/nice-forever/p/5371906.html)


>  **

### Linux下安装
** 

下载Anaconda
https://www.anaconda.com/download/#linux
执行：Anaconda2-4.0.0-Linux-x86_64.sh
安装 OpenCV
conda install opencv
安装完后 
import cv2
如果没有提示错误，即安装成功。 

dlib安装
conda install -c conda-forge dlib
安装完后
import dlib
如果没有提示错误，即安装成功。


然后你就可以happy的玩转人脸技术了，嗨起来吧，老铁
