# Speaker notes

## 1. Title

- Open with one sentence: relational models may achieve strong benchmark scores without learning the relational mechanism we actually care about.
- The talk asks how to make that mechanism more explicit and compact.

## 2. Problem definition

- The three gaps are related but distinct: shortcut dependence is an evaluation/robustness issue, coarse relations are a representation issue, and cell-level computation is an efficiency issue.
- Concretely, RT distinguishes FK direction but does not explicitly parameterize each linked table pair: `Results -> Drivers` and `Results -> Races` are both treated as foreign-to-primary links.
- RT also keeps individual cells as the reasoning units across its attention layers, whereas the proposed models encode cells once and perform subsequent propagation over compact row states.
- Avoid saying RT has no relational reasoning. The precise claim is that its architecture offers a much shorter non-relational route when self-labels are visible.

## 3. NSL validation protocol

- Standard and NSL mask the same seed target and evaluate the same checkpoint on the same test queries.
- Standard may expose sampled target-column values from other task rows sharing the query entity; NSL skips exactly those cells.
- NSL retains other row features, labels for other entities, and FK structure. A larger Standard-to-NSL drop indicates stronger dependence on this specific shortcut.
- Because removing a cell can admit a replacement under the fixed budget, describe NSL as a resampled-context stress test rather than a frozen causal intervention.

## Optional: Shortcut mechanism (currently hidden)

- In RT, cells from the same table and column can communicate directly under the column-attention mask.
- Therefore a masked target can directly read historical labels of the same entity in one sublayer; multi-hop FK reasoning is optional rather than impossible.
- Historical labels are legal context, not necessarily leakage. The concern is over-reliance.

## 4. Classification evidence

- These are paired Standard and NSL evaluations of the same reproduced RT checkpoint.
- Every value on this slide comes from the local evaluation files, not from RT's published results table; this is checkpoint evaluation, not a claim that RT was retrained.
- The slide reports all ten tasks; emphasize the macro drop and use the bold red entries to identify the four largest degradations.
- NSL means historical values of the target column for the target entity are removed from the sampled context.

## Optional: Regression evidence (currently hidden)

- This is an independent diagnostic with the same qualitative pattern.
- Seven of eight tasks decline and five obtain negative R-squared after self-label removal.
- Explicitly say that regression for the proposed model is not yet a finalized paper claim.

## 5. Design response

- The design does not discard cells. It uses them once to initialize row states.
- The main reasoning unit then becomes a database row.
- RelGraph adds a second graph whose nodes represent query-local table-pair relations. Its final relation states produce condition vectors that are added to the corresponding typed FK messages; they do not directly overwrite row states.

## 6. RowGraph-Base architecture

- Walk left to right: sample context, encode cells, pool rows, build the candidate-augmented row graph, propagate, score candidates.
- Base has no relation-condition vector and is the clean control for the row-level backbone.
- The architecture figure presents the finalized binary-classification formulation only: candidates `c0` and `c1` represent False and True.

## 7. RelGraph architecture

- The lower row graph is the same backbone as Base.
- The auxiliary graph is processed first; its relation representations condition all corresponding FK messages.
- The orange mapping uses `chi(e)` to select one relation state for every retained FK pair; the forward and reverse copies of that FK share the resulting condition.

## 8. Sampler

- The budget counts cells, not rows; the last retained row may be only partially serialized.
- Forward FK-to-parent expansion receives priority; reverse expansions are randomized at the shallowest frontier.
- The future filter is applied to reverse-FK database children for forecasting tasks; each reverse expansion retains at most 256 database children.

## 9. Sampling example I: eligible relational neighborhood

- This binary example uses the F1 Driver DNF task: the seed target is masked and `driverId = 10` is the FK anchor.
- The table lists rows made eligible by traversal, not a claim that all reachable rows fit into the final sample.
- The paper and current experiments use one consistent budget, `S_max = 2048` serialized cells.

## 10. Sampling example II: traversal and serialization

- First follow `driverId` forward from the task row to its primary row in `Drivers`; then reverse-look up the `Results`, `Qualifying`, and `Standings` rows that reference this driver.
- From those rows, forward FK links reach `Races` and `Constructors`; `Races` reaches `Circuits`, while reverse constructor links reach `Constructor Results` and `Constructor Standings`.
- The right-hand table is schematic and shows the actual serialization rule: append non-key, non-null value cells row by row.
- PK values are omitted and FK values become graph edges. If the budget is exhausted, only a prefix of the final retained row enters `S_g`.
- Distinguish `S_g`, which may contain the masked target position, from `C_g^in`, the unmasked cells supplied to encoding and pooling.

## 11. Cell encoding and pooling

- Numeric, text, datetime, and Boolean values use different value encoders. A shared affine-plus-RMSNorm encoder processes the precomputed column-name feature.
- PK/FK values are structural and do not enter the cell encoder. Column-name encoding distinguishes non-key fields whose values look similar but whose semantics differ.
- Mean pooling captures overall row content; max pooling preserves salient features.
- The target value is removed before this stage, so it cannot enter through either cell encoding or pooling.

## 12. Candidate-augmented row graph

- Each sampled row becomes one node and each FK becomes two directed copies with distinct types.
- Historical visible labels connect only from rows into the matching candidate.
- There are no candidate-to-row edges, preventing candidate feedback into the context.

## 13. Base forward

- Messages are typed by direction and label status, then mean-aggregated with a residual self update.
- Base sets the relation condition to zero in every FK message.
- This makes Base versus RelGraph a controlled architectural ablation.

## 14. RelGraph forward

- A relation node is the ordered pair `(child table, parent table)`, not an individual row-level edge.
- The four directed edge types describe how two relations share child or parent endpoints.
- After two relation layers, every row-level FK edge receives the state of its matching relation node as a condition vector.

## 15. Predictor head

- The shared head compares the final seed state to each candidate state.
- Binary classification depends on the score difference, so there is no task-specific classifier.

## 16. Standard results

- RelGraph reaches the same displayed macro AUROC as published RT. The published table rounds RT and Griffin to 22M; the 8.0x ratio uses RT's exact 22.3M implementation count versus RelGraph's 2.78M.
- The 2.1-point Base-to-RelGraph gain is the controlled evidence for relation conditioning.
- Do not claim statistical equivalence from equal one-decimal means.

## 17. NSL results

- Base has the smallest macro drop and the highest NSL macro score.
- RelGraph remains much more robust than paired RT, but relation conditioning is not the source of all robustness.
- Keep the claim protocol-level: our checkpoints explicitly reward Standard plus NSL validation, whereas the released RT checkpoints were selected differently.
- Trial Study Outcome is a useful natural control because its context contains no removable self-labels.

## 18. Full classification results

- This is a paired local comparison under both Standard and NSL; the RT Standard values here are not the published RT Table 1 values used on slide 16.
- Read the two column groups separately: each task has one pale-green winner in Standard and one in NSL.
- The task-level pattern is heterogeneous: RelGraph wins most Standard tasks among the proposed models, while RowGraph-Base often supplies the strongest NSL result.
- Trial Study Outcome is equal between Standard and NSL at the displayed precision because it contains no removable same-entity self-labels.

## 19. Future work

- The immediate empirical priority is to repeat training and evaluation with multiple random seeds and report mean plus standard deviation, rather than relying on a single run.
- Finalize and benchmark the existing regression extension before making it a paper result.
- Then adapt the shared row- and relation-level encoder to link prediction as a new task direction.

## Optional: Relation ablation (currently hidden)

- Separate the two conclusions: relation conditioning improves Standard accuracy; row-level construction supplies most observed NSL robustness.
- The NSL effect is heterogeneous and motivates a multi-seed analysis rather than a universal robustness claim.

## Optional: Takeaways (currently hidden)

- End on the conceptual shift: use cells to represent rows, then perform relational reasoning explicitly over rows and schema relations.
- State the strongest result and immediately preserve the claim boundary.
- Invite questions with the full task-level table ready.
