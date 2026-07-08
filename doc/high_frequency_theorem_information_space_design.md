# 高频定理模型与信息空间协同设计

**版本**: v0.1  
**日期**: 2026-06-30  
**范围**: 第一批高频模型族 `0-13, 21, 29, 75`  
**状态**: 设计规范，尚未替换现有运行代码

## 1. 目标与范围

本设计用于跑通可信状态转换闭环：

```text
Conic10K facts
  -> 纯解析与规范化
  -> SymbolicState S0
  -> theorem.match(S0) 得到变量绑定
  -> theorem.derive(S0, bindings) 得到 StateDelta
  -> 校验 postconditions
  -> 原子提交，得到 S1
```

当前阶段不设计 `AbstractState`，也不训练 selector。目标是先保证：

1. 信息空间能无损表达高频定理所需的输入和输出。
2. 每个 theorem action 只执行自身数学语义，不隐式组合其他定理。
3. applicator 产生可审计、可回放、可验证的状态变化。
4. gold model sequence 可以生成可靠的 `S0-y0-S1-y1-...` 轨迹。

`data/train_with_models_v2.json` 包含 5,359 条非空模型序列和 20,226 个模型步骤。最高频动作包括：

| Model | 次数 | 主要角色 |
|---:|---:|---|
| 5 | 1,698 | 双曲线横轴标准方程 |
| 3 | 1,588 | 椭圆横轴标准方程 |
| 7 | 1,569 | 抛物线向右标准方程 |
| 13 | 1,396 | 离心率公式 |
| 21 | 1,014 | 双曲线渐近线 |
| 29 | 890 | 抛物线准线 |
| 2 | 790 | 抛物线定义 |
| 0 | 650 | 椭圆定义 |
| 75 | 527 | 圆标准方程 |
| 1 | 510 | 双曲线定义 |
| 12 | 448 | 双曲线参数关系 |
| 11 | 403 | 椭圆参数关系 |

为避免只实现某个方向的特例，第一批按模型族覆盖定义模型 `0-2`、标准方程 `3-10`、参数关系 `11-13`、渐近线 `21`、准线 `29` 和圆标准方程 `75`。

## 2. 设计原则

### 2.1 解析不能偷偷完成定理推导

解析器可以执行分词、括号恢复、别名归一化、AST 构建和代数表达式的无损标准化。解析器不能从标准方程推导 `a,b,c,p`，不能从曲线类型自动加入定义式，也不能从 `a,b` 推导 `c,e`。

因此，现有 `StateConstructor._extract_equation_parameters()` 的行为最终应迁移到 Models 3-10，不能作为新 S0 的隐式组成部分。

### 2.2 信息按对象作用域存储

禁止以全局键 `parameters["a"]` 作为主事实源。应表达为：

```text
ParameterOf(G, semi_axis_a) = a
ParameterOf(G, semi_axis_b) = b
ParameterOf(G, focal_half_distance) = c
```

### 2.3 不猜测缺失信息

无法确定抛物线方向、参数正负或实体绑定时，返回 `PRECONDITION_UNRESOLVED`。不得使用“默认向右”“默认实体 G”等替代真实绑定。

### 2.4 一条 action 只实现一个 theorem

例如 Model 13 只实现 `e=c/a`。如果 `c` 未知而 `a,b` 已知，应先应用 Model 11 或 12；Model 13 不应在内部暗中推导 `c`。

### 2.5 新知识不能无条件覆盖旧知识

新事实只能新增、与已有事实等价或补充更精确的表示。若同一对象属性已有不等价值，必须返回 `CONFLICT`。

## 3. 信息空间 v1

### 3.1 核心结构

```python
@dataclass(frozen=True)
class SymbolRef:
    name: str
    type_name: str

@dataclass(frozen=True)
class Term:
    operator: str
    arguments: tuple

@dataclass(frozen=True)
class Fact:
    predicate: str
    arguments: tuple
    value: object | None
    provenance: "Provenance"
    raw_expression: str | None = None

@dataclass(frozen=True)
class Provenance:
    source_kind: str       # given | theorem | solver | normalization
    source_id: str         # fact id or model id
    evidence_fact_ids: tuple[str, ...]

@dataclass
class SymbolicStateV1:
    symbols: dict[str, SymbolRef]
    facts: dict[str, Fact]
    history: list["ApplicationResult"]
```

现有 `entities/equations/parameters/geometric_relations/coordinates/constraints` 可以暂时保留为兼容视图，但新的 theorem matcher 应读取 typed facts，而不是直接搜索字符串。

### 3.2 第一批必须支持的 predicate

| Predicate | 示例 |
|---|---|
| `TypeOf` | `TypeOf(G)=Hyperbola` |
| `ExpressionOf` | `ExpressionOf(G)=x^2/4-y^2/m^2-1` |
| `ConicStandardForm` | `ConicStandardForm(G,hyperbola,horizontal,A2,B2)` |
| `ParameterOf` | `ParameterOf(G,semi_axis_a_squared)=4` |
| `PointOnCurve` | `PointOnCurve(P,G)` |
| `FocusOf` | `FocusOf(G,F1)` |
| `DirectrixOf` | `DirectrixOf(G,L)` |
| `AsymptoteOf` | `AsymptoteOf(G,L1)` |
| `CoordinateOf` | `CoordinateOf(P)=(x0,y0)` |
| `DistanceOf` | `DistanceOf(P,F)=d` |
| `SlopeOf` | `SlopeOf(L)=k` |
| `EquationConstraint` | `Eq(lhs,rhs)` |
| `OrderConstraint` | `Gt(m,0)` |
| `DefinitionRelation` | 定义产生的距离关系 |

### 3.3 表达式、等价性和索引

数学值使用 SymPy-compatible AST 或等价结构化表达式；字符串只用于显示和原始信息保留。

```text
sqrt(m^2)       -> Abs(m)，除非状态中有 m>0
y = 5*x/2       -> Eq(y,5*x/2)
5*x - 2*y = 0   -> Eq(5*x-2*y,0)
```

状态至少提供 `by_predicate`、`by_subject`、`by_type` 和 `by_property` 索引。表达式规范化器负责判断等价，不负责增加新的几何知识。

## 4. Applicator 统一契约

```python
@dataclass(frozen=True)
class TheoremSpec:
    model_id: int
    name: str
    variables: dict[str, str]
    preconditions: tuple["FactPattern", ...]
    guards: tuple["Guard", ...]
    postconditions: tuple["FactPattern", ...]

@dataclass(frozen=True)
class StateDelta:
    add_symbols: tuple[SymbolRef, ...] = ()
    add_facts: tuple[Fact, ...] = ()
    refine_facts: tuple["FactRefinement", ...] = ()

@dataclass(frozen=True)
class ApplicationResult:
    model_id: int
    status: str
    binding: dict
    delta: StateDelta
    evidence_fact_ids: tuple[str, ...]
    postcondition_errors: tuple[str, ...]
```

模型接口为：

```python
match(state) -> list[Binding]
derive(state, binding, solver) -> StateDelta
validate(state_before, delta, state_after) -> list[str]
```

`match()` 返回实际变量绑定，而不是 bool。theorem 不直接修改 state；Applicator 在副本应用 delta，完成冲突和 postcondition 检查后再原子提交。

统一状态码：

```text
APPLIED
ALREADY_KNOWN
NO_MATCH
AMBIGUOUS_BINDING
PRECONDITION_UNRESOLVED
SOLVER_UNRESOLVED
CONFLICT
POSTCONDITION_FAILED
EXCEPTION
```

`ALREADY_KNOWN` 是幂等结果，不可作为新的 selector 训练 transition。

## 5. 高频模型详细规范

### 5.1 Models 0-2：圆锥曲线定义

定义模型必须支持两种明确模式，不能混为一个宽松 `can_apply()`。

#### Forward mode

输入已知曲线和曲线上的具体点，输出该点满足的定义关系。

Model 0：

```text
Preconditions:
  TypeOf(G)=Ellipse
  PointOnCurve(P,G)
  FocusOf(G,F1), FocusOf(G,F2)
  ParameterOf(G,semi_axis_a)=a
Conclusion:
  Eq(Distance(P,F1)+Distance(P,F2),2*a)
```

Model 1：

```text
Preconditions:
  TypeOf(G)=Hyperbola
  PointOnCurve(P,G)
  FocusOf(G,F1), FocusOf(G,F2)
  ParameterOf(G,semi_axis_a)=a
Conclusion:
  Eq(Abs(Distance(P,F1)-Distance(P,F2)),2*a)
```

Model 2：

```text
Preconditions:
  TypeOf(G)=Parabola
  PointOnCurve(P,G)
  FocusOf(G,F)
  DirectrixOf(G,L)
Conclusion:
  Eq(Distance(P,F),Distance(P,L))
```

#### Recognition mode

当 facts 给出距离轨迹定义而曲线实体未知时，可以反向产生 `LocusType` 或退化类型。Recognition mode 必须单独写 precondition 和 postcondition；例如距离和等于两焦点距离时是退化线段，不能无条件写成椭圆。

禁止仅因为存在某种曲线就加入带未绑定 `P,F1,F2` 的字符串，也禁止自动创造没有题目依据的具体点。

### 5.2 Models 3-6：椭圆与双曲线标准方程

这组模型负责把显式曲线方程解释为 scoped conic parameters。

Model 3 示例：

```text
Input:
  TypeOf(G)=Ellipse
  ExpressionOf(G)=Eq(x^2/A2+y^2/B2,1)
  A2>B2>0，或存在焦点在 xAxis 的事实以确定角色
Binding:
  G=G, orientation=horizontal, a2=A2, b2=B2
Delta:
  ConicStandardForm(G,ellipse,horizontal,A2,B2)
  ParameterOf(G,semi_axis_a_squared)=A2
  ParameterOf(G,semi_axis_b_squared)=B2
  ParameterOf(G,semi_axis_a)=sqrt_positive(A2)
  ParameterOf(G,semi_axis_b)=sqrt_positive(B2)
```

Model 4 将 orientation 改为 vertical。Models 5-6 对双曲线分别识别：

```text
x^2/A2-y^2/B2=1  -> horizontal
y^2/A2-x^2/B2=1  -> vertical
```

Guard 和 postconditions：

- 分母非零并满足圆锥曲线定义域。
- 椭圆的 `a2` 是长轴对应分母，不能仅按字符串出现顺序赋值。
- 符号分母无法比较时，允许结合焦点轴等显式事实绑定。
- 无法唯一确定角色时返回 `PRECONDITION_UNRESOLVED`。
- 标准形式代回后必须与原方程代数等价。
- 已有同名参数时必须等价。

### 5.3 Models 7-10：抛物线标准方程

必须遵循本项目/Conic10K 当前使用的记号：

```text
y^2=2*p*x  -> focus offset=p/2
x^2=2*p*y  -> focus offset=p/2
```

不要在实现时混入另一套常见的 `y^2=4px` 参数命名。

Model 7：

```text
Input:
  TypeOf(G)=Parabola
  ExpressionOf(G)=Eq(y^2,K*x), K>0
Binding:
  orientation=right, two_p=K, p=K/2
Delta:
  ConicStandardForm(G,parabola,right,K)
  ParameterOf(G,two_p)=K
  ParameterOf(G,p)=K/2
  FocusOffsetOf(G)=K/4
```

Models 8-10 分别对应 left/up/down。方向必须从标准方程的变量位置和系数符号得到，不允许默认。

本组模型可以输出焦点偏移参数；只有已有 `FocusOf(G,F)` 时才能把坐标写入具体 F。否则保存 `FocusCoordinateOf(G)`，不创造名为 `Focus` 的全局点。

### 5.4 Models 11-12：参数关系

Model 11：

```text
TypeOf(G)=Ellipse
Eq(a2,b2+c2)
```

Model 12：

```text
TypeOf(G)=Hyperbola
Eq(c2,a2+b2)
```

应用规则：

1. 每次 action 固定增加参数关系事实。
2. 只有恰好一个目标参数可由当前事实唯一求出时，才增加确定值。
3. 多个未知量时只增加 relation，不猜测数值。
4. `a,b,c` 与 `a2,b2,c2` 的平方关系作为显式事实保存。
5. 平方根需要结合 positivity constraint；否则保留根式或多值集合。

### 5.5 Model 13：离心率公式

```text
Preconditions:
  TypeOf(G) in {Ellipse,Hyperbola}
  ParameterOf(G,focal_half_distance)=c
  ParameterOf(G,semi_axis_a)=a
  NonZero(a)
Delta:
  ParameterOf(G,eccentricity)=simplify(c/a)
  Eq(Eccentricity(G),c/a)
```

可以增加平方形式变体：已知 `c2,a2` 时输出 `e2=c2/a2`；只有 positivity 足以确定正根时再输出 `e=sqrt(c2/a2)`。

禁止 Model 13 内部使用椭圆/双曲线参数关系推导 c，这属于 Models 11-12。

### 5.6 Model 21：双曲线渐近线

#### Forward mode

```text
Preconditions:
  TypeOf(G)=Hyperbola
  ConicStandardForm(G,hyperbola,orientation,a2,b2)
  a=sqrt_positive(a2), b=sqrt_positive(b2)
Horizontal delta:
  AsymptoteFamilyOf(G)={Eq(y,(b/a)*x),Eq(y,-(b/a)*x)}
Vertical delta:
  AsymptoteFamilyOf(G)={Eq(y,(a/b)*x),Eq(y,-(a/b)*x)}
```

#### Constraint-matching mode

如果题目已经给出 `OneOf(Asymptote(G))=L`，该 action 除了产生理论渐近线，还应增加可供后续 solver 使用的匹配约束：

```text
Eq(Slope(L)^2,b2/a2)     # horizontal
Eq(Slope(L)^2,a2/b2)     # vertical
```

使用平方斜率避免“给出的是正支还是负支”的不必要歧义。该模型只产生约束；解出 m 属于通用 SymbolicSolver，不应硬编码在 Model 21。

Postconditions：每条渐近线经过曲线中心，两条斜率互为相反数，斜率关系与曲线 orientation 一致。

### 5.7 Model 29：抛物线准线

```text
Preconditions:
  TypeOf(G)=Parabola
  ConicStandardForm(G,parabola,direction,...)
  FocusOffsetOf(G)=f
Delta:
  right -> DirectrixExpression(G)=Eq(x,-f)
  left  -> DirectrixExpression(G)=Eq(x, f)
  up    -> DirectrixExpression(G)=Eq(y,-f)
  down  -> DirectrixExpression(G)=Eq(y, f)
```

如果状态已有 `DirectrixOf(G,L)`，则同时加入 `ExpressionOf(L)`；否则保留函数项 `DirectrixExpression(G)`，不创造随意命名的 L。禁止在 direction 未知时默认 right。

### 5.8 Model 75：圆标准方程

```text
Preconditions:
  TypeOf(C)=Circle
  ExpressionOf(C) 可规范化为 (x-h)^2+(y-k)^2=r2
Delta:
  CenterCoordinateOf(C)=(h,k)
  ParameterOf(C,radius_squared)=r2
  ParameterOf(C,radius)=sqrt_positive(r2)
  CircleStandardForm(C,h,k,r2)
```

一般式 `x^2+y^2+Dx+Ey+F=0` 由 SymbolicSolver 完成配方，但该变换仍属于 Model 75 的 derivation，不属于 parser。

若已有 `CenterOf(C,O)`，增加 `CoordinateOf(O)=(h,k)`；没有具体中心实体时不创建全局名 `Center`。

## 6. SymbolicSolver 的边界

SymbolicSolver 提供无领域语义的计算能力：

```text
normalize_equation
equivalent
solve_one_unknown
simplify
positive_sqrt
complete_square
line_slope
substitute
check_consistency
```

它不知道 Model 21 是“渐近线定理”，也不主动向 state 增加事实。Theorem 决定调用什么计算，并把计算结果包装成有语义和 provenance 的 Fact。

## 7. Golden transition 测试范式

每个模型至少包含：

```text
positive_numeric
positive_symbolic
negative_missing_precondition
ambiguous_binding
already_known_idempotent
conflicting_existing_fact
postcondition_equivalence
```

Model 21 示例：

```text
Given:
  TypeOf(G)=Hyperbola
  ConicStandardForm(G,hyperbola,horizontal,4,m^2)
  Positive(m)
  OneOf(Asymptote(G))=L
  ExpressionOf(L)=Eq(5*x-2*y,0)
Expected delta:
  Eq(Slope(L)^2,m^2/4)
  Eq(25/4,m^2/4)
Not expected:
  ParameterOf(G,m)=5
```

`m=5` 应由后续通用求解步骤结合 `m>0` 得出，这能保持 theorem/application 边界清晰。

## 8. 第一批实施顺序

### Phase A：基础设施

1. 新增 typed `Fact/Term/Provenance`，保留旧字段兼容视图。
2. 新增 canonical expression 和 equivalence API。
3. 新增 `StateDelta/ApplicationResult`。
4. 新增冲突、幂等和原子提交机制。

### Phase B：最短闭环

按真实高频路径实现：

```text
Model 5 -> Model 21
Model 3 -> Model 11 -> Model 13
Model 7 -> Model 2 -> Model 29
Model 75
```

### Phase C：模型族扩展

1. 标准方程方向变体 `4,6,8,9,10`。
2. 定义模型的 recognition mode。
3. Model 12 及更多符号参数场景。

### Phase D：gold sequence dry-run

对全部训练序列输出统一状态码。每一步保存 binding、evidence 和 delta；失败后停止生成可信后续状态，但保留审计记录。

## 9. 第一批验收标准

进入批量状态轨迹生成前，应满足：

- 所有第一批 theorem 都有结构化 precondition 和 postcondition。
- 定理不直接修改 state。
- 同一输入得到完全相同的 delta。
- 幂等测试 100% 通过。
- 冲突测试 100% 检出。
- 不存在默认曲线名、默认点名或默认方向。
- golden transition 人工审核通过率至少 98%。
- parser 未识别事实必须保留为 `UnparsedFact`，不能静默丢弃。
- 训练和推理使用同一个纯解析 S0 构造流程。

## 10. 与当前代码的迁移关系

| 当前实现 | 目标位置 |
|---|---|
| `SymbolicState.entities` | `SymbolRef` + `TypeOf` |
| `parameters['a']` | `ParameterOf(G,semi_axis_a)` |
| `geometric_relations: List[str]` | typed `Fact` |
| `equations: List[str]` | `ExpressionOf` + expression AST |
| `can_apply() -> bool` | `match() -> list[Binding]` |
| `apply(state) -> bool` | `derive() -> StateDelta` |
| `applied_models` | `ApplicationResult` history |
| 初始化自动应用 Models 3-10 | 显式 gold/theorem action |

迁移期间旧接口可以通过 adapter 继续工作，但新 trajectory builder 只能消费满足本规范的 `ApplicationResult`。
