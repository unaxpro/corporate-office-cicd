import os
import sys

# Make the sibling module importable no matter where VS Code / the terminal runs from
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template_string, request  # noqa: E402
from corporate_network import CorporateNetwork, DEPARTMENTS, SERVERS  # noqa: E402

app = Flask(__name__)
network = CorporateNetwork()

PAGE = r"""
<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Coreline | Corporate Network Operations - CI/CD Updated</title>
<script>try{var t=localStorage.getItem('cl-theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.dataset.theme=t}catch(e){}</script>
<style>
:root{
  --bg:#f5f3ee;--surface:#ffffff;--surface2:#faf8f4;--ink:#13211f;--muted:#5d6e6a;--line:#e5e1d8;
  --primary:#0a8f7b;--primary-ink:#ffffff;--primary-soft:#dcf3ee;--primary-deep:#066b5c;
  --accent:#ff6b4a;--accent-soft:#ffe9e3;
  --ok:#13875f;--ok-soft:#dff4ea;--warn:#b86e00;--warn-soft:#fff1d6;--bad:#cc3340;--bad-soft:#fde8ea;
  --hero1:#0b3b36;--hero2:#0a8f7b;--shadow:0 1px 2px rgba(19,33,31,.05),0 10px 30px rgba(19,33,31,.06);
  --radius:18px;
}
[data-theme=dark]{
  --bg:#0c1413;--surface:#142120;--surface2:#101c1b;--ink:#e8f2ef;--muted:#8da39e;--line:#223533;
  --primary:#2bd1b4;--primary-ink:#04201b;--primary-soft:#12342f;--primary-deep:#7ce8d3;
  --accent:#ff8467;--accent-soft:#3a1f19;
  --ok:#4fd49c;--ok-soft:#10301f;--warn:#f0b24a;--warn-soft:#352711;--bad:#ff7b87;--bad-soft:#3a1a1e;
  --hero1:#0a2724;--hero2:#0f5f54;--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.25);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}
button{cursor:pointer}
a{color:inherit}
:focus-visible{outline:3px solid var(--primary);outline-offset:2px;border-radius:8px}
svg.i{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}

/* header */
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.top-in{display:flex;align-items:center;gap:20px;height:68px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px;letter-spacing:-.02em;text-decoration:none}
.logo-mark{width:34px;height:34px;border-radius:11px;background:linear-gradient(135deg,var(--primary),var(--accent));display:grid;place-items:center;color:#fff}
.logo-mark svg{width:19px;height:19px}
nav.main{display:flex;gap:4px;margin-left:12px}
nav.main a{padding:8px 14px;border-radius:99px;text-decoration:none;color:var(--muted);font-weight:600;font-size:14px;transition:.15s}
nav.main a:hover{color:var(--ink);background:var(--surface)}
nav.main a.active{background:var(--primary-soft);color:var(--primary-deep)}
.spacer{flex:1}
.chip-status{display:flex;align-items:center;gap:8px;padding:7px 13px;border-radius:99px;background:var(--surface);border:1px solid var(--line);font-size:13px;font-weight:600}
.pulse{width:9px;height:9px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 0 var(--ok);animation:pulse 2s infinite}
.pulse.warn{background:var(--warn);box-shadow:0 0 0 0 var(--warn)}
@keyframes pulse{70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}
.icon-btn{width:40px;height:40px;border-radius:12px;border:1px solid var(--line);background:var(--surface);display:grid;place-items:center}
.icon-btn:hover{border-color:var(--primary)}
[data-theme=dark] .sun{display:block}[data-theme=dark] .moon{display:none}
.sun{display:none}

/* hero */
.hero{margin:26px 0 22px;border-radius:26px;padding:38px 40px;color:#fff;background:radial-gradient(circle at 90% 10%,rgba(255,107,74,.35),transparent 40%),linear-gradient(135deg,var(--hero1),var(--hero2));position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.12) 1px,transparent 1px);background-size:22px 22px;mask-image:linear-gradient(90deg,transparent 30%,#000);pointer-events:none}
.hero>*{position:relative;z-index:1}
.hero .tag{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.2);padding:5px 12px;border-radius:99px;font-size:12px;font-weight:700;letter-spacing:.04em}
.hero h1{font-size:clamp(28px,4vw,42px);line-height:1.1;letter-spacing:-.03em;margin:16px 0 10px;max-width:640px}
.hero p{margin:0;max-width:560px;color:rgba(255,255,255,.82);font-size:16px}
.hero-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:11px 18px;border-radius:12px;border:1px solid var(--line);background:var(--surface);font-weight:700;font-size:14px;text-decoration:none;transition:.15s}
.btn:hover{transform:translateY(-1px);box-shadow:var(--shadow)}
.btn-primary{background:var(--primary);color:var(--primary-ink);border-color:var(--primary)}
.btn-accent{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn-ghost{background:rgba(255,255,255,.12);color:#fff;border-color:rgba(255,255,255,.3)}
.btn-sm{padding:8px 13px;font-size:13px;border-radius:10px}

/* notice */
.notice{display:flex;gap:12px;align-items:flex-start;background:var(--warn-soft);color:var(--warn);border-radius:14px;padding:13px 16px;font-size:14px;margin-bottom:22px}
.notice span{color:var(--ink);opacity:.85}
.notice button{margin-left:auto;background:none;border:0;opacity:.6;padding:2px}
.notice button:hover{opacity:1}

/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:34px}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow)}
.stat-top{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:13px;font-weight:600}
.stat-ico{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;background:var(--primary-soft);color:var(--primary-deep)}
.stat:nth-child(2) .stat-ico{background:var(--accent-soft);color:var(--accent)}
.stat:nth-child(3) .stat-ico{background:var(--ok-soft);color:var(--ok)}
.stat:nth-child(4) .stat-ico{background:var(--warn-soft);color:var(--warn)}
.stat-val{font-size:32px;font-weight:800;letter-spacing:-.03em;margin:12px 0 2px;line-height:1.1}
.stat-foot{font-size:13px;color:var(--muted)}

/* sections */
section.block{margin-bottom:38px}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:16px;flex-wrap:wrap}
.sec-head h2{margin:0;font-size:24px;letter-spacing:-.025em}
.sec-head p{margin:4px 0 0;color:var(--muted);max-width:560px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.pad{padding:24px}
.pill{display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:99px;font-size:12px;font-weight:700;white-space:nowrap}
.pill.ok{background:var(--ok-soft);color:var(--ok)}.pill.bad{background:var(--bad-soft);color:var(--bad)}.pill.warn{background:var(--warn-soft);color:var(--warn)}.pill.info{background:var(--primary-soft);color:var(--primary-deep)}

/* topology */
.topo{padding:28px 24px}
.tier-label{text-align:center;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.tier{display:grid;gap:14px}
.tier.four{grid-template-columns:repeat(4,1fr)}
.tier.core{grid-template-columns:minmax(0,260px) 60px minmax(0,260px);justify-content:center;align-items:center}
.wire{height:3px;border-radius:3px;background:repeating-linear-gradient(90deg,var(--primary) 0 8px,transparent 8px 14px);opacity:.7}
.vwire{display:flex;flex-direction:column;align-items:center;margin:8px 0 14px;color:var(--muted);font-size:12px;font-weight:600;gap:6px}
.vwire:before,.vwire:after{content:"";width:3px;height:16px;border-radius:3px;background:repeating-linear-gradient(180deg,var(--primary) 0 6px,transparent 6px 10px);opacity:.7}
.node{background:var(--surface2);border:1px solid var(--line);border-radius:16px;padding:16px;text-align:left;display:flex;flex-direction:column;gap:6px;transition:.18s;width:100%}
button.node:hover{border-color:var(--primary);transform:translateY(-3px);box-shadow:var(--shadow)}
.node-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.node-ico{width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:var(--primary-soft);color:var(--primary-deep)}
.node strong{font-size:15px}
.node small{color:var(--muted);font-size:13px}
.node .meta{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.node .hint{font-size:12px;font-weight:700;color:var(--primary-deep);opacity:0;transition:.15s;margin-top:2px}
button.node:hover .hint{opacity:1}
.dept-bar{height:5px;border-radius:5px;background:var(--c);margin-bottom:4px}
.core .node{align-items:center;text-align:center}
.dept-card{cursor:default}
.dept-card .count{color:var(--muted);font-size:13px}
.pcs{list-style:none;margin:10px 0 6px;padding:0;display:grid;gap:6px;max-height:268px;overflow:auto}
.pcs li{display:flex;gap:5px;align-items:stretch}
.pc-main{flex:1;min-width:0;text-align:left;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:7px 10px;display:flex;flex-direction:column;gap:0;transition:.15s}
.pc-main:hover{border-color:var(--primary)}
.pc-name{font-weight:700;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pc-ip{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--muted)}
.pc-ip.has{color:var(--ok)}
.pc-btn{min-width:36px;border-radius:10px;border:1px solid var(--line);background:var(--surface);display:grid;place-items:center;color:var(--muted);padding:0 6px;font-size:12px;font-weight:700}
.pc-btn:hover{border-color:var(--primary);color:var(--primary-deep)}
.pc-btn.del:hover{border-color:var(--bad);color:var(--bad)}
.pc-btn.del.armed{background:var(--bad);border-color:var(--bad);color:#fff;padding:0 10px}
.add-pc{margin-top:6px;width:100%;border-style:dashed;color:var(--primary-deep);background:transparent}
.sec-actions{display:flex;gap:8px;flex-wrap:wrap}
dialog{border:1px solid var(--line);border-radius:22px;padding:0;background:var(--surface);color:var(--ink);width:min(440px,calc(100vw - 32px));box-shadow:0 30px 80px rgba(0,0,0,.35)}
dialog::backdrop{background:rgba(8,20,18,.55);backdrop-filter:blur(3px)}
.dlg{padding:26px}
.dlg h3{margin:0 0 4px;font-size:20px;letter-spacing:-.02em}
.dlg>p{margin:0 0 20px;color:var(--muted);font-size:14px}
.dlg-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.qty{display:flex;gap:6px;margin:-6px 0 16px;flex-wrap:wrap}
.qty button{border:1px solid var(--line);background:var(--surface2);border-radius:99px;padding:5px 13px;font-weight:700;font-size:13px}
.qty button.on{background:var(--primary-soft);border-color:var(--primary);color:var(--primary-deep)}
.err{background:var(--bad-soft);color:var(--bad);border-radius:10px;padding:9px 12px;font-size:13px;font-weight:600;margin-bottom:14px}
.dlg-foot{display:flex;gap:10px;justify-content:flex-end;margin-top:6px}
.hint-t{font-size:12px;color:var(--muted);margin-top:-8px;margin-bottom:16px}

/* diagnostics */
.diag{display:grid;grid-template-columns:1.1fr 1fr;gap:0;overflow:hidden}
.diag-form{padding:26px;border-right:1px solid var(--line)}
.seg{display:flex;background:var(--surface2);border:1px solid var(--line);border-radius:14px;padding:4px;gap:4px;margin-bottom:22px}
.seg button{flex:1;border:0;background:none;padding:10px 8px;border-radius:10px;font-weight:700;font-size:14px;color:var(--muted);display:flex;gap:7px;align-items:center;justify-content:center}
.seg button.active{background:var(--surface);color:var(--primary-deep);box-shadow:0 1px 4px rgba(0,0,0,.1)}
.field{display:grid;gap:6px;margin-bottom:16px}
.field label{font-size:13px;font-weight:700}
.field select,.field input{width:100%;padding:12px 14px;border-radius:12px;border:1.5px solid var(--line);background:var(--surface);appearance:none;-webkit-appearance:none}
.field select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' fill='none' stroke='%238da39e' stroke-width='2'%3E%3Cpath d='m1 1 5 5 5-5'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:38px}
.field select:focus,.field input:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 4px var(--primary-soft)}
.presets{margin-top:20px}
.presets p{margin:0 0 8px;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.preset-row{display:flex;flex-wrap:wrap;gap:8px}
.preset{border:1px dashed var(--line);background:none;border-radius:99px;padding:6px 12px;font-size:13px;font-weight:600;color:var(--muted)}
.preset:hover{border-color:var(--primary);color:var(--primary-deep);border-style:solid}
.diag-out{padding:26px;background:var(--surface2);display:flex;flex-direction:column;min-height:340px}
.empty{margin:auto;text-align:center;color:var(--muted);max-width:260px}
.empty .ring{width:64px;height:64px;border-radius:50%;background:var(--surface);border:1px solid var(--line);display:grid;place-items:center;margin:0 auto 14px}
.result{animation:pop .25s ease}
@keyframes pop{from{opacity:0;transform:translateY(8px)}}
.res-head{display:flex;gap:14px;align-items:center;margin-bottom:18px}
.res-ico{width:48px;height:48px;border-radius:15px;display:grid;place-items:center}
.res-ico svg{width:26px;height:26px;stroke-width:2.4}
.res-ico.ok{background:var(--ok-soft);color:var(--ok)}.res-ico.bad{background:var(--bad-soft);color:var(--bad)}
.res-head h3{margin:0;font-size:19px;letter-spacing:-.02em}
.res-head p{margin:2px 0 0;color:var(--muted);font-size:14px}
.kv{display:grid;gap:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.kv div{display:flex;justify-content:space-between;gap:16px;padding:11px 15px;border-bottom:1px solid var(--line);font-size:14px}
.kv div:last-child{border:0}
.kv dt,.kv span:first-child{color:var(--muted)}
.kv b{font-weight:600;text-align:right;overflow-wrap:anywhere}
.steps{display:flex;gap:6px;flex-wrap:wrap;margin-top:14px}
.step{display:flex;align-items:center;gap:6px;font-size:12px;font-weight:700;background:var(--primary-soft);color:var(--primary-deep);padding:5px 11px;border-radius:99px}

/* lab + activity */
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.fault{display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid var(--line)}
.fault:first-child{padding-top:0}
.fault:last-of-type{border:0}
.fault-ico{width:42px;height:42px;border-radius:13px;background:var(--surface2);border:1px solid var(--line);display:grid;place-items:center;color:var(--muted);transition:.2s}
.fault.on .fault-ico{background:var(--bad-soft);color:var(--bad);border-color:transparent}
.fault-t{flex:1;min-width:0}
.fault-t strong{display:block;font-size:15px}.fault-t small{color:var(--muted);font-size:13px}
.switch{position:relative;width:50px;height:30px;border-radius:30px;border:0;background:var(--line);padding:0;transition:.2s;flex-shrink:0}
.switch:after{content:"";position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:50%;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.3);transition:.2s}
.switch.on{background:var(--bad)}.switch.on:after{transform:translateX(20px)}
.lab-foot{margin-top:18px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.timeline{display:grid;gap:2px;max-height:400px;overflow:auto;margin:0;padding:0;list-style:none}
.tl{display:flex;gap:12px;padding:10px 0;position:relative}
.tl:before{content:"";position:absolute;left:5px;top:26px;bottom:-8px;width:2px;background:var(--line)}
.tl:last-child:before{display:none}
.tl-dot{width:12px;height:12px;border-radius:50%;background:var(--muted);margin-top:5px;flex-shrink:0;border:3px solid var(--surface);box-shadow:0 0 0 1px var(--line);position:relative;z-index:1}
.tl.success .tl-dot{background:var(--ok)}.tl.warning .tl-dot{background:var(--warn)}.tl.error .tl-dot{background:var(--bad)}
.tl-t{font-size:14px;overflow-wrap:anywhere}.tl small{display:block;color:var(--muted);font-size:12px;font-family:ui-monospace,Menlo,monospace}
.muted{color:var(--muted)}

/* directory + ref */
.table-wrap{overflow:auto}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:14px 20px;border-bottom:1px solid var(--line);font-size:14px;white-space:nowrap}
th{font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);background:var(--surface2)}
tbody tr:last-child td{border:0}tbody tr:hover td{background:var(--surface2)}
code,.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}
.ref-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ref{background:#0f1c1b;color:#d3ece6;border-radius:14px;padding:16px;position:relative}
.ref h4{margin:0 0 10px;font-size:12px;letter-spacing:.1em;color:#6fe0cb;text-transform:uppercase}
.ref pre{margin:0;font:13px/1.8 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap}
.ref button{position:absolute;top:10px;right:10px;background:rgba(255,255,255,.1);border:0;color:#d3ece6;border-radius:8px;padding:5px 8px;font-size:12px}
.ref button:hover{background:rgba(255,255,255,.2)}
footer.foot{border-top:1px solid var(--line);padding:26px 0 100px;color:var(--muted);font-size:13px}
.foot .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.toast{position:fixed;left:50%;bottom:92px;transform:translate(-50%,20px);background:var(--ink);color:var(--bg);padding:12px 20px;border-radius:99px;font-weight:600;font-size:14px;opacity:0;pointer-events:none;transition:.25s;z-index:50;max-width:90vw}
.toast.show{opacity:1;transform:translate(-50%,0)}
.tabbar{display:none}

@media(max-width:1000px){
  .stats{grid-template-columns:repeat(2,1fr)}
  .diag{grid-template-columns:1fr}.diag-form{border-right:0;border-bottom:1px solid var(--line)}
  .two,.ref-grid{grid-template-columns:1fr}
  .tier.four{grid-template-columns:repeat(2,1fr)}
  #deptTier{grid-template-columns:1fr}
  nav.main{display:none}
  .tabbar{display:flex;position:fixed;bottom:0;left:0;right:0;z-index:30;background:var(--surface);border-top:1px solid var(--line);padding:6px 6px calc(6px + env(safe-area-inset-bottom,0px))}
  .tabbar a{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0;font-size:11px;font-weight:700;text-decoration:none;color:var(--muted);border-radius:12px}
  .tabbar a.active{color:var(--primary-deep);background:var(--primary-soft)}
}
@media(max-width:560px){
  .wrap{padding:0 16px}.hero{padding:28px 22px;border-radius:22px}
  .stat{padding:16px}.stat-val{font-size:26px}
  .pc-btn{min-width:42px;min-height:40px}.dlg-row{grid-template-columns:1fr}.tier.core{grid-template-columns:1fr;gap:0}.tier.core .wire{width:3px;height:26px;margin:0 auto;background:repeating-linear-gradient(180deg,var(--primary) 0 6px,transparent 6px 10px)}
  .chip-status span.t{display:none}
  .diag-form,.diag-out{padding:20px}
}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-monitor" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></symbol>
<symbol id="i-server" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></symbol>
<symbol id="i-tag" viewBox="0 0 24 24"><path d="M4 12V4h8l8 8-8 8z"/><circle cx="8.5" cy="8.5" r="1"/></symbol>
<symbol id="i-router" viewBox="0 0 24 24"><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 17h.01M11 17h.01M8 10a6 6 0 0 1 8 0M5.5 7a10 10 0 0 1 13 0"/></symbol>
<symbol id="i-switch" viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="8" rx="2"/><path d="M7 12h.01M11 12h.01M15 12h.01"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12 5 5 9-10"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-play" viewBox="0 0 24 24"><path d="M7 5v14l12-7z"/></symbol>
<symbol id="i-refresh" viewBox="0 0 24 24"><path d="M20 11A8 8 0 0 0 5.6 7M4 4v4h4M4 13a8 8 0 0 0 14.4 4M20 20v-4h-4"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5 19 19M5 19l1.5-1.5M17.5 6.5 19 5"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14A8 8 0 0 1 10 4a8 8 0 1 0 10 10z"/></symbol>
<symbol id="i-link" viewBox="0 0 24 24"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3A4 4 0 0 0 11 18.7l1-1"/></symbol>
<symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></symbol>
<symbol id="i-pulse" viewBox="0 0 24 24"><path d="M3 12h4l3-8 4 16 3-8h4"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11 12 3l9 8M5 10v10h14V10"/></symbol>
<symbol id="i-flask" viewBox="0 0 24 24"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/></symbol>
<symbol id="i-network" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="5" rx="1"/><rect x="3" y="16" width="6" height="5" rx="1"/><rect x="15" y="16" width="6" height="5" rx="1"/><path d="M12 8v4M6 16v-4h12v4"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></symbol>
<symbol id="i-activity" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-trash" viewBox="0 0 24 24"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></symbol>
<symbol id="i-arrows" viewBox="0 0 24 24"><path d="M7 7h13M16 3l4 4-4 4M17 17H4M8 13l-4 4 4 4"/></symbol>
</svg>

<header class="top"><div class="wrap top-in">
  <a class="logo" href="#overview"><span class="logo-mark"><svg class="i"><use href="#i-network"/></svg></span>Coreline</a>
  <nav class="main" id="mainNav">
    <a href="#overview" class="active">Overview</a>
    <a href="#topology">Topology</a>
    <a href="#diagnostics">Diagnostics</a>
    <a href="#lab">Failure lab</a>
    <a href="#activity">Activity</a>
  </nav>
  <div class="spacer"></div>
  <div class="chip-status"><span class="pulse" id="sideDot"></span><span class="t" id="sideState">All services healthy</span></div>
  <button class="icon-btn" id="themeBtn" aria-label="Toggle dark mode" title="Toggle dark mode"><svg class="i moon"><use href="#i-moon"/></svg><svg class="i sun"><use href="#i-sun"/></svg></button>
</div></header>

<main class="wrap" id="overview">
  <div class="hero">
    <span class="tag"><svg class="i" style="width:14px;height:14px"><use href="#i-pulse"/></svg> CORPORATE LAN · 5 VLANs</span>
    <h1>Your office network, at a glance.</h1>
    <p>Explore the topology, test how departments reach shared services, and break things on purpose to see what happens.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="#diagnostics"><svg class="i"><use href="#i-play"/></svg> Run a test</a>
      <a class="btn btn-ghost" href="#lab"><svg class="i"><use href="#i-flask"/></svg> Try the failure lab</a>
    </div>
  </div>

  <div class="notice" id="notice"><svg class="i"><use href="#i-info"/></svg><span><strong>Simulation only.</strong> This dashboard models network behaviour. It does not control Packet Tracer or send real packets &mdash; use your Packet Tracer results as evidence for the real network.</span><button aria-label="Dismiss" onclick="document.getElementById('notice').remove()"><svg class="i"><use href="#i-x"/></svg></button></div>

  <div class="stats">
    <div class="stat"><div class="stat-top"><span class="stat-ico"><svg class="i"><use href="#i-pulse"/></svg></span>System condition</div><div class="stat-val" id="mode">NORMAL</div><div class="stat-foot" id="modeFoot">No failures active</div></div>
    <div class="stat"><div class="stat-top"><span class="stat-ico"><svg class="i"><use href="#i-link"/></svg></span>Connection checks</div><div class="stat-val" id="ct">0</div><div class="stat-foot">Policy evaluations run</div></div>
    <div class="stat"><div class="stat-top"><span class="stat-ico"><svg class="i"><use href="#i-arrows"/></svg></span>Allowed / blocked</div><div class="stat-val"><span id="allow">0</span><span class="muted" style="font-size:20px;font-weight:500"> / </span><span id="block">0</span></div><div class="stat-foot">Under the demo access policy</div></div>
    <div class="stat"><div class="stat-top"><span class="stat-ico"><svg class="i"><use href="#i-tag"/></svg></span>DHCP leases</div><div class="stat-val" id="leases">0</div><div class="stat-foot" id="leaseFoot">Modeled, not live clients</div></div>
  </div>

  <section class="block" id="topology">
    <div class="sec-head"><div><h2>Network topology</h2><p>Add or remove PCs in each department. Tap a PC to use it in a test. Each department has its own VLAN; shared services live on VLAN 50.</p></div>
      <div class="sec-actions"><button class="btn btn-sm" onclick="assignAll()"><svg class="i" style="width:16px;height:16px"><use href="#i-tag"/></svg> Assign IPs to all</button><button class="btn btn-sm" id="resetPcsBtn" onclick="resetPcs()"><svg class="i" style="width:16px;height:16px"><use href="#i-refresh"/></svg> Default PCs</button></div></div>
    <div class="card topo">
      <p class="tier-label">Departments &middot; <span id="pcTotal">4 PCs</span></p>
      <div class="tier four" id="deptTier"></div>
      <div class="vwire">Access links</div>
      <div class="tier core">
        <div class="node"><div class="node-ico"><svg class="i"><use href="#i-switch"/></svg></div><strong>CORP-SW1</strong><small>Managed access switch</small></div>
        <div class="wire"></div>
        <div class="node"><div class="node-ico"><svg class="i"><use href="#i-router"/></svg></div><strong>CORP-R1</strong><small>Routing &middot; DHCP relay</small></div>
      </div>
      <div class="vwire">Trunk &middot; VLAN 50 &middot; 192.168.50.0/24</div>
      <p class="tier-label">Central services</p>
      <div class="tier four" id="srvTier"></div>
      <p class="muted" style="font-size:13px;margin:16px 0 0;text-align:center">*Email status reflects the project design; verify delivery in Packet Tracer.</p>
    </div>
  </section>

  <section class="block" id="diagnostics">
    <div class="sec-head"><div><h2>Diagnostics</h2><p>Pick a test, choose the devices, and see the result in plain language.</p></div></div>
    <div class="card diag">
      <div class="diag-form">
        <div class="seg" role="tablist">
          <button class="active" id="tabConnect" role="tab" onclick="setTab('connect')"><svg class="i"><use href="#i-link"/></svg>Connect</button>
          <button id="tabDhcp" role="tab" onclick="setTab('dhcp')"><svg class="i"><use href="#i-tag"/></svg>DHCP</button>
          <button id="tabDns" role="tab" onclick="setTab('dns')"><svg class="i"><use href="#i-search"/></svg>DNS</button>
        </div>
        <div id="paneConnect">
          <div class="field"><label for="src">From (source device)</label><select id="src"></select></div>
          <div class="field"><label for="dst">To (destination)</label><select id="dst"></select></div>
          <button class="btn btn-primary" onclick="connectTest()"><svg class="i"><use href="#i-play"/></svg> Run connection check</button>
          <div class="presets"><p>Quick examples</p><div class="preset-row">
            <button class="preset" onclick="preset('HR','web-server')">HR &rarr; Intranet</button>
            <button class="preset" onclick="preset('Finance','email-server')">Finance &rarr; Email</button>
            <button class="preset" onclick="preset('Sales','Finance')">Sales &rarr; Finance (blocked)</button>
            <button class="preset" onclick="presetSame()">Two PCs, same VLAN</button>
          </div></div>
        </div>
        <div id="paneDhcp" hidden>
          <div class="field"><label for="dhcpDevice">Which device needs an address?</label><select id="dhcpDevice"></select></div>
          <button class="btn btn-primary" onclick="dhcpTest()"><svg class="i"><use href="#i-tag"/></svg> Request DHCP lease</button>
        </div>
        <div id="paneDns" hidden>
          <div class="field"><label for="dnsName">Hostname to look up</label><input id="dnsName" value="intranet.corp.local" list="dnsList" autocomplete="off" spellcheck="false"><datalist id="dnsList"><option value="intranet.corp.local"><option value="mail.corp.local"><option value="dns.corp.local"><option value="dhcp.corp.local"></datalist></div>
          <button class="btn btn-primary" onclick="dnsTest()"><svg class="i"><use href="#i-search"/></svg> Resolve hostname</button>
          <div class="presets"><p>Try one</p><div class="preset-row">
            <button class="preset" onclick="setDns('mail.corp.local')">mail.corp.local</button>
            <button class="preset" onclick="setDns('dns.corp.local')">dns.corp.local</button>
            <button class="preset" onclick="setDns('unknown.corp.local')">unknown (not found)</button>
          </div></div>
        </div>
      </div>
      <div class="diag-out" id="out" aria-live="polite">
        <div class="empty"><div class="ring"><svg class="i"><use href="#i-activity"/></svg></div><strong>No result yet</strong><p style="margin:6px 0 0;font-size:14px">Run a test and the outcome will appear here.</p></div>
      </div>
    </div>
  </section>

  <section class="block" id="lab">
    <div class="sec-head"><div><h2>Failure lab &amp; activity</h2><p>Flip a switch to simulate an outage, then re-run a test to see the impact.</p></div><span class="pill warn">Test mode</span></div>
    <div class="two">
      <div class="card pad">
        <div id="faults"></div>
        <div class="lab-foot"><span class="muted" id="faultSummary">No failures active.</span><button class="btn btn-sm" onclick="resetAll()"><svg class="i" style="width:16px;height:16px"><use href="#i-refresh"/></svg> Restore all</button></div>
      </div>
      <div class="card pad" id="activity">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><strong style="font-size:16px">Recent activity</strong><span class="pill info" id="eventCount">0 events</span></div>
        <ul class="timeline" id="events"></ul>
      </div>
    </div>
  </section>

  <section class="block" id="services">
    <div class="sec-head"><div><h2>Service directory</h2><p>What runs where on the server VLAN.</p></div></div>
    <div class="card table-wrap"><table><thead><tr><th>Service</th><th>IPv4 address</th><th>Role</th><th>Protocol</th></tr></thead><tbody>
      <tr><td><strong>DNS-SRV</strong></td><td class="mono">192.168.50.10</td><td>Name resolution</td><td>DNS &middot; 53</td></tr>
      <tr><td><strong>DHCP-SRV</strong></td><td class="mono">192.168.50.11</td><td>Dynamic addressing</td><td>DHCP &middot; 67/68</td></tr>
      <tr><td><strong>WEB-SRV</strong></td><td class="mono">192.168.50.20</td><td>Internal portal</td><td>HTTP &middot; 80</td></tr>
      <tr><td><strong>MAIL-SRV</strong></td><td class="mono">192.168.50.30</td><td>Mail sending / retrieval</td><td>SMTP / POP3</td></tr>
    </tbody></table></div>
  </section>

  <section class="block">
    <div class="sec-head"><div><h2>Packet Tracer cheat sheet</h2><p>Commands to verify the real network. Use Simulation Mode to watch DHCP, DNS and HTTP events.</p></div></div>
    <div class="ref-grid">
      <div class="ref"><h4>Switch</h4><pre>show vlan brief
show interfaces trunk</pre><button onclick="copyRef(this)">Copy</button></div>
      <div class="ref"><h4>Router</h4><pre>show ip interface brief
show ip route</pre><button onclick="copyRef(this)">Copy</button></div>
      <div class="ref"><h4>PC</h4><pre>ipconfig
ping 192.168.50.20</pre><button onclick="copyRef(this)">Copy</button></div>
    </div>
  </section>
</main>

<footer class="foot"><div class="wrap"><span>Coreline &middot; Corporate Office Network Project</span><span>Student lab interface &middot; Not a production NMS</span></div></footer>

<nav class="tabbar" id="tabbar">
  <a href="#overview" class="active"><svg class="i"><use href="#i-home"/></svg>Home</a>
  <a href="#topology"><svg class="i"><use href="#i-network"/></svg>Topology</a>
  <a href="#diagnostics"><svg class="i"><use href="#i-play"/></svg>Test</a>
  <a href="#lab"><svg class="i"><use href="#i-flask"/></svg>Lab</a>
</nav>
<dialog id="addDlg" aria-labelledby="dlgTitle"><div class="dlg">
  <h3 id="dlgTitle">Add PCs</h3><p>New PCs join the department's VLAN and can request an address from DHCP.</p>
  <div class="err" id="addErr" hidden></div>
  <div class="field"><label for="addDept">Department</label><select id="addDept"></select></div>
  <div class="field"><label for="addName">Name <span class="muted" style="font-weight:500">(optional)</span></label><input id="addName" maxlength="24" placeholder="e.g. Reception PC" autocomplete="off"></div>
  <div class="hint-t">Leave blank to auto-name (HR PC 2, HR PC 3&hellip;). With several PCs, a name becomes &ldquo;Name 1, Name 2&hellip;&rdquo;.</div>
  <div class="field"><label for="addCount">How many?</label><input id="addCount" type="number" min="1" max="10" value="1" inputmode="numeric"></div>
  <div class="qty" id="qty"></div>
  <div class="dlg-foot"><button class="btn" onclick="$('addDlg').close()">Cancel</button><button class="btn btn-primary" id="addGo" onclick="submitAdd()"><svg class="i"><use href="#i-plus"/></svg> Add</button></div>
</div></dialog>
<div class="toast" id="toast" role="status"></div>

<script>
const SRVS={{ servers|tojson }};
const DEPT_COLORS=['#0a8f7b','#ff6b4a','#6c63ff','#e0a100'];
const SRV_ICON={'dns-server':'search','dhcp-server':'tag','web-server':'globe','email-server':'mail'};
const SRV_BADGE={'dns-server':'dns','dhcp-server':'dhcp','web-server':'web','email-server':'link'};
const FAULTS=[
  {k:'dns',icon:'search',t:'DNS service',d:'Hostname lookups stop working'},
  {k:'dhcp',icon:'tag',t:'DHCP service',d:'New devices cannot get an address'},
  {k:'web',icon:'globe',t:'Intranet web server',d:'The internal site goes offline'},
  {k:'link',icon:'bolt',t:'Core trunk link',d:'Departments lose access to all servers'}
];
const $=id=>document.getElementById(id);
const ic=(n,s)=>`<svg class="i"${s?` style="${s}"`:''}><use href="#i-${n}"/></svg>`;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let S={pcs:[],department_list:[],limits:{max_per_department:12,max_add_at_once:10}};
const pcById=k=>S.pcs.find(p=>p.id===k);
const pcsOf=d=>S.pcs.filter(p=>p.department===d);
const nameOf=k=>(pcById(k)||SRVS[k]||{label:k}).label;

function toast(m){const t=$('toast');t.textContent=m;t.classList.add('show');clearTimeout(window._tt);window._tt=setTimeout(()=>t.classList.remove('show'),2400)}
async function api(p,b,m){try{const r=await fetch(p,{method:m||(b?'POST':'GET'),headers:{'Content-Type':'application/json'},body:b?JSON.stringify(b):undefined});return await r.json()}catch(e){toast('Could not reach the server');return {success:false,reason:'Server unreachable'}}}

/* theme */
$('themeBtn').onclick=()=>{const n=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=n;try{localStorage.setItem('cl-theme',n)}catch(e){}};

/* build topology */
$('srvTier').innerHTML=Object.entries(SRVS).map(([k,s])=>`<button class="node" onclick="pickDest('${k}')"><div class="node-top"><span class="node-ico">${ic(SRV_ICON[k])}</span><span class="pill ok" id="b-${k}">Online</span></div><strong>${esc(s.label)}</strong><small>${esc(s.services.join(' · '))}</small><span class="meta">${esc(s.ip)}</span><span class="hint">Use as test target &rarr;</span></button>`).join('');
$('faults').innerHTML=FAULTS.map(f=>`<div class="fault" id="f-${f.k}"><span class="fault-ico">${ic(f.icon)}</span><div class="fault-t"><strong>${f.t}</strong><small>${f.d}</small></div><button class="switch" id="sw-${f.k}" role="switch" aria-checked="false" aria-label="Toggle ${f.t} failure" onclick="fault('${f.k}')"></button></div>`).join('');

/* tabs */
function setTab(t){
  for(const [k,id,pane] of [['connect','tabConnect','paneConnect'],['dhcp','tabDhcp','paneDhcp'],['dns','tabDns','paneDns']]){
    $(id).classList.toggle('active',k===t);$(pane).hidden=k!==t;
  }
}
function go(id){$(id).scrollIntoView({behavior:'smooth'})}
function pickSource(k){setTab('connect');$('src').value=k;$('dhcpDevice').value=k;toast(nameOf(k)+' selected as source');go('diagnostics')}
function firstPc(d){const p=pcsOf(d)[0];return p?p.id:null}
function pickDest(k){setTab('connect');$('dst').value=k;toast(nameOf(k)+' selected as target');go('diagnostics')}
function preset(sd,d){const s=firstPc(sd);const dd=SRVS[d]?d:firstPc(d);if(!s||!dd){toast('That department has no PCs');return}$('src').value=s;$('dst').value=dd;connectTest()}
function presetSame(){const g=S.department_list.map(x=>pcsOf(x.name)).find(l=>l.length>1);if(!g){toast('Add a second PC to a department first');openAdd(S.department_list[0].name);return}$('src').value=g[0].id;$('dst').value=g[1].id;connectTest()}
function setDns(n){$('dnsName').value=n;dnsTest()}

/* results */
function view(ok,title,sub,rows,extra){
  $('out').innerHTML=`<div class="result"><div class="res-head"><span class="res-ico ${ok?'ok':'bad'}">${ic(ok?'check':'x')}</span><div><h3>${esc(title)}</h3><p>${esc(sub)}</p></div></div>${rows.length?`<div class="kv">${rows.map(r=>`<div><span>${esc(r[0])}</span><b>${esc(r[1])}</b></div>`).join('')}</div>`:''}${extra||''}</div>`;
}
async function connectTest(){
  const s=$('src').value,d=$('dst').value;const r=await api('/api/connect',{source:s,destination:d});
  const ps=pcById(s),pd=pcById(d);const rows=[['From',nameOf(s)+(ps?' (VLAN '+ps.vlan+')':'')],['To',nameOf(d)+(SRVS[d]?' ('+SRVS[d].ip+')':pd?' (VLAN '+pd.vlan+')':'')]];
  view(!!r.success,r.success?'Connection allowed':'Connection blocked',r.reason||'',rows);
  toast(r.success?'Allowed by the model':'Blocked by the model');refresh();
}
async function dhcpTest(){
  const d=$('dhcpDevice').value;const r=await api('/api/dhcp',{device:d});
  if(r.success){const l=r.lease;
    view(true,'Lease assigned',nameOf(d)+' received an address from the central DHCP server.',[['IP address',l.ip],['Subnet mask',l.mask],['Default gateway',l.gateway],['DNS server',l.dns]],`<div class="steps">${l.exchange.map((x,i)=>`<span class="step">${i+1} &middot; ${esc(x)}</span>`).join('')}</div>`);
  }else view(false,'No lease assigned',r.reason||'Request failed',[['Device',nameOf(d)]]);
  toast(r.success?'DHCP lease created':'DHCP request failed');refresh();
}
async function dnsTest(){
  const n=$('dnsName').value;const r=await api('/api/dns',{name:n});
  if(r.success)view(true,'Hostname resolved',r.query+' points to '+r.answer,[['Query',r.query],['Record type',r.type],['Answer',r.answer]]);
  else view(false,'Lookup failed',r.reason||'No answer',[['Query',r.query||n]]);
  toast(r.success?'Hostname resolved':'DNS lookup failed');refresh();
}
async function fault(k){await api('/api/failure',{kind:k});const f=FAULTS.find(x=>x.k===k);const on=$('sw-'+k).classList.contains('on');toast(f.t+(on?' restored':' failed'));refresh()}
async function resetAll(){await api('/api/reset',{});toast('All services restored');refresh()}
function copyRef(b){const t=b.parentElement.querySelector('pre').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1500)}).catch(()=>toast('Copy not available'))}

/* PCs */
function renderPcs(){
  const cols=['#0a8f7b','#ff6b4a','#6c63ff','#e0a100'];
  $('deptTier').innerHTML=S.department_list.map((d,i)=>{
    const list=pcsOf(d.name);const full=list.length>=S.limits.max_per_department;
    return `<div class="node dept-card" style="--c:${cols[i%4]}"><div class="dept-bar"></div><div class="node-top"><span class="node-ico">${ic('monitor')}</span><span class="pill info">VLAN ${d.vlan}</span></div><strong>${esc(d.name)}</strong><span class="count">${list.length} PC${list.length===1?'':'s'} &middot; <span class="mono">${esc(d.subnet)}</span></span>
    <ul class="pcs">${list.map(p=>`<li><button class="pc-main" onclick="pickSource('${p.id}')" title="Use ${esc(p.label)} as test source"><span class="pc-name">${esc(p.label)}</span><span class="pc-ip ${p.has_lease?'has':''}">${p.has_lease?esc(p.ip):'No IP yet'}</span></button><button class="pc-btn" onclick="quickDhcp('${p.id}')" aria-label="Request IP for ${esc(p.label)}" title="Request IP address">${ic('tag','width:16px;height:16px')}</button><button class="pc-btn del" onclick="askDel(this,'${p.id}')" aria-label="Remove ${esc(p.label)}" title="Remove PC">${ic('trash','width:16px;height:16px')}</button></li>`).join('')}</ul>
    <button class="btn btn-sm add-pc" onclick="openAdd('${esc(d.name)}')" ${full?'disabled title="Department is full"':''}>${ic('plus','width:16px;height:16px')} ${full?'Department full':'Add PC'}</button></div>`}).join('');
  $('pcTotal').textContent=S.pcs.length+' PCs';
  const keep=[$('src').value,$('dst').value,$('dhcpDevice').value];
  const grp=(d,fn)=>`<optgroup label="${esc(d.name)} · VLAN ${d.vlan}">${pcsOf(d.name).map(fn).join('')}</optgroup>`;
  $('src').innerHTML=S.department_list.map(d=>grp(d,p=>`<option value="${p.id}">${esc(p.label)}${p.has_lease?' · '+p.ip:''}</option>`)).join('');
  $('dst').innerHTML=`<optgroup label="Central services">${Object.entries(SRVS).map(([k,s])=>`<option value="${k}">${esc(s.label)}</option>`).join('')}</optgroup>`+S.department_list.map(d=>grp(d,p=>`<option value="${p.id}">${esc(p.label)}</option>`)).join('');
  $('dhcpDevice').innerHTML=S.department_list.map(d=>grp(d,p=>`<option value="${p.id}">${esc(p.label)}</option>`)).join('');
  [['src',keep[0]],['dst',keep[1]],['dhcpDevice',keep[2]]].forEach(([id,v])=>{if([...$(id).options].some(o=>o.value===v))$(id).value=v});
  $('addDept').innerHTML=S.department_list.map(d=>`<option value="${esc(d.name)}">${esc(d.name)} · VLAN ${d.vlan}</option>`).join('');
}
function openAdd(dept){
  $('addErr').hidden=true;$('addName').value='';$('addCount').value=1;$('addDept').value=dept;setQty(1);
  $('qty').innerHTML=[1,2,3,5,10].map(n=>`<button type="button" data-n="${n}" onclick="setQty(${n})">${n}</button>`).join('');setQty(1);
  $('addDlg').showModal();$('addName').focus();
}
function setQty(n){$('addCount').value=n;document.querySelectorAll('#qty button').forEach(b=>b.classList.toggle('on',+b.dataset.n===+n))}
$('addCount').addEventListener('input',()=>setQty($('addCount').value));
$('addDlg').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.tagName==='INPUT'){e.preventDefault();submitAdd()}});
async function submitAdd(){
  const dept=$('addDept').value;
  const r=await api('/api/pcs',{department:dept,name:$('addName').value,count:+$('addCount').value||1});
  if(!r.success){$('addErr').textContent=r.reason||'Could not add PC';$('addErr').hidden=false;return}
  $('addDlg').close();toast(r.added.length===1?`Added ${r.added[0].label} to ${dept}`:`Added ${r.added.length} PCs to ${dept}`);refresh();
}
function askDel(btn,id){
  if(btn.classList.contains('armed')){doDel(id);return}
  btn.classList.add('armed');btn.innerHTML='Remove?';
  setTimeout(()=>{if(btn.isConnected){btn.classList.remove('armed');btn.innerHTML=ic('trash','width:16px;height:16px')}},3000);
}
async function doDel(id){
  const label=nameOf(id);const r=await api('/api/pcs/'+encodeURIComponent(id),null,'DELETE');
  toast(r.success?`Removed ${label}`:(r.reason||'Could not remove PC'));refresh();
}
async function quickDhcp(id){$('dhcpDevice').value=id;setTab('dhcp');await dhcpTest();go('diagnostics')}
async function assignAll(){
  const need=S.pcs.filter(p=>!p.has_lease);if(!need.length){toast('Every PC already has an address');return}
  let ok=0,bad=0,why='';for(const p of need){const r=await api('/api/dhcp',{device:p.id});if(r.success)ok++;else{bad++;why=r.reason||''}}
  toast(bad?`${ok} assigned, ${bad} failed (${why})`:`${ok} PC${ok===1?'':'s'} received an address`);refresh();
}
async function resetPcs(){
  const b=$('resetPcsBtn');if(!b.dataset.armed){b.dataset.armed=1;const o=b.innerHTML;b.textContent='Click again to confirm';setTimeout(()=>{delete b.dataset.armed;b.innerHTML=o},3000);return}
  delete b.dataset.armed;b.innerHTML='<svg class="i" style="width:16px;height:16px"><use href="#i-refresh"/></svg> Default PCs';
  await api('/api/pcs/reset',{});toast('Back to the 4 default PCs');refresh();
}

/* status */
async function refresh(){
  const s=await api('/api/status');if(!s.counters)return;S=s;renderPcs();
  const ok=s.mode==='NORMAL';
  $('mode').textContent=s.mode;$('mode').style.color=ok?'':'var(--warn)';
  $('modeFoot').textContent=ok?'No failures active':'One or more failures active';
  $('ct').textContent=s.counters.connection_tests;$('allow').textContent=s.counters.allowed;$('block').textContent=s.counters.blocked;
  $('leases').textContent=Object.keys(s.leases).length;$('leaseFoot').textContent='of '+s.pcs.length+' PCs hold a lease';
  $('sideState').textContent=ok?'All services healthy':'Degraded';$('sideDot').classList.toggle('warn',!ok);
  for(const k in SRV_BADGE){const failed=s.failures[SRV_BADGE[k]];const el=$('b-'+k);
    el.textContent=failed?(k==='email-server'?'Unreachable':'Failed'):(k==='email-server'?'Online*':'Online');el.className='pill '+(failed?'bad':'ok')}
  for(const f of FAULTS){const on=!!s.failures[f.k];$('sw-'+f.k).classList.toggle('on',on);$('sw-'+f.k).setAttribute('aria-checked',on);$('f-'+f.k).classList.toggle('on',on)}
  const act=FAULTS.filter(f=>s.failures[f.k]).map(f=>f.t);
  $('faultSummary').textContent=act.length?'Active: '+act.join(', '):'No failures active.';
  $('eventCount').textContent=s.recent_events.length+' events';
  $('events').innerHTML=s.recent_events.map(e=>`<li class="tl ${e.kind}"><span class="tl-dot"></span><div><div class="tl-t">${esc(e.event)}</div><small>${esc(e.time)}</small></div></li>`).join('')||'<li class="muted">No events yet</li>';
}

/* nav highlight */
const ids=['overview','topology','diagnostics','lab'];
const links=[...document.querySelectorAll('#mainNav a,#tabbar a')];
const io=new IntersectionObserver(es=>{for(const e of es)if(e.isIntersecting){links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+e.target.id))}},{rootMargin:'-40% 0px -55% 0px'});
ids.forEach(i=>{const el=$(i);if(el)io.observe(el)});
refresh();
</script>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE, depts=DEPARTMENTS, servers=SERVERS)

@app.get("/api/status")
def status():
    return jsonify(network.status())

@app.post("/api/dhcp")
def dhcp():
    body = request.get_json(silent=True) or {}
    return jsonify(network.dhcp_request(body.get("device", "hr-pc")))

@app.post("/api/dns")
def dns():
    body = request.get_json(silent=True) or {}
    return jsonify(network.dns_lookup(body.get("name", "")))

@app.post("/api/connect")
def connect():
    body = request.get_json(silent=True) or {}
    return jsonify(network.connect(body.get("source", "hr-pc"), body.get("destination", "web-server")))

@app.post("/api/failure")
def failure():
    body = request.get_json(silent=True) or {}
    try:
        return jsonify(network.toggle_failure(body.get("kind", "")))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.post("/api/pcs")
def add_pcs():
    body = request.get_json(silent=True) or {}
    result = network.add_pcs(body.get("department"), body.get("name"), body.get("count", 1))
    return jsonify(result), (201 if result["success"] else 400)

@app.delete("/api/pcs/<pc_id>")
def remove_pc(pc_id):
    result = network.remove_pc(pc_id)
    if result["success"]:
        return jsonify(result)
    return jsonify(result), (404 if result["reason"] == "Unknown PC" else 400)

@app.post("/api/pcs/reset")
def reset_pcs():
    return jsonify(network.reset_pcs())

@app.post("/api/reset")
def reset():
    return jsonify(network.reset())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
