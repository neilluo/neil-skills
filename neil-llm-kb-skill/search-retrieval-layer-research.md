# LLM Wiki Search & Retrieval Layer: Deep Research Report

## 1. QMD (Query Markup Documents)

### Overview
- **Author**: Tobias Lütke (Shopify CEO, @tobi)
- **GitHub**: https://github.com/tobi/qmd
- **Install**: `npm install -g @tobilu/qmd`
- **License**: MIT
- **Requirements**: Node.js >= 22 or Bun >= 1.0

### How It Works

QMD is an on-device search engine for markdown files combining three retrieval strategies:

```
User Query → Query Expansion (fine-tuned LLM) → [Original + Variants]
    ↓
Each query → BM25 (FTS5) + Vector Search (in parallel)
    ↓
RRF Fusion (k=60, original query ×2 weight, top-rank bonus)
    ↓
Top 30 candidates → LLM Re-ranking (qwen3-reranker, yes/no + logprobs)
    ↓
Position-Aware Blending:
  Rank 1-3:  75% RRF / 25% reranker
  Rank 4-10: 60% RRF / 40% reranker
  Rank 11+:  40% RRF / 60% reranker
    ↓
Final Results (scored 0-1)
```

### Three Search Modes

| Mode | Command | What It Does | LLM Required |
|------|---------|--------------|--------------|
| Keyword | `qmd search` | BM25 full-text only (fastest) | No |
| Semantic | `qmd vsearch` | Vector similarity only | Embedding model |
| Hybrid | `qmd query` | FTS + Vector + Query Expansion + Re-ranking | All 3 models |

### GGUF Models (auto-downloaded, ~2GB total)

| Model | Purpose | Size |
|-------|---------|------|
| embeddinggemma-300M-Q8_0 | Vector embeddings | ~300MB |
| qwen3-reranker-0.6b-q8_0 | Re-ranking | ~640MB |
| qmd-query-expansion-1.7B-q4_k_m | Query expansion (fine-tuned) | ~1.1GB |

### MCP Server Integration

```json
// Claude Desktop / Claude Code
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

**MCP Tools exposed:**
- `query` — Search with typed sub-queries (lex/vec/hyde), combined via RRF + reranking
- `get` — Retrieve document by path or docid (with fuzzy matching suggestions)
- `multi_get` — Batch retrieve by glob pattern, comma-separated list, or docids
- `status` — Index health and collection info

**HTTP Transport** (shared, long-lived server):
```bash
qmd mcp --http              # localhost:8181
qmd mcp --http --daemon     # background daemon
```

### Performance Characteristics

| Metric | Default SQLite Memory | QMD Hybrid | Improvement |
|--------|----------------------|------------|-------------|
| Recall Accuracy | ~45% | ~92% | +47pp |
| Avg Tokens per Query | ~25,000 | ~6,950 | 72% reduction |
| Token savings vs reading all files | - | - | **95%+** |
| API Cost (local) | Cloud costs | $0.00 | 100% savings |

**Benchmark scores** (from QMD repo fixture):
- BM25 alone: ~0.50
- Vector alone: ~0.70
- Hybrid/Full pipeline: ~1.00

### When to Use QMD vs Just Reading index.md

| Scenario | Use index.md | Use QMD |
|----------|-------------|---------|
| < 50 files, well-structured | ✓ | |
| 50-500 files | ✓ (with sub-indexes) | ✓ (optional) |
| 500+ files | | ✓ (required) |
| Exact keyword known | ✓ | ✓ (BM25 mode) |
| Conceptual/semantic query | | ✓ (vector/hybrid) |
| Cross-reference lookup | ✓ | |
| "I know it exists but can't find it" | | ✓ |
| Agent workflow automation | | ✓ |

---

## 2. Alternative Search Solutions for Markdown Knowledge Bases

### LanceDB (used by nashsu/llm_wiki)

- **GitHub**: https://github.com/lancedb/lancedb
- **Type**: Serverless vector database, embedded directly into apps
- **Features**: Vector search + full-text search + hybrid search
- **Used by**: nashsu/llm_wiki desktop app for "Vector Semantic Search"
- **Integration**: Any OpenAI-compatible embedding endpoint
- **Key advantage**: Zero infrastructure — database file lives alongside your data
- **Full-text search**: Native FTS on 41M+ Wikipedia-scale documents demonstrated

### Basic Memory

- **GitHub**: https://github.com/basicmachines-co/basic-memory
- **Type**: MCP-native knowledge graph system
- **Storage**: Plain Markdown files on disk
- **Search**: Semantic search + keyword matching via local embedding model
- **Key feature**: Two-way — AI and humans write to same files; wikilinks compound into a knowledge graph
- **MCP tools**: read, write, search, build_context
- **Pricing**: Free (AGPL) local, $15/mo cloud

### Mem0

- **Type**: Vector-backed long-term memory store
- **Features**: Auto-recall, auto-capture, fact extraction
- **Pricing**: Free (self-hosted) / $249/mo Pro
- **Best for**: Automatic fact extraction without manual note-writing

### Cognee

- **Type**: Knowledge graph engine
- **Features**: Entity/relationship extraction, graph traversal
- **Pricing**: Free local / $35/mo cloud
- **Best for**: Relational logic, connecting concepts across documents

### Memsearch

- **Type**: Standalone library from OpenClaw's memory architecture
- **Storage**: Markdown + Milvus vector indexing
- **Best for**: AI builders wanting memory without the full gateway

### Comparison Matrix

| System | Search Type | Setup | Recall | Token Efficiency | Cost |
|--------|------------|-------|--------|-----------------|------|
| QMD | BM25 + Vector + Rerank | Low (~5 min) | 92% | Excellent | Free (local) |
| LanceDB | Vector + FTS hybrid | Low | High | Good | Free |
| Basic Memory | Semantic + keyword | Low | Good | Good | Free/Cloud |
| Mem0 | Vector (auto-extract) | Low-Medium | 85-90% | Poor (2x LLM calls) | $249/mo |
| Cognee | Knowledge graph | Medium | High (relational) | Moderate | $35/mo |

---

## 3. Scale Thresholds: When index.md Stops Being Enough

### The Decision Framework

| Scale | Files | Total Size | Approach | Reason |
|-------|-------|-----------|----------|--------|
| **Small** | 1-50 | < 200KB | index.md only | Fits in context window easily |
| **Medium** | 50-200 | 200KB-1MB | Tiered index.md + optional search | Sub-indexes by category; LLM can still navigate |
| **Large** | 200-500 | 1-5MB | Search required as complement | index.md itself becomes > 5K tokens; LLM can't hold map + content |
| **Very Large** | 500+ | 5MB+ | Search is primary access method | Impossible to navigate manually; need retrieval |

### Signs You Need a Search Layer

1. **index.md exceeds ~5,000 tokens** — The navigation map itself consumes significant context budget
2. **Agent fails to find information it "should" know** — Asking questions with different vocabulary than what's in the wiki
3. **Agent reads wrong/adjacent files** — The routing logic breaks down with too many similar entries
4. **Context window fills before content is loaded** — index.md + selected files > context budget
5. **Semantic queries fail** — "How does X relate to Y?" when the answer spans 3+ files the agent doesn't know to load
6. **Maintenance overhead** — Keeping index.md accurate across 200+ files becomes a full-time job

### Structure Matters: Many Small Files vs Fewer Large Files

| Structure | Threshold for Search | Why |
|-----------|---------------------|-----|
| Many small files (< 2KB each) | Earlier (~100 files) | index.md grows linearly; each file = 1-3 lines in index |
| Fewer large files (5-20KB each) | Later (~50 files) but with different pain | Content within files needs sub-document search; can't load full file into context |
| Mixed (typical wiki) | ~150-200 files | Combination of both problems |

### The Context Window Math

With a 200K token context window:
- System prompt: ~10K tokens
- index.md (200 files): ~4-8K tokens
- Conversation history: ~20-50K tokens
- Available for content: ~130-160K tokens
- Average wiki page: ~2-4K tokens
- **Maximum pages loadable per query: ~30-80**

When your wiki has 500+ pages and the agent needs info from any of them, navigating by index.md means:
- Read index (~5K tokens) → Pick files → Read files (~20K tokens) → Answer
- Total per query: ~25K tokens minimum
- With QMD: Search → Get top 5 snippets (~3K tokens) → Answer
- **~87% token reduction**

---

## 4. Compilation vs Retrieval Tradeoffs

### The Spectrum

```
Pure Compilation (Karpathy)  ←→  Hybrid  ←→  Pure RAG
```

### Academic Evidence (arxiv.org/html/2605.18490v1)

A preregistered study comparing Vector RAG vs LLM-Compiled Wiki on 24 papers:

| Dimension | Winner | Magnitude |
|-----------|--------|-----------|
| Cross-paper synthesis (inter_paper_mapping) | **Wiki** | +6.6 points (large) |
| Answer organization (structural_integrity) | Wiki (weak) | +1.6 points |
| Point-source grounding (rubric) | RAG | +0.7 points |
| Claim-level citation accuracy | **Wiki** | 40% vs 19% supported |
| Per-query token cost | **RAG** | 21× cheaper per query |
| Latency | **RAG** | 6.6× faster |

**Key Findings:**
- Wiki excels at connecting findings across documents
- Wiki's claim-level citations are 2× more often supported than RAG's
- Wiki uses **21× more tokens per query** (opposite of expected — tool-loop browsing is expensive)
- RAG has a Pareto advantage on 4/13 questions (matches or beats wiki at 10× lower cost)
- A decomposition-RAG variant recovered 88% of wiki's synthesis advantage

### When to Use Each

| Approach | Best For | Fails When |
|----------|----------|-----------|
| **Pure Compilation** (Karpathy wiki) | Stable knowledge, deep synthesis, bounded domains | Rapidly changing data; very large corpora; per-query cost matters |
| **Pure RAG** | Dynamic data, point lookups, cost-sensitive queries | Multi-hop synthesis; maintaining coherent narrative |
| **Hybrid** (compiled + search fallback) | Medium-large KBs; mix of deep and shallow queries | Adds complexity; two systems to maintain |

### The Karpathy Pattern (Pure Compilation)

Three Layers:
1. **Raw Sources** (immutable) — articles, papers, notes. LLM reads but never modifies.
2. **The Wiki** (LLM-written) — summaries, entities, concepts. LLM creates/updates/cross-references.
3. **The Schema** (co-evolved) — configuration for structure and conventions.

Three Operations:
1. **Ingest** — New source → LLM processes → updates 10-15 pages
2. **Query** — Ask questions → LLM reads compiled wiki → answers
3. **Lint** — Health-check: contradictions, orphans, stale claims

**Philosophy**: "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

### Recommended Approach by Scale

| Scale | Strategy |
|-------|----------|
| < 100 files, slow-changing | Pure compilation. index.md navigation. No search needed. |
| 100-500 files, moderate change | Compilation + QMD search as fallback for edge cases |
| 500+ files or fast-changing | Compilation for core knowledge + RAG/search for dynamic portions |
| Rapidly changing data (daily) | RAG wins. Compilation can't keep up. |

---

## 5. Tool Ecosystem Map

### Ingestion & Conversion Tools

| Tool | Function | Link |
|------|----------|------|
| **trafilatura** | Web article extraction → clean text/markdown | https://trafilatura.readthedocs.io |
| **MarkItDown** (Microsoft) | PDF/DOCX/PPTX/XLSX/HTML/YouTube → Markdown | https://github.com/microsoft/markitdown |
| **Obsidian Web Clipper** | Browser extension → markdown in vault | Built into Obsidian |
| **MinerU** | Complex PDF parsing (tables, formulas, layouts) | Cloud API |
| **Tavily / SerpApi / SearXNG** | Web search → structured results for ingest | Various |

### Knowledge Organization Tools (Obsidian Ecosystem)

| Tool | Function |
|------|----------|
| **Obsidian** | Markdown editor with wikilinks, graph view, real-time preview |
| **Dataview** | Dynamic tables/queries from YAML frontmatter |
| **Graph View** | Visual relationship mapping (hubs, orphans, connections) |
| **Web Clipper** | One-click web → markdown |
| **Obsidian Git** | Auto-commit vault every 15 minutes |
| **Templates** | Consistent page structure (frontmatter, headings) |

### Search & Retrieval Tools

| Tool | Type | Best For |
|------|------|----------|
| **QMD** | BM25 + Vector + Rerank (local) | Primary search engine for markdown KBs |
| **LanceDB** | Embedded vector DB + FTS | App-integrated search |
| **Basic Memory** | MCP knowledge graph | Shared AI-human memory |
| **sqlite-vec** | SQLite vector extension | Lightweight embedding search |
| **pgvector** | PostgreSQL vector extension | Team/production deployments |

### CLI Tools for Wiki Maintenance

| Tool | Function |
|------|----------|
| `qmd update` | Re-index all collections (with pre-update hooks like git pull) |
| `qmd embed` | Generate/refresh vector embeddings |
| `qmd status` | Index health check |
| `qmd bench` | Benchmark search quality (precision@k, recall, MRR, F1) |
| `qmd cleanup` | Clean orphaned data |
| `qmd doctor` | Diagnose installation (runtime, GPU, embeddings) |

---

## 6. MCP Integration Patterns for Knowledge Bases

### Dedicated Wiki MCP Servers

| Server | Purpose | Tools |
|--------|---------|-------|
| **QMD MCP** (`qmd mcp`) | Hybrid search over markdown collections | query, get, multi_get, status |
| **llm-wiki-mcp** | Full Karpathy wiki pattern implementation | wiki_init, wiki_ingest, wiki_create_page, wiki_read_page, wiki_update_page, wiki_delete_page, wiki_search, wiki_lint |
| **Basic Memory** | Persistent AI memory as markdown | read, write, search, build_context |
| **nashsu/llm_wiki** | Desktop app with HTTP API + MCP | hybrid search, file read, graph traversal, source rescan |
| **Trafilatura MCP** | Web content extraction | extract (HTML→markdown), parallel processing |

### Architecture Patterns

#### Pattern 1: QMD as Search Sidecar
```
Agent → QMD MCP → Local SQLite + Vector Index → Results
                   ↑
           Markdown files on disk (source of truth)
```
- Agent uses `query` tool for semantic search
- Agent uses `get` tool for precise document retrieval
- Files remain as plain markdown; QMD indexes them

#### Pattern 2: llm-wiki-mcp as Full Wiki Manager
```
Agent → llm-wiki-mcp → Wiki vault (markdown files)
  ↓                      ↑
Raw Sources          index.md + log.md
```
- Agent uses `wiki_ingest` to process new sources
- Agent uses `wiki_search` for retrieval (uses QMD if available, falls back to substring)
- Agent uses `wiki_lint` for health checks

#### Pattern 3: Layered Memory (OpenClaw pattern)
```
Bootstrap Files (SOUL.md, AGENTS.md, MEMORY.md)
    ↓ (injected every session)
Session Context
    ↓ (compaction when full)
Retrieval Layer (QMD / built-in hybrid search)
    ↓ (on-demand via memory_search)
Daily Logs + External Collections
```

### MCP Server Configuration Examples

**Multi-source knowledge base:**
```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    },
    "llm-wiki": {
      "command": "npx",
      "args": ["llm-wiki-mcp", "--vault", "/path/to/wiki"]
    },
    "trafilatura": {
      "command": "uvx",
      "args": ["trafilatura-mcp"]
    }
  }
}
```

---

## 7. Recommended Search Stack by Scale

### Tier 1: Personal Notes (< 100 files)
- **Navigation**: index.md with descriptions
- **Search**: None needed (or QMD `search` for keyword mode)
- **Tools**: Obsidian + Web Clipper
- **Cost**: $0

### Tier 2: Growing Knowledge Base (100-500 files)
- **Navigation**: Tiered index.md (category sub-indexes)
- **Search**: QMD (hybrid mode) as MCP server
- **Tools**: Obsidian + Dataview + trafilatura + MarkItDown
- **Cost**: $0 (all local)

### Tier 3: Large Personal/Team Wiki (500-2000 files)
- **Navigation**: QMD is primary access method
- **Search**: QMD full pipeline (expansion + BM25 + vector + reranking)
- **Organization**: llm-wiki-mcp for structured ingestion
- **Tools**: Full Obsidian stack + git version control + scheduled updates
- **Cost**: $0 (local) or cloud hosting for team

### Tier 4: Production/Enterprise (2000+ files)
- **Search**: LanceDB or pgvector + custom retrieval pipeline
- **Augmentation**: Compiled wiki summaries for common queries + RAG for edge cases
- **MCP**: Custom MCP server wrapping your search infrastructure
- **Cost**: Variable (embedding compute, storage)

---

## 8. Key Sources & Links

| Resource | URL |
|----------|-----|
| QMD GitHub | https://github.com/tobi/qmd |
| QMD npm | https://www.npmjs.com/package/@tobilu/qmd |
| QMD MCP Market | https://mcpmarket.com/tools/skills/qmd-markdown-search |
| Karpathy's LLM Wiki Gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| nashsu/llm_wiki | https://github.com/nashsu/llm_wiki |
| llm-wiki-mcp | https://www.npmjs.com/package/llm-wiki-mcp |
| Basic Memory | https://github.com/basicmachines-co/basic-memory |
| LanceDB | https://lancedb.com |
| MarkItDown | https://github.com/microsoft/markitdown |
| trafilatura | https://trafilatura.readthedocs.io |
| Trafilatura MCP | https://mcpmarket.com/server/trafilatura |
| RAG vs Wiki Paper | https://arxiv.org/html/2605.18490v1 |
| MindStudio Index File Guide | https://www.mindstudio.ai/blog/llm-knowledge-base-index-file-no-vector-search |
| OpenClaw Memory Masterclass | https://velvetshark.com/openclaw-memory-masterclass |
| Awesome MCP Servers (Knowledge) | https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md |

---

## 9. Summary: The Decision Tree

```
START: How many markdown files?

├── < 50 files, < 200KB total
│   └── Just use index.md. No search needed.
│       Tool: Obsidian + manual organization
│
├── 50-200 files, well-structured
│   └── Tiered index.md + QMD keyword search as backup
│       Tool: qmd search (BM25 only, no models needed)
│
├── 200-500 files OR semantic queries needed
│   └── QMD hybrid search as primary retrieval
│       Tool: qmd query (full pipeline) via MCP
│
├── 500+ files OR team usage
│   └── QMD + compiled wiki layer (llm-wiki-mcp)
│       Search is primary; index.md is just one entry point
│
└── 2000+ files OR production workload
    └── LanceDB/pgvector + custom pipeline
        Compiled summaries for hot paths + RAG for long tail
```
