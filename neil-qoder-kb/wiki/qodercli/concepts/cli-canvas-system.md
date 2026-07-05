# Canvas 与 Recipes 系统

> QoderCLI 和 Qoder Desktop 共享的可视化渲染框架，通过 .canvas.tsx 文件和预置 Recipe 模板实现交互式代码审查、序列图、设计系统预览等可视化制品。

## 概述

Canvas 是 Qoder 产品线的可视化渲染系统，让 Agent 能生成交互式的 .canvas.tsx 文件，在 Desktop IDE 的 Canvas 预览面板中渲染。内置多个 Recipe（配方）模板，覆盖常见的可视化场景。

## 目录结构

```
~/.qoder/canvas/
├── recipes/                  # 预置配方模板
│   ├── code-review/         # 代码审查可视化
│   ├── design-system/       # 设计系统预览
│   ├── format-viewer/       # 格式查看器
│   └── sequence-diagram/    # 序列图生成
├── canvases/                 # 用户生成的制品
│   └── *.canvas.tsx         # TSX 格式的可视化文件
└── sdk/                      # Canvas 渲染 SDK
```

## 内置 Recipes

| Recipe | 用途 | 输出 |
|--------|------|------|
| code-review | 交互式代码审查 | 带差异高亮的审查界面 |
| design-system | 设计系统预览 | 组件库可视化 |
| format-viewer | 格式化数据查看 | JSON/YAML 美化展示 |
| sequence-diagram | 序列图 | 时序交互图 |

## .canvas.tsx 文件格式

Canvas 文件是 TSX（TypeScript + JSX）格式：

```tsx
// example.canvas.tsx
export default function MyCanvas() {
  return (
    <div>
      <h1>代码审查结果</h1>
      <DiffViewer
        oldCode={...}
        newCode={...}
        splitView={true}
      />
    </div>
  );
}
```

## 与 Desktop 集成

- Desktop IDE 的 Canvas 预览面板实时渲染 .canvas.tsx
- Agent 通过 `/canvas` 命令创建或编辑 canvas 文件
- Canvas SDK 提供渲染组件库

## 交叉引用

- [[desktop-editor]] — Desktop IDE 中 Canvas 的预览入口
- [[cli-command-system]] — /canvas 斜杠命令
- [[cli-skill]] — canvas skill 的 SKILL.md 定义

## 来源

- ~/.qoder/canvas/ 目录结构 [reverse-engineering] 2026-06-30
- QoderCLI 1.0.16 内置 Recipe 列表 [reverse-engineering] 2026-06-30
