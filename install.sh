#!/bin/bash
set -euo pipefail

# 🧠 Agent Memory Architecture — 一键安装
# 大脑+书架：给 AI Agent 一个真正的长期记忆系统

REPO="https://raw.githubusercontent.com/caoyiqing1987/agent-memory-architecture/main"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

echo "🧠 安装 Agent Memory Architecture..."
echo ""

# 1. 创建目录结构
mkdir -p "$HERMES_HOME/memories"
mkdir -p "$HOME/details/archive"

# 2. 下载模板（不覆盖已有文件）
echo "📄 下载记忆模板..."
for file in MEMORY.md USER.md; do
    target="$HERMES_HOME/memories/$file"
    if [ ! -f "$target" ]; then
        curl -fsSL "$REPO/templates/$file" -o "$target"
        echo "   ✓ $target"
    else
        echo "   - $target 已存在，跳过"
    fi
done

# 3. 下载归档脚本
echo "🔧 安装归档脚本..."
mkdir -p "$HERMES_HOME/scripts"
curl -fsSL "$REPO/scripts/archive-memory.py" -o "$HERMES_HOME/scripts/archive-memory.py"
chmod +x "$HERMES_HOME/scripts/archive-memory.py"
echo "   ✓ $HERMES_HOME/scripts/archive-memory.py"

# 4. 注册 cronjob（每周六凌晨4点）
echo "⏰ 注册归档 cronjob..."
if ! crontab -l 2>/dev/null | grep -q "archive-memory.py"; then
    (crontab -l 2>/dev/null; echo "0 4 * * 6 python3 $HERMES_HOME/scripts/archive-memory.py") | crontab -
    echo "   ✓ cronjob 已注册（周六 4:00）"
else
    echo "   - cronjob 已存在，跳过"
fi

# 5. 初始化 archive 索引
if [ ! -f "$HOME/details/archive/README.md" ]; then
    cat > "$HOME/details/archive/README.md" << 'INDEXEOF'
# 📚 记忆归档索引

自动归档的旧事件会全文保存在此目录，索引追加到本文件。
用 `grep` 搜索关键词即可找回：

    grep -r "关键词" ~/details/archive/

---
INDEXEOF
    echo "   ✓ 归档索引已初始化"
fi

# 6. 建议配置
echo ""
echo "⚙️  建议在 ~/.hermes/config.yaml 中添加："
echo ""
echo "  memory:"
echo "    memory_enabled: true"
echo "    user_profile_enabled: true"
echo "    memory_char_limit: 50000"
echo "    user_char_limit: 50000"
echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "  1. 编辑你的记忆：  vim $HERMES_HOME/memories/MEMORY.md"
echo "  2. 编辑你的偏好：  vim $HERMES_HOME/memories/USER.md"
echo "  3. 创建你的记录：  mkdir -p ~/details/projects && vim ~/details/projects/my-project.md"
echo "  4. 在 MEMORY.md 里加一行索引指向它"
echo "  5. 手动测试归档：  python3 $HERMES_HOME/scripts/archive-memory.py"
echo ""
echo "📖 完整文档：https://github.com/caoyiqing1987/agent-memory-architecture"
