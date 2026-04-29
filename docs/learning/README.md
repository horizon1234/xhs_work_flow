# 学习区

学习区负责解决两个问题：

1. 你需要学哪些技术
2. 这些技术和项目模块如何对应

建议阅读顺序：

1. [architecture.md](architecture.md)
2. [frontend-architecture.md](frontend-architecture.md)
3. [roadmap-12-weeks.md](roadmap-12-weeks.md)

## 学习区目标

在 12 周内补齐实现 V1 所需的关键能力：

1. Python 后端工程化
2. 数据库与缓存
3. 浏览器自动化与采集
4. LLM 调用与 Prompt 设计
5. 图片生成与封面合成
6. React/Next.js 审核台
7. 异步任务与调度
8. 数据分析与优化

## 学习和项目的映射关系

- 学 FastAPI，对应完成后端 API 骨架
- 学 PostgreSQL/Redis，对应完成表结构和任务状态机
- 学 Playwright，对应完成热点采集器原型
- 学 LLM，对应完成选题和文案生成服务
- 学图片处理，对应完成封面生成模块
- 学 Next.js，对应完成审核台页面
- 学调度与队列，对应完成后台任务工作流

## 前端专题

如果你现在主要想补前端，可以优先看：

1. [frontend-architecture.md](frontend-architecture.md)
2. [architecture.md](architecture.md)
3. [roadmap-12-weeks.md](roadmap-12-weeks.md)

## 前端入门补充

如果你之前主要接触后端，可以先把前端项目理解成一套“运行在浏览器里的界面程序”，但它通常不是直接双击某个 `.js` 文件就能打开，而是需要先启动一个前端开发服务。

### 1. `package.json` 是什么

`package.json` 可以理解成前端项目的说明书，主要记录三类信息：

1. 项目名字和版本
2. 依赖了哪些库
3. 可以执行哪些命令

以 `frontend/package.json` 为例：

- `dependencies` 里声明了项目依赖 `next`、`react`、`react-dom`
- `scripts` 里声明了 `dev`、`build`、`start` 这些常用命令

所以 `package.json` 的作用，类似 Python 项目里的“依赖清单 + 项目启动命令说明”。它不是业务代码，但前端项目通常离不开它。

### 2. `npm` 是什么

`npm` 是 Node.js 生态里最常见的包管理工具，可以理解成前端世界里安装依赖和运行脚本的工具。

它常见的用途有：

1. 安装项目依赖，比如 `npm install`
2. 运行 `package.json` 里的脚本，比如 `npm run dev`
3. 管理项目需要的前端库版本

如果类比 Python：

- `npm install` 有点像安装 `requirements.txt` 里的依赖
- `npm run dev` 有点像运行项目定义好的启动命令

### 3. `npm run dev` 是什么

`npm run dev` 的意思是：执行 `package.json` 里 `scripts.dev` 对应的命令。

当前项目里：

```json
"scripts": {
	"dev": "next dev"
}
```

所以 `npm run dev` 实际执行的是 `next dev`。

对这个项目来说，它的作用就是：

1. 启动 Next.js 的前端开发服务
2. 让浏览器可以访问前端页面
3. 在你改代码后自动重新编译和刷新页面

可以把它理解成“把前端项目跑起来”。如果它没有启动，浏览器一般就无法通过 `http://127.0.0.1:3000` 访问这个前端页面。

### 4. 为什么它是一个前端服务

因为 Next.js 不是单纯把静态文件扔给浏览器，它在开发阶段会启动一个本地 Web 服务，负责做这些事情：

1. 接收浏览器请求，比如访问 `/`
2. 根据 `app/` 目录规则找到对应页面，比如 `app/page.js`
3. 编译 React 页面代码
4. 把页面结果返回给浏览器

所以访问首页时，实际过程是：

1. 浏览器访问 `127.0.0.1:3000`
2. Next.js 开发服务收到请求
3. 它把 `app/page.js` 对应的页面渲染出来
4. 浏览器显示这个页面

### 5. 端口为什么默认是 3000

在这个项目里你没有单独看到端口配置，是因为 `next dev` 默认就使用 `3000` 端口。

也就是说，下面这个命令：

```bash
npm run dev
```

本质上等于：

```bash
next dev
```

而 `next dev` 默认端口就是 `3000`。这是 Next.js 的默认行为，不一定非要写在项目配置里。

如果以后你想改端口，常见方式有两种：

```bash
npm run dev -- --port 3001
```

或者：

```bash
PORT=3001 npm run dev
```

### 6. 前端和后端为什么通常都要启动

这个项目当前是前后端分离的开发方式：

1. 后端服务跑在 `8000` 端口，负责提供 API
2. 前端服务跑在 `3000` 端口，负责显示页面和发请求

所以通常需要两个服务同时启动：

1. 启动 FastAPI 后端
2. 启动 Next.js 前端

然后浏览器先访问前端页面，前端页面再通过 `fetch` 去请求后端 API。

### 7. 如果 `npm run dev` 报错怎么办

你当前终端里的退出码是 `127`，这通常表示命令没找到。对前端项目来说，最常见的原因是还没有先安装依赖。

常见启动顺序是：

```bash
cd frontend
npm install
npm run dev
```

如果 `npm install` 成功，项目目录里通常会出现 `node_modules/`，这时再运行 `npm run dev`，Next.js 开发服务才更可能正常启动。
