<p align="center">
  <a href="#简体中文"><img src="https://img.shields.io/badge/语言-简体中文-red" alt="简体中文"></a>
  <a href="#繁體中文"><img src="https://img.shields.io/badge/語言-繁體中文-orange" alt="繁體中文"></a>
  <a href="#english"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/Version-v1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-0-brightgreen" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Tests-66%20passed-success" alt="Tests">
  <img src="https://img.shields.io/badge/Storage-SQLite-informational" alt="SQLite">
  <img src="https://img.shields.io/badge/Platform-OS%20Independent-lightgrey" alt="Cross Platform">
</p>

<p align="center">
  <b>简体中文</b> | <a href="#繁體中文">繁體中文</a> | <a href="#english">English</a>
</p>

---

<h1 align="center" id="简体中文">PromptForge Pro</h1>

<p align="center">
  <b>轻量级终端 AI Prompt 智能管理与优化引擎</b><br>
  <i>在终端中高效管理、评分、搜索和优化你的 AI Prompt</i>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PromptForge-Pro">GitHub 仓库</a> &bull;
  <a href="https://pypi.org/project/promptforge/">PyPI 页面</a> &bull;
  <a href="#快速开始">快速开始</a> &bull;
  <a href="#详细使用指南">使用文档</a>
</p>

---

## 目录

- [项目介绍](#项目介绍)
- [核心特性](#核心特性)
- [快速开始](#快速开始)
- [详细使用指南](#详细使用指南)
  - [add - 添加 Prompt](#add---添加-prompt)
  - [list - 列出 Prompt](#list---列出-prompt)
  - [search - 搜索 Prompt](#search---搜索-prompt)
  - [show - 查看 Prompt 详情](#show---查看-prompt-详情)
  - [edit - 编辑 Prompt](#edit---编辑-prompt)
  - [delete - 删除 Prompt](#delete---删除-prompt)
  - [score - 评分 Prompt](#score---评分-prompt)
  - [export - 导出 Prompt](#export---导出-prompt)
  - [export-all - 批量导出](#export-all---批量导出)
  - [tags - 标签管理](#tags---标签管理)
  - [stats - 统计信息](#stats---统计信息)
  - [tui - 交互式仪表盘](#tui---交互式仪表盘)
  - [version - 版本信息](#version---版本信息)
- [设计思路与迭代规划](#设计思路与迭代规划)
- [打包与部署指南](#打包与部署指南)
- [贡献指南](#贡献指南)
- [开源协议](#开源协议)

---

## 项目介绍

**PromptForge Pro** 是一款专为 AI 时代打造的 **轻量级终端 Prompt 管理与优化引擎**。无论你是 AI 研究者、提示词工程师，还是日常使用 ChatGPT / Claude / Gemini 的重度用户，PromptForge 都能帮助你在命令行中高效地组织、评估和迭代你的 Prompt 库。

在日常使用 AI 大模型的过程中，我们往往会积累大量 Prompt —— 写作助手、代码生成、翻译工具、数据分析......但随着数量增长，**找不到、管不好、评不了** 成了普遍痛点。PromptForge 正是为了解决这些问题而生：

- **找不到？** 内置 TF-IDF 语义搜索引擎，支持中英文混合检索，毫秒级定位目标 Prompt
- **管不好？** 分类 + 标签 + 版本追踪，构建你专属的 Prompt 知识库
- **评不了？** 5 维度智能评分系统，从长度、结构、关键词、清晰度、完整性全面评估 Prompt 质量

> **核心理念：零依赖、纯终端、快如闪电。** PromptForge 仅依赖 Python 标准库，无需安装任何第三方包，SQLite 本地存储确保数据安全，即装即用。

---

## 核心特性

### Prompt 模板管理

完整的 CRUD 操作，支持 **分类** 和 **标签** 双维度组织体系。每个 Prompt 自动生成唯一 ID，支持版本追踪，让你对每一次修改都了然于胸。

```bash
# 添加一个带分类和标签的 Prompt
promptforge add --title "Python 代码审查助手" \
  --content "你是一位资深 Python 开发者，请审查以下代码..." \
  --tags "代码审查,Python,最佳实践" \
  --category coding
```

### 5 维度智能评分

独创的 Prompt 质量评估体系，满分 100 分，从五个关键维度进行量化分析：

| 维度 | 满分 | 评估内容 |
|------|------|----------|
| **长度评分** | 15 | Prompt 长度是否在最佳范围（100-2000 字符） |
| **结构评分** | 25 | 是否包含角色设定、任务描述、输出格式等结构要素 |
| **关键词评分** | 20 | 是否使用明确的行动动词和具体指令 |
| **清晰度评分** | 20 | 句子长度、冗余程度和表达清晰度 |
| **完整性评分** | 20 | 约束条件、示例、边界情况等完整性要素 |

```bash
# 对指定 Prompt 进行评分，获取详细分析和优化建议
promptforge score <id>
```

### TF-IDF 语义搜索

基于 **TF-IDF（词频-逆文档频率）** 算法实现的关键词搜索引擎，原生支持中英文混合分词和模糊匹配：

- 英文单词自动提取和归一化
- 中文字符单字 + 双字组合索引
- 内置中英文双语停用词过滤
- 余弦相似度排序 + 模糊匹配加分
- 搜索结果高亮片段展示

```bash
# 搜索包含"翻译"或"translate"的 Prompt
promptforge search "翻译助手"
```

### 版本追踪与差异对比

每次编辑 Prompt 都会自动创建版本快照，附带变更说明。你可以随时回溯历史版本，对比不同版本之间的差异。

```bash
# 编辑 Prompt，自动记录版本
promptforge edit <id> --content "更新后的内容..." --note "优化了输出格式要求"
```

### 多格式导出

支持将 Prompt 导出为 **JSON、YAML、Markdown、纯文本** 四种格式，满足不同场景的使用需求。支持单个导出和批量导出。

```bash
# 导出为 Markdown 格式
promptforge export <id> --format md

# 批量导出所有 Prompt 为 JSON
promptforge export-all --format json --dir ./my_prompts
```

### TUI 交互式仪表盘

纯文本菜单驱动的交互式终端界面，无需 `curses` 依赖。通过键盘操作即可完成所有 Prompt 管理任务，适合沉浸式工作流。

```bash
# 启动交互式仪表盘
promptforge tui
```

### 使用统计与分析

实时统计你的 Prompt 库使用情况，包括总数、分类分布、平均评分、标签热度等数据，帮助你持续优化 Prompt 质量。

```bash
# 查看统计信息
promptforge stats

# 以 JSON 格式输出，方便程序处理
promptforge stats --json
```

### 全面测试覆盖

内置 **66 个单元测试**，覆盖核心引擎、评分系统、搜索引擎等关键模块，确保代码质量和功能稳定性。

```bash
# 运行测试
pytest tests/ -v
```

---

## 快速开始

### 环境要求

| 项目 | 要求 |
|------|------|
| **Python** | >= 3.9（推荐 3.10+） |
| **操作系统** | Windows / macOS / Linux |
| **外部依赖** | 无（零依赖设计） |
| **磁盘空间** | < 5 MB |

### 安装

**方式一：从 PyPI 安装（推荐）**

```bash
pip install promptforge
```

**方式二：从源码安装（开发模式）**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
pip install -e .
```

**方式三：直接运行（无需安装）**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
python -m promptforge version
```

### 验证安装

```bash
promptforge version
# 输出: PromptForge v1.0.0
```

### 三分钟上手

```bash
# 1. 添加你的第一个 Prompt
promptforge add \
  --title "代码评审助手" \
  --content "你是一位资深软件工程师，擅长代码审查。请从以下维度评审代码：1. 代码质量与可读性 2. 潜在的 Bug 和安全风险 3. 性能优化建议 4. 最佳实践合规性。请用中文回答，并给出具体的改进建议和代码示例。" \
  --tags "代码审查,工程实践,质量" \
  --category coding

# 2. 查看自动评分结果
promptforge score <返回的ID>

# 3. 列出所有 Prompt
promptforge list --sort score --limit 10

# 4. 搜索 Prompt
promptforge search "代码审查"

# 5. 导出为 Markdown
promptforge export <ID> --format md --output review_assistant.md

# 6. 查看统计信息
promptforge stats
```

---

## 详细使用指南

### add - 添加 Prompt

添加一个新的 Prompt 到本地数据库。添加时会自动进行质量评分（可通过 `--no-score` 跳过）。

**语法**

```bash
promptforge add --title <标题> --content <内容> [--category <分类>] [--tags <标签>] [--no-score]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--title` | `-t` | 是 | - | Prompt 标题 |
| `--content` | `-c` | 是 | - | Prompt 内容 |
| `--category` | `-cat` | 否 | `general` | 分类名称 |
| `--tags` | - | 否 | 空 | 标签（逗号分隔） |
| `--no-score` | - | 否 | `false` | 跳过自动评分 |

**使用示例**

```bash
# 添加一个写作助手 Prompt
promptforge add \
  --title "技术博客写作助手" \
  --content "你是一位经验丰富的技术博主。请根据我提供的主题，撰写一篇结构清晰、内容深入的技术博客文章。要求：1. 包含引人入胜的开头 2. 使用代码示例说明关键概念 3. 总结核心要点 4. 字数控制在1500-2000字" \
  --tags "写作,技术博客,内容创作" \
  --category writing

# 添加一个翻译 Prompt，跳过自动评分
promptforge add \
  --title "中英翻译专家" \
  --content "你是一位专业翻译，精通中英双语。请将以下内容翻译为地道的英文，保持原文的语气和风格。" \
  --tags "翻译,双语" \
  --category translation \
  --no-score

# 添加一个数据分析 Prompt
promptforge add \
  -t "数据分析报告生成器" \
  -c "作为数据分析师，请根据提供的原始数据生成一份专业的分析报告。报告应包含：数据概览、趋势分析、异常检测、可视化建议和行动建议。请使用 Markdown 格式输出。" \
  --tags "数据分析,报告,可视化" \
  --category analysis
```

**输出示例**

```
Prompt added successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: 技术博客写作助手
  Score: 78.5/100
```

---

### list - 列出 Prompt

列出数据库中的所有 Prompt，支持按分类、标签过滤，以及多字段排序。

**语法**

```bash
promptforge list [--category <分类>] [--tag <标签>] [--sort <排序字段>] [--order <方向>] [--limit <数量>] [--offset <偏移>]
promptforge ls [同上参数]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--category` | `-cat` | 否 | 全部 | 按分类过滤 |
| `--tag` | `-t` | 否 | 全部 | 按标签过滤 |
| `--sort` | `-s` | 否 | `updated_at` | 排序字段（`updated_at`/`score`/`title`/`created_at`/`usage_count`） |
| `--order` | `-o` | 否 | `desc` | 排序方向（`asc`/`desc`） |
| `--limit` | `-l` | 否 | `20` | 显示数量 |
| `--offset` | - | 否 | `0` | 偏移量（分页用） |

**使用示例**

```bash
# 列出所有 Prompt，按评分从高到低排序
promptforge list --sort score --order desc

# 列出 coding 分类的 Prompt
promptforge list --category coding

# 列出带有"翻译"标签的 Prompt，显示前 5 个
promptforge list --tag 翻译 --limit 5

# 按创建时间升序排列，跳过前 10 条（分页）
promptforge list --sort created_at --order asc --offset 10 --limit 10

# 查看使用次数最多的 Prompt
promptforge list --sort usage_count --limit 10

# 使用短命令别名
promptforge ls -cat writing -s score -l 5
```

---

### search - 搜索 Prompt

使用 TF-IDF 语义搜索引擎查找 Prompt。支持中英文混合搜索和模糊匹配。

**语法**

```bash
promptforge search <查询关键词> [--limit <数量>] [--no-fuzzy]
promptforge find <查询关键词> [同上参数]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | - | 是 | - | 搜索关键词 |
| `--limit` | `-l` | 否 | `10` | 返回结果数量 |
| `--no-fuzzy` | - | 否 | `false` | 禁用模糊匹配 |

**使用示例**

```bash
# 搜索包含"代码"的 Prompt
promptforge search "代码生成"

# 搜索英文关键词
promptforge search "code review best practices"

# 中英文混合搜索
promptforge search "Python 数据分析"

# 限制返回结果数量
promptforge search "翻译" --limit 5

# 禁用模糊匹配，仅精确匹配
promptforge search "API设计" --no-fuzzy

# 使用短命令别名
promptforge find "机器学习"
```

**输出示例**

```
Search results for '代码生成' (3):

  1. Python 代码生成助手 (Score: 85, Match: 0.92)
     ID: a1b2c3d4
     > 你是一位资深 Python 开发者，请根据需求生成高质量的代码...

  2. SQL 查询优化器 (Score: 72, Match: 0.78)
     ID: e5f6g7h8
     > 请优化以下 SQL 查询，提高执行效率...

  3. 代码审查清单 (Score: 68, Match: 0.65)
     ID: i9j0k1l2
     > 请按照以下清单审查代码...
```

---

### show - 查看 Prompt 详情

显示指定 Prompt 的完整信息，包括内容、评分、标签、版本等。

**语法**

```bash
promptforge show <ID>
promptforge view <ID>
```

**参数说明**

| 参数 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | Prompt ID（支持短 ID，即 ID 的前几位） |

**使用示例**

```bash
# 使用完整 ID 查看
promptforge show a1b2c3d4-e5f6-7890-abcd-ef1234567890

# 使用短 ID 查看（只要能唯一识别即可）
promptforge show a1b2c3d4

# 使用别名
promptforge view a1b2c3d4
```

---

### edit - 编辑 Prompt

编辑已有 Prompt 的任意字段。每次编辑会自动创建版本快照。

**语法**

```bash
promptforge edit <ID> [--title <新标题>] [--content <新内容>] [--category <新分类>] [--tags <新标签>] [--note <变更说明>] [--no-score]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--title` | `-t` | 否 | - | 新标题 |
| `--content` | `-c` | 否 | - | 新内容 |
| `--category` | `-cat` | 否 | - | 新分类 |
| `--tags` | - | 否 | - | 新标签（逗号分隔） |
| `--note` | `-n` | 否 | `CLI edit` | 变更说明 |
| `--no-score` | - | 否 | `false` | 跳过自动评分 |

**使用示例**

```bash
# 更新 Prompt 内容
promptforge edit a1b2c3d4 \
  --content "更新后的 Prompt 内容..." \
  --note "增加了输出格式要求和约束条件"

# 更新标题和标签
promptforge edit a1b2c3d4 \
  --title "高级代码审查助手" \
  --tags "代码审查,Python,安全,性能"

# 更新分类
promptforge edit a1b2c3d4 --category devops

# 仅更新内容，跳过重新评分
promptforge edit a1b2c3d4 --content "新内容..." --no-score
```

**输出示例**

```
Prompt updated successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Version: 2
  Score: 82.3/100
```

---

### delete - 删除 Prompt

从数据库中删除指定的 Prompt。默认会要求确认，可通过 `--yes` 跳过。

**语法**

```bash
promptforge delete <ID> [--yes]
promptforge rm <ID> [--yes]
promptforge del <ID> [--yes]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--yes` | `-y` | 否 | `false` | 跳过确认提示 |

**使用示例**

```bash
# 删除 Prompt（会弹出确认提示）
promptforge delete a1b2c3d4

# 直接删除，不询问
promptforge delete a1b2c3d4 --yes

# 使用短命令别名
promptforge rm a1b2c3d4 -y
promptforge del a1b2c3d4 -y
```

---

### score - 评分 Prompt

对指定 Prompt 进行 5 维度质量评分，输出详细的评分报告和优化建议。

**语法**

```bash
promptforge score <ID>
```

**参数说明**

| 参数 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | Prompt ID |

**使用示例**

```bash
# 对 Prompt 进行评分
promptforge score a1b2c3d4
```

**输出示例**

```
Prompt Score Report
====================
Title: Python 代码审查助手
ID: a1b2c3d4

Dimension Scores:
  Length Score:        12.0/15  (良好)
  Structure Score:     20.0/25  (优秀)
  Keyword Score:       16.0/20  (良好)
  Clarity Score:       17.0/20  (良好)
  Completeness Score:  15.0/20  (良好)

Total Score: 80.0/100

Suggestions:
  - 建议添加约束条件，帮助AI更准确地理解需求
  - 建议添加示例，提高输出的可预测性
```

---

### export - 导出 Prompt

将单个 Prompt 导出为指定格式的文件或输出到终端。

**语法**

```bash
promptforge export <ID> --format <格式> [--output <文件路径>] [--with-versions]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--format` | `-f` | 否 | `json` | 导出格式（`json`/`yaml`/`md`/`txt`） |
| `--output` | `-o` | 否 | 终端输出 | 输出文件路径 |
| `--with-versions` | - | 否 | `false` | 包含版本历史 |

**使用示例**

```bash
# 导出为 JSON 格式（输出到终端）
promptforge export a1b2c3d4 --format json

# 导出为 Markdown 文件
promptforge export a1b2c3d4 --format md --output my_prompt.md

# 导出为 YAML，包含版本历史
promptforge export a1b2c3d4 --format yaml --with-versions

# 导出为纯文本
promptforge export a1b2c3d4 -f txt -o prompt.txt

# 自动从文件扩展名推断格式
promptforge export a1b2c3d4 -o my_prompt.json
```

---

### export-all - 批量导出

将所有（或按条件筛选的）Prompt 批量导出到指定目录。

**语法**

```bash
promptforge export-all [--format <格式>] [--dir <目录>] [--category <分类>] [--tag <标签>]
```

**参数说明**

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--format` | `-f` | 否 | `md` | 导出格式（`json`/`yaml`/`md`/`txt`） |
| `--dir` | `-d` | 否 | `./exports` | 导出目录 |
| `--category` | `-cat` | 否 | 全部 | 按分类过滤 |
| `--tag` | `-t` | 否 | 全部 | 按标签过滤 |

**使用示例**

```bash
# 批量导出所有 Prompt 为 Markdown
promptforge export-all --format md --dir ./my_prompt_library

# 仅导出 coding 分类的 Prompt
promptforge export-all --category coding --dir ./coding_prompts

# 导出带有"翻译"标签的 Prompt 为 JSON
promptforge export-all --tag 翻译 --format json --dir ./translation_prompts

# 导出到自定义目录
promptforge export-all -f yaml -d /home/user/backups/prompts
```

---

### tags - 标签管理

列出数据库中所有已使用的标签及其关联的 Prompt 数量。

**语法**

```bash
promptforge tags
```

**使用示例**

```bash
# 查看所有标签
promptforge tags
```

**输出示例**

```
Tags (8):
  代码审查              (5 prompts)
  Python                (8 prompts)
  翻译                  (3 prompts)
  写作                  (4 prompts)
  数据分析              (2 prompts)
  最佳实践              (6 prompts)
  安全                  (2 prompts)
  性能优化              (3 prompts)
```

---

### stats - 统计信息

显示 Prompt 库的综合统计信息，包括总数、分类分布、平均评分等。

**语法**

```bash
promptforge stats [--json]
```

**参数说明**

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--json` | 否 | `false` | 以 JSON 格式输出 |

**使用示例**

```bash
# 查看统计信息（格式化输出）
promptforge stats

# 以 JSON 格式输出（方便脚本处理）
promptforge stats --json
```

**输出示例**

```
PromptForge Statistics
======================
Total Prompts:        42
Total Categories:     6
Total Tags:           18
Average Score:        72.5/100
Top Category:         coding (15 prompts)
Top Tag:              Python (12 prompts)
Latest Prompt:        API 设计指南 (2 hours ago)
```

---

### tui - 交互式仪表盘

启动基于文本菜单的交互式终端界面，通过键盘操作管理 Prompt。

**语法**

```bash
promptforge tui
```

**使用示例**

```bash
# 启动 TUI
promptforge tui
```

TUI 界面提供以下功能菜单：
- 浏览和搜索 Prompt
- 添加和编辑 Prompt
- 评分和导出 Prompt
- 查看统计信息
- 标签管理

> 按 `Ctrl+C` 或选择退出选项即可离开 TUI。

---

### version - 版本信息

显示 PromptForge 的版本号。

**语法**

```bash
promptforge version
promptforge -v
```

**使用示例**

```bash
promptforge version
# 输出: PromptForge v1.0.0
```

---

## 设计思路与迭代规划

### 设计哲学

PromptForge 的核心设计遵循以下原则：

1. **零依赖原则** —— 仅使用 Python 标准库，无需安装任何第三方包。这意味着你可以在任何安装了 Python 3.9+ 的环境中直接使用，不受网络环境限制。

2. **数据自主可控** —— 使用 SQLite 本地存储，所有数据保存在你的机器上。不依赖任何云服务，不收集任何用户数据，确保隐私安全。

3. **渐进式复杂度** —— 简单操作用单条命令完成，复杂操作通过 TUI 交互式界面实现。新手可以快速上手，老手可以高效操作。

4. **中英文原生支持** —— 评分引擎、搜索引擎、停用词库均原生支持中英文，无需额外配置。

### 架构设计

```
promptforge/
  cli.py        # CLI 命令行入口（argparse）
  engine.py     # 核心业务逻辑引擎
  database.py   # SQLite 数据库管理
  scorer.py     # 5 维度质量评分引擎
  searcher.py   # TF-IDF 语义搜索引擎
  exporter.py   # 多格式导出器
  models.py     # 数据模型定义
  tui.py        # TUI 交互式仪表盘
  utils.py      # 工具函数集
```

### 迭代规划

**v1.0（当前版本）**
- [x] Prompt CRUD 管理
- [x] 5 维度质量评分
- [x] TF-IDF 语义搜索
- [x] 版本追踪
- [x] 多格式导出
- [x] TUI 交互式仪表盘
- [x] 使用统计
- [x] 66 个单元测试

**v1.1（规划中）**
- [ ] Prompt 模板市场（社区共享）
- [ ] 导入功能（从 JSON/YAML/Markdown 导入）
- [ ] Prompt 变量模板（支持 `{{variable}}` 占位符）
- [ ] 配置文件支持（自定义评分权重）

**v2.0（远期规划）**
- [ ] Web UI 界面
- [ ] API 服务器模式
- [ ] Prompt A/B 测试
- [ ] 插件系统

---

## 打包与部署指南

### 构建 distribution 包

```bash
# 安装构建工具
pip install build

# 构建 sdist 和 wheel
python -m build

# 构建产物位于 dist/ 目录
ls dist/
# promptforge-1.0.0.tar.gz
# promptforge-1.0.0-py3-none-any.whl
```

### 发布到 PyPI

```bash
# 安装 Twine
pip install twine

# 检查包
twine check dist/*

# 上传到 PyPI（测试环境）
twine upload --repository testpypi dist/*

# 上传到 PyPI（正式环境）
twine upload dist/*
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["promptforge"]
CMD ["tui"]
```

```bash
# 构建镜像
docker build -t promptforge:1.0.0 .

# 运行
docker run -it -v ~/.promptforge:/root/.promptforge promptforge:1.0.0 tui
```

### 数据备份

PromptForge 使用 SQLite 存储数据，数据库文件默认位于用户目录下。你可以直接复制数据库文件进行备份：

```bash
# 备份数据库
cp ~/.promptforge/promptforge.db ~/backup/promptforge_$(date +%Y%m%d).db
```

---

## 贡献指南

我们欢迎并感谢所有形式的贡献！无论你是提交 Bug 报告、改进文档，还是贡献代码，都是对项目的巨大支持。

### 如何贡献

1. **Fork** 本仓库
2. 创建你的特性分支：`git checkout -b feature/amazing-feature`
3. 提交你的改动：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 **Pull Request**

### 开发环境搭建

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=promptforge --cov-report=html
```

### 代码规范

- 遵循 PEP 8 编码规范
- 所有公共函数和方法必须包含文档字符串
- 新功能必须附带对应的单元测试
- 提交信息使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式

### 提交 Issue

如果你发现了 Bug 或有功能建议，请在 [GitHub Issues](https://github.com/gitstq/PromptForge-Pro/issues) 中提交。提交 Issue 时请尽量包含以下信息：

- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 运行环境（Python 版本、操作系统等）

---

## 开源协议

本项目基于 **MIT License** 开源。

```
MIT License

Copyright (c) 2024 PromptForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <b>简体中文</b> | <a href="#繁體中文">繁體中文</a> | <a href="#english">English</a>
</p>

---
---

<h1 align="center" id="繁體中文">PromptForge Pro</h1>

<p align="center">
  <b>輕量級終端 AI Prompt 智慧管理與優化引擎</b><br>
  <i>在終端中高效管理、評分、搜尋和優化你的 AI Prompt</i>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PromptForge-Pro">GitHub 儲存庫</a> &bull;
  <a href="https://pypi.org/project/promptforge/">PyPI 頁面</a> &bull;
  <a href="#快速開始-1">快速開始</a> &bull;
  <a href="#詳細使用指南-1">使用文件</a>
</p>

---

## 目錄

- [專案介紹](#專案介紹)
- [核心特性](#核心特性-1)
- [快速開始](#快速開始-1)
- [詳細使用指南](#詳細使用指南-1)
  - [add - 新增 Prompt](#add---新增-prompt)
  - [list - 列出 Prompt](#list---列出-prompt)
  - [search - 搜尋 Prompt](#search---搜尋-prompt)
  - [show - 查看 Prompt 詳情](#show---查看-prompt-詳情)
  - [edit - 編輯 Prompt](#edit---編輯-prompt)
  - [delete - 刪除 Prompt](#delete---刪除-prompt)
  - [score - 評分 Prompt](#score---評分-prompt)
  - [export - 匯出 Prompt](#export---匯出-prompt)
  - [export-all - 批次匯出](#export-all---批次匯出)
  - [tags - 標籤管理](#tags---標籤管理)
  - [stats - 統計資訊](#stats---統計資訊)
  - [tui - 互動式儀表板](#tui---互動式儀表板)
  - [version - 版本資訊](#version---版本資訊)
- [設計思路與迭代規劃](#設計思路與迭代規劃-1)
- [打包與部署指南](#打包與部署指南-1)
- [貢獻指南](#貢獻指南-1)
- [開源協議](#開源協議-1)

---

## 專案介紹

**PromptForge Pro** 是一款專為 AI 時代打造的**輕量級終端 Prompt 管理與優化引擎**。無論你是 AI 研究者、提示詞工程師，還是日常使用 ChatGPT / Claude / Gemini 的重度使用者，PromptForge 都能幫助你在命令列中高效地組織、評估和迭代你的 Prompt 庫。

在日常使用 AI 大模型的過程中，我們往往會累積大量 Prompt —— 寫作助手、程式碼生成、翻譯工具、資料分析......但隨著數量增長，**找不到、管不好、評不了** 成了普遍痛點。PromptForge 正是為了解決這些問題而生：

- **找不到？** 內建 TF-IDF 語義搜尋引擎，支援中英文混合檢索，毫秒級定位目標 Prompt
- **管不好？** 分類 + 標籤 + 版本追蹤，建構你專屬的 Prompt 知識庫
- **評不了？** 5 維度智慧評分系統，從長度、結構、關鍵詞、清晰度、完整性全面評估 Prompt 品質

> **核心理念：零依賴、純終端、快如閃電。** PromptForge 僅依賴 Python 標準庫，無需安裝任何第三方套件，SQLite 本機儲存確保資料安全，即裝即用。

---

## 核心特性

### Prompt 模板管理

完整的 CRUD 操作，支援**分類**和**標籤**雙維度組織體系。每個 Prompt 自動產生唯一 ID，支援版本追蹤，讓你對每一次修改都了然於胸。

```bash
# 新增一個帶分類和標籤的 Prompt
promptforge add --title "Python 程式碼審查助手" \
  --content "你是一位資深 Python 開發者，請審查以下程式碼..." \
  --tags "程式碼審查,Python,最佳實踐" \
  --category coding
```

### 5 維度智慧評分

獨創的 Prompt 品質評估體系，滿分 100 分，從五個關鍵維度進行量化分析：

| 維度 | 滿分 | 評估內容 |
|------|------|----------|
| **長度評分** | 15 | Prompt 長度是否在最佳範圍（100-2000 字元） |
| **結構評分** | 25 | 是否包含角色設定、任務描述、輸出格式等結構要素 |
| **關鍵詞評分** | 20 | 是否使用明確的行動動詞和具體指令 |
| **清晰度評分** | 20 | 句子長度、冗餘程度和表達清晰度 |
| **完整性評分** | 20 | 約束條件、範例、邊界情況等完整性要素 |

```bash
# 對指定 Prompt 進行評分，取得詳細分析和優化建議
promptforge score <id>
```

### TF-IDF 語義搜尋

基於 **TF-IDF（詞頻-逆文件頻率）** 演算法實作的關鍵詞搜尋引擎，原生支援中英文混合分詞和模糊比對：

- 英文單字自動擷取和正規化
- 中文字元單字 + 雙字組合索引
- 內建中英文雙語停用詞過濾
- 餘弦相似度排序 + 模糊比對加分
- 搜尋結果高亮片段展示

```bash
# 搜尋包含"翻譯"或"translate"的 Prompt
promptforge search "翻譯助手"
```

### 版本追蹤與差異比對

每次編輯 Prompt 都會自動建立版本快照，附帶變更說明。你可以隨時回溯歷史版本，對比不同版本之間的差異。

```bash
# 編輯 Prompt，自動記錄版本
promptforge edit <id> --content "更新後的內容..." --note "優化了輸出格式要求"
```

### 多格式匯出

支援將 Prompt 匯出為 **JSON、YAML、Markdown、純文字** 四種格式，滿足不同場景的使用需求。支援單個匯出和批次匯出。

```bash
# 匯出為 Markdown 格式
promptforge export <id> --format md

# 批次匯出所有 Prompt 為 JSON
promptforge export-all --format json --dir ./my_prompts
```

### TUI 互動式儀表板

純文字選單驅動的互動式終端介面，無需 `curses` 依賴。透過鍵盤操作即可完成所有 Prompt 管理任務，適合沉浸式工作流程。

```bash
# 啟動互動式儀表板
promptforge tui
```

### 使用統計與分析

即時統計你的 Prompt 庫使用情況，包括總數、分類分佈、平均評分、標籤熱度等資料，幫助你持續優化 Prompt 品質。

```bash
# 查看統計資訊
promptforge stats

# 以 JSON 格式輸出，方便程式處理
promptforge stats --json
```

### 全面測試覆蓋

內建 **66 個單元測試**，涵蓋核心引擎、評分系統、搜尋引擎等關鍵模組，確保程式碼品質和功能穩定性。

```bash
# 執行測試
pytest tests/ -v
```

---

## 快速開始

### 環境需求

| 項目 | 需求 |
|------|------|
| **Python** | >= 3.9（建議 3.10+） |
| **作業系統** | Windows / macOS / Linux |
| **外部依賴** | 無（零依賴設計） |
| **磁碟空間** | < 5 MB |

### 安裝

**方式一：從 PyPI 安裝（推薦）**

```bash
pip install promptforge
```

**方式二：從原始碼安裝（開發模式）**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
pip install -e .
```

**方式三：直接執行（無需安裝）**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
python -m promptforge version
```

### 驗證安裝

```bash
promptforge version
# 輸出: PromptForge v1.0.0
```

### 三分鐘上手

```bash
# 1. 新增你的第一個 Prompt
promptforge add \
  --title "程式碼審查助手" \
  --content "你是一位資深軟體工程師，擅長程式碼審查。請從以下維度審查程式碼：1. 程式碼品質與可讀性 2. 潛在的 Bug 和安全風險 3. 效能優化建議 4. 最佳實踐合規性。請用中文回答，並給出具體的改進建議和程式碼範例。" \
  --tags "程式碼審查,工程實踐,品質" \
  --category coding

# 2. 查看自動評分結果
promptforge score <傳回的ID>

# 3. 列出所有 Prompt
promptforge list --sort score --limit 10

# 4. 搜尋 Prompt
promptforge search "程式碼審查"

# 5. 匯出為 Markdown
promptforge export <ID> --format md --output review_assistant.md

# 6. 查看統計資訊
promptforge stats
```

---

## 詳細使用指南

### add - 新增 Prompt

新增一個新的 Prompt 到本機資料庫。新增時會自動進行品質評分（可透過 `--no-score` 跳過）。

**語法**

```bash
promptforge add --title <標題> --content <內容> [--category <分類>] [--tags <標籤>] [--no-score]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--title` | `-t` | 是 | - | Prompt 標題 |
| `--content` | `-c` | 是 | - | Prompt 內容 |
| `--category` | `-cat` | 否 | `general` | 分類名稱 |
| `--tags` | - | 否 | 空 | 標籤（逗號分隔） |
| `--no-score` | - | 否 | `false` | 跳過自動評分 |

**使用範例**

```bash
# 新增一個寫作助手 Prompt
promptforge add \
  --title "技術部落格寫作助手" \
  --content "你是一位經驗豐富的技術博主。請根據我提供的主題，撰寫一篇結構清晰、內容深入的技術部落格文章。要求：1. 包含引人入勝的開頭 2. 使用程式碼範例說明關鍵概念 3. 總結核心要點 4. 字數控制在1500-2000字" \
  --tags "寫作,技術部落格,內容創作" \
  --category writing

# 新增一個翻譯 Prompt，跳過自動評分
promptforge add \
  --title "中英翻譯專家" \
  --content "你是一位專業翻譯，精通中英雙語。請將以下內容翻譯為道地的英文，保持原文的語氣和風格。" \
  --tags "翻譯,雙語" \
  --category translation \
  --no-score

# 新增一個資料分析 Prompt
promptforge add \
  -t "資料分析報告產生器" \
  -c "作為資料分析師，請根據提供的原始資料產生一份專業的分析報告。報告應包含：資料概覽、趨勢分析、異常偵測、視覺化建議和行動建議。請使用 Markdown 格式輸出。" \
  --tags "資料分析,報告,視覺化" \
  --category analysis
```

**輸出範例**

```
Prompt added successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: 技術部落格寫作助手
  Score: 78.5/100
```

---

### list - 列出 Prompt

列出資料庫中的所有 Prompt，支援按分類、標籤過濾，以及多欄位排序。

**語法**

```bash
promptforge list [--category <分類>] [--tag <標籤>] [--sort <排序欄位>] [--order <方向>] [--limit <數量>] [--offset <偏移>]
promptforge ls [同上參數]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--category` | `-cat` | 否 | 全部 | 按分類過濾 |
| `--tag` | `-t` | 否 | 全部 | 按標籤過濾 |
| `--sort` | `-s` | 否 | `updated_at` | 排序欄位（`updated_at`/`score`/`title`/`created_at`/`usage_count`） |
| `--order` | `-o` | 否 | `desc` | 排序方向（`asc`/`desc`） |
| `--limit` | `-l` | 否 | `20` | 顯示數量 |
| `--offset` | - | 否 | `0` | 偏移量（分頁用） |

**使用範例**

```bash
# 列出所有 Prompt，按評分從高到低排序
promptforge list --sort score --order desc

# 列出 coding 分類的 Prompt
promptforge list --category coding

# 列出帶有"翻譯"標籤的 Prompt，顯示前 5 個
promptforge list --tag 翻譯 --limit 5

# 按建立時間升序排列，跳過前 10 條（分頁）
promptforge list --sort created_at --order asc --offset 10 --limit 10

# 查看使用次數最多的 Prompt
promptforge list --sort usage_count --limit 10

# 使用短命令別名
promptforge ls -cat writing -s score -l 5
```

---

### search - 搜尋 Prompt

使用 TF-IDF 語義搜尋引擎查找 Prompt。支援中英文混合搜尋和模糊比對。

**語法**

```bash
promptforge search <查詢關鍵詞> [--limit <數量>] [--no-fuzzy]
promptforge find <查詢關鍵詞> [同上參數]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `query` | - | 是 | - | 搜尋關鍵詞 |
| `--limit` | `-l` | 否 | `10` | 傳回結果數量 |
| `--no-fuzzy` | - | 否 | `false` | 停用模糊比對 |

**使用範例**

```bash
# 搜尋包含"程式碼"的 Prompt
promptforge search "程式碼產生"

# 搜尋英文關鍵詞
promptforge search "code review best practices"

# 中英文混合搜尋
promptforge search "Python 資料分析"

# 限制傳回結果數量
promptforge search "翻譯" --limit 5

# 停用模糊比對，僅精確比對
promptforge search "API設計" --no-fuzzy

# 使用短命令別名
promptforge find "機器學習"
```

**輸出範例**

```
Search results for '程式碼產生' (3):

  1. Python 程式碼產生助手 (Score: 85, Match: 0.92)
     ID: a1b2c3d4
     > 你是一位資深 Python 開發者，請根據需求產生高品質的程式碼...

  2. SQL 查詢最佳化器 (Score: 72, Match: 0.78)
     ID: e5f6g7h8
     > 請最佳化以下 SQL 查詢，提高執行效率...

  3. 程式碼審查清單 (Score: 68, Match: 0.65)
     ID: i9j0k1l2
     > 請按照以下清單審查程式碼...
```

---

### show - 查看 Prompt 詳情

顯示指定 Prompt 的完整資訊，包括內容、評分、標籤、版本等。

**語法**

```bash
promptforge show <ID>
promptforge view <ID>
```

**參數說明**

| 參數 | 必填 | 說明 |
|------|------|------|
| `id` | 是 | Prompt ID（支援短 ID，即 ID 的前幾位） |

**使用範例**

```bash
# 使用完整 ID 查看
promptforge show a1b2c3d4-e5f6-7890-abcd-ef1234567890

# 使用短 ID 查看（只要能唯一識別即可）
promptforge show a1b2c3d4

# 使用別名
promptforge view a1b2c3d4
```

---

### edit - 編輯 Prompt

編輯已有 Prompt 的任意欄位。每次編輯會自動建立版本快照。

**語法**

```bash
promptforge edit <ID> [--title <新標題>] [--content <新內容>] [--category <新分類>] [--tags <新標籤>] [--note <變更說明>] [--no-score]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--title` | `-t` | 否 | - | 新標題 |
| `--content` | `-c` | 否 | - | 新內容 |
| `--category` | `-cat` | 否 | - | 新分類 |
| `--tags` | - | 否 | - | 新標籤（逗號分隔） |
| `--note` | `-n` | 否 | `CLI edit` | 變更說明 |
| `--no-score` | - | 否 | `false` | 跳過自動評分 |

**使用範例**

```bash
# 更新 Prompt 內容
promptforge edit a1b2c3d4 \
  --content "更新後的 Prompt 內容..." \
  --note "增加了輸出格式要求和約束條件"

# 更新標題和標籤
promptforge edit a1b2c3d4 \
  --title "進階程式碼審查助手" \
  --tags "程式碼審查,Python,安全,效能"

# 更新分類
promptforge edit a1b2c3d4 --category devops

# 僅更新內容，跳過重新評分
promptforge edit a1b2c3d4 --content "新內容..." --no-score
```

**輸出範例**

```
Prompt updated successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Version: 2
  Score: 82.3/100
```

---

### delete - 刪除 Prompt

從資料庫中刪除指定的 Prompt。預設會要求確認，可透過 `--yes` 跳過。

**語法**

```bash
promptforge delete <ID> [--yes]
promptforge rm <ID> [--yes]
promptforge del <ID> [--yes]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--yes` | `-y` | 否 | `false` | 跳過確認提示 |

**使用範例**

```bash
# 刪除 Prompt（會彈出確認提示）
promptforge delete a1b2c3d4

# 直接刪除，不詢問
promptforge delete a1b2c3d4 --yes

# 使用短命令別名
promptforge rm a1b2c3d4 -y
promptforge del a1b2c3d4 -y
```

---

### score - 評分 Prompt

對指定 Prompt 進行 5 維度品質評分，輸出詳細的評分報告和優化建議。

**語法**

```bash
promptforge score <ID>
```

**參數說明**

| 參數 | 必填 | 說明 |
|------|------|------|
| `id` | 是 | Prompt ID |

**使用範例**

```bash
# 對 Prompt 進行評分
promptforge score a1b2c3d4
```

**輸出範例**

```
Prompt Score Report
====================
Title: Python 程式碼審查助手
ID: a1b2c3d4

Dimension Scores:
  Length Score:        12.0/15  (良好)
  Structure Score:     20.0/25  (優秀)
  Keyword Score:       16.0/20  (良好)
  Clarity Score:       17.0/20  (良好)
  Completeness Score:  15.0/20  (良好)

Total Score: 80.0/100

Suggestions:
  - 建議新增約束條件，幫助AI更準確地理解需求
  - 建議新增範例，提高輸出的可預測性
```

---

### export - 匯出 Prompt

將單個 Prompt 匯出為指定格式的檔案或輸出到終端。

**語法**

```bash
promptforge export <ID> --format <格式> [--output <檔案路徑>] [--with-versions]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `id` | 是 | - | Prompt ID |
| `--format` | `-f` | 否 | `json` | 匯出格式（`json`/`yaml`/`md`/`txt`） |
| `--output` | `-o` | 否 | 終端輸出 | 輸出檔案路徑 |
| `--with-versions` | - | 否 | `false` | 包含版本歷史 |

**使用範例**

```bash
# 匯出為 JSON 格式（輸出到終端）
promptforge export a1b2c3d4 --format json

# 匯出為 Markdown 檔案
promptforge export a1b2c3d4 --format md --output my_prompt.md

# 匯出為 YAML，包含版本歷史
promptforge export a1b2c3d4 --format yaml --with-versions

# 匯出為純文字
promptforge export a1b2c3d4 -f txt -o prompt.txt

# 自動從副檔名推斷格式
promptforge export a1b2c3d4 -o my_prompt.json
```

---

### export-all - 批次匯出

將所有（或按條件篩選的）Prompt 批次匯出到指定目錄。

**語法**

```bash
promptforge export-all [--format <格式>] [--dir <目錄>] [--category <分類>] [--tag <標籤>]
```

**參數說明**

| 參數 | 縮寫 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--format` | `-f` | 否 | `md` | 匯出格式（`json`/`yaml`/`md`/`txt`） |
| `--dir` | `-d` | 否 | `./exports` | 匯出目錄 |
| `--category` | `-cat` | 否 | 全部 | 按分類過濾 |
| `--tag` | `-t` | 否 | 全部 | 按標籤過濾 |

**使用範例**

```bash
# 批次匯出所有 Prompt 為 Markdown
promptforge export-all --format md --dir ./my_prompt_library

# 僅匯出 coding 分類的 Prompt
promptforge export-all --category coding --dir ./coding_prompts

# 匯出帶有"翻譯"標籤的 Prompt 為 JSON
promptforge export-all --tag 翻譯 --format json --dir ./translation_prompts

# 匯出到自訂目錄
promptforge export-all -f yaml -d /home/user/backups/prompts
```

---

### tags - 標籤管理

列出資料庫中所有已使用的標籤及其關聯的 Prompt 數量。

**語法**

```bash
promptforge tags
```

**使用範例**

```bash
# 查看所有標籤
promptforge tags
```

**輸出範例**

```
Tags (8):
  程式碼審查              (5 prompts)
  Python                (8 prompts)
  翻譯                  (3 prompts)
  寫作                  (4 prompts)
  資料分析              (2 prompts)
  最佳實踐              (6 prompts)
  安全                  (2 prompts)
  效能最佳化            (3 prompts)
```

---

### stats - 統計資訊

顯示 Prompt 庫的綜合統計資訊，包括總數、分類分佈、平均評分等。

**語法**

```bash
promptforge stats [--json]
```

**參數說明**

| 參數 | 必填 | 預設值 | 說明 |
|------|------|--------|------|
| `--json` | 否 | `false` | 以 JSON 格式輸出 |

**使用範例**

```bash
# 查看統計資訊（格式化輸出）
promptforge stats

# 以 JSON 格式輸出（方便腳本處理）
promptforge stats --json
```

**輸出範例**

```
PromptForge Statistics
======================
Total Prompts:        42
Total Categories:     6
Total Tags:           18
Average Score:        72.5/100
Top Category:         coding (15 prompts)
Top Tag:              Python (12 prompts)
Latest Prompt:        API 設計指南 (2 hours ago)
```

---

### tui - 互動式儀表板

啟動基於文字選單的互動式終端介面，透過鍵盤操作管理 Prompt。

**語法**

```bash
promptforge tui
```

**使用範例**

```bash
# 啟動 TUI
promptforge tui
```

TUI 介面提供以下功能選單：
- 瀏覽和搜尋 Prompt
- 新增和編輯 Prompt
- 評分和匯出 Prompt
- 查看統計資訊
- 標籤管理

> 按 `Ctrl+C` 或選擇退出選項即可離開 TUI。

---

### version - 版本資訊

顯示 PromptForge 的版本號。

**語法**

```bash
promptforge version
promptforge -v
```

**使用範例**

```bash
promptforge version
# 輸出: PromptForge v1.0.0
```

---

## 設計思路與迭代規劃

### 設計哲學

PromptForge 的核心設計遵循以下原則：

1. **零依賴原則** —— 僅使用 Python 標準庫，無需安裝任何第三方套件。這意味著你可以在任何安裝了 Python 3.9+ 的環境中直接使用，不受網路環境限制。

2. **資料自主可控** —— 使用 SQLite 本機儲存，所有資料保存在你的機器上。不依賴任何雲端服務，不收集任何使用者資料，確保隱私安全。

3. **漸進式複雜度** —— 簡單操作用單條命令完成，複雜操作透過 TUI 互動式介面實作。新手可以快速上手，老手可以高效操作。

4. **中英文原生支援** —— 評分引擎、搜尋引擎、停用詞庫均原生支援中英文，無需額外設定。

### 架構設計

```
promptforge/
  cli.py        # CLI 命令列入口（argparse）
  engine.py     # 核心業務邏輯引擎
  database.py   # SQLite 資料庫管理
  scorer.py     # 5 維度品質評分引擎
  searcher.py   # TF-IDF 語義搜尋引擎
  exporter.py   # 多格式匯出器
  models.py     # 資料模型定義
  tui.py        # TUI 互動式儀表板
  utils.py      # 工具函式集
```

### 迭代規劃

**v1.0（目前版本）**
- [x] Prompt CRUD 管理
- [x] 5 維度品質評分
- [x] TF-IDF 語義搜尋
- [x] 版本追蹤
- [x] 多格式匯出
- [x] TUI 互動式儀表板
- [x] 使用統計
- [x] 66 個單元測試

**v1.1（規劃中）**
- [ ] Prompt 模板市集（社群共享）
- [ ] 匯入功能（從 JSON/YAML/Markdown 匯入）
- [ ] Prompt 變數模板（支援 `{{variable}}` 佔位符）
- [ ] 設定檔支援（自訂評分權重）

**v2.0（遠期規劃）**
- [ ] Web UI 介面
- [ ] API 伺服器模式
- [ ] Prompt A/B 測試
- [ ] 外掛系統

---

## 打包與部署指南

### 建構 distribution 套件

```bash
# 安裝建構工具
pip install build

# 建構 sdist 和 wheel
python -m build

# 建構產物位於 dist/ 目錄
ls dist/
# promptforge-1.0.0.tar.gz
# promptforge-1.0.0-py3-none-any.whl
```

### 發佈到 PyPI

```bash
# 安裝 Twine
pip install twine

# 檢查套件
twine check dist/*

# 上傳到 PyPI（測試環境）
twine upload --repository testpypi dist/*

# 上傳到 PyPI（正式環境）
twine upload dist/*
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["promptforge"]
CMD ["tui"]
```

```bash
# 建構映像檔
docker build -t promptforge:1.0.0 .

# 執行
docker run -it -v ~/.promptforge:/root/.promptforge promptforge:1.0.0 tui
```

### 資料備份

PromptForge 使用 SQLite 儲存資料，資料庫檔案預設位於使用者目錄下。你可以直接複製資料庫檔案進行備份：

```bash
# 備份資料庫
cp ~/.promptforge/promptforge.db ~/backup/promptforge_$(date +%Y%m%d).db
```

---

## 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論你是提交 Bug 回報、改進文件，還是貢獻程式碼，都是對專案的巨大支援。

### 如何貢獻

1. **Fork** 本儲存庫
2. 建立你的特性分支：`git checkout -b feature/amazing-feature`
3. 提交你的改動：`git commit -m 'Add some amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 提交 **Pull Request**

### 開發環境建置

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/ -v

# 執行測試並產生覆蓋率報告
pytest tests/ --cov=promptforge --cov-report=html
```

### 程式碼規範

- 遵循 PEP 8 編碼規範
- 所有公共函式和方法必須包含文件字串
- 新功能必須附帶對應的單元測試
- 提交資訊使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式

### 提交 Issue

如果你發現了 Bug 或有功能建議，請在 [GitHub Issues](https://github.com/gitstq/PromptForge-Pro/issues) 中提交。提交 Issue 時請盡量包含以下資訊：

- 問題描述
- 重現步驟
- 期望行為
- 實際行為
- 執行環境（Python 版本、作業系統等）

---

## 開源協議

本專案基於 **MIT License** 開源。

```
MIT License

Copyright (c) 2024 PromptForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <a href="#简体中文">简体中文</a> | <b>繁體中文</b> | <a href="#english">English</a>
</p>

---
---

<h1 align="center" id="english">PromptForge Pro</h1>

<p align="center">
  <b>Lightweight Terminal AI Prompt Manager & Optimization Engine</b><br>
  <i>Manage, score, search, and optimize your AI Prompts efficiently from the terminal</i>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PromptForge-Pro">GitHub Repository</a> &bull;
  <a href="https://pypi.org/project/promptforge/">PyPI Page</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#detailed-usage-guide">Documentation</a>
</p>

---

## Table of Contents

- [Introduction](#introduction)
- [Core Features](#core-features)
- [Quick Start](#quick-start)
- [Detailed Usage Guide](#detailed-usage-guide)
  - [add - Add a Prompt](#add---add-a-prompt)
  - [list - List Prompts](#list---list-prompts)
  - [search - Search Prompts](#search---search-prompts)
  - [show - View Prompt Details](#show---view-prompt-details)
  - [edit - Edit a Prompt](#edit---edit-a-prompt)
  - [delete - Delete a Prompt](#delete---delete-a-prompt)
  - [score - Score a Prompt](#score---score-a-prompt)
  - [export - Export a Prompt](#export---export-a-prompt)
  - [export-all - Batch Export](#export-all---batch-export)
  - [tags - Tag Management](#tags---tag-management)
  - [stats - Statistics](#stats---statistics)
  - [tui - Interactive Dashboard](#tui---interactive-dashboard)
  - [version - Version Info](#version---version-info)
- [Design Philosophy & Roadmap](#design-philosophy--roadmap)
- [Packaging & Deployment Guide](#packaging--deployment-guide)
- [Contributing Guide](#contributing-guide)
- [License](#license)

---

## Introduction

**PromptForge Pro** is a lightweight terminal-based AI Prompt management and optimization engine built for the AI era. Whether you are an AI researcher, prompt engineer, or a power user of ChatGPT / Claude / Gemini, PromptForge helps you organize, evaluate, and iterate on your Prompt library right from the command line.

As we interact with large language models daily, we inevitably accumulate a growing collection of Prompts -- writing assistants, code generators, translation tools, data analyzers, and more. But as the collection grows, three universal pain points emerge: **can't find them, can't organize them, can't evaluate them**. PromptForge was built to solve exactly these problems:

- **Can't find?** Built-in TF-IDF semantic search engine with native Chinese-English mixed-language support, locating target Prompts in milliseconds
- **Can't organize?** Categories + tags + version tracking to build your personal Prompt knowledge base
- **Can't evaluate?** 5-dimension intelligent scoring system that comprehensively assesses Prompt quality across length, structure, keywords, clarity, and completeness

> **Core philosophy: zero dependencies, pure terminal, lightning fast.** PromptForge relies solely on the Python standard library -- no third-party packages required. SQLite local storage ensures data security and privacy. Install and go.

---

## Core Features

### Prompt Template Management

Full CRUD operations with a **category + tag** dual-dimension organization system. Every Prompt automatically gets a unique ID with version tracking, so you always know what changed and when.

```bash
# Add a Prompt with category and tags
promptforge add --title "Python Code Review Assistant" \
  --content "You are a senior Python developer. Please review the following code..." \
  --tags "code-review,Python,best-practices" \
  --category coding
```

### 5-Dimension Intelligent Scoring

An original Prompt quality assessment framework with a maximum score of 100, quantitatively analyzing five key dimensions:

| Dimension | Max Score | What It Evaluates |
|-----------|-----------|-------------------|
| **Length Score** | 15 | Whether the Prompt length falls within the optimal range (100-2000 characters) |
| **Structure Score** | 25 | Presence of role setting, task description, output format, and other structural elements |
| **Keyword Score** | 20 | Use of clear action verbs and specific instructions |
| **Clarity Score** | 20 | Sentence length, redundancy, and expression clarity |
| **Completeness Score** | 20 | Constraints, examples, edge cases, and other completeness factors |

```bash
# Score a specific Prompt and get detailed analysis with optimization suggestions
promptforge score <id>
```

### TF-IDF Semantic Search

A keyword search engine built on the **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm with native Chinese-English mixed tokenization and fuzzy matching:

- Automatic English word extraction and normalization
- Chinese character single-character + bigram indexing
- Built-in bilingual (Chinese/English) stop word filtering
- Cosine similarity ranking + fuzzy match bonus
- Search result highlight snippets

```bash
# Search for Prompts containing "translation" or "translate"
promptforge search "translation assistant"
```

### Version Tracking & Diff Comparison

Every edit to a Prompt automatically creates a version snapshot with a change note. You can trace back through history and compare differences between versions at any time.

```bash
# Edit a Prompt -- version is automatically recorded
promptforge edit <id> --content "Updated content..." --note "Improved output format requirements"
```

### Multi-Format Export

Export Prompts in **JSON, YAML, Markdown, or plain text** formats to suit different use cases. Supports both single and batch export.

```bash
# Export as Markdown
promptforge export <id> --format md

# Batch export all Prompts as JSON
promptforge export-all --format json --dir ./my_prompts
```

### TUI Interactive Dashboard

A text menu-driven interactive terminal interface with no `curses` dependency. Manage all your Prompts through keyboard navigation -- perfect for an immersive workflow.

```bash
# Launch the interactive dashboard
promptforge tui
```

### Usage Statistics & Analytics

Real-time statistics about your Prompt library, including total count, category distribution, average score, tag popularity, and more. Helps you continuously improve your Prompt quality.

```bash
# View statistics
promptforge stats

# Output as JSON for programmatic processing
promptforge stats --json
```

### Comprehensive Test Coverage

**66 unit tests** covering core engine, scoring system, search engine, and other critical modules, ensuring code quality and functional stability.

```bash
# Run tests
pytest tests/ -v
```

---

## Quick Start

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | >= 3.9 (3.10+ recommended) |
| **Operating System** | Windows / macOS / Linux |
| **External Dependencies** | None (zero-dependency design) |
| **Disk Space** | < 5 MB |

### Installation

**Option 1: Install from PyPI (Recommended)**

```bash
pip install promptforge
```

**Option 2: Install from Source (Development Mode)**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
pip install -e .
```

**Option 3: Run Directly (No Installation)**

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro
python -m promptforge version
```

### Verify Installation

```bash
promptforge version
# Output: PromptForge v1.0.0
```

### Three-Minute Getting Started

```bash
# 1. Add your first Prompt
promptforge add \
  --title "Code Review Assistant" \
  --content "You are a senior software engineer specializing in code review. Please review the code from the following dimensions: 1. Code quality and readability 2. Potential bugs and security risks 3. Performance optimization suggestions 4. Best practices compliance. Please respond in English with specific improvement suggestions and code examples." \
  --tags "code-review,engineering,quality" \
  --category coding

# 2. Check the auto-generated score
promptforge score <returned-id>

# 3. List all Prompts
promptforge list --sort score --limit 10

# 4. Search for Prompts
promptforge search "code review"

# 5. Export as Markdown
promptforge export <ID> --format md --output review_assistant.md

# 6. View statistics
promptforge stats
```

---

## Detailed Usage Guide

### add - Add a Prompt

Add a new Prompt to the local database. Quality scoring is performed automatically (can be skipped with `--no-score`).

**Syntax**

```bash
promptforge add --title <title> --content <content> [--category <category>] [--tags <tags>] [--no-score]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--title` | `-t` | Yes | - | Prompt title |
| `--content` | `-c` | Yes | - | Prompt content |
| `--category` | `-cat` | No | `general` | Category name |
| `--tags` | - | No | empty | Tags (comma-separated) |
| `--no-score` | - | No | `false` | Skip auto scoring |

**Examples**

```bash
# Add a writing assistant Prompt
promptforge add \
  --title "Technical Blog Writer" \
  --content "You are an experienced tech blogger. Based on the topic I provide, write a well-structured, in-depth technical blog post. Requirements: 1. Include an engaging introduction 2. Use code examples to illustrate key concepts 3. Summarize core takeaways 4. Keep word count between 1500-2000 words" \
  --tags "writing,blog,content-creation" \
  --category writing

# Add a translation Prompt, skip auto scoring
promptforge add \
  --title "Chinese-English Translation Expert" \
  --content "You are a professional translator fluent in both Chinese and English. Please translate the following content into natural, idiomatic English while preserving the original tone and style." \
  --tags "translation,bilingual" \
  --category translation \
  --no-score

# Add a data analysis Prompt using short flags
promptforge add \
  -t "Data Analysis Report Generator" \
  -c "As a data analyst, please generate a professional analysis report based on the raw data provided. The report should include: data overview, trend analysis, anomaly detection, visualization recommendations, and action items. Please output in Markdown format." \
  --tags "data-analysis,report,visualization" \
  --category analysis
```

**Output Example**

```
Prompt added successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: Technical Blog Writer
  Score: 78.5/100
```

---

### list - List Prompts

List all Prompts in the database with support for category/tag filtering and multi-field sorting.

**Syntax**

```bash
promptforge list [--category <category>] [--tag <tag>] [--sort <field>] [--order <direction>] [--limit <count>] [--offset <offset>]
promptforge ls [same parameters as above]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--category` | `-cat` | No | All | Filter by category |
| `--tag` | `-t` | No | All | Filter by tag |
| `--sort` | `-s` | No | `updated_at` | Sort field (`updated_at`/`score`/`title`/`created_at`/`usage_count`) |
| `--order` | `-o` | No | `desc` | Sort direction (`asc`/`desc`) |
| `--limit` | `-l` | No | `20` | Number of results to show |
| `--offset` | - | No | `0` | Offset for pagination |

**Examples**

```bash
# List all Prompts sorted by score (highest first)
promptforge list --sort score --order desc

# List Prompts in the coding category
promptforge list --category coding

# List Prompts with the "translation" tag, show top 5
promptforge list --tag translation --limit 5

# Sort by creation time (ascending), skip first 10 (pagination)
promptforge list --sort created_at --order asc --offset 10 --limit 10

# View most frequently used Prompts
promptforge list --sort usage_count --limit 10

# Using short command alias
promptforge ls -cat writing -s score -l 5
```

---

### search - Search Prompts

Search for Prompts using the TF-IDF semantic search engine. Supports Chinese-English mixed queries and fuzzy matching.

**Syntax**

```bash
promptforge search <query> [--limit <count>] [--no-fuzzy]
promptforge find <query> [same parameters as above]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `query` | - | Yes | - | Search keywords |
| `--limit` | `-l` | No | `10` | Maximum number of results |
| `--no-fuzzy` | - | No | `false` | Disable fuzzy matching |

**Examples**

```bash
# Search for Prompts about code generation
promptforge search "code generation"

# Search with English keywords
promptforge search "code review best practices"

# Mixed Chinese-English search
promptforge search "Python data analysis"

# Limit result count
promptforge search "translation" --limit 5

# Disable fuzzy matching for exact matches only
promptforge search "API design" --no-fuzzy

# Using short command alias
promptforge find "machine learning"
```

**Output Example**

```
Search results for 'code generation' (3):

  1. Python Code Generator (Score: 85, Match: 0.92)
     ID: a1b2c3d4
     > You are a senior Python developer. Please generate high-quality code based on the requirements...

  2. SQL Query Optimizer (Score: 72, Match: 0.78)
     ID: e5f6g7h8
     > Please optimize the following SQL query to improve execution efficiency...

  3. Code Review Checklist (Score: 68, Match: 0.65)
     ID: i9j0k1l2
     > Please review the code according to the following checklist...
```

---

### show - View Prompt Details

Display complete information about a specific Prompt, including content, score, tags, version, and more.

**Syntax**

```bash
promptforge show <ID>
promptforge view <ID>
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Prompt ID (short ID supported -- first few characters are enough if unique) |

**Examples**

```bash
# View using full ID
promptforge show a1b2c3d4-e5f6-7890-abcd-ef1234567890

# View using short ID (as long as it's unique)
promptforge show a1b2c3d4

# Using alias
promptforge view a1b2c3d4
```

---

### edit - Edit a Prompt

Edit any field of an existing Prompt. Each edit automatically creates a version snapshot.

**Syntax**

```bash
promptforge edit <ID> [--title <new-title>] [--content <new-content>] [--category <new-category>] [--tags <new-tags>] [--note <change-note>] [--no-score]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `id` | - | Yes | - | Prompt ID |
| `--title` | `-t` | No | - | New title |
| `--content` | `-c` | No | - | New content |
| `--category` | `-cat` | No | - | New category |
| `--tags` | - | No | - | New tags (comma-separated) |
| `--note` | `-n` | No | `CLI edit` | Change note |
| `--no-score` | - | No | `false` | Skip auto re-scoring |

**Examples**

```bash
# Update Prompt content
promptforge edit a1b2c3d4 \
  --content "Updated Prompt content..." \
  --note "Added output format requirements and constraints"

# Update title and tags
promptforge edit a1b2c3d4 \
  --title "Advanced Code Review Assistant" \
  --tags "code-review,Python,security,performance"

# Update category
promptforge edit a1b2c3d4 --category devops

# Update content only, skip re-scoring
promptforge edit a1b2c3d4 --content "New content..." --no-score
```

**Output Example**

```
Prompt updated successfully!
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Version: 2
  Score: 82.3/100
```

---

### delete - Delete a Prompt

Remove a specific Prompt from the database. Confirmation is required by default (can be skipped with `--yes`).

**Syntax**

```bash
promptforge delete <ID> [--yes]
promptforge rm <ID> [--yes]
promptforge del <ID> [--yes]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `id` | - | Yes | - | Prompt ID |
| `--yes` | `-y` | No | `false` | Skip confirmation prompt |

**Examples**

```bash
# Delete a Prompt (will show confirmation prompt)
promptforge delete a1b2c3d4

# Delete without confirmation
promptforge delete a1b2c3d4 --yes

# Using short command aliases
promptforge rm a1b2c3d4 -y
promptforge del a1b2c3d4 -y
```

---

### score - Score a Prompt

Perform a 5-dimension quality assessment on a specific Prompt, outputting a detailed score report with optimization suggestions.

**Syntax**

```bash
promptforge score <ID>
```

**Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `id` | Yes | Prompt ID |

**Examples**

```bash
# Score a Prompt
promptforge score a1b2c3d4
```

**Output Example**

```
Prompt Score Report
====================
Title: Python Code Review Assistant
ID: a1b2c3d4

Dimension Scores:
  Length Score:        12.0/15  (Good)
  Structure Score:     20.0/25  (Excellent)
  Keyword Score:       16.0/20  (Good)
  Clarity Score:       17.0/20  (Good)
  Completeness Score:  15.0/20  (Good)

Total Score: 80.0/100

Suggestions:
  - Consider adding constraints to help AI better understand requirements
  - Consider adding examples to improve output predictability
```

---

### export - Export a Prompt

Export a single Prompt to a specified format, either to a file or to the terminal.

**Syntax**

```bash
promptforge export <ID> --format <format> [--output <file-path>] [--with-versions]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `id` | - | Yes | - | Prompt ID |
| `--format` | `-f` | No | `json` | Export format (`json`/`yaml`/`md`/`txt`) |
| `--output` | `-o` | No | stdout | Output file path |
| `--with-versions` | - | No | `false` | Include version history |

**Examples**

```bash
# Export as JSON (to terminal)
promptforge export a1b2c3d4 --format json

# Export as Markdown file
promptforge export a1b2c3d4 --format md --output my_prompt.md

# Export as YAML with version history
promptforge export a1b2c3d4 --format yaml --with-versions

# Export as plain text
promptforge export a1b2c3d4 -f txt -o prompt.txt

# Auto-detect format from file extension
promptforge export a1b2c3d4 -o my_prompt.json
```

---

### export-all - Batch Export

Batch export all (or filtered) Prompts to a specified directory.

**Syntax**

```bash
promptforge export-all [--format <format>] [--dir <directory>] [--category <category>] [--tag <tag>]
```

**Parameters**

| Parameter | Short | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `--format` | `-f` | No | `md` | Export format (`json`/`yaml`/`md`/`txt`) |
| `--dir` | `-d` | No | `./exports` | Export directory |
| `--category` | `-cat` | No | All | Filter by category |
| `--tag` | `-t` | No | All | Filter by tag |

**Examples**

```bash
# Batch export all Prompts as Markdown
promptforge export-all --format md --dir ./my_prompt_library

# Export only Prompts in the coding category
promptforge export-all --category coding --dir ./coding_prompts

# Export Prompts tagged "translation" as JSON
promptforge export-all --tag translation --format json --dir ./translation_prompts

# Export to a custom directory
promptforge export-all -f yaml -d /home/user/backups/prompts
```

---

### tags - Tag Management

List all tags used in the database along with the number of associated Prompts.

**Syntax**

```bash
promptforge tags
```

**Examples**

```bash
# View all tags
promptforge tags
```

**Output Example**

```
Tags (8):
  code-review           (5 prompts)
  Python                (8 prompts)
  translation           (3 prompts)
  writing               (4 prompts)
  data-analysis         (2 prompts)
  best-practices        (6 prompts)
  security              (2 prompts)
  performance           (3 prompts)
```

---

### stats - Statistics

Display comprehensive statistics about your Prompt library, including total count, category distribution, average score, and more.

**Syntax**

```bash
promptforge stats [--json]
```

**Parameters**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--json` | No | `false` | Output in JSON format |

**Examples**

```bash
# View statistics (formatted output)
promptforge stats

# Output as JSON (for script processing)
promptforge stats --json
```

**Output Example**

```
PromptForge Statistics
======================
Total Prompts:        42
Total Categories:     6
Total Tags:           18
Average Score:        72.5/100
Top Category:         coding (15 prompts)
Top Tag:              Python (12 prompts)
Latest Prompt:        API Design Guide (2 hours ago)
```

---

### tui - Interactive Dashboard

Launch the text menu-driven interactive terminal interface for keyboard-based Prompt management.

**Syntax**

```bash
promptforge tui
```

**Examples**

```bash
# Launch the TUI
promptforge tui
```

The TUI provides the following menu options:
- Browse and search Prompts
- Add and edit Prompts
- Score and export Prompts
- View statistics
- Tag management

> Press `Ctrl+C` or select the exit option to leave the TUI.

---

### version - Version Info

Display the PromptForge version number.

**Syntax**

```bash
promptforge version
promptforge -v
```

**Examples**

```bash
promptforge version
# Output: PromptForge v1.0.0
```

---

## Design Philosophy & Roadmap

### Design Principles

PromptForge is built on the following core principles:

1. **Zero Dependencies** -- Only the Python standard library is used. No third-party packages needed. This means you can use it in any environment with Python 3.9+ installed, regardless of network conditions.

2. **Data Sovereignty** -- SQLite local storage keeps all your data on your own machine. No cloud services, no data collection, full privacy guaranteed.

3. **Progressive Complexity** -- Simple tasks are done with single commands; complex workflows are handled through the TUI interactive interface. Beginners can get started quickly; power users can work efficiently.

4. **Native Bilingual Support** -- The scoring engine, search engine, and stop word lists natively support both Chinese and English, with no additional configuration needed.

### Architecture

```
promptforge/
  cli.py        # CLI entry point (argparse)
  engine.py     # Core business logic engine
  database.py   # SQLite database management
  scorer.py     # 5-dimension quality scoring engine
  searcher.py   # TF-IDF semantic search engine
  exporter.py   # Multi-format exporter
  models.py     # Data model definitions
  tui.py        # TUI interactive dashboard
  utils.py      # Utility functions
```

### Roadmap

**v1.0 (Current Release)**
- [x] Prompt CRUD management
- [x] 5-dimension quality scoring
- [x] TF-IDF semantic search
- [x] Version tracking
- [x] Multi-format export
- [x] TUI interactive dashboard
- [x] Usage statistics
- [x] 66 unit tests

**v1.1 (Planned)**
- [ ] Prompt template marketplace (community sharing)
- [ ] Import functionality (from JSON/YAML/Markdown)
- [ ] Prompt variable templates (support `{{variable}}` placeholders)
- [ ] Configuration file support (custom scoring weights)

**v2.0 (Long-term Vision)**
- [ ] Web UI interface
- [ ] API server mode
- [ ] Prompt A/B testing
- [ ] Plugin system

---

## Packaging & Deployment Guide

### Building Distribution Packages

```bash
# Install build tools
pip install build

# Build sdist and wheel
python -m build

# Build artifacts are in the dist/ directory
ls dist/
# promptforge-1.0.0.tar.gz
# promptforge-1.0.0-py3-none-any.whl
```

### Publishing to PyPI

```bash
# Install Twine
pip install twine

# Check the package
twine check dist/*

# Upload to PyPI (test environment)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["promptforge"]
CMD ["tui"]
```

```bash
# Build the image
docker build -t promptforge:1.0.0 .

# Run the container
docker run -it -v ~/.promptforge:/root/.promptforge promptforge:1.0.0 tui
```

### Data Backup

PromptForge uses SQLite for data storage. The database file is located in your home directory by default. Simply copy the database file to back up your data:

```bash
# Backup the database
cp ~/.promptforge/promptforge.db ~/backup/promptforge_$(date +%Y%m%d).db
```

---

## Contributing Guide

We welcome and appreciate contributions of all forms! Whether you submit a bug report, improve documentation, or contribute code, every contribution makes a difference.

### How to Contribute

1. **Fork** this repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Submit a **Pull Request**

### Development Setup

```bash
git clone https://github.com/gitstq/PromptForge-Pro.git
cd PromptForge-Pro

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=promptforge --cov-report=html
```

### Code Standards

- Follow PEP 8 coding conventions
- All public functions and methods must include docstrings
- New features must include corresponding unit tests
- Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) format

### Submitting Issues

If you find a bug or have a feature suggestion, please open an issue on [GitHub Issues](https://github.com/gitstq/PromptForge-Pro/issues). When submitting an issue, please include:

- Problem description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Runtime environment (Python version, OS, etc.)

---

## License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2024 PromptForge Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <a href="#简体中文">简体中文</a> | <a href="#繁體中文">繁體中文</a> | <b>English</b>
</p>
