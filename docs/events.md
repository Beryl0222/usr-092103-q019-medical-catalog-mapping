# 事件载荷约定

所有事件共用信封字段：`event_id`、`event_type`、`aggregate_type`、`aggregate_id`、`occurred_at`、`version`、`summary`（见 `contracts/domain.schema.json`）。业务内容放在 `payload` 中；`version` 为事件所涉对象的版本号，对象引用写作 `<aggregate_id>@v<version>`。枚举取值含义见 `docs/glossary.md`。

## CATALOG_PUBLISHED → catalog_revision

目录版本发布（国家或地方）。

- `scope`：目录范围（`catalog_scope`）。
- `effective_from`：生效日期；生效区域用 `effective_regions` 列表。
- `supersedes`：被替代的前一版本引用。

样例：`data/samples/01-catalog-published.json`

## ITEM_DEFINED → service_item

服务项目版本定义。

- `catalog_ref`：所属目录版本引用。
- `item_code`、`name`：项目编码与名称。
- `definition`：项目定义；`unit`：计价单位；`service_boundary`：服务边界说明。
- `payment_conditions`：支付条件列表，提交前检查据此列出缺失条件。

样例：`data/samples/02-item-defined.json`

## CANDIDATE_GENERATED → mapping_candidate

自动候选生成，仅展示相似依据，未审核前不得进入结算。

- `local_item_ref`：地方项目引用；`national_item_refs`：候选国家项目引用列表。
- `evidence`：相似依据列表，每项含 `basis`（`similarity_basis`）、`score`、`detail`。

样例：`data/samples/05-candidate-generated.json`

## MAPPING_PROPOSED → mapping_claim

映射主张提出，可引用自动候选作为依据。

- `local_item_ref`：地方项目引用。
- `result_kind`：主张的映射结果类别（`mapping_result_kind`）。
- `components`：组成明细，每项含 `national_item_ref` 与 `share_note`（拆分时各部分的国家项目及分摊说明）。
- `candidate_refs`：所依据的自动候选；`status` 固定为 `proposed`。

样例：`data/samples/06-mapping-proposed.json`

## OPINION_RECORDED → expert_opinion

专家意见登记。

- `subject_ref`：所审对象及版本引用。
- `expert`、`conclusion`、`rationale`：专家、结论与理由。

样例：`data/samples/07-opinion-recorded.json`

## SPLIT_VALIDATED → split_validation

组合拆分重复计费边界校验完成。

- `claim_ref`：被校验的映射主张版本引用。
- `combo_category`：组合类别（护理、量表、麻醉等）。
- `result`：校验结果（`split_check_result`）；`boundary_notes`：边界说明。

样例：`data/samples/08-split-validated.json`

## MAPPING_REVIEWED → mapping_claim

映射主张审核完成，给出正式结果。

- `status`：审核结论（`approved` / `rejected`）。
- `result_kind`：正式映射结果类别；不可映射主张以 `unmappable` 结清。
- `opinion_refs`、`split_validation_refs`：所依据的专家意见与拆分校验。
- `reviewer`：审核方；驳回时以 `rationale` 记录理由。

样例：`data/samples/09-mapping-reviewed.json`、`data/samples/10-mapping-reviewed-unmappable.json`

## BATCH_RELEASED → release_batch

常规发布批次发布。

- `batch_kind`：固定为 `regular`。
- `released_refs`：本批次发布的目录或映射版本引用列表。

样例：`data/samples/11-batch-released.json`

## OBJECTION_RAISED → objection

省级人员提出异议，必须附证据。

- `subject_ref`：异议对象及版本引用。
- `raised_by`：提出方；`claim`：异议内容。
- `evidence_refs`：证据引用列表。

样例：`data/samples/12-objection-raised.json`

## OBJECTION_RESOLVED → objection

异议处理完成，记录采纳或驳回及理由。

- `resolution`：处理结果（`objection_resolution`）。
- `rationale`：采纳或驳回的理由；`resolved_by`：发布方。

样例：`data/samples/13-objection-resolved.json`

## CORRECTION_RELEASED → release_batch

更正批次发布，不改动已冻结快照。

- `batch_kind`：固定为 `correction`。
- `corrects_refs`：被更正的版本引用；`released_refs`：本次发布的新版本引用。
- `source_objection_refs`：触发更正的异议（如有）。

样例：`data/samples/14-correction-released.json`

## SNAPSHOT_FROZEN → settlement_snapshot

跨省结算请求冻结所用目录与映射版本。

- `request_id`：结算请求标识。
- `frozen_catalogs`：冻结的目录版本引用列表。
- `frozen_claims`：冻结的映射主张版本引用列表（仅 `approved` 版本可进入）。

样例：`data/samples/03-snapshot-frozen.json`、`data/samples/15-snapshot-frozen-after-correction.json`

## BILL_EXPLAINED → bill_explanation

账单解释生成，支撑提交前检查与审计追溯。

- `fee_line_ref`：费用行引用；`service_date`：服务发生日期（据以选择生效版本）。
- `snapshot_ref`：所用结算快照引用。
- `outcome`：解释结果（`explanation_outcome`）。
- `national_item_refs`、`local_item_ref`、`claim_ref`、`catalog_refs`：国家项目、地方编码、映射版本与当时目录版本。
- `review_refs`：审核过程事件引用。
- `missing_conditions`：当 `outcome` 为 `missing_conditions` 时列出缺失的支付条件。

样例：`data/samples/04-bill-explained.json`、`data/samples/16-bill-explained-missing-conditions.json`
