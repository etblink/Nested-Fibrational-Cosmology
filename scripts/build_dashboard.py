#!/usr/bin/env python3
"""
Phase 6 — build a self-contained, read-only, local-first dashboard.
Inlines metadata/*.json into a single dashboard/index.html that opens directly
in a browser (file://) with no server and no network. Read-only by construction:
there is no write path back to any canon or metadata file.
"""
import json, os, datetime, html

def load(p): return json.load(open(p))

def main():
    claims=load("metadata/claims.json")
    edges=load("metadata/edges.json")
    views=load("metadata/views.json")
    census=load("metadata/census.json")
    # stale-label audit + review queue are parsed from the markdown deliverables at a coarse level;
    # for the MVP we surface the machine-visible signals: historical/superseded/review_needed claims.
    payload={
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "claims": claims, "edges": edges, "views": views, "census": census,
    }
    data_js=json.dumps(payload, ensure_ascii=False)
    htmlpage=TEMPLATE.replace("/*__DATA__*/", data_js)
    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/index.html","w") as f: f.write(htmlpage)
    print(f"dashboard/index.html written ({len(htmlpage)} bytes); {len(claims)} claims, {len(edges)} edges")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NFC Canon Dashboard (read-only)</title>
<style>
:root{--bg:#0f1115;--panel:#171a21;--ink:#e6e8ec;--mut:#9aa3af;--line:#262b34;
 --D:#6b7280;--U:#22c55e;--C:#3b82f6;--B:#a855f7;--O:#ef4444;--R:#94a3b8;
 --hist:#b45309;--sup:#9a3412;--rev:#b91c1c;--cur:#166534;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
 font:14px/1.5 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:14px 18px;border-bottom:1px solid var(--line);display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
h1{font-size:16px;margin:0;font-weight:650}.sub{color:var(--mut);font-size:12px}
nav{display:flex;gap:4px;padding:8px 12px;border-bottom:1px solid var(--line);flex-wrap:wrap}
nav button{background:var(--panel);color:var(--ink);border:1px solid var(--line);
 padding:6px 11px;border-radius:7px;cursor:pointer;font-size:13px}
nav button.active{background:#20406b;border-color:#2b5488}
main{padding:16px 18px}.panel{display:none}.panel.active{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:8px 0 18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px}
.card .n{font-size:26px;font-weight:700}.card .l{color:var(--mut);font-size:12px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600;position:sticky;top:0;background:var(--bg);cursor:pointer}
tr:hover td{background:#12151b}
.tag{display:inline-block;min-width:20px;text-align:center;border-radius:5px;padding:1px 6px;font-weight:700;font-size:11px;color:#0b0d10}
.tD{background:var(--D)}.tU{background:var(--U)}.tC{background:var(--C)}.tB{background:var(--B)}.tO{background:var(--O)}.tR{background:var(--R)}
.pill{display:inline-block;border-radius:20px;padding:1px 8px;font-size:11px;font-weight:600}
.p-hist{background:var(--hist);color:#fff}.p-sup{background:var(--sup);color:#fff}
.p-rev{background:var(--rev);color:#fff}.p-cur{background:var(--cur);color:#fff}.p-gen{background:#334155;color:#fff}
input,select{background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:7px 9px;border-radius:7px;font-size:13px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.mut{color:var(--mut)}.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.warn{background:#3f2d0e;border:1px solid #6b4e1a;border-radius:8px;padding:9px 12px;margin:8px 0;color:#f6d78a}
.note{background:#0e2033;border:1px solid #1c3a56;border-radius:8px;padding:9px 12px;margin:8px 0}
a{color:#7dd3fc}.bar{height:10px;border-radius:5px;display:inline-block}
details{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:6px 0}
summary{cursor:pointer}
svg text{fill:var(--ink)}
</style></head><body>
<header>
 <h1>NFC Canon Dashboard</h1>
 <span class="sub">read-only · local-first · generated <span id="gen"></span></span>
 <span class="sub" id="commit"></span>
</header>
<nav id="nav"></nav>
<main id="main"></main>
<script>
const DATA=/*__DATA__*/;
const $=(s,e=document)=>e.querySelector(s), el=(t,a={},...c)=>{const n=document.createElement(t);
 for(const k in a){if(k==='html')n.innerHTML=a[k];else if(k==='class')n.className=a[k];else n.setAttribute(k,a[k]);}
 c.forEach(x=>n.append(x));return n;};
document.getElementById('gen').textContent=new Date(DATA.generated).toLocaleString();
document.getElementById('commit').textContent='census commit '+(DATA.census.census_commit||'?');
const esc=s=>(s==null?'':String(s)).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
const tag=t=>`<span class="tag t${t}">${t}</span>`;
function claimState(c){ // classify for the current/historical/superseded/review legend
 if(c.review_needed) return ['REVIEW','p-rev'];
 if(c.superseded_by) return ['superseded','p-sup'];
 if(c.historical) return ['historical','p-hist'];
 return ['current','p-cur'];
}
const PANELS=[
 ['overview','Branch overview'],['counts','Status counts'],['open','Open obligations'],
 ['frontier','Frontier accountings'],['stale','Stale / review queue'],
 ['explorer','Claim explorer'],['deps','Dependency graph'],['snapshot','Release snapshot'],
 ['reports','Generated reports'],['legend','Legend']];
const nav=document.getElementById('nav'), main=document.getElementById('main');
PANELS.forEach(([id,label],i)=>{
 const b=el('button',{},label); b.onclick=()=>show(id);
 if(i===0)b.classList.add('active'); b.dataset.id=id; nav.append(b);
 main.append(el('div',{class:'panel'+(i===0?' active':''),id:'panel-'+id}));
});
function show(id){document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active',b.dataset.id===id));
 document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('active',p.id==='panel-'+id));}

// ---- Branch overview ----
(function(){const p=$('#panel-overview');
 p.append(el('div',{class:'note',html:'Each branch\'s <b>current posture</b> is the verbatim A1 status proposition (review-approved). Postures are per-branch; there is no single corpus-wide status number.'}));
 const bp=DATA.views.branch_posture_view;
 const byB={}; DATA.claims.forEach(c=>{const b=c.branch;(byB[b]=byB[b]||{D:0,U:0,C:0,B:0,O:0,R:0,total:0});byB[b][c.status_tag]++;byB[b].total++;});
 const t=el('table');t.innerHTML='<thead><tr><th>Branch</th><th>Current posture (A1)</th><th>D</th><th>U</th><th>C</th><th>B</th><th>O</th><th>R</th><th>claims</th></tr></thead>';
 const tb=el('tbody');
 Object.keys(bp).forEach(b=>{const s=byB[b]||{};
  tb.append(el('tr',{html:`<td><b>${b}</b></td><td>${esc(bp[b])}</td>
   <td>${s.D||0}</td><td>${s.U||0}</td><td>${s.C||0}</td><td>${s.B||0}</td>
   <td>${s.O?('<b style=color:#ef4444>'+s.O+'</b>'):0}</td><td>${s.R||0}</td><td>${s.total||0}</td>`}));});
 t.append(tb);p.append(t);
})();

// ---- Status counts ----
(function(){const p=$('#panel-counts');
 const env=DATA.census.environment_census, grep=DATA.census.raw_grep_census;
 p.append(el('div',{class:'warn',html:'<b>F-3 resolved:</b> the stale State-of-Canon table (443/209/685) is superseded. Two authoritative censuses are shown, each answering a different question.'}));
 const g=el('div',{class:'grid'});
 ['D','U','C','B','O','R'].forEach(k=>g.append(el('div',{class:'card',html:`<div class="n">${grep[k]}</div><div class="l">${tag(k)} raw \\status census</div>`})));
 p.append(el('h3',{},'Raw \\status census (review-endorsed F-3 figures)'));p.append(g);
 // bar
 const total=Object.values(grep).reduce((a,b)=>a+b,0);
 const bar=el('div',{});['D','U','C','B','O','R'].forEach(k=>{const w=100*grep[k]/total;
  bar.append(el('span',{class:'bar t'+k,style:`width:${w}%`,title:`${k}: ${grep[k]}`}));});
 p.append(bar);p.append(el('div',{class:'mut',html:`total ${total} status mentions`}));
 p.append(el('h3',{},'Environment-declaration census (claim records)'));
 const g2=el('div',{class:'grid'});
 ['D','U','C','B','O','R'].forEach(k=>g2.append(el('div',{class:'card',html:`<div class="n">${env[k]}</div><div class="l">${tag(k)} declarations</div>`})));
 p.append(g2);
 p.append(el('div',{class:'note',html:'<b>prose-mention delta</b> (raw − declarations) = '+JSON.stringify(DATA.census.prose_mention_delta)+' — inline prose status mentions (GR narrative, NS sub-lemma tags), not standalone declarations.'}));
})();

// ---- Open obligations (syntactic [O]) ----
(function(){const p=$('#panel-open');
 const open=DATA.claims.filter(c=>c.status_tag==='O');
 p.append(el('div',{class:'note',html:`<b>Accounting I — syntactic [O] census: ${open.length}.</b> Only environments literally tagged [O]. Distinct from the 110-label roster and the 4-item reduced frontier.`}));
 const t=el('table');t.innerHTML='<thead><tr><th>Label</th><th>Branch</th><th>Section</th><th>Discharge basis / residual</th></tr></thead>';
 const tb=el('tbody');open.forEach(c=>tb.append(el('tr',{html:`<td class="mono">${esc(c.claim_id)}</td><td>${c.branch}</td><td>${esc(c.source_section)}</td><td>${esc(c.discharge_basis||'')}</td>`})));
 t.append(tb);p.append(t);})();

// ---- Frontier accountings ----
(function(){const p=$('#panel-frontier');
 const acc=DATA.census.frontier_accountings;
 p.append(el('div',{class:'warn',html:'<b>'+esc(acc._warning)+'</b>'}));
 const g=el('div',{class:'grid'});
 g.append(el('div',{class:'card',html:`<div class="n">${acc.I_syntactic_O_census.count}</div><div class="l">I · syntactic [O] census</div>`}));
 g.append(el('div',{class:'card',html:`<div class="n">${acc.II_named_obligation_roster.count}</div><div class="l">II · named ob: roster</div>`}));
 g.append(el('div',{class:'card',html:`<div class="n">${acc.III_reduced_irreducible_frontier.count}</div><div class="l">III · reduced frontier</div>`}));
 g.append(el('div',{class:'card',html:`<div class="n">10</div><div class="l">IV · branch postures</div>`}));
 p.append(g);
 p.append(el('h3',{},'III — Reduced irreducible frontier (deep open mathematics)'));
 const t=el('table');t.innerHTML='<thead><tr><th>Item</th><th>Live labels</th></tr></thead>';const tb=el('tbody');
 acc.III_reduced_irreducible_frontier.items.forEach(it=>tb.append(el('tr',{html:`<td><b>${esc(it.item)}</b></td><td class="mono">${it.labels.map(esc).join(', ')}</td>`})));
 t.append(tb);p.append(t);
 p.append(el('div',{class:'mut',html:'Note: CouplingTransfer is <b>not</b> in this list (review ruling F-6: conditionally discharged, non-blocking).'}));
})();

// ---- Stale / review queue ----
(function(){const p=$('#panel-stale');
 const rev=DATA.claims.filter(c=>c.review_needed);
 const hist=DATA.claims.filter(c=>c.historical||c.superseded_by);
 p.append(el('div',{class:'note',html:`<b>Review queue:</b> ${rev.length} claim(s) flagged review_needed · <b>Historical/superseded:</b> ${hist.length} claim(s). Fuller phrase-level audit in STALE_LABEL_AUDIT.md.`}));
 const mk=(title,arr)=>{p.append(el('h3',{},title));const t=el('table');
  t.innerHTML='<thead><tr><th>Label</th><th>Branch</th><th>State</th><th>Superseded by</th><th>Reviewer note</th></tr></thead>';
  const tb=el('tbody');arr.forEach(c=>{const [lab,cls]=claimState(c);
   tb.append(el('tr',{html:`<td class="mono">${esc(c.claim_id)}</td><td>${c.branch}</td><td><span class="pill ${cls}">${lab}</span></td><td class="mono">${esc(c.superseded_by||'')}</td><td>${esc(c.reviewer_note||'')}</td>`}));});
  t.append(tb);p.append(t);};
 mk('Human-review-required',rev.length?rev:[]);
 if(!rev.length)p.append(el('div',{class:'mut',html:'(no machine-flagged review_needed claims; narrative REVIEW_NEEDED items are tracked in CANON_REWRITE_PLAN.md §queue)'}));
 mk('Historical / superseded claims',hist);
})();

// ---- Claim explorer ----
(function(){const p=$('#panel-explorer');
 const row=el('div',{class:'row'});
 const q=el('input',{placeholder:'search label / section / note…',size:32});
 const fb=el('select'),fs=el('select');
 fb.append(el('option',{value:''},'all branches'));[...new Set(DATA.claims.map(c=>c.branch))].sort().forEach(b=>fb.append(el('option',{value:b},b)));
 fs.append(el('option',{value:''},'all status'));['D','U','C','B','O','R'].forEach(s=>fs.append(el('option',{value:s},s)));
 const cnt=el('span',{class:'mut'});
 row.append(q,fb,fs,cnt);p.append(row);
 const t=el('table');t.innerHTML='<thead><tr><th>Label</th><th>Type</th><th>St</th><th>Branch</th><th>Section</th><th>State</th></tr></thead>';
 const tb=el('tbody');t.append(tb);p.append(t);
 function render(){const qq=q.value.toLowerCase(),bb=fb.value,ss=fs.value;tb.innerHTML='';
  const rows=DATA.claims.filter(c=>(!bb||c.branch===bb)&&(!ss||c.status_tag===ss)&&
   (!qq||(c.claim_id+' '+c.source_section+' '+(c.reviewer_note||'')).toLowerCase().includes(qq)));
  cnt.textContent=rows.length+' claims';
  rows.slice(0,600).forEach(c=>{const[lab,cls]=claimState(c);
   tb.append(el('tr',{html:`<td class="mono">${esc(c.claim_id)}</td><td>${c.claim_type}</td><td>${tag(c.status_tag)}</td><td>${c.branch}</td><td>${esc(c.source_section)}</td><td><span class="pill ${cls}">${lab}</span></td>`}));});
  if(rows.length>600)tb.append(el('tr',{html:`<td colspan=6 class="mut">… ${rows.length-600} more (refine search)</td>`}));}
 q.oninput=render;fb.onchange=render;fs.onchange=render;render();
})();

// ---- Dependency graph (label -> deps, per claim; text adjacency for read-only MVP) ----
(function(){const p=$('#panel-deps');
 p.append(el('div',{class:'note',html:`${DATA.edges.length} proof-citation edges across ${new Set(DATA.edges.map(e=>e.from)).size} proven statements. 0 cycles (validated). Pick a claim to see what it depends on and what depends on it.`}));
 const sel=el('input',{placeholder:'type a label, e.g. prop:YM-status',size:36});p.append(sel);
 const out=el('div',{});p.append(out);
 const fwd={},rev={};DATA.edges.forEach(e=>{(fwd[e.from]=fwd[e.from]||[]).push(e.to);(rev[e.to]=rev[e.to]||[]).push(e.from);});
 sel.oninput=()=>{const k=sel.value.trim();out.innerHTML='';if(!k)return;
  out.append(el('details',{open:''},el('summary',{html:`<b>${esc(k)}</b> depends on (${(fwd[k]||[]).length})`}),
    el('div',{class:'mono',html:(fwd[k]||[]).map(esc).join('<br>')||'—'})));
  out.append(el('details',{open:''},el('summary',{html:`depended on by (${(rev[k]||[]).length})`}),
    el('div',{class:'mono',html:(rev[k]||[]).map(esc).join('<br>')||'—'})));};
})();

// ---- Release snapshot ----
(function(){const p=$('#panel-snapshot');const rs=DATA.views.release_snapshot_view;
 p.append(el('div',{class:'note',html:'This snapshot can be diffed against a future <span class=mono>metadata/census.json</span> to see exactly what changed between releases.'}));
 p.append(el('pre',{class:'mono',html:esc(JSON.stringify(rs,null,2))}));})();

// ---- Generated reports ----
(function(){const p=$('#panel-reports');
 p.append(el('div',{class:'note',html:'Generated artifacts (source of truth = the identically-named .tex). Never hand-edited; regenerated by pdflatex.'}));
 const files=['NFC_Book_I','NFC_Book_II','NFC_Book_III','NFC_Book_IV','NFC_Book_V','NFC_Book_VI','NFC_Book_VII','NFC_BIO_Branch','NFC_CRYST_Branch','NFC_GR_Branch','NFC_LING_Branch','NFC_NS_Branch','NFC_RH_Branch','NFC_SCC_Branch','NFC_SM_Branch','NFC_SPEC_Branch','NFC_YM_Branch'];
 const t=el('table');t.innerHTML='<thead><tr><th>Artifact</th><th>Source of truth</th><th>Kind</th></tr></thead>';const tb=el('tbody');
 files.forEach(f=>tb.append(el('tr',{html:`<td class="mono">${f}.pdf</td><td class="mono">${f}.tex</td><td><span class="pill p-gen">generated</span></td>`})));
 t.append(tb);p.append(t);})();

// ---- Legend ----
(function(){const p=$('#panel-legend');
 p.append(el('div',{html:`
  <p><b>Status tags:</b> ${tag('D')} definition/standing · ${tag('U')} unconditional · ${tag('C')} conditional · ${tag('B')} bridge · ${tag('O')} open · ${tag('R')} remark</p>
  <p><b>Claim state:</b> <span class="pill p-cur">current</span> <span class="pill p-hist">historical/intake</span> <span class="pill p-sup">superseded</span> <span class="pill p-rev">review-required</span> <span class="pill p-gen">generated artifact</span></p>
  <p class="mut">Read-only build. There is no write path from this page to any canon or metadata file. Rebuild after metadata changes with <span class="mono">make dashboard</span>.</p>`}));})();
</script></body></html>"""

if __name__=="__main__": main()
