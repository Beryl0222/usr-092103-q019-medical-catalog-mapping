"""校验领域事件公共字段。枚举取值与 contracts/domain.schema.json 保持一致。"""

from datetime import datetime

REQUIRED = ("event_id", "event_type", "aggregate_type", "aggregate_id", "occurred_at", "version", "summary")

EVENT_TYPES = (
    "CATALOG_PUBLISHED",
    "ITEM_DEFINED",
    "CANDIDATE_GENERATED",
    "MAPPING_PROPOSED",
    "OPINION_RECORDED",
    "SPLIT_VALIDATED",
    "MAPPING_REVIEWED",
    "BATCH_RELEASED",
    "OBJECTION_RAISED",
    "OBJECTION_RESOLVED",
    "CORRECTION_RELEASED",
    "SNAPSHOT_FROZEN",
    "BILL_EXPLAINED",
)

AGGREGATE_TYPES = (
    "catalog_revision",
    "service_item",
    "mapping_candidate",
    "mapping_claim",
    "expert_opinion",
    "split_validation",
    "objection",
    "release_batch",
    "settlement_snapshot",
    "bill_explanation",
)

NON_EMPTY = ("event_id", "aggregate_id", "summary")

def validate_event(record: dict) -> list[str]:
    errors = [f"缺少字段：{name}" for name in REQUIRED if name not in record]
    event_type = record.get("event_type")
    if event_type is not None and event_type not in EVENT_TYPES:
        errors.append(f"未登记的事件类型：{event_type}")
    aggregate_type = record.get("aggregate_type")
    if aggregate_type is not None and aggregate_type not in AGGREGATE_TYPES:
        errors.append(f"未登记的聚合类型：{aggregate_type}")
    for name in NON_EMPTY:
        value = record.get(name)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"{name} 必须是非空字符串")
    version = record.get("version")
    if version is not None and (isinstance(version, bool) or not isinstance(version, int) or version < 1):
        errors.append("version 必须是正整数")
    occurred_at = record.get("occurred_at")
    if occurred_at is not None:
        try:
            datetime.fromisoformat(occurred_at)
        except (TypeError, ValueError):
            errors.append("occurred_at 必须是 ISO 8601 日期时间")
    return errors
