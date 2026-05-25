# ===== System Rules =====
# 这段写你的 AI Agent 应该遵守的行为规则。
# 格式自由，用 § 分隔条目。

"记忆"=保存到 ~/details/ 层级文件。memory 只维护索引+系统规则。
输出规则：简洁直接，不要啰嗦。数据分析优先用表格。

# ===== Tool Rules =====
# 工具偏好、搜索方式、常用命令路径。

搜索: 优先用本地搜索工具，浏览器只用于交互操作。

# ===== Behavioral Rules =====
# 特定的行为约束、汇报格式、做事方式。

# ===== details/ Index =====
# 指向 ~/details/ 下完整记录的短索引行。
# 格式：主题 -> ~/details/目录/文件名.md
#
# 示例：
# projects.md — 在管项目+交期
# business.md — 业务/客户/公司

# ===== Archive =====
# 14 天前的自动归档到 ~/details/archive/
# 用 grep 找回：grep -r "关键词" ~/details/archive/
