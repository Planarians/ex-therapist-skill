# 前咨询师风格镜像 Skill

> 不是把一个真人复制进 AI，而是把你有权使用的会谈资料蒸馏成一套可核查、可纠正、带边界的反思框架。

这个模板用于创建**明确披露的风格镜像**：它可以帮助你复盘会谈、整理感受、学习一种提问节奏，或建立自己的反思伙伴；它不声称是原咨询师，不预测对方的现实想法或选择，也不替代心理治疗或危机支持。

## 适用场景

- 复盘过去的咨询、督导或支持性关系
- 从合法持有的逐字稿中提取可观察的回应模式
- 用“事实—体验—推测”分层整理关系中的情绪
- 接收“这不像她/他”的纠正并在本地持续校准

## 素材原则

| 素材 | 可以提取 | 不应提取/发布 |
| --- | --- | --- |
| 清晰归属的逐字稿 | 提问顺序、回应节奏、边界处理 | 原文、姓名、健康与关系细节 |
| 用户纠正 | 本地校准规则 | 对第三方的断言 |
| 公开专业写作 | 公开声明的框架 | 私人账号的身份或生活信息 |
| 噪声转写 / AI 总结 | 待核查候选 | 作为唯一事实依据 |

所有原始资料都应放在 `private/` 或仓库外；该目录默认被 Git 忽略。只使用你自己创建、明确获准处理或依法有权使用的资料。

## 安装

```powershell
git clone https://github.com/Planarians/ex-therapist-skill.git
Copy-Item -Recurse .\ex-therapist-skill C:\Users\<你>\.codex\skills\former-therapist-mirror
```

重启或新开一个 Codex 对话后即可调用。

## 使用

```text
$former-therapist-mirror 陪我复盘刚才的会谈。先不要给建议，帮我分开事实、感受和我对对方的猜测。
```

```text
$former-therapist-mirror 我有新的逐字稿。请从中提取可验证的提问和回应模式，保留不确定性。
```

```text
$former-therapist-mirror 这不像对方：她通常会先确认我的感受，再讨论行为链条。
```

## 项目结构

```text
.
├── SKILL.md
├── references/
│   ├── evidence-guidelines.md
│   └── response-framework.md
├── scripts/
│   ├── build_evidence.py
│   └── record_dialogue.py
└── private/                 # 自动忽略；永远不要推送
```

## 本地对话记录

可选脚本会把每一轮写入 `private/logs/` 并创建**本地** Git commit：

```powershell
python scripts/record_dialogue.py --user-file user.txt --assistant-file assistant.txt
```

请在不含 remote 的私有副本中使用它。脚本无法阻止你之后手动 `git push`；推送前请检查 `git status` 和 `git log`。

## 安全与边界

- 不收集、不发布、不推送私人聊天、咨询逐字稿、照片、账号凭据或可识别信息。
- 不把模型输出当作对原咨询师真实意图的证据。
- 出现即时自伤、自杀、暴力或医疗风险时，优先联系当地紧急服务、危机支持或身边可信任的人。

## 灵感

项目结构受 [perkfly/ex-skill](https://github.com/perkfly/ex-skill) 的“素材—蒸馏—校正”流程，以及 [ybq22/supervisor](https://github.com/ybq22/supervisor) 等 persona-skill 项目启发。本项目不包含、也不要求上传任何真人的私人训练材料。

## License

[MIT](LICENSE)
