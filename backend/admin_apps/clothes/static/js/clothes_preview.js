// 追加された画像の配列
let imageFiles = [];

// プレビューエリアのグローバル変数を定義
let previewArea;

// プレビューを表示する関数
function previewImages(input) {
    for (const file of input.files) {
        const reader = new FileReader();
        
        reader.onload = function (e) {
            const imgWrapper = createImageWrapper(e.target.result, file.name);
            previewArea.appendChild(imgWrapper); // プレビューに追加
            imageFiles.push(file); // 配列にファイルを追加
        };

        reader.readAsDataURL(file);
    }
}

// 画像を表示するためのラッパーを作成
function createImageWrapper(src, fileName) {
    const imgWrapper = document.createElement('div');
    imgWrapper.style.position = 'relative';
    imgWrapper.draggable = true; // ドラッグ可能にする

    const imgElement = document.createElement('img');
    imgElement.src = src;

    // モーダル機能を追加
    imgElement.onclick = function() {
        const modalImage = document.getElementById('modal-image');
        modalImage.src = src; // 拡大表示する画像を設定
        document.getElementById('image-modal').style.display = 'flex'; // モーダルを表示
    };

    // 削除ボタンを追加
    const deleteButton = document.createElement('button');
    deleteButton.classList.add('image-delete-button'); // クラスを追加
    deleteButton.innerText = '×';
    deleteButton.onclick = function () {
        imgWrapper.parentNode.removeChild(imgWrapper); // 削除
        imageFiles = imageFiles.filter(item => item.name !== fileName); // 配列から削除
    };

    imgWrapper.appendChild(imgElement);
    imgWrapper.appendChild(deleteButton);

    // ドラッグイベントのリスナーを追加
    imgWrapper.addEventListener('dragstart', function(event) {
        event.dataTransfer.setData('text/plain', fileName); // ファイル名をデータとして保存
        event.dataTransfer.effectAllowed = 'move'; // 移動を許可
    });

    imgWrapper.addEventListener('dragover', function(event) {
        event.preventDefault(); // デフォルトの動作を防ぐ
    });

    imgWrapper.addEventListener('drop', function(event) {
        event.preventDefault(); // デフォルトの動作を防ぐ

        const draggedFileName = event.dataTransfer.getData('text/plain');
        const draggedElement = [...previewArea.children].find(child => {
            const img = child.querySelector('img');
            return img && img.src.includes(draggedFileName);
        });

        if (draggedElement && draggedElement !== imgWrapper) {
            const previewImages = [...previewArea.children];
            const draggedIndex = previewImages.indexOf(draggedElement);
            const dropIndex = previewImages.indexOf(imgWrapper);

            // 画像の位置を入れ替え
            if (draggedIndex > dropIndex) {
                previewArea.insertBefore(draggedElement, imgWrapper);
            } else {
                previewArea.insertBefore(draggedElement, imgWrapper.nextSibling);
            }

            // imageFiles配列の順序も入れ替える
            const draggedFile = imageFiles[draggedIndex];
            // 配列からドラッグされた要素を削除
            imageFiles.splice(draggedIndex, 1);
            // 新しい位置に挿入
            imageFiles.splice(dropIndex, 0, draggedFile);
        }
    });

    return imgWrapper;
}

// 既存の画像をプレビューに表示
function addExistingImages() {
    imageFiles = []; // imageFilesを初期化
    existingImages.forEach(function(image) {
        const imgWrapper = createImageWrapper(imageDir + '/' + image, image);

        // 既存の画像情報を配列に追加（URLやファイル名）
        imageFiles.push(new File([], image, { type: 'image/jpeg' })); // 一旦ファイルとして追加

        // 削除ボタンを追加
        imgWrapper.querySelector('.image-delete-button').onclick = function () {
            previewArea.removeChild(imgWrapper);
            existingImages = existingImages.filter(img => img !== image); // 削除
            imageFiles = imageFiles.filter(item => item.name !== image); // imageFilesからも削除
        };

        previewArea.appendChild(imgWrapper);
    });
}

// 画像を保存する関数で fetch を使用
function saveImages(formData) {
    return fetch('/save-clothes-images/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Images saved successfully:', data);
    })
    .catch(error => {
        console.error('Error saving images:', error);
    });
}

// DOMが読み込まれた後に実行
document.addEventListener('DOMContentLoaded', function() {
    // previewAreaをここで初期化
    previewArea = document.getElementById('preview-area');
    previewArea.innerHTML = ''; // プレビューをクリア

    // ドロップイベントのリスナーを設定
    previewArea.addEventListener('dragover', function(event) {
        event.preventDefault();
    });

    previewArea.addEventListener('drop', function(event) {
        event.preventDefault();
        const files = event.dataTransfer.files;
        previewImages({ files });
    });

    // ページが読み込まれたら既存の画像を追加
    addExistingImages();

    // モーダルを閉じる処理
    document.getElementById('close-modal').onclick = function() {
        document.getElementById('image-modal').style.display = 'none'; // モーダルを非表示
    };

    // 保存ボタンのクリックイベント
    const saveButton = document.querySelector('input[name="_save"]');
    const adminForm = document.querySelector('#clothes_form'); // clothesモデル編集用フォーム

    saveButton.addEventListener('click', function(event) {
        event.preventDefault();

        // FormData オブジェクトを作成
        const formData = new FormData(adminForm);

        // 画像配列をループしてFormDataに追加
        imageFiles.forEach((image) => {
            formData.append('image-input', image); // 既存の画像は実際にはファイル名
        });

        // 画像保存を実行
        saveImages(formData).then(function() {
            adminForm.submit(); // 画像保存後にフォーム送信
        });
    });
});
