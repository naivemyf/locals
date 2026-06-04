# Localspecialty（当地特产推荐）

> 一个基于 Django 的本地特产发现、分享与管理平台。用户可以浏览特产、阅读相关文章、收藏感兴趣的内容；商家可以注册并发布自己的特色产品；平台通过协同过滤算法为用户提供个性化推荐。

## 功能

### 特产发现与推荐
- **智能推荐引擎**：基于用户收藏行为和兴趣标签，采用协同过滤算法实现个性化特产推荐
- **冷启动处理**：新用户通过兴趣分类选择快速建立偏好画像
- **热门推荐**：展示平台收藏量最高的特产与文章
- **随机推荐**：为未登录或数据不足的用户提供内容发现

### 用户系统
- 用户注册 / 登录 / 注销
- 个人资料查看与编辑
- 密码修改
- 基于角色的权限管理（普通用户、商家、管理员）

### 内容管理
- **特产商品**：支持商品添加、编辑、删除，包含图片上传、标签分类、成份描述
- **文章发布**：集成 CKEditor 富文本编辑器，支持图文混排、代码高亮
- **标签分类**：商品和文章按标签归类，支持标签维度浏览
- **收藏功能**：用户可收藏感兴趣的文章和特产

### 商家系统
- 商家独立注册（含公司信息、法人身份验证）
- 商家专属登录入口
- 商品管理（添加、查看、编辑、下架）
- 文章管理（发布、编辑、删除）
- 商家资质审核流程

### 管理员后台
- **内容审核**：文章三级审核（待审核 → 初审 → 审核通过）、商品审核、商家审核
- **批量操作**：支持文章和商品的批量审核
- **公告管理**：发布、编辑、删除系统公告
- **数据统计**：饼图展示文章和商品数据分布
- **敏感词过滤**：基于 Aho-Corasick 自动机的敏感词检测

## 技术栈

| 类别 | 技术 |
|------|------|
| **框架** | Django 6.0.5 |
| **语言** | Python 3.14 |
| **数据库** | SQLite（开发）/ MySQL（生产，腾讯云 CynosDB） |
| **前端** | Bootstrap + jQuery + 原生 CSS/JS |
| **富文本** | django-ckeditor |
| **图片处理** | Pillow |
| **敏感词过滤** | pyahocorasick（AC 自动机） |
| **编码检测** | chardet |
| **数据库驱动** | PyMySQL |

## 项目结构

```
Localspecialty/
├── Localspecialty/         # Django 项目配置
│   ├── settings.py         # 全局配置（数据库、中间件、CKEditor 等）
│   ├── urls.py             # 路由配置
│   ├── wsgi.py             # WSGI 入口
│   └── asgi.py             # ASGI 入口
├── app/                    # 主应用
│   ├── models.py           # 数据模型（用户、商品、文章、收藏等）
│   ├── admin.py            # Django Admin 配置
│   ├── middleware/
│   │   └── auth.py         # 登录认证中间件
│   ├── view/               # 视图函数
│   │   ├── index.py        # 首页与推荐逻辑
│   │   ├── account.py      # 用户账户管理
│   │   ├── article.py      # 文章 CRUD
│   │   ├── commdity.py     # 商品 CRUD
│   │   ├── admin.py        # 管理员后台
│   │   ├── merchant.py     # 商家功能
│   │   ├── localspec.py    # 兴趣选择
│   │   ├── user_recommd.py # 推荐算法
│   │   └── find.py         # 搜索发现
│   ├── utils/              # 工具模块
│   │   ├── auth_utils.py   # 登录工具
│   │   ├── bootsrap.py     # Bootstrap 表单封装
│   │   ├── code.py         # 验证码
│   │   ├── const.py        # 常量
│   │   ├── encrypt.py      # 加密工具
│   │   ├── form.py         # 表单定义
│   │   ├── pagination.py   # 分页组件
│   │   ├── sensitivewords.py # 敏感词过滤
│   │   └── uploadImage.py  # 图片上传
│   ├── migrations/         # 数据库迁移文件
│   └── templates/          # 模板文件
│       ├── user/           # 用户端页面
│       ├── admin/          # 管理端页面
│       ├── article/        # 文章页面
│       ├── commdity/       # 商品页面
│       └── merchant/       # 商家页面
├── static/                 # 静态资源
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── pic/                # 用户上传图片
│   ├── ckeditor/           # CKEditor 静态文件
│   └── plugins/
├── manage.py               # Django 管理入口
├── requirements.txt        # Python 依赖
└── db.sqlite3              # SQLite 数据库文件
```

## 模型

| 模型 | 说明 |
|------|------|
| `Role` | 角色表（用户 / 商家 / 管理员） |
| `User` | 用户表（含子管理员申请、商家审核状态） |
| `Commdity` | 商品表（特产名、成份、描述、图片、标签、审核状态） |
| `Article` | 文章表（标题、内容、作者、关联特产、三级审核） |
| `Enshrine` | 收藏表（支持收藏文章和商品） |
| `Choice` | 兴趣分类表（用于冷启动推荐） |
| `Recommend` | 用户兴趣评分表 |
| `Merchant` | 商家信息表（公司名称、法人信息等） |
| `Message` | 系统公告表 |


### 环境要求

- Python 3.10+
- pip

### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd Localspecialty

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 执行数据库迁移
python manage.py migrate

# 5. 导入初始数据（可选）
python manage.py loaddata data.json

# 6. 启动开发服务器
python manage.py runserver
```

启动后访问 `http://127.0.0.1:8000/` 即可进入首页。

### 数据库配置

默认使用 SQLite 进行开发。如需切换到 MySQL，在 `Localspecialty/settings.py` 中注释掉 SQLite 配置，启用 MySQL 配置并填入正确的数据库连接信息。

## 推荐算法

基于用户的协同过滤推荐系统：

1. **用户画像构建**：根据用户收藏的文章和商品标签，统计各标签的收藏频次
2. **相似度计算**：使用距离计算目标用户与其他用户的相似度
3. **Top-N 推荐**：找到最相似用户，将其偏好标签与目标用户标签融合
4. **冷启动处理**：新用户通过兴趣分类选择建立初始偏好，收藏不足时使用热门推荐或随机推荐
5. **混合推荐**：协同过滤结果 + 个人收藏热榜融合排序

## 路由

### 用户端
| 路由 | 说明 |
|------|------|
| `/` `/index/` | 首页 |
| `/login/` | 用户登录 |
| `/register/` | 用户注册 |
| `/user/<id>/info/` | 用户信息 |
| `/user/myinfo/edit/` | 编辑资料 |
| `/user/pd/edit/` | 修改密码 |
| `/user/fav/` | 文章收藏 |
| `/user/favcomm/` | 商品收藏 |
| `/user/mess/list/` | 公告列表 |
| `/chocies/fav/` | 兴趣选择 |
| `/tag/<id>/` | 标签浏览 |
| `/article/list/` | 文章列表 |
| `/article/<id>/detail/` | 文章详情 |
| `/commdity/listall/` | 全部商品 |
| `/commdity/<id>/detail/` | 商品详情 |

### 商家端
| 路由 | 说明 |
|------|------|
| `/merchant/` | 商家首页 |
| `/merchant/login/` | 商家登录 |
| `/merchant/register/` | 商家注册 |
| `/commdity/add/` | 添加商品 |
| `/commdity/list/` | 我的商品 |
| `/article/add/` | 发布文章 |
| `/article/listme/` | 我的文章 |

### 管理端
| 路由 | 说明 |
|------|------|
| `/admin/login/` | 管理员登录 |
| `/admin/` | 管理员首页（审核统计） |
| `/admin/artlistno/` | 待审核文章 |
| `/admin/commlistno/` | 待审核商品 |
| `/admin/melistno/` | 待审核商家 |
| `/admin/mess/add/` | 添加公告 |
| `/admin/chart/pie/` | 数据统计图表 |

## 注意事项

- 项目目前 `DEBUG = True`，`SECRET_KEY` 已暴露，生产环境部署前请务必修改
- `ALLOWED_HOSTS` 仅配置了本地地址，部署时需更新
- 默认使用 SQLite 数据库，生产环境建议切换到 MySQL 或其他高性能数据库
- 媒体文件（用户上传图片）存储在 `static/pic/` 目录下
