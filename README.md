## PyQt5-LAN-File-Share

本程序是华中科技大学2023学年**陈建文老师的Python公选课**结课作业，选题为*C9: 使用GUI共享文件*。

> 作者：ChlorineC @ HUST CS, 2023
> 
> 作业仅供参考，鼓励独立思考。如果你有任何疑问欢迎联系我：462241980@qq.com

### 技术实现

本程序采用Python内建的 `http` 库，基于HTTP和TCP实现实现目录映射和文件发送，具体方案为：

- 在本地维护一个 `./shared` 目录，默认在这个目录建立HTTP服务器
- 局域网内其他机器访问指定IP地址+端口，获取目录的HTML并交由 `BeautifulSoup` 和 `lxml` 解析出文件名和链接
- 根据解析出的信息在本地渲染出列表，并根据用户输入再次发送HTTP请求（需要注意区分目录请求和文件请求）
- 界面渲染采用 [PyQt5](https://pypi.org/project/PyQt5/) 和 [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 进行绘制

### 如何运行项目

如果你不想探究源码的话，最好的方法是直接通过 [Release](https://github.com/KiritoKing/HUST-Python/releases) 下载独立EXE运行（暂未编译*nix系统版本）

如果你想下载源码自己运行和编译，本项目需要的所有依赖均存储在 `./requirements.txt` 中。注意，本人使用的是 **`conda` 管理的 Python3.11 环境**，其余环境不保证正确运行，简单项目也没做 docker 镜像。

```shell
# Clone this repo
git clone https://github.com/KiritoKing/HUST-Python.git

# Create venv & Install dependencies
conda create --name hust-pyqt5 python=3.11
conda activate hust-pyqt5
conda install --file requirements.txt

# Run main.py in you Conda Prompt
python ./main.py
