// onChange関数はスプレッドシートの変更時のみトリガーします。
// このコードは脆弱なのでWebアプリとしてデプロイしたり、トリガーを設定したスプレッドシートは他人に共有しないでください。
function onChange(e) {
    //変更されたシートの取得
    const sheet = e.source.getActiveSheet();
    //シートの最終行取得
    const lastCol = sheet.getLastColumn();
    //ヘッダー行の最取得
    const header = sheet.getRange(1, 1, 1, lastCol).getValues()[0];
    //イベントに関わるカラムのindexを取得
    const title = header.indexOf('タイトル');
    const script = header.indexOf('スクリプト');
    const executionResult = header.indexOf('実行結果');
    const executionResult2 = header.indexOf('成否');

    //選択された範囲を取得
    const activeRange = sheet.getActiveRange();
    //編集された最初の行を取得
    const startRow = activeRange.getRow();
    //編集された最後の行を取得
    const endRow = activeRange.getLastRow();
    //編集された行の一覧を取得
    const rows = sheet.getRange(startRow, 1, endRow - startRow + 1, lastCol - 1).getValues();

    //変更が加えられた行のスクリプトを実行して「実行結果」のセルを変更
    rows.forEach((row, rowIndex) => {
        if ((row[title] !== '') && (row[script] !== '') && row[script] !== 'スクリプト'){
            try {
              // スクリプトの実行
              var code = "(function(){"+ row[script] + "})();"
              var result = eval(code);
              sheet.getRange(startRow + rowIndex, executionResult + 1).setValue(result);
              sheet.getRange(startRow + rowIndex, executionResult2 + 1).setValue("成功");
            } catch (error) {
              // エラー時のハンドリング
              sheet.getRange(startRow + rowIndex, executionResult + 1).setValue(error);
              sheet.getRange(startRow + rowIndex, executionResult2 + 1).setValue("失敗");
            }
        }
    });
}

