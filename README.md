# invest-research

开放Agent Skills投资研究技能，当前版本 **0.2.0**。研究港美股公司、股票与ETF，复核报告、解释方法。采用SKILL.md、相对引用、普通文本及可选标准库脚本，无厂商私有API、SDK、连接器或特定模型依赖，不执行交易。

## 两种安装

| 安装包 | 包含内容 | 获取方式 |
|---|---|---|
| [完整包](https://raw.githubusercontent.com/sunJack1991/invest-research/main/dist/invest-research-0.2.0-complete.zip) | 核心技能和完整公共快照，共525文件 | 可离线读取公共资料 |
| [按需包](https://raw.githubusercontent.com/sunJack1991/invest-research/main/dist/invest-research-0.2.0.zip) | 核心技能、目录和资源锁，共19文件 | 按需经宿主HTTPS/Git读取并核指纹 |

两种包锁定同一[公共资源库](https://github.com/sunJack1991/invest-resources)版本0.1.0，commit `8464b992128502bb88a1d6f393ee0e58381625c1`。公共库含250章笔记、112批次及复算、阅读进度、疑点核验、详细方法和纯历史节号映射，共506文件/495项资料。

下载解压后，导入含SKILL.md的完整invest-research目录，不要只复制入口。克隆本仓库后安装skills/invest-research目录，相当于按需模式；完整包比该目录多出resources/library。不要同时安装同名两份。

WorkBuddy按其[本地技能导入机制](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)加载；支持项目技能目录时可放入使用者项目的.codebuddy/skills。其他Agent按公开的技能发现规则加载。已做格式及包级验证，尚未完成实际客户端导入和模型行为实测。

完整包离线能力指公共资料读取；最新财报、行情等仍需用户提供或宿主实际取得。按需模式无网络且无本地快照时，列出具体缺口，不冒充已完成专题研究。

## 使用

自然语言即可，不要求手填JSON：

- “研究某公司（代码、市场），给我关键结论。”
- “复核这份报告，指出重大问题。”并提供可读原文。
- “解释DCF和剩余收益模型的适用条件。”
- “研究这只ETF，附完整报告及估值附录。”

通用研究只需唯一标的；复核需报告，解释需具体问题。个人适配才核使用者自己的IPS、用途、期限、资金、持仓及相关实施约束；缺个人资料仍可研究，不推定可买额度或政策通过。

默认简体中文、对话中展示必要结论、不写文件；完整报告、估值/证据附录、决策记录和复核清单按需提供。见[技能入口](skills/invest-research/SKILL.md)与[输入输出约定](skills/invest-research/references/input-output.md)。

## 个人IPS、独立报告与自有资料

在技能目录外建立[个人工作区](skills/invest-research/assets/project.md)，保存自己的IPS、书籍/笔记、数据、运行和报告。用[项目配置](skills/invest-research/assets/project.json)与[运行模板](skills/invest-research/assets/run.json)记录Skill版本/commit、资源commit、文件指纹及实际读取范围、个人政策版本和补充来源。

原书、解码全文、图像、维护者IPS/资产和独立报告不在公共库。历史政策只保留纯节号映射；书中案例数字不是用户资产或默认阈值。自有资料可增加证据与反证，不静默覆盖基础文件。只读保护由宿主权限落实。

## 核对与升级

[资源锁](skills/invest-research/resources.lock.json)固定真实commit及目录/manifest指纹，[目录](skills/invest-research/resources/catalog.json)提供按需路由。公共资源库可独立补书；旧安装、旧IPS及旧报告继续引用旧commit，不每次追随main。升级审阅差异后再切换，保留个人工作区。

可选Python 3标准库工具，以技能目录为工作目录：

```sh
python3 -B scripts/check_integrity.py
python3 -B scripts/resources.py status
python3 -B scripts/resources.py verify
```

verify检查完整快照；按需模式用read逐项核对，也可用--library指定单独克隆的相同快照。读取器只读，不写缓存、不安装软件、不调用模型。没有Python时用宿主读取/HTTPS及指纹能力；Python不是研究运行前提。详见[资源说明](skills/invest-research/references/resources.md)。包指纹见[SHA256SUMS](dist/SHA256SUMS)，0.1.0旧包保留，同版本不覆盖不同内容。

维护：[Agents](Agents.md)、[PRD](invest-research_PRD_0.2.0.md)、[架构](Tech_Arch.md)、[日志](Change_Log.md)。尚未指定开源许可证。
