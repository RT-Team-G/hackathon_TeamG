document.addEventListener('DOMContentLoaded' , () => {
/* ======================================
    1. config
========================================= */
const INITIAL_TIME_SECONDS = 60;
const ONE_SECOND_MS = 1000;
const SECONDS_PER_MINUTE = 60;
const alarmSound = new Audio('https://assets.mixkit.co/active_storage/sfx/995/995-preview.mp3');

let timerLeft = INITIAL_TIME_SECONDS;
let timerId = null;

/* ======================================
    2. 要素の取得
========================================= */
const toggleBtn = document.getElementById('toggle-btn');
const resetBtn = document.getElementById('reset-btn');
const timerDisplay = document.getElementById('timer-display');
const adjustBtns = document.querySelectorAll('.btn-adjust');

/* ======================================
    3. UIの更新・制御関数
========================================= */
// 時間表示整え(mm:ss)
function updateDisplay() {
    const s = (timerLeft % SECONDS_PER_MINUTE).toString().padStart(2, '0');
    const m = Math.floor(timerLeft / SECONDS_PER_MINUTE).toString().padStart(2, '0');
    timerDisplay.textContent = `${m}:${s}`;
}

// ボタンの制御
function setButtonsState(isRunning) {
    if (isRunning) {
        toggleBtn.textContent = 'ストップ';
        toggleBtn.classList.add('is-active');
    } else {
        toggleBtn.textContent = 'スタート';
        toggleBtn.classList.remove('is-active');
    }

    adjustBtns.forEach(btn => {
        btn.disabled = isRunning;
    });
}

/* ======================================
    4. タイマーエンジン
========================================= */
function startCountdown() {
    if (timerId !== null) {
        clearInterval(timerId);
    }
    timerId = setInterval(() => {
        timerLeft--;
        updateDisplay();
        
        if (timerLeft <= 0) {
            stopCountdown();
            alarmSound.play();
        }
    }, ONE_SECOND_MS);
}

function stopCountdown() {
    clearInterval(timerId);
    timerId = null;
    setButtonsState(false);
}

/* ======================================
    5. イベントリスナー
========================================= */
// スタートとストップを統合
toggleBtn.addEventListener('click', () => {
    if (timerId === null) {
        if (timerLeft > 0) {
            setButtonsState(true);
            startCountdown();
        }
    } else {
        stopCountdown()
    }
})

// リセットボタン押下時の挙動
resetBtn.addEventListener('click', () => {
    stopCountdown()
    timerLeft = INITIAL_TIME_SECONDS;
    updateDisplay();
})

// 時間の追加の処理
adjustBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const addTime = parseInt(btn.dataset.time, 10);
        if (!isNaN(addTime)) {
            timerLeft += addTime;
            updateDisplay();
        }
    })
})
    
/* ======================================
    6. 初期化
========================================= */
updateDisplay();
setButtonsState(false);
})






















