document.addEventListener('DOMContentLoaded' , () => {
    /* ======================================
        1. config
    ========================================= */
    const MAX_CARDS = 5;
    const MIN_CARDS = 1;

    /* ======================================
        2. 要素の取得
    ========================================= */
    const allCards = document.querySelectorAll('.training-post-card');
    const addBtn = document.querySelector('.add-btn');
    const removeBtns = document.querySelectorAll('.remove-btn');
    const mainSelects = document.querySelectorAll('.main-select');

    /* ======================================
        3. ボタン制御と状態の更新   
    ========================================= */
    function updateButtonStatus() {
        const visibleCards = document.querySelectorAll('.training-post-card.is-visible')
        const visibleCardCnt = visibleCards.length
        
        addBtn.disabled = (visibleCardCnt === MAX_CARDS);  // 追加　もず
        addBtn.style.display = (visibleCardCnt === MAX_CARDS) ? 'none':'flex';

        removeBtns.forEach(btn => {
            btn.disabled = (visibleCardCnt === MIN_CARDS);
        })

        allCards.forEach(card => {
            const inputs = card.querySelectorAll('input, select');  // ALL→All もず
            const mainSelect = card.querySelector('.main-select');  // 必須選択肢
            const isvisible = card.classList.contains('is-visible');  // continas→contains もず

            inputs.forEach(input => {
                input.disabled = !isvisible;  // .isvisible→isvisible もず
            })

            // 表示されているカードのセレクトボックスだけを必須にする もず
            if (mainSelect) {
                if (isvisible) {
                    mainSelect.required = true;  // 必須にする
                } else {
                    mainSelect.required = false;  // 必須を解除する
                }
                
                // mainSelect.required = isvisible;  ←削除　もず
            }
        })
    }

    // /* ======================================
    //     4. その他欄の切り替え
    // ========================================= */
    // mainSelects.forEach(select => {
    //     select.addEventListener('change', () => {
    //         const currentCard = select.closest('.training-post-card')
    //         const otherInput = currentCard.querySelector('.other-input-wrapper')
            
    //         if (select.value === 'other') {
    //             otherInput.style.display = 'block'
    //             otherInput.querySelector('input').disabled = false;
    //             input.required = true; // ここ確認
    //         } else {
    //             otherInput.style.display = 'none'
    //             otherInput.querySelector('input').disabled = true;
    //             input.required = false; // ここ確認
    //         }
    //     })
    // })

    /* ======================================
        5. 追加ボタン
    ========================================= */
    // 1. HTMLからボタン要素を探して変数「addBtn」に代入する（htmlとの紐づけに必要）
    // const addBtn = document.querySelector('.add-btn');  // 再宣言となっているため不要(エラー出る)

    addBtn.addEventListener('click', () => {
        const hiddenCards = document.querySelectorAll('.training-post-card:not(.is-visible)');
        const nextCard = hiddenCards[0];
        
        if (nextCard) {
            nextCard.classList.add('is-visible');

            // // 表示されたカードのセレクトボックスを必須入力にする
            // const select = nextCard.querySelector('.main-select');
            // if (select) select.required = true;　　←削除　もず

            updateButtonStatus();
        }
    })

    /* ======================================
        6. 削除ボタン
    ========================================= */
    // 画面全体のクリックを監視し、✕ボタン（.remove-btn）が押された時だけ処理を実行します
    document.addEventListener('click', (e) => {
        // クリックされた要素、またはその親に .remove-btn があるかチェック
        const btn = e.target.closest('.remove-btn');
        if (!btn || btn.disabled) return; // ボタンがない、または無効化されていれば無視

        const currentCard = btn.closest('.training-post-card');
        if (!currentCard) return;

        const inputs = currentCard.querySelectorAll('input, select');
        
        // カードを非表示にする
        currentCard.classList.remove('is-visible');
        
        // 入力値を安全に初期化
        inputs.forEach(input => {
            if (input.tagName === 'SELECT') {
                input.selectedIndex = 0;
            } else {
                input.value = '';
            }
        });

        // 状態を更新
        currentCard.parentNode.appendChild(currentCard); // 非表示にしたカード要素を末尾へ移動
        updateButtonStatus();
    });

    /* ======================================
        6. 初期化
    ========================================= */
    updateButtonStatus();

    // removeBtns.forEach(btn => {
    //     btn.addEventListener('click', () => {
    //         const currentCard = btn.closest('.training-post-card');  // btn.closest ではなく e.target.closest に変更してクリックされたカードを正確に特定
    //         const inputs = currentCard.querySelectorAll('input, select');
            
    //         currentCard.classList.remove('is-visible');
            
    //         // 入力値を安全に初期化
    //         inputs.forEach(input => {
    //             if (input.tagName === 'SELECT') {
    //                 input.selectedIndex = 0;
    //             } else {
    //                 input.value = '';
    //             }
    //         });

    //         // inputs.forEach(input => input.value = '');

    //         // const otherInput = currentCard.querySelector('.other-input-wrapper');
    //         // if (otherInput) {
    //         //     otherInput.style.display = 'none';
    //         // }

    //         // currentCard.parentNode.appendChild(currentCard);
    //         updateButtonStatus();
    //     })
    // })

    // /* ======================================
    //     7. 初期化
    // ========================================= */
    // updateButtonStatus();
})