# 公共资源与两种安装方式

本Skill与公共阅读资源分库维护。实际资源仓库、版本、40位commit及目录/manifest指纹在[resources.lock.json](../resources.lock.json)；[资源目录](../resources/catalog.json)按路径、书号与类型列出文件及SHA-256。外部资源必须固定快照，不能在每次研究时自动追随main。

## 完整安装

选择complete ZIP，解压后的invest-research目录包含resources/library完整公共快照。复制整个技能目录安装即可离线读取公共笔记、复算、记录和详细方法。已有个人IPS及报告不放进技能目录，也不随升级覆盖。完整不表示包含原书、维护者私人原件或已取得最新市场数据。

## 按需Git安装

普通ZIP包含核心技能、资源目录和锁定信息，不含整个公共库。Agent按当前问题先选catalog中的条目，用宿主HTTPS/Git能力读取固定commit下的文件，核对完整内容SHA-256后，只加载当前需要的部分。Git能力不是必需，普通公开HTTPS原始文件也可读取。不得把网页链接本身当成已经读到正文。

URL构成为`https://raw.githubusercontent.com/{repository}/{commit}/{path}`，中文和空格按URL编码，保留目录分隔符。repository与commit从锁文件取，path只取catalog登记项。没有联网能力时改用已取得的完整快照；两者均不可用则列出具体资源缺口，不能声称完成所需专题研究。

## 可选标准库工具

scripts/resources.py只读文件或固定公开HTTPS，不写缓存、不改配置、不安装软件、不调用模型或私有API。宿主有Python 3时可用；没有Python时按上述目录/HTTP和宿主能力完成同样读取。

```sh
python3 -B scripts/resources.py status
python3 -B scripts/resources.py verify
python3 -B scripts/resources.py read --path '阅读记录/逐章笔记/所需文件.md' --start-line 1 --end-line 30
```

命令示例以技能目录为工作目录；read的文件名须从目录选择真实条目。完整安装优先本地读取，普通安装按需联网；也可用`--library`指定另行克隆且核对过的资源快照。verify检查完整快照，read逐项核内容指纹，截取显示范围仍须据实登记。

## 阅读顺序与来源边界

研究先读核心方法，再按主题在catalog搜索书号、章节、复算或详细方法。历史IPS节号以独立文件/节号映射保留，相关个人政策叙述不公开；映射不是使用者政策。书籍历史案例数字与教学复算仍保留，并标明数字来源，不能解释为用户资产。原书、图像与临时解码全文未随库提供；不能从过去的读完记录推定自己本次已读原书，也不能把未核原披露转为已核事实。

## 用户工作区及报告引用

用户IPS、独立报告和自有书籍/资料放在技能目录外。按[工作区约定](../assets/project.md)登记基础版本、自有来源、实际读取范围和冲突。官方方法、公共阅读记录与个人政策分别记录；自有资料可以补充证据和提出反证，不静默覆盖官方文件或其他人的政策。

报告引用至少保存Skill版本及实际commit、资源仓库commit、所用文件路径/SHA-256与实际读取段落、个人IPS版本/哈希、用户补充资料来源。使用[运行记录](../assets/run.json)记录当次实际内容，未读取项不填成已读取。旧报告固定旧版本，资源库补书或Skill升级不回改旧判断。

## 显式升级

资源库由维护者补充，旧书号和旧commit保留。Skill维护者核对新资源后更新锁文件、提升Skill版本，重新发布两种包。使用者审阅差异后再安装新版本；不合并覆盖个人工作区。只读保护由宿主权限落实，提示词和哈希只用于约束行为和发现差异。
