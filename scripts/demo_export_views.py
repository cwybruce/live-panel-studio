"""Authored outer function-block rectangles, with space for their neon bloom."""

BLOCKS = {
    'rag-explainer': [
        ('rag-hero', '主流程 · 问题到回答', 28, 192, 928, 355),
        ('rag-retrieve', '检索候选', 28, 566, 454, 300),
        ('rag-rerank', '重排证据', 502, 566, 454, 300),
        ('rag-ground', '引用与依据', 28, 886, 454, 305),
        ('rag-abstain', '无依据时说明', 502, 886, 454, 305)],
    'agent-team': [
        ('agentEditorial-hero', '主流程 · 四角色交接', 28, 194, 928, 383),
        ('agentEditorial-decompose', '任务拆解', 28, 596, 454, 284),
        ('agentEditorial-time-lanes', '时间泳道', 502, 596, 454, 284),
        ('agentEditorial-handoff-package', '交接包', 28, 900, 454, 286),
        ('agentEditorial-event-replay', '事件回放', 502, 900, 454, 286)],
    'product-request': [
        ('requestEditorial-hero', '主流程 · 请求与返回', 28, 194, 928, 383),
        ('requestEditorial-key-value', '缓存命中', 28, 596, 454, 284),
        ('requestEditorial-source-of-truth', '读取原始记录', 502, 596, 454, 284),
        ('requestEditorial-merge-the-branches', '分支合流', 28, 900, 454, 286),
        ('requestEditorial-illustrative-counter', '请求计数', 502, 900, 454, 286)],
    'knowledge-card': [
        ('knowledge-hero', '主流程 · 展开书页', 28, 192, 928, 360),
        ('story-input', '明确输入', 28, 571, 454, 294),
        ('story-process', '展示过程', 502, 571, 454, 294),
        ('story-check', '核对输出', 28, 885, 454, 306),
        ('story-recap', '回顾要点', 502, 885, 454, 306)],
    'business-workflow': [
        ('workflow-hero', '主流程 · 工单看板', 28, 192, 928, 422),
        ('story-assign', '问题分配', 28, 634, 454, 266),
        ('story-complete', '完成与验收', 502, 634, 454, 266),
        ('story-review', '复核状态', 28, 920, 454, 271),
        ('story-retry', '补充资料与重试', 502, 920, 454, 271)],
    'incident-replay': [
        ('incidentEditorial-hero', '主流程 · 依赖与告警', 28, 194, 928, 383),
        ('incidentEditorial-metric-replay', '余量曲线', 28, 596, 928, 284),
        ('incidentEditorial-threshold-relation', '阈值关系', 28, 900, 454, 286),
        ('incidentEditorial-recovery-checks', '恢复检查', 502, 900, 454, 286)],
    'component-lab': [
        ('lab-hero', '发光角色', 28, 201, 928, 247),
        ('component-02-converge', '节点汇聚', 28, 466, 928, 236),
        ('component-03-proportion', '比例环', 28, 707, 454, 240),
        ('component-04-reveal', '虚实对比', 502, 707, 454, 240),
        ('component-05-distribute', '分支流带', 28, 965, 454, 228),
        ('component-06-progress', '任务看板', 502, 965, 454, 228)],
    'avatar-themes': [
        ('avatar-hero', '游走导览', 28, 201, 928, 351),
        ('component-01-appearance', '角色外观', 28, 571, 454, 287),
        ('component-02-attention', '导览焦点', 502, 571, 454, 287),
        ('component-03-timeline', '回放时间线', 28, 877, 928, 316)],
}


def export_views(scene):
    views = []
    for name, label, x, y, width, height in BLOCKS[scene]:
        # H.264 yuv420p needs even dimensions. The 12px margin keeps the bloom.
        width, height = width + 24, height + 24
        views.append({'id': name, 'label': label,
                      'crop': [x - 12, y - 12, width + width % 2, height + height % 2]})
    return views
