
"""FastAPI 后端应用入口。

这个文件负责创建并暴露整个后端服务的 app 对象，通常会作为启动入口被 Uvicorn 或其他 ASGI 服务器加载。

补充说明：
1. `from xxx import yyy` 的意思：从模块 `xxx` 中导入名字为 `yyy` 的对象，之后当前文件里可以直接使用 `yyy`，不必写成 `xxx.yyy`。
2. `async def` 定义的是异步函数：调用后返回协程对象，通常配合 `await` 使用，适合处理网络 IO、数据库 IO 这类等待型任务。
3. 注解通常指类型注解，例如 `_: FastAPI`、`-> AsyncIterator[None]`、`-> FastAPI`，作用是说明参数和返回值的预期类型，便于阅读、补全和静态检查。
4. Python 定义变量通常直接写 `name = value`；定义方法或函数通常写 `def func(...):`，如果是异步函数则写 `async def func(...):`。
"""

# 从 Python 标准库 `collections.abc` 中导入 `AsyncIterator`。
# `AsyncIterator` 是异步迭代器类型注解，这里用来说明 lifespan 会异步地产生流程控制。
from collections.abc import AsyncIterator
# 从 Python 标准库 `contextlib` 中导入 `asynccontextmanager`。
# 这个装饰器可以把一个异步生成器函数包装成“异步上下文管理器”，常用于应用启动/关闭生命周期。
from contextlib import asynccontextmanager

# 从 FastAPI 框架中导入 `FastAPI` 主类，用来创建 Web 应用实例。
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 从项目的路由汇总模块中导入总路由对象，用于把所有 API 挂载到应用上。
from app.api.router import api_router
# 从项目配置模块中导入 `settings` 配置对象，用于读取应用名、版本、API 前缀等配置。
from app.core.config import settings
# 从数据库会话模块中导入 `init_db`，用于在应用启动时初始化数据库相关资源。
from app.db.session import init_db


# `@asynccontextmanager` 表示下面的异步函数会被当作异步上下文管理器使用。
# FastAPI 会在应用启动时进入这个上下文，在应用关闭时退出这个上下文。
@asynccontextmanager
# `async def` 定义异步函数。
# `_: FastAPI` 里的 `_` 是参数名，表示这里接收一个 FastAPI 实例但当前实现里不会使用它。
# `FastAPI` 是这个参数的类型注解。
# `-> AsyncIterator[None]` 是返回值注解，表示这个函数会返回一个异步迭代器，且这里不产出业务值。
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # 调用数据库初始化逻辑，通常用于建表、准备连接或初始化底层资源。
    init_db()
    # `yield` 把启动阶段和关闭阶段分隔开。
    # `yield` 之前的代码在应用启动时执行，`yield` 之后的代码会在应用关闭时执行。
    yield


# 使用普通的 `def` 定义同步函数；函数名是 `create_app`。
# `-> FastAPI` 是返回值注解，表示这个函数返回一个 FastAPI 应用实例。
def create_app() -> FastAPI:
    # Python 里定义变量通常直接写 `变量名 = 值`。
    # 这里定义了局部变量 `app`，值是新创建的 FastAPI 应用对象。
    app = FastAPI(
        # 设置应用标题，通常会显示在 Swagger 文档页面中。
        title=settings.app_name,
        # 设置应用版本号，也会显示在接口文档中。
        version=settings.app_version,
        # 设置 Swagger 文档地址为 `/docs`。
        docs_url="/docs",
        # 设置 ReDoc 文档地址为 `/redoc`。
        redoc_url="/redoc",
        # 注册应用生命周期处理函数；FastAPI 会在启动/关闭时调用上面的 `lifespan`。
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 把项目里的总路由注册到应用上，并统一加上配置中的 API 前缀。
    app.include_router(api_router, prefix=settings.api_prefix)
    # 返回创建好的 FastAPI 应用实例。
    return app


# 在模块加载时直接创建全局变量 `app`。
# 这样像 `uvicorn app.main:app` 这样的启动命令就可以直接拿到应用对象。
app = create_app()
