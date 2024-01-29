# Take away
使用RVM！
### Install
```bash
sudo apt update
sudo apt upgrade
ruby --version
gem install jekyll bundler
bundle init
bundle install
```

### Run
```bash
/bin/bash --login
rvm use ruby-3.1.0
bundle exec jekyll serve
```

如果你想要在本地运行一个GitHub Pages网站，你需要做的主要是克隆该GitHub仓库，并在本地设置一个适合的静态网站服务器。大多数GitHub Pages网站使用Jekyll作为静态网站生成器，但也可能使用其他技术。下面是一般步骤：

### 1. 克隆GitHub仓库
首先，克隆你的GitHub Pages仓库到本地。打开VSCode的终端，使用以下命令：

```bash
git clone [GitHub仓库的URL]
```

### 2. 安装Jekyll（如果使用Jekyll）
如果该GitHub Pages网站使用Jekyll，你需要在本地安装Ruby和Jekyll。请按照以下步骤操作：

- **安装Ruby：** 访问[Ruby官网](https://www.ruby-lang.org/)，下载并安装适合你操作系统的Ruby版本。
- **安装Jekyll和Bundler：** 打开终端或命令提示符，运行以下命令：

  ```bash
  gem install jekyll bundler
  ```

### 3. 运行静态网站服务器
在你的项目目录中，打开终端或命令提示符，执行以下步骤：

- **进入仓库目录：**
  
  ```bash
  cd path/to/your/repo
  ```

- **如果是Jekyll网站，运行Jekyll服务：**

  ```bash
  bundle exec jekyll serve
  ```

  这会启动一个本地服务器，通常在 `http://localhost:4000`。

- **如果不是Jekyll网站，使用HTTP服务器：**
  
  如果网站不是用Jekyll生成的，你可能需要一个简单的HTTP服务器。例如，你可以使用Python的简易HTTP服务器。在Python 3中，你可以在仓库的根目录运行以下命令来启动一个服务器：

  ```bash
  python -m http.server
  ```

  这通常会在 `http://localhost:8000` 启动服务器。

### 注意事项
- 确保你遵循了GitHub Pages仓库中的任何特定说明，因为有些网站可能有特定的依赖或配置要求。
- 如果网站使用了其他静态站点生成器或特定的构建过程，你需要根据相应的文档进行操作。

完成以上步骤后，你就可以在浏览器中输入相应的本地服务器地址来访问你的GitHub Pages网站了。