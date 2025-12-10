#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精簡版：生成包含多個 scenario 分支的可執行倉庫生成器
使用： python3 generate_repo.py
"""
import os
import json
import shutil
from pathlib import Path

REPO = "2026-endgames"
USER = "ORIGNALBLUE"  # 已替換為你的 GitHub 使用者名稱

def write_file(path, content, make_executable=False):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    if make_executable:
        os.chmod(path, 0o755)
    print(f"✓ {path}")

def gen_scenario(branch, data):
    base = f"{REPO}/branches/{branch}"
    # scenario.json
    write_file(f"{base}/scenario.json", json.dumps(data["json"], indent=2, ensure_ascii=False))
    # scenario.md (簡要)
    j = data["json"]
    md_lines = [
        f"# {j.get('title','')}",
        "",
        f"**Branch:** `{j.get('branch','')}`  ",
        f"**Summary:** {j.get('summary','')}",
        f"**Time horizon:** {j.get('time_horizon','')}",
        f"**Probability:** {j.get('probability_estimate','')}",
        f"**Status:** {j.get('status','')}",
        "",
        "## 1. 關鍵觸發節點（Top 5）",
    ]
    for i, t in enumerate(j.get("triggers", [])[:5], 1):
        md_lines.append(f"{i}. **{t.get('title','')}** — {t.get('description','')} (狀態: {t.get('current_status','')})")
    md_lines += ["", "## 2. 主要參與者", ", ".join(j.get("key_actors", [])), "", "## 3. 主要後果"]
    for c in j.get("primary_consequences", []):
        md_lines.append(f"- {c}")
    md_lines += ["", "## 4. 監測訊號", j.get("mitigations_and_signals", ["",""])[0], "", "## 5. 緩解策略", j.get("mitigations_and_signals", ["",""])[1], "", "## 6. 數據來源", ", ".join(j.get("data_sources", []))]
    write_file(f"{base}/scenario.md", "\n".join(md_lines))
    # diagram.mmd
    write_file(f"{base}/diagram.mmd", data.get("mmd", ""))

# 精簡但涵蓋 12 個結局的資料（每項保留必要欄位）
SCENARIOS = {
    "nuclear-peace": {
        "json": {
            "id":"scenario-001","title":"Nuclear Peace","branch":"nuclear-peace",
            "summary":"地緣緊張緩解、核風險顯著下降","probability_estimate":"10%","time_horizon":"2026-Q4","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"高階外交密談達成停火框架","description":"主要對立國家達成區域停火秘密協議","current_status":"未發生"},
                {"id":"t2","title":"核持國重啟核查機制","description":"重啟核查與裁軍對話","current_status":"未發生"}
            ],
            "key_actors":["Major Nuclear States","UN/IAEA","OPEC+"],
            "primary_consequences":["地緣政治解凍與經濟復甦","國防開支重審"],
            "mitigations_and_signals":["觀察衛星透明度協議簽署","觀察軍事撤離進度"],
            "data_sources":["2025-12外交政策報告","2026-Q1能源市場數據"]
        },
        "mmd":"flowchart LR\n  T1 --> T2 --> Outcome[Nuclear Peace]"
    },
    "china-grok": {
        "json": {
            "id":"scenario-002","title":"China-Grok","branch":"china-grok",
            "summary":"中國成為領先商用AGI國家","probability_estimate":"25%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"國產模型超越國際基準","description":"國內模型性能提升","current_status":"進行中"},
                {"id":"t3","title":"政府驅動國產替代","description":"政府採購推動國產化","current_status":"已實現"}
            ],
            "key_actors":["Chinese Government","Alibaba/Tencent/Baidu"],
            "primary_consequences":["AI技術標準二元化","供應鏈分裂"],
            "mitigations_and_signals":["觀察算力基建項目進度"],
            "data_sources":["DeepSeek V3報告 2025-Q4"]
        },
        "mmd":"flowchart LR\n  T1 --> T3 --> Outcome[China-Grok]"
    },
    "asi-singularity": {
        "json": {
            "id":"scenario-003","title":"Asia-Singularity","branch":"asi-singularity",
            "summary":"亞洲多國合力成為全球AI新中心","probability_estimate":"15%","time_horizon":"2026-Q4","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"跨國科研聯盟突破","description":"日韓等國研究突破","current_status":"未發生"}
            ],
            "key_actors":["Japan/Korea/Singapore Governments","Regional Tech Giants"],
            "primary_consequences":["AI領導權轉移亞洲"],
            "mitigations_and_signals":["觀察突破性論文作者國籍"],
            "data_sources":["RCEP AI工作組報告"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Asia-Singularity]"
    },
    "us-clampdown": {
        "json": {
            "id":"scenario-004","title":"US Regulatory Clampdown","branch":"us-clampdown",
            "summary":"美國主導大規模監管與商業限制","probability_estimate":"30%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"國會通過實質法規","description":"通過具懲罰力的聯邦AI法規","current_status":"進行中"}
            ],
            "key_actors":["US Congress/NTIA/NIST","Big Tech Legal"],
            "primary_consequences":["AI創新速度放緩"],
            "mitigations_and_signals":["觀察國會聽證會法案條文"],
            "data_sources":["美國國會AI法案追蹤"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[US Clampdown]"
    },
    "fragmented-internet": {
        "json": {
            "id":"scenario-005","title":"Fragmented Internet","branch":"fragmented-internet",
            "summary":"AI生態地緣化分裂，技術標準碎片化","probability_estimate":"35%","time_horizon":"2026-Q4","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"出口管制與數據主權法加劇","description":"AI硬體出口管制與數據在地化","current_status":"已實現"}
            ],
            "key_actors":["Major Governments","Cloud Providers"],
            "primary_consequences":["全球AI效率降低"],
            "mitigations_and_signals":["觀察區域AI平台API差異"],
            "data_sources":["歐盟數據法案進度"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Fragmented Internet]"
    },
    "corporate-dominion": {
        "json": {
            "id":"scenario-006","title":"Corporate Dominion","branch":"corporate-dominion",
            "summary":"大型科技公司壟斷AI基礎設施","probability_estimate":"40%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"雲與模型整合更深","description":"雲商與模型商深度整合","current_status":"已實現"}
            ],
            "key_actors":["Big Tech","Antitrust Regulators"],
            "primary_consequences":["AI創新集中化"],
            "mitigations_and_signals":["觀察併購活動"],
            "data_sources":["Big Tech Q4財報"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Corporate Dominion]"
    },
    "open-agicommons": {
        "json": {
            "id":"scenario-007","title":"Open-AGI Commons","branch":"open-agicommons",
            "summary":"開源AGI生態成功商用化民主化","probability_estimate":"15%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"可商用開源模型達標","description":"開源模型性能接近閉源","current_status":"進行中"}
            ],
            "key_actors":["Open-Source Foundations","SMEs"],
            "primary_consequences":["市場民主化"],
            "mitigations_and_signals":["觀察GitHub/HF下載量"],
            "data_sources":["Hugging Face社群統計"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Open-AGI Commons]"
    },
    "ai-winter-2": {
        "json": {
            "id":"scenario-008","title":"AI Winter 2.0","branch":"ai-winter-2",
            "summary":"AI投資採用回落市場信心受挫","probability_estimate":"20%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"高預期產品未達標","description":"AGI前身產品表現平平","current_status":"未發生"}
            ],
            "key_actors":["VC Funds","Media"],
            "primary_consequences":["投資泡沫破裂"],
            "mitigations_and_signals":["觀察AI初創裁員數量"],
            "data_sources":["Crunchbase AI投資數據"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[AI Winter 2.0]"
    },
    "accident-cascade": {
        "json": {
            "id":"scenario-009","title":"Accident Cascade","branch":"accident-cascade",
            "summary":"AI觸發重大系統性事故連鎖中斷","probability_estimate":"10%","time_horizon":"2026-Q2","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"自動化系統連鎖失效","description":"AI控制基礎設施錯誤決策","current_status":"未發生"}
            ],
            "key_actors":["Infrastructure Operators","Regulators"],
            "primary_consequences":["經濟活動短暫停擺"],
            "mitigations_and_signals":["觀察基礎設施AI審計報告"],
            "data_sources":["AI事故資料庫"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Accident Cascade]"
    },
    "decentralized-edge": {
        "json": {
            "id":"scenario-010","title":"Decentralized-Edge Uprising","branch":"decentralized-edge",
            "summary":"邊緣去中心化AI普及難以控管","probability_estimate":"10%","time_horizon":"2026-Q4","status":"🟡 進行中",
            "triggers":[
                {"id":"t1","title":"小型高效模型硬體普及","description":"輕量模型與邊緣ASIC普及","current_status":"進行中"}
            ],
            "key_actors":["Hardware Manufacturers","Open-Source AI Developers"],
            "primary_consequences":["監管套利增加"],
            "mitigations_and_signals":["觀察邊緣AI晶片出貨量"],
            "data_sources":["邊緣AI硬體市場報告"]
        },
        "mmd":"flowchart LR\n  T1 --> Outcome[Decentralized Edge]"
    },
    "co-governance": {
        "json": {
            "id":"scenario-011","title":"Stabilized Co-Governance","branch":"co-governance",
            "summary":"國際多方共治體系漸成常態","probability_estimate":"10%","time_horizon":"2026-Q4","status":"🟡 進行中",
            "triggers":[
                {"id":"t4","title":"透明度工具成常態","description":"訓練數據評估結果透明化","current_status":"進行中"}
            ],
            "key_actors":["G7/G20/UN Bodies","Major Tech"],
            "primary_consequences":["AI風險有效管理"],
            "mitigations_and_signals":["觀察透明度工具採用率"],
            "data_sources":["G20 AI工作組報告"]
        },
        "mmd":"flowchart LR\n  T4 --> Outcome[Co-Governance]"
    },
    "ai-geopower": {
        "json": {
            "id":"scenario-012","title":"AI-Enabled Geopolitical Leverage","branch":"ai-geopower",
            "summary":"AI成為新型戰略籌碼地緣優勢","probability_estimate":"30%","time_horizon":"2026-Q3","status":"🟡 進行中",
            "triggers":[
                {"id":"t2","title":"新型出口限制成常態","description":"AI能力視為國安資產限制出口","current_status":"已實現"}
            ],
            "key_actors":["Major Powers","Defense Contractors"],
            "primary_consequences":["科技民族主義升溫"],
            "mitigations_and_signals":["觀察國防AI預算變化"],
            "data_sources":["國防白皮書AI章節"]
        },
        "mmd":"flowchart LR\n  T2 --> Outcome[AI-Geopower]"
    }
}

def main():
    if os.path.exists(REPO):
        shutil.rmtree(REPO)
    print("\n📦 生成場景...")
    for branch, data in SCENARIOS.items():
        gen_scenario(branch, data)

    # README
    readme_lines = [
        "# 2026-Endgames: AI & Geopolitical Scenarios",
        "",
        "12 種可能的未來結局 — 每個分支包含 scenario.json, scenario.md, diagram.mmd",
        "",
        "## Summary table",
        "| 結局 | 機率 | 時間軸 | 狀態 | 分支 |",
        "|---|---:|---|---|---|",
    ]
    for b, d in SCENARIOS.items():
        j = d["json"]
        readme_lines.append(f"| {j['title']} | {j['probability_estimate']} | {j['time_horizon']} | {j['status']} | [`{b}`](branches/{b}) |")
    readme_lines += ["", f"**Maintainer:** @{USER}", "", f"**Last Updated:** 2025-12-10"]
    write_file(f"{REPO}/README.md", "\n".join(readme_lines))

    # branches index
    idx = ["# Branches", ""]
    for b, d in SCENARIOS.items():
        j = d["json"]
        idx += [f"## [{j['title']}]({b})", f"**Summary:** {j['summary']}", f"**Probability:** {j['probability_estimate']} | **Status:** {j['status']}", f"Files: [JSON]({b}/scenario.json) | [MD]({b}/scenario.md) | [Diagram]({b}/diagram.mmd)", ""]
    write_file(f"{REPO}/branches/README.md", "\n".join(idx))

    # scripts/analyze.py (簡單分析)
    analyze_py = \"\"\"#!/usr/bin/env python3
import json, glob
files = glob.glob('branches/*/scenario.json')
data = [json.load(open(f,encoding='utf-8')) for f in files]
total = sum(len(d.get('triggers',[])) for d in data)
realized = sum(1 for d in data for t in d.get('triggers',[]) if '已實現' in t.get('current_status',''))
ongoing = sum(1 for d in data for t in d.get('triggers',[]) if '進行中' in t.get('current_status',''))
print('總觸發節點:', total)
print('已實現:', realized)
print('進行中:', ongoing)
print('\\n機率排序:')
for s in sorted(data, key=lambda x: float(x.get('probability_estimate','0%').strip('%')), reverse=True):
    print(s.get('probability_estimate','?'), '-', s.get('title','?'))
\"\"\"
    write_file(f"{REPO}/scripts/analyze.py", analyze_py, make_executable=True)

    # minimal workflow
    workflow = \"\"\"name: Monthly Update Reminder
on:
  schedule:
    - cron: '0 9 1 * *'
jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run analysis
        run: python3 scripts/analyze.py
\"\"\"
    write_file(f"{REPO}/.github/workflows/monthly-update.yml", workflow)

    # .gitignore & LICENSE
    write_file(f"{REPO}/.gitignore", "__pycache__/\n*.pyc\n.DS_Store\n")
    write_file(f"{REPO}/LICENSE", "MIT License\n\nCopyright (c) 2025 Your Name\n")

    print(f"\n✅ 完成：已生成 ./{REPO}/")
    print("下一步：")
    print(f"  cd {REPO}")
    print("  git init && git add . && git commit -m 'Initial commit: scenarios'")
    print(f"  （若使用 GitHub CLI）gh repo create {REPO} --public --source=. --remote=origin --push")

if __name__ == "__main__":
    main()
