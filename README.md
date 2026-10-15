# invest-research

用于港美股公司、股票与 ETF 研究、投资报告复核和方法解释的开放 Agent Skills 包。当前版本 **0.1.0**。

采用 `SKILL.md`、相对引用、普通 Markdown/JSON 与可选离线脚本，不依赖厂商私有 API、SDK、连接器或特定模型。研究资料由宿主 Agent 实际具备的读取与检索能力提供。本技能不执行交易。

## 安装

下载 [0.1.0 技能 ZIP](https://github.com/sunJack1991/invest-research/raw/c861c52487629a8a972e89402c153c83320c2f76/dist/invest-research-0.1.0.zip)，在支持本地技能导入的客户端中导入；若客户端要求目录，解压后选择含 `SKILL.md` 的完整 `invest-research` 目录。

也可以克隆仓库：

```sh
git clone https://github.com/sunJack1991/invest-research.git
```

实际技能位于 `skills/invest-research/`。请按客户端的技能发现规则复制整个目录，不要只复制 `SKILL.md`，也不要把整个仓库当作技能目录。

WorkBuddy 可按其[技能导入说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)导入本地包；支持项目技能目录的场景可将完整技能目录放入使用者项目的 `.codebuddy/skills/`。其他 Agent 按其公开的技能导入机制加载。已核对格式及公开文档，尚未进行 WorkBuddy 实际导入和模型行为测试。

## 使用

直接用自然语言提出请求，无需填写 JSON：

- “研究某公司（证券代码、上市市场），给我关键结论。”
- “复核这份报告，列出重大错误和证据缺口。”并提供可读取报告。
- “解释 DCF 和剩余收益模型分别适合什么情况。”
- “研究某只 ETF，附完整研究报告和证据附录。”

通用研究只需能唯一定位的标的；报告复核需可读原文；方法解释需具体问题。个人适配才需要使用者自己的 IPS、资金用途、期限、持仓和相关实施约束。缺个人资料仍可做通用研究，但不能推定个人可买额度或政策通过。

默认用简体中文在对话中显示核心判断、证据、估值或缺口、五门结论、反方风险和下一步。完整报告、估值附录、证据附录、决策记录及复核清单按需提供；默认不写文件。详见[输入输出约定](skills/invest-research/references/input-output.md)与[技能入口](skills/invest-research/SKILL.md)。

## 版本与资料保护

基础技能与个人工作区分开：个人 IPS、持仓、扩展书籍、数据和产出保存在使用者自己的目录。基础文件的只读权限由宿主或文件系统落实，提示词与哈希不提供写保护。

安装后记录版本与实际 commit；升级时显式切换固定版本或 commit，不在每次研究时自动追随最新分支。保留旧版及个人资料。可选完整性核对（只需 Python 3 标准库，不联网、不写文件）：

```sh
python3 -B skills/invest-research/scripts/check_integrity.py
```

ZIP 指纹见 [SHA256SUMS](dist/SHA256SUMS)。日常读取和研究不需要 Python。

本仓库仅提供可移植核心方法与空白模板，不包含原书全文、维护者个人 IPS、资产数据、原始阅读证据或历史备份。书目与材料限制见[来源说明](skills/invest-research/references/sources.md)。尚未指定开源许可证。

维护规则见 [Agents.md](Agents.md)、[PRD](invest-research_PRD_0.1.0.md)、[架构](Tech_Arch.md)与[变更日志](Change_Log.md)。
