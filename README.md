# Vietnam Renewable Energy Dashboard

越南可再生能源厂商展示看板 - 包含EPC承包商、开发商、主机厂商、银行、运维、物流、安装厂商信息。

## ✨ 功能特点

- 🔍 **搜索功能**: 快速搜索公司或项目
- 📊 **交互式看板**: 点击项目查看详细信息（关联的银行、开发商、OEM等）
- 📥 **Excel下载**: 点击看板顶部按钮下载完整Excel报告
- 🔄 **自动更新**: 每季度自动更新数据

## 📁 文件结构

```
EPC O&M TRANSPORTATION Information/
├── index.html                              # 主看板页面（直接浏览器打开）
├── Vietnam_Renewable_Energy_Report.xlsx    # Excel报告（可下载）
├── generate_full_report_v2.py              # 数据生成脚本
├── README.md                               # 说明文档
├── .github/
│   └── workflows/
│       └── update-dashboard.yml            # GitHub Actions 自动更新配置
├── logos/                                  # 公司Logo文件夹
│   ├── IPC_E&C.png
│   ├── PC1_Group.png
│   └── ...
├── ASEAN Wind and Energy Storage...xlsx    # 原始数据（备份，无需上传）
└── Update Vietnam SEPC...xlsx              # 原始数据（备份，无需上传）
```

---

## 🖼️ 如何替换公司Logo

### 方法1：手动替换Logo图片

1. **准备Logo图片**
   - 格式：PNG、JPG、SVG 都可以
   - 建议尺寸：200x200 像素左右（正方形）
   - 背景：透明或白色最佳

2. **命名规则**
   - 文件名格式：`公司名称.png`（空格用下划线替换）
   - 例如：
     - IPC E&C → `IPC_E&C.png`
     - PC1 Group → `PC1_Group.png`
     - Vestas → `Vestas.png`

3. **放入logos文件夹**
   - 将图片放入 `logos/` 文件夹

4. **重新运行脚本**
   ```bash
   python generate_full_report_v2.py
   ```

### 方法2：修改脚本中的Logo URL

打开 `generate_full_report_v2.py`，找到 `epc_companies` 列表（约第20行），修改 `logo_url`：

```python
{
    "name": "IPC E&C",
    "logo_url": "https://your-logo-url.com/logo.png",  # ← 修改这里
    "website": "https://ipcenc.com.vn",
    ...
}
```

### 方法3：直接修改HTML中的Logo

如果不想重新运行脚本，可以直接编辑 `index.html`：

1. 搜索 `<div class="company-logo">`
2. 将 `<img src="logos/xxx.png">` 替换为新的图片路径
3. 或将首字母缩写替换为 `<img src="你的logo路径">`

---

## 🚀 部署到 GitHub Pages

### 步骤1：创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 填写：
   - Repository name: `vietnam-renewable-dashboard`（或其他名称）
   - 选择 **Public**
   - ✅ Add a README file（可选）
4. 点击 **Create repository**

### 步骤2：上传文件

**方法A：网页上传（简单）**

1. 在仓库页面点击 **Add file** → **Upload files**
2. 拖拽以下文件到上传区域：
   - `index.html` - 主看板
   - `Vietnam_Renewable_Energy_Report.xlsx` - Excel报告
   - `logos/` - Logo文件夹
   - `.github/workflows/update-dashboard.yml` - 自动更新配置（可选）
3. 点击 **Commit changes**

> 💡 **注意**: 原始数据Excel文件不需要上传，只需要部署生成后的文件

**方法B：使用Git命令行**

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/vietnam-renewable-dashboard.git
cd vietnam-renewable-dashboard

# 2. 复制文件
# 将 index.html 和 logos/ 文件夹复制到此目录

# 3. 提交并推送
git add .
git commit -m "Add dashboard"
git push origin main
```

### 步骤3：启用GitHub Pages

1. 进入仓库页面
2. 点击 **Settings**（设置）
3. 左侧菜单找到 **Pages**
4. 在 **Source** 下：
   - Branch: 选择 `main`
   - Folder: 选择 `/ (root)`
5. 点击 **Save**

### 步骤4：访问网站

等待1-2分钟后，访问：
```
https://你的用户名.github.io/vietnam-renewable-dashboard/
```

---

## 🔄 自动更新

### 更新周期

考虑到风电项目开发周期较长（通常6-12个月），本看板采用**季度更新**策略：

| 更新时间 | 日期 |
|---------|------|
| Q1 | 1月1日 |
| Q2 | 4月1日 |
| Q3 | 7月1日 |
| Q4 | 10月1日 |

### GitHub Actions 自动更新

本项目已配置 GitHub Actions，会在以下情况自动运行：

1. **定时触发**: 每季度第一天 UTC 00:00（北京时间 08:00）
2. **手动触发**: 在 Actions 页面点击 "Run workflow"
3. **推送触发**: 当 `generate_full_report_v2.py` 被修改时

### 手动触发更新

在 GitHub 仓库页面：
1. 点击 **Actions** 标签
2. 选择 **Update Dashboard** 工作流
3. 点击 **Run workflow** → **Run workflow**

---

## 🔧 手动更新数据

如需更新公司或项目数据：

1. 编辑 `generate_full_report_v2.py`
2. 修改以下数据列表：
   - `epc_companies` - EPC承包商
   - `projects` - 项目信息
   - `banks` - 银行
   - `oems` - 主机厂商
   - `om_contractors` - 运维厂商
   - `logistics_companies` - 物流厂商
   - `installers` - 安装厂商
   - `developers` - 开发商

3. 运行脚本重新生成：
   ```bash
   python generate_full_report_v2.py
   ```

4. 提交更改到 GitHub（会自动触发更新）

---

## 📞 联系

如有问题，请联系项目维护者。
