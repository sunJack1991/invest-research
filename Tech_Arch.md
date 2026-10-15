# 技术架构

skills/invest-research为19文件按需技能。resources.lock.json锁定公共库commit及catalog/manifest指纹，resources/catalog.json路由495项资料；scripts/resources.py以标准库只读固定HTTPS或本地快照并核指纹。

完整ZIP增加resources/library的506文件快照，根manifest登记全部525文件。两种包使用相同核心方法、输入及输出接口；历史阅读、当前实际读取及原披露核验分开记录。

用户IPS、自有资料及报告留在工作区，project.json和run.json记录版本与来源。资源库可独立补书；Skill审阅后更新锁、升级版本和两种ZIP，旧报告不回改。无必需API/SDK或Python运行依赖，缺能力时显示缺口；客户端实测不由包校验推定。
