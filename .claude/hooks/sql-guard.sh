#!/bin/bash
# Snowflake 크레딧 세이프가드 — PreToolUse hook
# Bash 도구 호출 시 위험한 SQL 패턴을 사전 차단한다.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# jq 파싱 실패 시 통과
[ -z "$COMMAND" ] && exit 0

# 위험 SQL 패턴 차단
if echo "$COMMAND" | grep -qiE '(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE\s+TABLE|DELETE\s+FROM.*WITHOUT|ALTER\s+WAREHOUSE.*SET\s+WAREHOUSE_SIZE\s*=\s*.(X?L|MEDIUM|LARGE))'; then
  echo "BLOCKED: 위험한 SQL 감지. DROP/TRUNCATE/대형 Warehouse 변경은 수동으로 실행하세요."
  echo "REMEDIATION: reviewer 에이전트로 먼저 검증하거나, Snowflake 웹에서 직접 실행."
  exit 2
fi

# Cortex AI 전체 실행 경고 (LIMIT 없이)
if echo "$COMMAND" | grep -qiE 'CORTEX\.(COMPLETE|CLASSIFY|SENTIMENT)' && ! echo "$COMMAND" | grep -qiE 'LIMIT\s+[0-9]'; then
  echo "WARNING: Cortex AI 호출에 LIMIT이 없습니다. 전체 실행 시 크레딧이 대량 소비됩니다."
  echo "REMEDIATION: LIMIT 10으로 먼저 테스트 후 전체 실행하세요."
  exit 2
fi

exit 0
