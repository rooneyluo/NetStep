NetStep/
├── api/                     # API 層：處理路由和 HTTP 請求
│   ├── v1/                  # API 版本化
│   │   ├── auth.py          # 認證相關的路由
│   │   ├── users.py         # 使用者相關的路由
│   │   ├── events.py        # 活動相關的路由
│   │   └── __init__.py      # 將所有路由匯集
│   └── __init__.py
├── core/                    # 核心功能（全局工具、設定）
│   ├── config.py            # 應用程序配置
│   ├── security.py          # 密碼哈希與 JWT 處理
│   └── __init__.py
├── db/                      # 資料庫相關邏輯
│   ├── migrations/          # 資料庫遷移文件（例如 Alembic）
│   ├── models/              # ORM 模型
│   │   ├── __init__.py      # 匯總所有模型
│   │   ├── users.py         # Users 表模型
│   │   ├── events.py        # Events 表模型
│   │   ├── locations.py     # Locations 表模型
│   │   ├── feedbacks.py     # Feedbacks 表模型
│   │   ├── participants.py  # Participants 表模型
│   │   └── tokens.py        # Tokens 表模型
│   ├── __init__.py          # 資料庫初始化
│   ├── config.py            # 資料庫配置
│   ├── init_db.py           # 資料庫初始化邏輯
│   └── session.py           # 資料庫會話管理
├── features/                # 按功能模組劃分
│   ├── auth/                # 認證模組
│   │   ├── repository.py    # 資料存取層
│   │   ├── service.py       # 業務邏輯層
│   │   ├── schemas.py       # Pydantic 模型
│   │   └── __init__.py
│   ├── users/               # 使用者模組
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── __init__.py
│   ├── events/              # 活動模組
│   │   ├── repository.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── __init__.py
│   └── __init__.py
├── tests/                   # 測試文件
│   ├── unit/                # 單元測試
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── __init__.py
│   ├── integration/         # 整合測試 (跨模組測試)
│   │   ├── test_login_flow.py
│   │   └── __init__.py
│   └── __init__.py
├── utils/                   # 工具函數
│   ├── common.py            # 通用工具 (e.g., 日期處理, 字符串工具)
│   ├── email.py             # 郵件工具
│   └── __init__.py
├── main.py                  # 應用入口
├── requirements.txt         # Python 依賴
└── README.md                # 專案說明文件