// Simple local demo state (replace with real backend later)
const state = {
  user: null,
  templates: [
    { id: 'default', name: 'Default Minutes', description: 'Concise minutes with actions and decisions.', sections: ['Title','Date/Time','Attendees','Agenda','Decisions','Action Items','Risks','Next Meeting'] },
    { id: 'board', name: 'Board Meeting', description: 'Formal structure for board sessions.', sections: ['Title','Date/Time','Attendees','Agenda','Resolutions','Motions','Votes','Action Items'] },
    { id: 'sprint', name: 'Sprint Review', description: 'Engineering review and planning notes.', sections: ['Sprint','Participants','Highlights','Metrics','Demos','Decisions','Backlog','Action Items'] }
  ],
  selectedTemplateId: null,
  transcript: '',
  minutes: null,
  minutesHistory: []
};

// Elements
const views = {
  dashboard: document.getElementById('view-dashboard'),
  templates: document.getElementById('view-templates'),
  minutes: document.getElementById('view-minutes'),
  account: document.getElementById('view-account'),
};
const navButtons = document.querySelectorAll('.nav-item');
const templatePreview = document.getElementById('template-preview');
const transcriptEl = document.getElementById('transcript');
const minutesPreview = document.getElementById('minutes-preview');
const templatesList = document.getElementById('templates-list');
const minutesList = document.getElementById('minutes-list');
const userEmailSpan = document.getElementById('user-email');
const authModal = document.getElementById('auth-modal');
const authForm = document.getElementById('auth-form');
const closeAuth = document.getElementById('close-auth');
const logoutBtn = document.getElementById('logout');
const rememberCb = document.getElementById('remember');
const accountEmail = document.getElementById('account-email');
const accountPassword = document.getElementById('account-password');
const accountRemember = document.getElementById('account-remember');
const saveAccount = document.getElementById('save-account');
// Template editor fields
const tplName = document.getElementById('tpl-name');
const tplDesc = document.getElementById('tpl-desc');
const tplSections = document.getElementById('tpl-sections');
const tplPrompts = document.getElementById('tpl-prompts');
const saveTemplateBtn = document.getElementById('save-template');

// Routing
function showView(name){
  Object.values(views).forEach(v=>v.classList.add('hidden'));
  views[name].classList.remove('hidden');
  navButtons.forEach(b=>b.classList.toggle('active', b.dataset.view===name));
}

// Auth (demo only: stores hashed-ish password in localStorage)
function shaBase(s){ // very naive; replace with real hashing server-side
  let h=0; for(let i=0;i<s.length;i++){ h=((h<<5)-h)+s.charCodeAt(i); h|=0; } return 'p'+Math.abs(h);
}
function keyUser(ns){
  if(!state.user) return `${ns}:guest`;
  const id = state.user.email.toLowerCase();
  return `users:${id}:${ns}`;
}

function loadUserData(){
  // Load per-user templates and minutes from storage
  try{
    const tplKey = keyUser('templates');
    const minKey = keyUser('minutes');
    const t = localStorage.getItem(tplKey);
    const m = localStorage.getItem(minKey);
    if(t){ state.templates = JSON.parse(t); }
    if(m){ state.minutesHistory = JSON.parse(m); }
  }catch(e){ console.warn('Failed to load user data', e); }
}

function persistUserData(){
  try{
    const tplKey = keyUser('templates');
    const minKey = keyUser('minutes');
    localStorage.setItem(tplKey, JSON.stringify(state.templates));
    localStorage.setItem(minKey, JSON.stringify(state.minutesHistory));
  }catch(e){ console.warn('Failed to persist user data', e); }
}

function saveSession(user, persist){
  state.user = user;
  userEmailSpan.textContent = user?.email || 'Guest';
  accountEmail.value = user?.email || '';
  if(persist){ localStorage.setItem('session', JSON.stringify(user)); }
  else { sessionStorage.setItem('session', JSON.stringify(user)); }
  loadUserData();
  renderTemplates();
  renderTemplatePreview();
  renderMinutesHistory();
}
function loadSession(){
  const saved = localStorage.getItem('session') || sessionStorage.getItem('session');
  if(saved){ state.user = JSON.parse(saved); userEmailSpan.textContent = state.user.email; accountEmail.value = state.user.email; loadUserData(); }
}
function signOut(){
  state.user = null; userEmailSpan.textContent = 'Guest'; accountEmail.value='';
  localStorage.removeItem('session'); sessionStorage.removeItem('session');
}

// UI Renderers
function renderTemplatePreview(){
  const tpl = state.templates.find(t=>t.id===state.selectedTemplateId);
  if(!tpl){ templatePreview.innerHTML = '<span class="muted">No template selected.</span>'; return; }
  templatePreview.innerHTML = `
    <div class="card">
      <h4>${tpl.name}</h4>
      <p class="muted">${tpl.description}</p>
      <div>${tpl.sections.map(s=>`<span class="badge">${s}</span>`).join(' ')}</div>
    </div>`;
}

function renderTemplates(){
  templatesList.innerHTML = state.templates.map(t=>`
    <div class="card">
      <h4>${t.name}</h4>
      <p class="muted">${t.description}</p>
      <div style="margin:8px 0;">${t.sections.slice(0,6).map(s=>`<span class="badge">${s}</span>`).join(' ')}</div>
      <button class="btn small" data-select-template="${t.id}">Use Template</button>
      <button class="btn small ghost" data-edit-template="${t.id}">Edit</button>
    </div>
  `).join('');
}

function renderMinutes(){
  const m = state.minutes;
  if(!m){ minutesPreview.innerHTML = '<span class="muted">No minutes yet. Generate to preview.</span>'; return; }
  minutesPreview.innerHTML = Object.entries(m).map(([k,v])=>{
    const title = k.split('_').map(w=>w[0].toUpperCase()+w.slice(1)).join(' ');
    const body = Array.isArray(v) ? `<ul>${v.map(x=>`<li>${x}</li>`).join('')}</ul>` : `<p>${v}</p>`;
    return `<h4>${title}</h4>${body}`;
  }).join('');
}

function renderMinutesHistory(){
  minutesList.innerHTML = state.minutesHistory.map((item, idx)=>`
    <div class="row">
      <div>
        <div><strong>${item.title || 'Untitled Minutes'}</strong></div>
        <div class="muted" style="font-size:12px">${new Date(item.ts).toLocaleString()} • Template: ${item.template || '—'}</div>
      </div>
      <div>
        <button class="btn small" data-view-minutes-idx="${idx}">View</button>
        <button class="btn small ghost" data-delete-minutes-idx="${idx}">Delete</button>
      </div>
    </div>
  `).join('');
}

// Fake API calls (replace with serverless endpoints)
async function apiTranscribe(file){
  // In demo, we just return a placeholder string
  return 'Sample transcript: Discuss project timeline, budget risks, and action items for next sprint.';
}
async function apiGenerateMinutes(transcript, template){
  // In demo, we emulate a structured response based on the template sections
  const byKey = (name, text)=> ({title: name, text});
  const map = {
    'Title': 'Project Sync — Week 12',
    'Date/Time': new Date().toLocaleString(),
    'Attendees': 'A. Smith, B. Lee, C. Patel',
    'Agenda': ['Timeline update', 'Budget review', 'Risks', 'Next steps'],
    'Decisions': ['Push release by 1 week', 'Reduce scope of v1'],
    'Action Items': ['Alice: finalize timeline (Fri)', 'Ben: update budget (Thu)', 'Chris: draft comms (Mon)'],
    'Risks': ['Vendor delay on API', 'Limited QA bandwidth'],
    'Next Meeting': 'Next Tue 10:00 AM'
  };
  const result = {};
  template.sections.forEach(s=>{
    const key = s.toLowerCase().replace(/\s+/g,'_');
    result[key] = Array.isArray(map[s]) ? map[s] : (map[s] || '');
  });
  return result;
}

// Events
document.getElementById('choose-template').addEventListener('click',()=> showView('templates'));
document.getElementById('change-template').addEventListener('click',()=> showView('templates'));
document.getElementById('clear-transcript').addEventListener('click',()=>{ state.transcript=''; transcriptEl.value=''; });
document.getElementById('generate').addEventListener('click', async ()=>{
  const tpl = state.templates.find(t=>t.id===state.selectedTemplateId) || state.templates[0];
  state.selectedTemplateId = tpl.id;
  const minutes = await apiGenerateMinutes(state.transcript || transcriptEl.value, tpl);
  state.minutes = minutes; renderMinutes();
  const title = minutes.title || 'Project Minutes';
  state.minutesHistory.unshift({ ts: Date.now(), template: tpl.name, title, minutes });
  persistUserData();
  renderMinutesHistory();
});

document.getElementById('template-file').addEventListener('change', async (e)=>{
  const file = e.target.files?.[0]; if(!file) return;
  try{
    const text = await file.text();
    const data = JSON.parse(text);
    if(!data.id) data.id = (data.name || 'custom').toLowerCase().replace(/[^a-z0-9]+/g,'-');
    state.templates.push(data);
    renderTemplates();
    alert('Template imported.');
  }catch(err){ alert('Invalid template file. Expected JSON.'); }
});

document.getElementById('audio-input').addEventListener('change', async (e)=>{
  const file = e.target.files?.[0]; if(!file) return;
  const t = await apiTranscribe(file);
  state.transcript = t; transcriptEl.value = t; showView('dashboard');
});

templatesList.addEventListener('click', (e)=>{
  const btn = e.target.closest('button[data-select-template]');
  const edit = e.target.closest('button[data-edit-template]');
  if(btn){
    state.selectedTemplateId = btn.getAttribute('data-select-template');
    renderTemplatePreview();
    showView('dashboard');
  }
  if(edit){
    const id = edit.getAttribute('data-edit-template');
    const t = state.templates.find(x=>x.id===id);
    if(t){
      tplName.value = t.name || '';
      tplDesc.value = t.description || '';
      tplSections.value = (t.sections || []).join(', ');
      tplPrompts.value = t.prompts ? JSON.stringify(t.prompts, null, 2) : '';
    }
  }
});

saveTemplateBtn.addEventListener('click', ()=>{
  const name = tplName.value.trim() || 'Custom Template';
  const id = name.toLowerCase().replace(/[^a-z0-9]+/g,'-');
  const description = tplDesc.value.trim();
  const sections = tplSections.value.split(',').map(s=>s.trim()).filter(Boolean);
  let prompts = undefined;
  if(tplPrompts.value.trim()){
    try{ prompts = JSON.parse(tplPrompts.value); }
    catch(e){ alert('Prompts must be valid JSON.'); return; }
  }
  const existingIdx = state.templates.findIndex(t=>t.id===id);
  const tpl = { id, name, description, sections, prompts };
  if(existingIdx>=0) state.templates[existingIdx] = tpl; else state.templates.push(tpl);
  persistUserData();
  renderTemplates();
  alert('Template saved for your account.');
});

minutesList.addEventListener('click', (e)=>{
  const v = e.target.closest('button[data-view-minutes-idx]');
  const d = e.target.closest('button[data-delete-minutes-idx]');
  if(v){ const idx = +v.getAttribute('data-view-minutes-idx'); state.minutes = state.minutesHistory[idx].minutes; showView('dashboard'); renderMinutes(); }
  if(d){ const idx = +d.getAttribute('data-delete-minutes-idx'); state.minutesHistory.splice(idx,1); persistUserData(); renderMinutesHistory(); }
});

document.getElementById('clear-minutes').addEventListener('click', ()=>{
  if(confirm('Delete all saved minutes?')){ state.minutesHistory = []; persistUserData(); renderMinutesHistory(); }
});

// Auth events
authForm.addEventListener('submit', (e)=>{
  e.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const persist = rememberCb.checked;
  if(!email || !password) return;
  const storedUsers = JSON.parse(localStorage.getItem('users') || '{}');
  if(!storedUsers[email]){
    storedUsers[email] = { password: shaBase(password) };
  }else{
    if(storedUsers[email].password !== shaBase(password)){
      alert('Incorrect password'); return;
    }
  }
  localStorage.setItem('users', JSON.stringify(storedUsers));
  saveSession({ email }, persist);
  authModal.classList.add('hidden');
});

closeAuth.addEventListener('click', ()=> authModal.classList.add('hidden'));
logoutBtn.addEventListener('click', ()=>{ signOut(); authModal.classList.remove('hidden'); });
saveAccount.addEventListener('click', ()=>{
  if(!state.user){ alert('Not signed in.'); return; }
  const email = state.user.email;
  const newPass = accountPassword.value.trim();
  const persist = accountRemember.checked;
  const users = JSON.parse(localStorage.getItem('users') || '{}');
  if(newPass){ users[email] = { password: shaBase(newPass) }; localStorage.setItem('users', JSON.stringify(users)); accountPassword.value=''; }
  saveSession({ email }, persist);
  alert('Settings saved');
});

// Nav
navButtons.forEach(b=> b.addEventListener('click', ()=> showView(b.dataset.view)));
document.getElementById('new-meeting').addEventListener('click', ()=>{ showView('dashboard'); transcriptEl.value=''; state.transcript=''; state.minutes=null; renderMinutes(); });

// Initial load
function init(){
  loadSession();
  renderTemplates();
  renderTemplatePreview();
  renderMinutes();
  renderMinutesHistory();
  if(!state.user){ authModal.classList.remove('hidden'); }
  showView('dashboard');
}
init();
