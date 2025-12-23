async function getJSON(url, options) {
const res = await fetch(url, options);
const data = await res.json().catch(() => ({}));
if (!res.ok || (data && data.ok === false)) {
    const msg = (data && data.error) ? data.error : `요청 실패 (${res.status})`;
    throw new Error(msg);
}
return data;
}

const form      = document.querySelector('#predict-form');
const lineSel   = form.querySelector('#line_no');
const dirSel    = form.querySelector('#direction');
const hourSel   = form.querySelector('#hour_input');
const btn       = form.querySelector('#btnPredict');
const loader    = form.querySelector('#loader');
const errBox    = form.querySelector('#error');

const resultBox = document.querySelector('#result');
const rLine     = document.querySelector('#r-line');
const rDir      = document.querySelector('#r-dir');
const rBand     = document.querySelector('#r-band');
const rProb     = document.querySelector('#r-prob');
const rAcc      = document.querySelector('#r-acc');
const rPrec     = document.querySelector('#r-prec');
const rRec      = document.querySelector('#r-rec');
const rF1       = document.querySelector('#r-f1');
const rMax      = document.querySelector('#r-max');
const rExp      = document.querySelector('#r-exp');
const rRmse     = document.querySelector('#r-rmse');
const rMae      = document.querySelector('#r-mae');
const cmBox     = document.querySelector('#cm-container');

function setLoading(isLoading) {
loader.style.display = isLoading ? 'block' : 'none';
btn.disabled = isLoading; // 버튼만 잠금
}
function setError(msg='') { errBox.textContent = msg; }
function clearResult() {
resultBox.style.display = 'none';
[rLine,rDir,rBand,rProb,rAcc,rPrec,rRec,rF1,rMax,rExp,rRmse,rMae].forEach(el=>el.textContent='');
cmBox.innerHTML = '';
}

async function initPage() {
try {
    const init = await getJSON('/api/init');
    // 노선
    lineSel.innerHTML = '<option value="" disabled selected>노선을 선택하세요</option>';
    (init.known_lines || []).forEach(l => {
    const opt = document.createElement('option');
    opt.value = l; opt.textContent = l;
    lineSel.appendChild(opt);
    });
    // 시간(HH:MM)
    hourSel.innerHTML = '';
    (init.allowed_hours || []).forEach(h => {
    const opt = document.createElement('option');
    opt.value = h; opt.textContent = h;
    hourSel.appendChild(opt);
    });
    // 방향 초기화
    dirSel.innerHTML = '<option value="" disabled selected>노선을 먼저 선택하세요</option>';
    dirSel.disabled = true;
} catch (e) {
    setError(`초기 데이터 로드 오류: ${e.message}`);
}
}

async function loadDirections(lineVal) {
dirSel.innerHTML = '<option value="" disabled selected>방향을 선택하세요</option>';
dirSel.disabled = true;
if (!lineVal) return;
try {
    const data = await getJSON(`/api/directions/${encodeURIComponent(lineVal)}`);
    (data.directions || []).forEach(d => {
    const opt = document.createElement('option');
    opt.value = d; opt.textContent = d;
    dirSel.appendChild(opt);
    });
    dirSel.disabled = false;
} catch (e) {
    setError(`방향 로드 오류: ${e.message}`);
}
}

function renderConfusionMatrix(cmObj) {
cmBox.innerHTML = '';
if (!cmObj || !Array.isArray(cmObj.matrix)) return;
const M = cmObj.matrix; // [[TN,FP],[FN,TP]] (행=실제, 열=예측)

if (!Array.isArray(M) || M.length !== 2 || M[0].length !== 2 || M[1].length !== 2) {
    cmBox.textContent = '혼동행렬 형식이 올바르지 않습니다.';
    return;
}

// 요청 형식: 열=예측(1→0), 행=실제(1→0)
// 실제=1: [TP, FN] = [M[1][1], M[1][0]]
// 실제=0: [FP, TN] = [M[0][1], M[0][0]]
const table = document.createElement('table');
table.className = 'cm';

const thead = document.createElement('thead');
thead.innerHTML = `<tr><th></th><th>예측=1</th><th>예측=0</th></tr>`;
table.appendChild(thead);

const tbody = document.createElement('tbody');
const tr1 = document.createElement('tr');
tr1.innerHTML = `<th>실제=1</th><td>${M[1][1]}</td><td>${M[1][0]}</td>`;
const tr0 = document.createElement('tr');
tr0.innerHTML = `<th>실제=0</th><td>${M[0][1]}</td><td>${M[0][0]}</td>`;
tbody.appendChild(tr1);
tbody.appendChild(tr0);
table.appendChild(tbody);

cmBox.appendChild(table);
}

function renderResult(r, m) {
rLine.textContent = r['노선'];
rDir.textContent  = r['방향'];
rBand.textContent = r['시간'];
rProb.textContent = r['지연발생확률(%)'];

rAcc.textContent  = (m && typeof m.accuracy  === 'number') ? (m.accuracy  * 100).toFixed(2) : '';
rPrec.textContent = (m && typeof m.precision === 'number') ? (m.precision * 100).toFixed(2) : '';
rRec.textContent  = (m && typeof m.recall    === 'number') ? (m.recall    * 100).toFixed(2) : '';
rF1.textContent   = (m && typeof m.f1        === 'number') ? (m.f1        * 100).toFixed(2) : '';

rMax.textContent  = r['예측_최대지연분'];
rExp.textContent  = r['기대_지연분'];
rRmse.textContent = (m && typeof m.rmse === 'number') ? m.rmse.toFixed(2) : '';
rMae.textContent  = (m && typeof m.mae  === 'number') ? m.mae.toFixed(2)  : '';

renderConfusionMatrix(m && m.confusion_matrix);
resultBox.style.display = 'block';
}

async function handleSubmit(e) {
e.preventDefault();
clearResult(); setError('');
if (!form.checkValidity()) { setError('입력값을 확인해 주세요.'); return; }

const payload = {
    line_no: String(lineSel.value),
    direction: String(dirSel.value),
    hour: String(hourSel.value)
};

try {
    setLoading(true);
    const data = await getJSON('/api/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
    });
    renderResult(data.result, data.metrics);
} catch (e) {
    setError(`예측 실패: ${e.message}`);
} finally {
    setLoading(false);
}
}

lineSel.addEventListener('change', (e) => {
dirSel.value = '';
loadDirections(e.target.value);
});
form.addEventListener('submit', handleSubmit);

initPage();