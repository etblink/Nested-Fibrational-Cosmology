let metadata = null;
let currentPersona = null;
let currentBranch = null;
let currentCluster = null;
let currentRecoveryMode = 'core';
let stageHistory = ['landing'];
const stages = ['landing','selector','contract','kernel','doctrine','antiref','source','branchmap','clusters','clusterdetail','clustercompare','recovery','route','archive','branchdetail'];
const labels = {
  landing:'Start', selector:'Persona', contract:'Contract', kernel:'Anchor', doctrine:'Doctrine', antiref:'Hardening', source:'Source', branchmap:'Branches', clusters:'Clusters', clusterdetail:'Cluster Detail', clustercompare:'Compare Clusters', recovery:'Recovery', route:'Route', archive:'Archive', branchdetail:'Detail'
};

async function init(){
  const res = await fetch('canonical_metadata.json');
  metadata = await res.json();
  renderAll();
  showStage('landing', false);
}

function renderAll(){
  renderLanding();
  renderSelector();
  renderContract();
  renderKernel();
  renderDoctrine();
  renderAntiRef();
  renderSource();
  renderBranchMap();
  renderClusters();
  renderClusterDetail();
  renderClusterCompare();
  renderRecovery();
  renderArchive();
  renderRoute();
  renderBranchDetail();
  renderProgress('landing');
  renderPathState();
}

function showStage(id, push=true){
  document.querySelectorAll('.stage').forEach(s=>s.classList.remove('active'));
  document.getElementById(`stage-${id}`).classList.add('active');
  if(push){
    if(stageHistory[stageHistory.length-1] !== id) stageHistory.push(id);
  }
  renderProgress(id);
  renderPathState();
}

function backOne(){
  if(stageHistory.length <= 1){ showStage('landing', false); return; }
  stageHistory.pop();
  showStage(stageHistory[stageHistory.length-1], false);
}

function restartJourney(){
  currentPersona = null;
  currentBranch = null;
  currentCluster = null;
  currentRecoveryMode = 'core';
  stageHistory = ['landing'];
  renderRoute();
  renderRecovery();
  showStage('landing', false);
}

function renderProgress(active){
  const nav = document.getElementById('progress-nav');
  nav.innerHTML = stages.map(s=>{
    const locked = isStageLocked(s);
    return `<a href="#" class="progress-link ${active===s?'active':''} ${locked?'locked-link':''}" onclick="event.preventDefault(); ${locked?'':`showStage('${s}')`}">${labels[s]}${locked?' · locked':''}</a>`;
  }).join('');
}

function isStageLocked(stage){
  if(stage === 'branchdetail') return !currentBranch;
  if(stage === 'clusterdetail') return !currentCluster;
  if(stage === 'route') return !currentPersona;
  if(stage === 'recovery') return false;
  return false;
}

function renderPathState(){
  const el = document.getElementById('path-state');
  const active = stageHistory[stageHistory.length-1] || 'landing';
  const path = ['Start'];
  if(currentPersona) path.push(personaLabel(currentPersona));
  if(active !== 'landing' && active !== 'selector') path.push(labels[active]);
  if(currentRecoveryMode === 'extended' && (active === 'recovery' || currentPersona === 'recovery' || currentPersona === 'physicist' || currentPersona === 'collaborator')) path.push('K0 annex');
  if(currentCluster && (active === 'clusterdetail' || active === 'clusters')) path.push(currentCluster);
  if(currentBranch) path.push(currentBranch);
  const steps = path.map((p,i)=>`<span class="path-pill ${i===path.length-1?'active':''}">${p}</span>`).join('<span class="path-sep">→</span>');
  el.innerHTML = `<div class="path-label">Current path</div><div class="path-trail">${steps}</div>`;
}

function personaLabel(code){
  return ({editor:'Editor', mathematician:'Referee', physicist:'Physicist', public:'General', collaborator:'Collaborator', recovery:'Tester'})[code] || 'Route';
}

function statusInfo(code){
  return metadata.status_definitions.find(x=>x.code===code) || metadata.status_definitions[0];
}
function statusBadge(code){
  const s = statusInfo(code);
  return `<span class="status ${s.css}">${s.label}</span>`;
}
function openDoc(file){ window.open(`docs/${file}`, '_blank'); }

function sceneWrap(kicker,title,subtitle,body='',foot=''){
  return `<div class="scene"><div class="scene-path">${renderInlinePath()}</div>${kicker?`<div class="kicker">${kicker}</div>`:''}<h2>${title}</h2>${subtitle?`<p class="subtitle">${subtitle}</p>`:''}${body}${foot?`<div class="scene-footer">${foot}</div>`:''}</div>`;
}

function renderInlinePath(){
  const active = stageHistory[stageHistory.length-1] || 'landing';
  const items = ['Start'];
  if(currentPersona) items.push(personaLabel(currentPersona));
  const coreStages = ['contract','kernel','doctrine','antiref','source','branchmap','clusters','clusterdetail','clustercompare','recovery','route','archive','branchdetail'];
  if(coreStages.includes(active)) items.push(labels[active]);
  if(currentCluster && active === 'clusterdetail') items.push(currentCluster);
  if(currentBranch && active === 'branchdetail') items.push(currentBranch);
  return `<div class="inline-path">${items.map((x,i)=>`<span>${x}</span>`).join('<span class="path-sep">→</span>')}</div>`;
}

function choiceCard({title,desc,preview,action,variant='primary',locked=false}){
  return `<div class="choice-card ${locked?'locked-card':''}"><h3>${title}</h3><p>${desc}</p><p class="preview"><strong>Next:</strong> ${preview}</p><div class="btn-row"><button class="btn ${variant==='secondary'?'btn-secondary':variant==='ghost'?'btn-ghost':'btn-primary'}" ${locked?'disabled':''} onclick="${locked?'':action}">${locked?'Locked':'Choose'}</button></div></div>`;
}

function smallDocCard(code, extra=''){
  const d = metadata.docs[code]; if(!d) return '';
  return `<div class="doc-card compact"><div class="meta">${code} · ${d.role}</div><h3>${d.title}</h3>${statusBadge(d.status)}<p>${d.summary}</p>${extra}<div class="btn-row"><button class="btn btn-secondary" onclick="openDoc('${d.file}')">Open</button></div></div>`;
}

function docCard(code, extra=''){
  return smallDocCard(code, extra);
}

function renderLockedNext(nextSteps){
  return `<div class="locked-panel"><div class="meta">Visible next steps</div>${nextSteps.map(n=>`<div class="lock-row"><span class="lock-name">${n.name}</span><span class="lock-note">${n.note}</span></div>`).join('')}</div>`;
}

function renderLanding(){
  const body = `
    <div class="banner">Asset honesty: this build uses real PDFs from the uploaded public stack, submission packet, and suite bundle wherever those files were available.</div>
    <div class="grid">${[
      {title:'Begin guided entry', desc:'Take the governed route from anchor to doctrine to source.', preview:'Persona selection, then the common anchor sequence.', action:`showStage('selector')`},
      {title:'Open controlled archive', desc:'Browse canon-aware files directly.', preview:'Archive cards with code, status, and reading context.', action:`showStage('archive')`, variant:'secondary'},
      {title:'Open recovery modes', desc:'Test core recovery or the extended K0 annex.', preview:'Two-mode validation view.', action:`showStage('recovery')`, variant:'ghost'}
    ].map(choiceCard).join('')}</div>`;
  document.getElementById('stage-landing').innerHTML = sceneWrap('Governed front door','Dream Suite Guided Intake','A branching theorem-navigation system with visible consequences, reversible routes, and controlled deepening.', body);
}

function renderSelector(){
  const cards = [
    ['editor','Editor / journal gatekeeper','Keep the route narrow and public-anchor first.','Kernel anchor, then submission shell.'],
    ['mathematician','Mathematician / referee','Take the serious-reader spine.','KR4 → JR3 → A → IR8 → D2 → BR.'],
    ['physicist','Physicist / frontier reader','Move from source to branches, with K0 annex visible.','BR, then K07/R3Q, then BB/BY/BH.'],
    ['public','General reader','Start broad, then deepen only if needed.','Overview-first public stack.'],
    ['collaborator','Collaborator / steward','See doctrine, source, annex, and handoff materials.','D2 → BR → K07 → R3Q → IR8.'],
    ['recovery','Recovery / validation tester','Test the canonical set before and after the annex.','Core mode versus extended K0 mode.']
  ];
  const body = `<div class="grid">${cards.map(([k,t,d,p])=>choiceCard({title:t,desc:d,preview:p,action:`selectPersona('${k}')`}).replace('Choose','Take this route')).join('')}</div>`;
  document.getElementById('stage-selector').innerHTML = sceneWrap('Choose one path','What kind of reader are you?','Pick one route now. You can switch later without losing the governed order.', body);
}

function selectPersona(p){
  currentPersona = p;
  currentBranch = null;
  currentRecoveryMode = (p === 'physicist' || p === 'collaborator' || p === 'recovery') ? 'extended' : 'core';
  renderRoute();
  renderRecovery();
  showStage('contract');
}

function renderContract(){
  const body = `<div class="grid two-up">${[
    {title:'Continue in governed order', desc:'Use the common intake sequence before branching.', preview:'Kernel anchor next.', action:`showStage('kernel')`},
    {title:'Review recovery modes first', desc:'Preview core versus annex testing before continuing.', preview:'Recovery screen, then return to the route.', action:`showStage('recovery')`, variant:'secondary'},
    {title:'Browse archive now', desc:'Bypass the sequence, but keep canon-aware labels.', preview:'Controlled archive with reading context.', action:`showStage('archive')`, variant:'ghost'}
  ].map(choiceCard).join('')}</div>${renderLockedNext([
    {name:'Branch detail', note:'Unlocks after source and branch map.'},
    {name:'Persona packet', note:'Appears after the shared doctrine path.'}
  ])}`;
  document.getElementById('stage-contract').innerHTML = sceneWrap('One shared rule','Before you branch, the suite fixes a common intake order.','This is the non-narrative equivalent of a choose-your-own-adventure fork: one clear decision, visible consequences.', body);
}

function renderKernel(){
  const body = `<div class="grid two-up">${choiceCard({title:'Read the finite anchor first', desc:'Start with the strongest unconditional layer.', preview:'Doctrine and status law next.', action:`showStage('doctrine')`}).replace('Choose','Continue')} ${choiceCard({title:'Open the anchor documents', desc:'Inspect the public and serious versions directly.', preview:'Kernel public anchor and A.', action:`openDoc('${metadata.docs.KPUB.file}')`, variant:'secondary'}).replace('Choose','Open KPUB')} </div><div class="grid two-up">${smallDocCard('KPUB')}${smallDocCard('A')}</div>${renderLockedNext([{name:'Branch map',note:'Visible after the source hub.'},{name:'K0 annex',note:'Visible in recovery mode and physicist/collaborator routes.'}])}`;
  document.getElementById('stage-kernel').innerHTML = sceneWrap('Shared first serious screen','Kernel public anchor','Every governed route encounters the finite anchor before synthesis or branch escalation.', body, `<button class="btn btn-ghost" onclick="showStage('contract')">Back to contract</button>`);
}

function renderDoctrine(){
  const rows = metadata.status_definitions.map(s=>`<tr><td>${statusBadge(s.code)}</td><td>${s.description}</td></tr>`).join('');
  const body = `<table class="table"><tr><th>Status</th><th>Meaning</th></tr>${rows}</table><div class="grid two-up">${choiceCard({title:'Accept the status law', desc:'Continue once the four-part doctrine is clear.', preview:'Anti-referee hardening next.', action:`showStage('antiref')`}).replace('Choose','Continue')}${choiceCard({title:'Open D2 now', desc:'Inspect the evidentiary law directly.', preview:'D2 in a new tab.', action:`openDoc('${metadata.docs.D2.file}')`, variant:'secondary'}).replace('Choose','Open D2')}</div>`;
  document.getElementById('stage-doctrine').innerHTML = sceneWrap('Status before ambition','What kind of claim are you looking at?','This screen keeps unconditional, conditional, and computational material visibly separate.', body, `<button class="btn btn-ghost" onclick="showStage('kernel')">Back to anchor</button>`);
}

function renderAntiRef(){
  const body = `<div class="warning"><strong>Three front-loaded rules</strong><ul class="list"><li>No theorem is upgraded by citation alone.</li><li>No downstream claim is stronger than its named bridge stack.</li><li>No admissibility class is licensed by self-reference to the conclusion it is supposed to support.</li></ul></div><div class="grid two-up">${choiceCard({title:'Proceed to source hub', desc:'Move from doctrine to the upstream source layer.', preview:'BR, BR note, and K0 annex choices.', action:`showStage('source')`}).replace('Choose','Continue')}${choiceCard({title:'Browse canon-aware archive', desc:'Take an advanced-access detour.', preview:'Archive with labels preserved.', action:`showStage('archive')`, variant:'secondary'}).replace('Choose','Open archive')}</div>`;
  document.getElementById('stage-antiref').innerHTML = sceneWrap('Hardening layer','What may not be smuggled through the UI?','These rules make the consequences of later choices explicit before the source layer appears.', body, `<button class="btn btn-ghost" onclick="showStage('doctrine')">Back to doctrine</button>`);
}

function renderSource(){
  const body = `<div class="grid">${[
    {title:'Inspect BR as the source layer', desc:'See the unconditional upstream route.', preview:'Open BR and its dependency note.', action:`openDoc('${metadata.docs.BR.file}')`},
    {title:'Test the K0 annex', desc:'Add the self-consistency route to K0 = 7.', preview:'Recovery mode or physicist/collaborator packet.', action:`setRecoveryMode('extended'); showStage('recovery')`, variant:'secondary'},
    {title:'Move to the branch map', desc:'View the three downstream branch families.', preview:'BB, BY, BH with inspect buttons.', action:`showStage('branchmap')`, variant:'ghost'}
  ].map(choiceCard).join('')}</div><div class="grid two-up">${smallDocCard('BR')}${smallDocCard('BRN')}${smallDocCard('K07')}${smallDocCard('R3Q')}</div>`;
  document.getElementById('stage-source').innerHTML = sceneWrap('Upstream fork','What sits before the branches?','BR is upstream of BB, BY, and BH. The K0 annex strengthens the validation route without replacing the core recovery set.', body, `<button class="btn btn-ghost" onclick="showStage('antiref')">Back to hardening</button>`);
}

function setRecoveryMode(mode){
  currentRecoveryMode = mode;
  renderRecovery();
  renderPathState();
}

function renderBranchMap(){
  const branches = Object.entries(metadata.branches).map(([code,b])=>choiceCard({
    title:`${code} · ${metadata.docs[code].title}`,
    desc:b.claim,
    preview:`Inspect bridge stack: ${b.bridge_stack.join(' → ')}`,
    action:`inspectBranch('${code}')`,
    variant:'secondary'
  }).replace('Choose','Inspect'));
  const body = `<div class="grid">${branches.join('')}</div>${renderLockedNext([{name:'Persona packet',note:'Unlocks after you finish the shared route.'},{name:'Advanced archive',note:'Available now, but bypasses path sequence.'}])}`;
  document.getElementById('stage-branchmap').innerHTML = sceneWrap('Choose a branch or continue','Which downstream consequence do you want to inspect?','These are branch-specific drilldowns, not new foundations.', body, `<div class="btn-row"><button class="btn btn-primary" onclick="showStage('clusters')">Continue to branch clusters</button><button class="btn btn-ghost" onclick="showStage('source')">Back to source</button></div>`);
}

function inspectBranch(code){
  currentBranch = code;
  renderBranchDetail();
  showStage('branchdetail');
}

function renderBranchDetail(){
  const code = currentBranch || 'BB';
  const b = metadata.branches[code];
  const d = metadata.docs[code];
  if(!b || !d) return;
  const body = `<table class="table"><tr><th>Branch claim</th><td>${b.claim}</td></tr><tr><th>Status</th><td>${statusBadge(b.status)}</td></tr><tr><th>Bridge stack</th><td>${b.bridge_stack.join(' → ')}</td></tr><tr><th>Governing files</th><td>${b.governing_files.map(g=>metadata.docs[g]?metadata.docs[g].title:g).join(', ')}</td></tr><tr><th>Residual vulnerability</th><td>${b.residual}</td></tr></table><div class="grid two-up">${choiceCard({title:'Open the branch PDF',desc:'Read the branch package directly.',preview:'PDF opens in a new tab.',action:`openDoc('${d.file}')`,variant:'secondary'}).replace('Choose','Open')}${choiceCard({title:'Compare a different branch',desc:'Return to the branch map and inspect another route.',preview:'Back to BB/BY/BH choices.',action:`showStage('branchmap')`,variant:'ghost'}).replace('Choose','Compare')}</div>`;
  document.getElementById('stage-branchdetail').innerHTML = sceneWrap('One branch at a time', d.title, 'This screen exists so branch differences are interpreted rather than inferred.', body, `<button class="btn btn-ghost" onclick="showStage('branchmap')">Back to branch map</button>`);
}


function renderClusters(){
  const cards = Object.entries(metadata.clusters).map(([code,c])=>choiceCard({
    title:c.title,
    desc:c.summary,
    preview:`Unlocks papers after: ${c.unlock_after.join(' → ')}`,
    action:`inspectCluster('${code}')`,
    variant:'secondary'
  }).replace('Choose','Open cluster')).join('');
  const body = `<div class="grid two-up">${cards}</div>${renderLockedNext([{name:'Recovery modes',note:'Still available after cluster inspection.'},{name:'Persona packet',note:'Remains route-specific after the shared path.'}])}`;
  document.getElementById('stage-clusters').innerHTML = sceneWrap('Governed deepening','Which paper cluster do you want to unlock?','These clusters expose more of the ~97-paper architecture, but only through prerequisite-aware branch deepening.', body, `<div class="btn-row"><button class="btn btn-primary" onclick="showStage('clustercompare')">Compare clusters</button><button class="btn btn-secondary" onclick="showStage('recovery')">Continue to recovery</button><button class="btn btn-ghost" onclick="showStage('branchmap')">Back to branches</button></div>`);
}

function inspectCluster(code){
  currentCluster = code;
  renderClusterDetail();
  showStage('clusterdetail');
}

function renderClusterDetail(){
  const code = currentCluster || Object.keys(metadata.clusters)[0];
  const c = metadata.clusters[code];
  if(!c) return;
  const rows = c.items.map(item=>{
    const d = metadata.docs[item];
    if(!d) return '';
    return `<div class="doc-card compact"><div class="meta">${item} · ${d.role}</div><h3>${d.title}</h3>${statusBadge(d.status)}<p>${d.summary}</p><p class="mini"><strong>Prerequisite context:</strong> ${c.unlock_after.join(' → ')}</p><div class="btn-row"><button class="btn btn-secondary" onclick="openDoc('${d.file}')">Open</button>${metadata.branches[item]?`<button class="btn btn-ghost" onclick="inspectBranch('${item}')">Inspect branch</button>`:''}</div></div>`;
  }).join('');
  const body = `<div class="banner"><strong>Unlock after:</strong> ${c.unlock_after.join(' → ')}</div><div class="archive-grid">${rows}</div>`;
  document.getElementById('stage-clusterdetail').innerHTML = sceneWrap('Cluster unlock', c.title, 'Every surfaced paper here is shown as a lawful stewarded unlock: code, role, status, prerequisite, and one-line purpose remain visible.', body, `<div class="btn-row"><button class="btn btn-secondary" onclick="showStage('clusters')">Back to clusters</button><button class="btn btn-ghost" onclick="showStage('clustercompare')">Compare clusters</button><button class="btn btn-ghost" onclick="showStage('recovery')">Continue to recovery</button></div>`);
}


function renderClusterCompare(){
  const order = metadata.cluster_compare_order || Object.keys(metadata.clusters);
  const rows = order.map(code=>{
    const c = metadata.clusters[code];
    const papers = c.items.map(item=>{
      const d = metadata.docs[item];
      return `<div class="mini"><strong>${item}</strong> · ${d?d.role:'paper'} · ${d?statusInfo(d.status).label:''}</div>`;
    }).join('');
    return `<tr><td><strong>${code}</strong><br>${c.title}</td><td>${c.unlock_after.join(' → ')}</td><td>${c.summary}</td><td>${papers}</td><td><button class="btn btn-secondary" onclick="inspectCluster('${code}')">Open</button></td></tr>`;
  }).join('');
  const body = `<div class="banner"><strong>Comparison view:</strong> compare the governed deepening paths before committing to one cluster.</div><table class="table"><tr><th>Cluster</th><th>Unlock after</th><th>Purpose</th><th>Surfaced papers</th><th>Action</th></tr>${rows}</table>`;
  document.getElementById('stage-clustercompare').innerHTML = sceneWrap('Cluster comparison','Compare F, S, M, and G as stewarded unlocks','This screen makes the growing 97-paper architecture legible without flattening it into a single archive dump.', body, `<div class="btn-row"><button class="btn btn-secondary" onclick="showStage('clusters')">Back to clusters</button><button class="btn btn-ghost" onclick="showStage('recovery')">Continue to recovery</button></div>`);
}

function renderRecovery(){
  const coreChoices = metadata.recovery_core.map(code=>smallDocCard(code, `<p class="mini"><strong>Why here:</strong> core recovery spine.</p>`)).join('');
  const annexChoices = metadata.recovery_annex.map(code=>smallDocCard(code, `<p class="mini"><strong>Why here:</strong> K0-theorem annex.</p>`)).join('');
  const modeBanner = currentRecoveryMode === 'extended'
    ? `<div class="banner"><strong>Extended mode active.</strong> The K0 annex is now part of the active route state.</div>`
    : `<div class="banner"><strong>Core mode active.</strong> Start with the minimal canonical reconstruction set.</div>`;
  const body = `${modeBanner}<div class="grid two-up">${choiceCard({title:'Use core recovery only',desc:'Test whether a reader reconstructs the governed suite without the K0 annex.',preview:'KR4, JR3, A, IR8, D2, BR.',action:`setRecoveryMode('core'); renderRecovery()`,variant:currentRecoveryMode==='core'?'primary':'secondary'}).replace('Choose',currentRecoveryMode==='core'?'Selected':'Select')}${choiceCard({title:'Add the K0 annex',desc:'Test whether the reader upgrades K0 = 7 to theorem-language after the core pass.',preview:'Adds K07 and R3Q.',action:`setRecoveryMode('extended'); renderRecovery()`,variant:currentRecoveryMode==='extended'?'primary':'secondary'}).replace('Choose',currentRecoveryMode==='extended'?'Selected':'Select')}</div><div class="grid two-up"><div>${coreChoices}</div><div>${annexChoices}</div></div><div class="banner"><strong>Scoring rubric</strong><ol class="list"><li>Can the reader separate unconditional, conditional, and computational material?</li><li>Do they place BR upstream of BB/BY/BH?</li><li>Do they treat IR8 and D2 as governance/status sources rather than theorem promotion devices?</li><li>After the annex, do they explicitly upgrade K0 = 7 to theorem-language?</li></ol></div>`;
  document.getElementById('stage-recovery').innerHTML = sceneWrap('Validation fork','Do you want the core test or the extended K0 test?','This is a choice with explicit consequences: the selected mode becomes part of the route state.', body, `<div class="btn-row"><button class="btn btn-primary" onclick="renderRoute(); showStage('route')">Continue to selected route</button><button class="btn btn-ghost" onclick="showStage('branchmap')">Back to branches</button></div>`);
}

function renderRoute(){
  const codes = metadata.personas[currentPersona] || metadata.personas.public;
  const routeTitle = ({editor:'Editor lane', mathematician:'Mathematician / referee lane', physicist:'Physicist lane', public:'General reader lane', collaborator:'Collaborator lane', recovery:'Recovery tester lane'})[currentPersona] || 'Route';
  const filtered = currentRecoveryMode === 'core' ? codes.filter(c=>!metadata.recovery_annex.includes(c)) : codes;
  const cards = filtered.map((code, idx) => docCard(code, `<p class="mini"><strong>Step:</strong> ${idx+1} in this route.</p>`)).join('');
  const compareChoices = currentPersona ? `<div class="grid two-up">${['editor','mathematician','physicist','public','collaborator','recovery'].filter(p=>p!==currentPersona).slice(0,3).map(p=>choiceCard({title:`Compare with ${personaLabel(p)}`,desc:'See how a different route would sequence the same canon.',preview:'Switch persona while preserving the governed route mechanics.',action:`currentPersona='${p}'; renderRoute(); showStage('route')`,variant:'ghost'}).replace('Choose','Compare')).join('')}</div>` : '';
  const body = `${(currentPersona==='physicist'||currentPersona==='mathematician'||currentPersona==='collaborator')?'<div class="banner"><strong>Governed deepening available:</strong> Use the cluster screen to unlock more of the 97-paper architecture without bypassing prerequisites.</div>':''}<div class="banner"><strong>Active mode:</strong> ${currentRecoveryMode === 'extended' ? 'Extended K0 annex' : 'Core canonical route'}</div><div class="archive-grid">${cards}</div>${compareChoices}`;
  document.getElementById('stage-route').innerHTML = sceneWrap('Your selected packet', routeTitle, 'This is the route implied by your earlier choices. You can still rewind, compare, or switch route.', body, `<div class="btn-row"><button class="btn btn-secondary" onclick="showStage('archive')">Open archive</button><button class="btn btn-ghost" onclick="showStage('selector')">Switch route</button></div>`);
}

function renderArchive(){
  const items = metadata.archive_order.map(code=>{
    const d = metadata.docs[code]; if(!d) return '';
    const predecessor = metadata.recovery_core.includes(code) ? 'Core recovery' : metadata.recovery_annex.includes(code) ? 'K0 annex' : d.role;
    const lockedNote = code === 'K07' || code === 'R3Q' ? `<p class="mini"><strong>Annex role:</strong> add after the core test.</p>` : '';
    return `<div class="doc-card"><div class="meta">${code}</div><h3>${d.title}</h3>${statusBadge(d.status)}<p>${d.summary}</p><p class="mini"><strong>Role:</strong> ${d.role}<br><strong>Context:</strong> ${predecessor}</p>${lockedNote}<div class="btn-row"><button class="btn btn-secondary" onclick="openDoc('${d.file}')">Open</button>${metadata.branches[code]?`<button class="btn btn-ghost" onclick="inspectBranch('${code}')">Inspect</button>`:''}</div></div>`;
  }).join('');
  const body = `<div class="warning">Advanced access. This archive preserves codes, statuses, and reading context, but it bypasses the guided sequence.</div><div class="archive-grid">${items}</div>`;
  document.getElementById('stage-archive').innerHTML = sceneWrap('Controlled archive','Browse directly, but keep the canon visible.','This is the non-flat archive: every card carries status and route context.', body, `<button class="btn btn-ghost" onclick="backOne()">Back to previous step</button>`);
}

window.addEventListener('DOMContentLoaded', init);
