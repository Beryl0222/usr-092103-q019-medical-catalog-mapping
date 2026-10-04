# 医保项目目录映射

本仓库保存医保项目目录映射的领域词汇、交换事件与中文联调样例，供后续服务在统一身份和版本语义下协作。

## 资料结构

- `contracts/domain.schema.json`：领域事件的公共信封与稳定枚举。
- `docs/glossary.md`：核心对象、枚举取值与版本、结算语义规则。
- `docs/events.md`：各事件类型的载荷约定。
- `data/sample.json`：一条最小业务事件样例。
- `data/samples/`：按时间顺序排列的联调样例，覆盖全部已登记事件类型。
- `src/`：公共字段的基础校验代码。
- `tests/`：验证样例能够通过基础约定。

## 核心对象

catalog_revision（目录版本）、service_item（服务项目）、mapping_candidate（自动候选）、mapping_claim（映射主张）、expert_opinion（专家意见）、split_validation（拆分校验）、objection（异议）、release_batch（发布批次）、settlement_snapshot（结算快照）、bill_explanation（账单解释）。

## 已登记事件

CATALOG_PUBLISHED、ITEM_DEFINED、CANDIDATE_GENERATED、MAPPING_PROPOSED、OPINION_RECORDED、SPLIT_VALIDATED、MAPPING_REVIEWED、BATCH_RELEASED、OBJECTION_RAISED、OBJECTION_RESOLVED、CORRECTION_RELEASED、SNAPSHOT_FROZEN、BILL_EXPLAINED。

这些内容只规定跨模块交换的起点，不包含具体业务流程、存储或接口实现。当前阶段目标是让每一条具体账单都能被解释；完整的国家与各省目录映射服务在此语义上逐步演进。

## 本地检查

```bash
python3 -m unittest discover -s tests
```
