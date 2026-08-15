# 前咨询师风格镜像 Skill

> 不复制真人；把你有权使用的会谈资料，转成可核查、可撤回、可纠正的私人反思框架。

这是一个面向 Codex 的隐私优先模板。它能协助你复盘已结束的咨询或支持性关系、从逐字稿中归纳**可观察的回应方式**，并以明确披露的“风格镜像”陪你反思。它不是原咨询师，不会声称知道对方的现实想法、行踪、感受或边界，也不能代替心理治疗、诊断或紧急支持。

## 能做什么

| 能力 | 产出 | 默认位置 |
| --- | --- | --- |
| 会谈复盘 | 将事件、体验、猜测分开；提出一个可继续探索的问题 | 当前对话 |
| 风格提取 | 识别提问顺序、反映方式、节奏、边界与修复方式 | `private/evidence.json` |
| 材料登记 | 记录来源类型、校验值、权限说明；不复制原文件 | `private/sources.jsonl` |
| 图片／PDF 辅助 | 在 Codex 对话中附上你有权处理的文件，提取可见文字后再人工核查 | 当前对话 + 本地证据报告 |
| 纠正机制 | 将“这不像她/他”的反馈记成可审计的本地校准项 | `private/corrections.jsonl` |
| 本地版本轨迹 | 每次确认保存后，写入私有日志并创建本地 Git commit | `private/logs/` |

## 先读这三条边界

1. 只处理你创建、已获明确许可或依法有权处理的资料。不要抓取、保存或上传他人的私密账号、私聊、照片、健康信息、联系方式或凭据。
2. 抽取的是模式，不是身份：例如“会先反映感受，再问一个具体问题”，而不是“对方一定是怎样的人”。
3. 所有私人材料都放在 `private/` 或仓库外；它们永远不应推送到 GitHub。自动提交只适用于**没有 remote 的本地私有副本**。

更完整的证据边界见 [evidence-guidelines.md](references/evidence-guidelines.md)。

## 安装

```powershell
git clone https://github.com/Planarians/ex-therapist-skill.git former-therapist-mirror
Copy-Item -Recurse .\former-therapist-mirror C:\Users\<你的用户名>\.codex\skills\former-therapist-mirror
```

重新打开 Codex 对话后，直接以 `$former-therapist-mirror` 开头提出请求即可。公开模板不需要、也不应连接任何社交媒体或私人账号。

## 快速开始

### 1. 先用空白镜像对话

```text
$former-therapist-mirror 帮我复盘这段互动。不要急着建议；先把发生的事、我的感受、以及我对对方动机的猜测分开。
```

```text
$former-therapist-mirror 用温和、短句、一次只问一个问题的方式陪我想想。若你作出解释，请把它标为假设。
```

此阶段只使用通用反思框架，不会假装知道任何真人。

### 2. 登记你有权使用的本地材料

将原文件保存在本机的 `private/raw/`（或完全放在仓库外），然后仅登记元信息：

```powershell
python scripts/register_source.py --source private/raw/session-01.md --kind transcript --rights "我创建或获准用于私人复盘"
python scripts/register_source.py --source private/raw/notes.json --kind export --rights "我的个人导出"
```

登记不会复制原文件；它只写入来源名、文件类型、SHA-256 校验值、用途和权限声明。不要把 `private/` 加到版本控制或上传。

### 3. 建立候选证据报告

对文本、Markdown 或 JSON 导出运行：

```powershell
python scripts/build_evidence.py --source private/raw/session-01.md --output private/evidence.json
```

报告只给出段落数量、问题候选和待核查线索。它不是人格结论；请对照原始材料，确认说话者归属和转写准确性，再写出私人规则。

图片、扫描件和 PDF 的推荐做法是：在 Codex 对话中附上你有权处理的文件，请它先提取**可见文字**并标出不确定处；随后将人工核查过的文字保存为本地 `.md` 或 `.txt`，再运行证据报告。不要把截图中的私人信息提交到仓库。

### 4. 使用并校准回应方式

```text
$former-therapist-mirror 我有一段经过核查的会谈文字。请只提取可观察的回应模式：开场、澄清、反映、挑战、收束与边界。每条写明证据强度。
```

```text
$former-therapist-mirror 这不像对方：在困难内容出现时，她通常先确认我的体验，再讨论行为链条。把这条标成待验证的本地纠正，不要将它当成事实。
```

把纠正写入本地私有记录：

```powershell
python scripts/add_correction.py --text "先确认体验，再讨论行为链条" --confidence tentative --context "用户对一次回应的纠正"
```

只有当同一模式得到多份独立材料支持时，才把它升级为稳定的私人规则。

## 支持的材料来源

| 来源 | 可做什么 | 建议输入 | 说明 |
| --- | --- | --- | --- |
| 咨询逐字稿／访谈记录 | 分析回应顺序与提问风格 | `.md`、`.txt` | 优先使用有清晰说话者的版本 |
| 私人笔记 | 记录你自己的体验与纠正 | `.md`、`.txt` | 不把你的记忆写成对方意图的事实 |
| 用户导出的结构化资料 | 作为待核查线索 | `.json` | 先删除第三方身份与敏感字段 |
| 图片／聊天截图 | 提取可见文字、标注 OCR 不确定处 | `.png`、`.jpg`、`.webp` | 附到当前对话；不要推送原图 |
| PDF／扫描件 | 提取并人工复核文字 | `.pdf` | 附到当前对话；再保存核查后的文本 |
| 公开专业写作 | 理解已公开的方法或框架 | URL／文本 | 只限公开、专业相关的内容 |

不支持、也不应尝试：私密账号抓取、未授权聊天导出、凭据或令牌保存、对真人心理状态和现实行动的推断。

## 生成内容的结构

镜像中的私人工作笔记建议分为两层：

| 层 | 内容 | 例子 |
| --- | --- | --- |
| 共同情境 | 时间线、反复主题、已确认的互动偏好、未决问题 | “谈及关系紧张时，倾向先澄清事件顺序” |
| 回应模式 | 开场、反映、提问、假设、挑战、收束、边界 | “一次只问一个可回答的问题” |

每条规则都应带有来源日期（可泛化）、证据强度和不确定性说明。不要保留可识别的姓名、原句、地点、联系方式或第三方隐私。

运行逻辑是：

```text
用户当下的内容
  → 区分事件／体验／猜测
  → 选择经证据支持的回应模式
  → 反映 + 一个具体问题 + 可拒绝的选择
  → 用户纠正后写入私有校准记录
```

通用回应顺序见 [response-framework.md](references/response-framework.md)。

## 自动保存与版本管理

若希望把每次**确认要保留的**对话记录成 Git 提交，请为私有资料另建一个没有 remote 的本地仓库：

```powershell
mkdir $env:USERPROFILE\former-therapist-private
Set-Location $env:USERPROFILE\former-therapist-private
git init
Copy-Item -Recurse <本项目路径>\* .
git remote -v       # 应当没有输出
```

然后在该私有副本中执行：

```powershell
python scripts/record_dialogue.py --user-file user.txt --assistant-file assistant.txt
```

脚本会写到 `private/logs/YYYY-MM-DD.jsonl` 并创建一次本地 commit。若发现 Git remote，脚本会拒绝执行，避免把私人日志误推到 GitHub。要查看或回退本地版本：

```powershell
git log --oneline
git show <commit>
git revert <commit>
```

`git revert` 会新增一个撤销提交，保留审计轨迹；不要用它替代获得当事人同意或删除已外泄的材料。

## 项目结构

```text
former-therapist-mirror/
├── SKILL.md                         # Codex 入口与工作边界
├── references/
│   ├── evidence-guidelines.md       # 来源、证据与最小化原则
│   └── response-framework.md        # 通用反思回应框架
├── scripts/
│   ├── register_source.py           # 本地来源登记，不复制原文件
│   ├── build_evidence.py            # 文本候选证据报告
│   ├── add_correction.py            # 私有校准记录
│   └── record_dialogue.py           # 无 remote 时的本地对话提交
└── private/                         # Git 忽略；只属于你，不可上传
```

## 安全与求助

- 模型输出是反思辅助，不是临床判断或对原咨询师的真实再现。
- 不诊断、不处方，不根据零散材料给他人贴标签。
- 出现即时自伤、自杀、暴力或医疗风险时，暂停风格模拟，优先联系当地紧急服务、危机支持或身边可信任的人。

## 灵感

项目结构受 [perkfly/ex-skill](https://github.com/perkfly/ex-skill) 的“素材—蒸馏—校正”流程，以及 [ybq22/supervisor](https://github.com/ybq22/supervisor) 等 persona-skill 项目启发。本项目不包含、也不要求上传任何真人的私人训练材料。

## License

[MIT](LICENSE)
