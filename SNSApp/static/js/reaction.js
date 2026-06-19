const forms = document.querySelectorAll('.reaction')

forms.forEach(function(form) {
    form.addEventListener(
        'submit', async function(event){
            event.preventDefault();

            if (!event.submitter) {
            console.error("【原因候補1】event.submitter が取得できません。");
            return;
            }

            const formData = new FormData(form);
            const clickedReactionId = event.submitter.value; // クリックされたボタンのvalue値
            formData.append('reaction_id', clickedReactionId);

            console.log("送信したリアクションID:", clickedReactionId);

            const response =
            await fetch(
                form.action, {
                method : 'POST',
                body: formData
                }
            )
            const data = await response.json();
            console.log("サーバーからのレスポンス：", data);

            // 画面の数字を書き換える
            if (data.reaction_count) {
                data.reaction_count.forEach(item => {
                    // item.id と clickedReactionId を文字列に統一して比較
                    if (String(item.id) === String(clickedReactionId)) {
                        console.log(`IDが一致しました。対象ID: ${item.id}, 新しいカウント数: ${item.count}`);

                        // 【ここを修正】event.submitter（クリックされたボタン）の中から直接 .count-text を探す
                        const countElement = event.submitter.querySelector('.count-text');
                        
                        if (countElement) {
                            console.log("HTML要素を見つけました。数値を書き換えます:", countElement);
                            countElement.innerText = item.count;
                        } else {
                            console.error("【原因候補2】ボタンの中に .count-text クラスの要素が見つかりません。");
                        }
                    }
                    // // 押されたボタンのvalue(reaction_id)と、届いたデータのidが一致するか確認
                    // if(event.submitter.value == item.id) {
                    //     // フォーム内にある数字を表示している要素(count-text)
                    //     const countElement = form.querySelector('.count-text');
                    //     if(countElement) {
                    //         // 数字を最新のカウントに書き換える
                    //         countElement.innerText = item.count;
                    //     }
                    // }
                    
                })
            }
        }
    )
});