#!/bin/bash
# Setup cronjob for memory archiving
# Usage: bash setup-cron.sh [schedule]
# Default: every Saturday at 4:00 AM

set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SCRIPT="$HERMES_HOME/scripts/archive-memory.py"
SCHEDULE="${1:-"0 4 * * 6"}"

if [ ! -f "$SCRIPT" ]; then
    echo "❌ 找不到归档脚本：$SCRIPT"
    echo "   请先运行 install.sh"
    exit 1
fi

# Remove existing memory-archive cron if present
if crontab -l 2>/dev/null | grep -q "archive-memory.py"; then
    crontab -l 2>/dev/null | grep -v "archive-memory.py" | crontab -
fi

# Add new cron
(crontab -l 2>/dev/null; echo "$SCHEDULE python3 $SCRIPT") | crontab -

echo "✅ cronjob 已注册"
echo "   时间：$SCHEDULE"
echo "   脚本：$SCRIPT"
