year_list = ['2021', '2020', '2019']
school_list = ['Z会', 'ベネッセ', '河合塾']

zkai_exam_list = ['共通テスト実践模試', 'センター直前トライアル']
bene_exam_list = ['ベネッセ・駿台マーク模試', 'ベネッセ・駿台記述模試', '総合学力マーク模試']
kawai_exam_list = ['全統記述模試', '全統マーク模試', '全統共通マーク模試', 'センターKパック']


subject_list = ['国語', '数学①', '数学②',
                '英語(筆記)', '英語(リスニング)', '理科①', '理科②', '公民', '地歴A', '地歴B']

def divide_exam(school):
    if school == 'Z会':
        return zkai_exam_list
    if school == 'ベネッセ':
        return bene_exam_list
    if school == '河合塾':
        return kawai_exam_list
