"""keel-viz — a self-contained interactive requirements tracer (docs/process.md §14).

Reads the authored layers plus the derived build/rtm/rtm.json and emits one
offline, dependency-free HTML into build/viz.html: expandable flowdown columns
(Profiles → Stakeholders → BRD → Scenarios → PRD → Criteria), click-to-radiate
closure with connector wires drawn in the gutters, coverage heat modes, a
BRD×PRD matrix view, search, and a detail panel. Runs for any keel project;
the output is derived (build/ is gitignored), so authored content is untouched.
"""
import json, html, http.server, socketserver, functools, webbrowser
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def build_model(root):
    docs = root / "docs"
    nodes, edges = [], []

    def node(nid, layer, label, text, meta):
        nodes.append({"id": nid, "layer": layer, "label": label,
                      "text": text or "", "meta": meta})

    def edge(a, b, kind="flow"):
        edges.append({"from": a, "to": b, "kind": kind})

    def rows(sub, glob="*.yaml"):
        d = docs / sub
        if not d.exists():
            return
        for f in sorted(d.glob(glob)):
            if f.name.startswith("_") or ".template." in f.name:
                continue
            yield f, (yaml.safe_load(f.read_text()) or {})

    for f, d in rows("profiles"):
        if "alias" not in d:
            continue
        pa = d["alias"]
        node(pa, "profile", pa, (d.get("persona") or {}).get("role", d.get("slug", "")),
             {"kind": d.get("kind"), "rank": d.get("rank"), "status": d.get("status"),
              "env": (d.get("context") or {}).get("environment", "")})
        for s in d.get("stakeholders") or []:
            node(s["alias"], "stakeholder", s["alias"], s.get("role", ""), {"profile": pa})
            edge(pa, s["alias"])

    for f, d in rows("brd"):
        prof = (d.get("meta") or {}).get("profile")
        for r in d.get("requirements") or []:
            node(r["alias"], "brd", r["alias"], r.get("statement", ""),
                 {"profile": prof, "stakeholder": r.get("stakeholder_alias"),
                  "stakeholder_name": r.get("stakeholder_name", ""),
                  "p_buy": r.get("priority_buying"), "p_stk": r.get("priority_stakeholder"),
                  "acceptance": r.get("acceptance", "")})
            if r.get("stakeholder_alias"):
                edge(r["stakeholder_alias"], r["alias"])

    for f in sorted((docs / "scenarios").glob("*.md")) if (docs / "scenarios").exists() else []:
        if ".template." in f.name:
            continue
        parts = f.read_text().split("---")
        if len(parts) < 3:
            continue
        fm = yaml.safe_load(parts[1]) or {}
        if "alias" not in fm:
            continue
        node(fm["alias"], "scenario", fm["alias"], fm.get("slug", ""),
             {"mode": fm.get("mode"), "stakeholder": fm.get("stakeholder_alias")})
        if fm.get("stakeholder_alias"):
            edge(fm["stakeholder_alias"], fm["alias"], "actor")

    sections = {}
    for f, d in rows("prd"):
        sec = d.get("section")
        for r in d.get("requirements") or []:
            sections[r["alias"]] = sec
            node(r["alias"], "prd", r["alias"], r.get("text", ""),
                 {"type": r.get("type"), "witness": r.get("witness"),
                  "priority_po": r.get("priority_po"), "section": sec})

    for l in ((yaml.safe_load((docs / "trace/links.yaml").read_text()) or {}).get("links") or []) \
            if (docs / "trace/links.yaml").exists() else []:
        src = (l.get("from") or "").partition("@")[0]
        rel = l.get("relation", "satisfies")
        for tgt in l.get("spec") or []:
            t = tgt.partition("@")[0]
            if t.startswith("section:"):
                for a, s in sections.items():
                    if s == t.split(":", 1)[1]:
                        edge(src, a, rel)
            else:
                edge(src, t, rel)

    for f, d in rows("criteria"):
        for r in d.get("criteria") or []:
            ref = (r.get("refines") or "").partition("@")[0]
            node(r["alias"], "criterion", r["alias"], r.get("text", ""),
                 {"witness": r.get("witness"), "refines": ref, "section": d.get("section")})
            if ref:
                edge(ref, r["alias"], "refines")

    status = {}
    rj = root / "build/rtm/rtm.json"
    if rj.exists():
        try:
            g = json.loads(rj.read_text())
            for a, row in {**(g.get("prd") or {}), **(g.get("criteria") or {})}.items():
                status[a] = "witnessed" if row.get("tests") else "unwitnessed"
        except Exception:
            pass

    return {"nodes": nodes, "edges": edges, "status": status, "project": root.resolve().name}


def render(data):
    return _TEMPLATE.replace("__PAYLOAD__", json.dumps(data)) \
                    .replace("__PROJECT__", html.escape(data["project"]))


def write(root):
    if yaml is None:
        raise SystemExit("req viz: pyyaml required")
    out = root / "build" / "viz.html"
    out.parent.mkdir(exist_ok=True)
    data = build_model(root)
    out.write_text(render(data))
    return out, len(data["nodes"]), len(data["edges"])


def serve(root, port=8777, open_browser=True):
    out, n, e = write(root)
    directory = str((root / "build").resolve())
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    url = f"http://localhost:{port}/viz.html"
    print(f"viz: {n} nodes · {e} edges · serving {url}  (Ctrl-C to stop)")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nviz: stopped")


_TEMPLATE = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<title>keel-viz — __PROJECT__</title>
<style>
:root{--ink:#22303c;--navy:#184a7b;--steel:#2f6b8f;--slate:#5b6770;--muted:#8a97a0;
--line:#d7dee4;--surf:#fcfcfb;--page:#eef1f4;--good:#2f8f4e;--amber:#e6a817;--red:#c43d3d;--dim:.1}
*{box-sizing:border-box}html,body{margin:0;height:100%;font:13px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--page)}
header{display:flex;align-items:center;gap:12px;padding:8px 14px;background:var(--navy);color:#fff;position:sticky;top:0;z-index:30}
header b{font-size:15px;letter-spacing:.3px}header .sp{flex:1}header .hint{font-size:11px;opacity:.82}
header input{padding:5px 9px;border:0;border-radius:5px;width:220px;font:12px system-ui}
header select,header button{padding:5px 9px;border:0;border-radius:5px;background:#2f6b8f;color:#fff;font:12px system-ui;cursor:pointer}
header button.on{background:#0e6b57}
#scroller{position:relative;height:calc(100% - 42px);overflow:auto}
#inner{position:relative;display:flex;gap:62px;min-width:max-content;padding:14px 24px 60px}
svg#wires{position:absolute;inset:0;pointer-events:none;z-index:4;overflow:visible}
.col{width:216px;flex:0 0 216px;display:flex;flex-direction:column}
.col h2{margin:0 0 6px;padding:6px 9px;font-size:11px;letter-spacing:.5px;text-transform:uppercase;color:#fff;border-radius:5px;position:sticky;top:0;z-index:6}
.col.profile h2{background:#184a7b}.col.stakeholder h2{background:#2f6b8f}.col.brd h2{background:#3a6fb0}
.col.scenario h2{background:#6b4fb3}.col.prd h2{background:#1f7a5a}.col.criterion h2{background:#0e6b57}
.card{background:var(--surf);border:1px solid var(--line);border-left:3px solid var(--muted);border-radius:5px;
padding:6px 8px;margin-bottom:6px;cursor:pointer;position:relative;z-index:5;transition:opacity .12s,box-shadow .1s}
.card .a{font:600 11px ui-monospace,Menlo,monospace;color:var(--navy)}
.card .t{font-size:11px;color:var(--slate);margin-top:2px;max-height:2.7em;overflow:hidden}
.card .chip{position:absolute;top:6px;right:6px;font:600 9px ui-monospace;padding:0 4px;border-radius:3px;color:#fff}
.card.dim{opacity:var(--dim)}.card.sel{box-shadow:0 0 0 2px var(--navy)}
.card.up{border-left-color:var(--amber)}.card.down{border-left-color:var(--good)}
.card.hl{outline:2px solid var(--amber);outline-offset:1px}
#panel{position:fixed;right:0;top:42px;width:340px;height:calc(100% - 42px);background:#fff;border-left:1px solid var(--line);
box-shadow:-4px 0 14px rgba(0,0,0,.07);transform:translateX(100%);transition:transform .16s;z-index:25;overflow-y:auto;padding:14px}
#panel.open{transform:translateX(0)}
#panel h3{margin:0 0 2px;font:600 13px ui-monospace;color:var(--navy)}
#panel .lay{font-size:10px;letter-spacing:.5px;text-transform:uppercase;color:var(--muted)}
#panel p{font-size:12px;margin:8px 0}
#panel .sec{font:600 10px system-ui;letter-spacing:.5px;text-transform:uppercase;color:var(--slate);margin:12px 0 3px;border-bottom:1px solid var(--line);padding-bottom:2px}
#panel .rel{font:11px ui-monospace;color:var(--steel);cursor:pointer;display:block;padding:1px 0}
#panel .rel:hover{text-decoration:underline}#panel .x{position:absolute;right:10px;top:8px;cursor:pointer;color:var(--muted);font-size:17px}
#legend{position:fixed;left:12px;bottom:12px;background:#fff;border:1px solid var(--line);border-radius:6px;padding:7px 9px;font-size:10px;z-index:20;box-shadow:0 2px 8px rgba(0,0,0,.07)}
#legend .r{display:flex;align-items:center;gap:5px;margin:2px 0}#legend i{width:10px;height:10px;border-radius:2px;display:inline-block}
#matrix{display:none;padding:16px 24px}#matrix.show{display:block}#scroller.matrix #inner{display:none}
#matrix table{border-collapse:collapse}#matrix th{font:600 9px ui-monospace;color:var(--slate);padding:2px}
#matrix th.rot{writing-mode:vertical-rl;transform:rotate(180deg);height:120px;vertical-align:bottom}
#matrix td{width:15px;height:15px;border:1px solid #eef1f4;border-radius:3px}#matrix td.rl{width:auto;border:0;font:11px ui-monospace;padding-right:6px;text-align:right;white-space:nowrap}
</style></head><body>
<header>
  <b>keel-viz</b><span class=hint>__PROJECT__ · click a node → radiate ▲ up (who it serves) / ▼ down (what it drives)</span>
  <span class=sp></span>
  <input id=q placeholder="search alias / text…">
  <select id=heat><option value=layer>colour: layer</option><option value=priority>colour: priority</option><option value=witness>colour: witness</option><option value=gap>colour: gaps</option></select>
  <button id=mtoggle>matrix</button><button id=reset>clear</button>
</header>
<div id=scroller>
  <div id=inner><svg id=wires></svg></div>
  <div id=matrix></div>
</div>
<div id=panel><span class=x onclick="closePanel()">×</span><div id=pbody></div></div>
<div id=legend></div>
<script>
const DATA=__PAYLOAD__;
const LAYERS=[["profile","Profiles"],["stakeholder","Stakeholders"],["brd","Business req"],
              ["scenario","Scenarios"],["prd","PRD"],["criterion","Criteria"]];
const LC={profile:'#184a7b',stakeholder:'#2f6b8f',brd:'#3a6fb0',scenario:'#6b4fb3',prd:'#1f7a5a',criterion:'#0e6b57'};
const PRI=["#6f2c0c","#9c3f14","#c9531f","#eb6834","#ef9c68"];
const byId={};DATA.nodes.forEach(n=>byId[n.id]=n);
const out={},inc={};DATA.nodes.forEach(n=>{out[n.id]=[];inc[n.id]=[]});
DATA.edges.forEach(e=>{if(out[e.from]&&inc[e.to]){out[e.from].push(e);inc[e.to].push(e);}});
const inner=document.getElementById('inner'),wires=document.getElementById('wires'),scroller=document.getElementById('scroller');
const cardEl={};let selected=null;
function esc(s){return (s||'').replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]))}
LAYERS.forEach(([L,title])=>{
  const list=DATA.nodes.filter(n=>n.layer===L);
  if(!list.length && (L==='criterion'||L==='scenario') ) return;
  const col=document.createElement('div');col.className='col '+L;
  col.innerHTML='<h2>'+title+' · '+list.length+'</h2>';
  list.sort((a,b)=>(a.meta.rank||a.meta.p_buy||a.meta.priority_po||9)-(b.meta.rank||b.meta.p_buy||b.meta.priority_po||9));
  list.forEach(n=>{const c=document.createElement('div');c.className='card';c.dataset.id=n.id;
    c.innerHTML='<div class=a>'+n.id+'</div><div class=t>'+esc(n.text.slice(0,130))+'</div>';
    c.onclick=()=>select(n.id);col.appendChild(c);cardEl[n.id]=c;});
  inner.appendChild(col);
});
function closure(id,dir){const seen=new Set(),st=[id];
  while(st.length){const x=st.pop();(dir==='up'?inc[x]:out[x]).forEach(e=>{const nx=dir==='up'?e.from:e.to;
    if(!seen.has(nx)){seen.add(nx);st.push(nx);}});}return seen;}
function select(id){selected=id;location.hash=id;
  const up=closure(id,'up'),down=closure(id,'down');
  DATA.nodes.forEach(n=>{const c=cardEl[n.id];if(!c)return;c.classList.remove('dim','sel','up','down');
    if(n.id===id)c.classList.add('sel');else if(up.has(n.id))c.classList.add('up');
    else if(down.has(n.id))c.classList.add('down');else c.classList.add('dim');});
  drawWires(id,up,down);showPanel(id,up,down);}
function anchor(el,side){const r=el.getBoundingClientRect(),ir=inner.getBoundingClientRect();
  return {x:(side==='r'?r.right:r.left)-ir.left,y:r.top+r.height/2-ir.top};}
function drawWires(id,up,down){
  wires.setAttribute('width',inner.scrollWidth);wires.setAttribute('height',inner.scrollHeight);
  const set=new Set([id,...up,...down]);let paths='';
  paths='<defs><marker id=ah viewBox="0 0 8 8" refX=7 refY=4 markerWidth=6 markerHeight=6 orient=auto>'+
        '<path d="M0,0 L8,4 L0,8 z" fill="#8a97a0"/></marker></defs>';
  DATA.edges.forEach(e=>{if(!set.has(e.from)||!set.has(e.to))return;
    const A=cardEl[e.from],B=cardEl[e.to];if(!A||!B)return;
    const a=anchor(A,'r'),b=anchor(B,'l');if(b.x<a.x-4)return;
    const col=(up.has(e.from)&&(up.has(e.to)||e.to===id))?'#e6a817':'#2f8f4e';
    const mx=(a.x+b.x)/2;
    paths+=`<path d="M${a.x},${a.y} C${mx},${a.y} ${mx},${b.y} ${b.x-6},${b.y}" fill=none stroke="${col}" stroke-width=1.4 opacity=.75 marker-end="url(#ah)"/>`;});
  wires.innerHTML=paths;}
function showPanel(id,up,down){const n=byId[id],m=n.meta,pb=document.getElementById('pbody');
  let h='<h3>'+id+'</h3><div class=lay>'+n.layer+(m.section?' · '+m.section:'')+(m.mode?' · '+m.mode:'')+'</div><p>'+esc(n.text)+'</p>';
  const f=[];if(m.status)f.push('status: '+m.status);if(m.rank!=null)f.push('rank '+m.rank);
  if(m.priority_po!=null)f.push('P_po '+m.priority_po);if(m.p_buy!=null)f.push('P_buy '+m.p_buy);
  if(m.witness)f.push('witness: '+m.witness);if(m.type)f.push(m.type);if(m.stakeholder_name)f.push(m.stakeholder_name);
  const wv=DATA.status[id];if(wv)f.push('coverage: '+wv);
  if(m.acceptance)h+='<div class=sec>acceptance</div><p style="font-size:11px">'+esc(m.acceptance)+'</p>';
  if(f.length)h+='<div class=sec>facts</div><p style="font:11px ui-monospace">'+f.map(esc).join(' · ')+'</p>';
  const U=[...up].filter(x=>byId[x]).sort(),D=[...down].filter(x=>byId[x]).sort();
  if(U.length){h+='<div class=sec>▲ serves / drives value for ('+U.length+')</div>';U.forEach(x=>h+='<span class=rel onclick="select(\''+x+'\')">'+x+' · '+byId[x].layer+'</span>');}
  if(D.length){h+='<div class=sec>▼ radiates down to ('+D.length+')</div>';D.forEach(x=>h+='<span class=rel onclick="select(\''+x+'\')">'+x+' · '+byId[x].layer+'</span>');}
  pb.innerHTML=h;document.getElementById('panel').classList.add('open');}
function closePanel(){document.getElementById('panel').classList.remove('open');}
function heatColor(n,mode){
  if(mode==='priority'){const p=n.meta.priority_po||n.meta.p_buy;return p?PRI[p-1]:'#c3c2b7';}
  if(mode==='witness'){if(n.layer==='prd'||n.layer==='criterion'){const s=DATA.status[n.id]||n.meta.witness;
    return s==='witnessed'?'#2f8f4e':(s==='none'?'#8a97a0':'#c43d3d');}return '#c3c2b7';}
  if(mode==='gap'){const orphanUp=(inc[n.id]||[]).length===0&&n.layer!=='profile';
    const orphanDown=(out[n.id]||[]).length===0&&n.layer!=='prd'&&n.layer!=='criterion';
    return (orphanUp||orphanDown)?'#c43d3d':'#2f8f4e';}
  return LC[n.layer];}
function applyHeat(){const mode=document.getElementById('heat').value;
  DATA.nodes.forEach(n=>{const c=cardEl[n.id];if(!c)return;const col=heatColor(n,mode);
    if(!c.classList.contains('sel'))c.style.borderLeftColor=col;
    let chip=c.querySelector('.chip');
    if(mode==='priority'){const p=n.meta.priority_po||n.meta.p_buy;setChip(c,p?'P'+p:'',col);}
    else if(mode==='witness'&&(n.layer==='prd'||n.layer==='criterion')){setChip(c,(DATA.status[n.id]||n.meta.witness||'—').slice(0,4),col);}
    else setChip(c,'',col);});
  buildLegend(mode);if(selected)select(selected);}
function setChip(c,txt,col){let chip=c.querySelector('.chip');if(!txt){if(chip)chip.remove();return;}
  if(!chip){chip=document.createElement('span');chip.className='chip';c.appendChild(chip);}chip.textContent=txt;chip.style.background=col;}
function buildLegend(mode){const L=document.getElementById('legend');let h='';
  if(mode==='priority')h='<div class=r><i style="background:#6f2c0c"></i>P1 highest</div><div class=r><i style="background:#ef9c68"></i>P5 lowest</div>';
  else if(mode==='witness')h='<div class=r><i style="background:#2f8f4e"></i>witnessed</div><div class=r><i style="background:#c43d3d"></i>unwitnessed</div><div class=r><i style="background:#8a97a0"></i>n/a</div>';
  else if(mode==='gap')h='<div class=r><i style="background:#2f8f4e"></i>connected</div><div class=r><i style="background:#c43d3d"></i>orphan / uncovered</div>';
  else h=LAYERS.filter(([l])=>DATA.nodes.some(n=>n.layer===l)).map(([l,t])=>'<div class=r><i style="background:'+LC[l]+'"></i>'+t+'</div>').join('');
  h+='<div class=r style="margin-top:4px"><i style="background:#e6a817"></i>▲ up wire</div><div class=r><i style="background:#2f8f4e"></i>▼ down wire</div>';
  L.innerHTML=h;}
// matrix view: BRD rows × PRD cols
function buildMatrix(){const brd=DATA.nodes.filter(n=>n.layer==='brd'),prd=DATA.nodes.filter(n=>n.layer==='prd');
  const rel={};DATA.edges.forEach(e=>{if(byId[e.from]&&byId[e.from].layer==='brd'&&byId[e.to]&&byId[e.to].layer==='prd')rel[e.from+'|'+e.to]=e.kind;});
  const RC={satisfies:'#1c5cab',partial:'#3987e5',informs:'#86b6ef',conflicts:'#c43d3d'};
  let h='<table><tr><th></th>'+prd.map(p=>'<th class=rot>'+p.id+'</th>').join('')+'</tr>';
  brd.forEach(b=>{h+='<tr><td class=rl title="'+esc(b.text)+'">'+b.id+'</td>'+
    prd.map(p=>{const r=rel[b.id+'|'+p.id];return '<td style="background:'+(r?RC[r]||'#999':'#f4f6f8')+'" title="'+b.id+'→'+p.id+(r?' '+r:'')+'"></td>';}).join('')+'</tr>';});
  h+='</table>';document.getElementById('matrix').innerHTML=h;}
document.getElementById('mtoggle').onclick=e=>{const on=scroller.classList.toggle('matrix');
  document.getElementById('matrix').classList.toggle('show',on);e.target.classList.toggle('on',on);
  if(on){buildMatrix();closePanel();}};
document.getElementById('reset').onclick=()=>{selected=null;wires.innerHTML='';closePanel();location.hash='';
  DATA.nodes.forEach(n=>{const c=cardEl[n.id];if(c)c.classList.remove('dim','sel','up','down');});applyHeat();};
document.getElementById('q').oninput=e=>{const v=e.target.value.toLowerCase();
  DATA.nodes.forEach(n=>{const c=cardEl[n.id];if(!c)return;c.classList.toggle('hl',!!v&&(n.id.includes(v)||n.text.toLowerCase().includes(v)));});};
document.getElementById('heat').onchange=applyHeat;
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('reset').click();});
scroller.addEventListener('scroll',()=>{if(selected)drawWires(selected,closure(selected,'up'),closure(selected,'down'));});
window.addEventListener('resize',()=>{if(selected)select(selected);});
applyHeat();
if(location.hash&&byId[location.hash.slice(1)])select(location.hash.slice(1));
</script></body></html>"""
