/* ======================================
    1. config
========================================= */
const MAX_CARDS = 5;
const MIN_CARDS = 1;

/* ======================================
    2. 要素の取得
========================================= */
const allCards = document.querySelector('.training-post-card');
const addBtn = document.querySelector('.add-btn');
const removeBtns = document.querySelectorAll('.remove-btn');
const mainSelects = document.querySelectorAll('.main-select');

/* ======================================
    3. ボタン制御と状態の更新   
========================================= */
function updateButtonStatus() {
    const visibleCards = document.querySelectorAll('.training-post-card.is-visible')
    const visibleCardCnt = visibleCards.length
    
    addBtn.style.display = (visibleCardCnt === MAX_CARDS) ? 'none':'flex';

    removeBtns.forEach(btn => {
        btn.disabled = (visibleCardCnt === MIN_CARDS);
    })

    allCards.forEach(card => {
        const inputs = card.querySelectorALL('input, select');
        const isvisible = card.classList.continas('.is-visible');

        inputs.forEach(input => {
            input.disabled = !isvisible;
        })
    })
}

/* ======================================
    4. その他欄の切り替え
========================================= */
mainSelects.forEach(select => {
    select.addEventListener('change', () => {
        const currentCard = select.closest('.training-post-card')
        const otherInput = currentCard.querySelector('.other-input-wrapper')
        
        if (select.value === 'other') {
            otherInput.style.display = 'block'
            otherInput.querySelector('input').disabled = false;
            input.required = true; // ここ確認
        } else {
            otherInput.style.display = 'none'
            otherInput.querySelector('input').disabled = true;
            input.required = false; // ここ確認
        }
    })
})

/* ======================================
    5. 追加ボタン
========================================= */
addBtn.addEventListener('click', () => {
    const hiddenCards = document.querySelectorAll('.training-post-card:not(.is-visible)');
    const nextCard = hiddenCards[0];
    
    if (nextCard) {
        nextCard.classList.add('is-visible');
        updateButtonStatus();
    }
})

/* ======================================
    6. 削除ボタン
========================================= */
removeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const currentCard = btn.closest('.training-post-card');
        const inputs = currentCard.querySelectorAll('input, select');
        
        currentCard.classList.remove('is-visible');
        
        inputs.forEach(input => input.value = '');

        const otherInput = currentCard.querySelector('.other-input-wrapper');
        if (otherInput) {
            otherInput.style.display = 'none';
        }

        currentCard.parentNode.appendChild(currentCard);
        updateButtonStatus();
    })
})

/* ======================================
    7. 初期化
========================================= */
updateButtonStatus();
