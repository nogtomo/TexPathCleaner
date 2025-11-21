import maya.cmds as cmds
import os

def strip_full_path_to_sourceimages():
    """
    シーン内のすべてのfileノードのテクスチャパスを
    'sourceimages'フォルダ以下からの相対パスに変換します。
    """
    
    # シーン内のすべてのfileノードを取得
    file_nodes = cmds.ls(type='file')
    
    if not file_nodes:
        print("シーン内にfileノード（テクスチャ）は見つかりませんでした。")
        return
    
    # sourceimages フォルダ名
    # Windows/Linux/Mac いずれの環境でも動作するようにパス区切りを考慮
    sourceimages_folder = 'sourceimages'
    
    print("--- テクスチャパスの相対パス化を開始 ---")
    
    for node in file_nodes:
        # 現在のテクスチャパスを取得
        current_path = cmds.getAttr(node + '.fileTextureName')
        
        # パスが空またはNoneの場合はスキップ
        if not current_path:
            print(f"警告: {node} のパスが空です。スキップします。")
            continue
            
        # パス区切り文字を正規化（Windowsの\を/に統一）
        normalized_path = current_path.replace('\\', '/')
        
        # 'sourceimages' がパスに含まれているかチェック
        if sourceimages_folder in normalized_path:
            
            # 'sourceimages' の位置を探す
            try:
                # sourceimagesとその後のパス区切り文字を含むインデックスを取得
                # 例: /path/to/project/sourceimages/texture.jpg
                #     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ この部分を削除したい
                index = normalized_path.index(sourceimages_folder)
                
                # 'sourceimages' から始まる部分を新しいパスとして取得
                new_relative_path = normalized_path[index:]
                
                # パスをfileノードに設定
                cmds.setAttr(node + '.fileTextureName', new_relative_path, type="string")
                
                print(f"✅ 更新: {node}")
                print(f"  旧パス: {current_path}")
                print(f"  新パス: {new_relative_path}")
                
            except ValueError:
                # index()で見つからないことは稀ですが、念のため
                print(f"エラー: {node} のパスに 'sourceimages' が見つかりませんでした。")
        else:
            print(f"スキップ: {node} のパスには 'sourceimages' が含まれていません。パス: {current_path}")

    print("--- テクスチャパスの相対パス化が完了しました ---")

# 関数を実行
strip_full_path_to_sourceimages()