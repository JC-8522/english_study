"""Regression checks for practical meanings, categories and context-sensitive US readings."""
from pathlib import Path
import unittest

from add_american_reading_guides import ENTRY
from check_active_words import normalize

LIBRARY = Path(__file__).resolve().parents[1] / '分类词库'


class DailyDomainVocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = {}
        for path in (LIBRARY / '分册').glob('*.md'):
            text = path.read_text(encoding='utf8')
            category = text.splitlines()[0][2:]
            for match in ENTRY.finditer(text):
                _, word, ipa, spelling, notes, stress, meaning, first, second = match.groups()
                cls.entries[normalize(word)] = dict(category=category, ipa=ipa, spelling=spelling,
                    notes=notes, meaning=meaning, first=first, second=second)

    def test_practical_coverage_across_all_fourteen_domains(self):
        for word in ('deadlift', 'dumbbell', 'pickup game', 'free throw', 'restraining order',
                     'credit score', 'tax return', 'ballot measure', 'jet lag', 'drywall',
                     'split the check', 'medium-rare', 'cappuccino', 'margarita',
                     'freezing rain', 'carbon footprint', 'pothos', 'tire rotation',
                     'light rail', 'HOV lane'):
            with self.subTest(word=word):
                self.assertIn(normalize(word), self.entries)

    def test_familiar_spellings_include_the_missing_daily_senses(self):
        for word, required in {
            'reps': ('重复次数', 'reps'), 'quad': ('股四头肌', 'quads'),
            'prune': ('修剪', 'prune'), 'cabinet': ('内阁', 'cabinet'),
            'shoulder': ('路肩', 'shoulder'), 'commute': ('通勤', 'commute'),
            'annual': ('一年生', 'annuals'), 'cola': ('可乐', 'cola'),
        }.items():
            with self.subTest(word=word):
                entry = self.entries[word]
                self.assertIn(required[0], entry['meaning'])
                self.assertIn(required[1], entry['first'] + entry['second'])
        self.assertNotIn('rep', self.entries)  # Existing reps covers repetitions.

    def test_actual_meanings_determine_primary_chapters(self):
        for word, expected in {
            'roster': '比赛规则与赛程', 'layup': '球类动作与得分',
            'deposition': '庭审证据与裁决', 'siding': '建筑结构与建材',
            'ecosystem': '生态保护与水土资源', 'groundwater': '生态保护与水土资源',
            'cola': '果汁软饮与其他饮品', 'magnolia': '花草',
            'sedan': '机动车与骑行工具', 'locomotive': '铁路与地铁',
            'street food': '菜式与餐次', 'chess': '游戏爱好与休闲',
        }.items():
            with self.subTest(word=word):
                self.assertTrue(self.entries[word]['category'].endswith(expected))

    def test_context_selects_noun_adjective_or_vehicle_pronunciation(self):
        self.assertEqual(self.entries['moped']['spelling'], 'MOH-pehd')
        self.assertTrue(self.entries['wind chill']['spelling'].startswith('WIHND '))
        self.assertTrue(self.entries['wind advisory']['spelling'].startswith('WIHND '))
        self.assertIn('REE-fuhnd', self.entries['tax refund']['spelling'])
        self.assertNotIn('ayt', self.entries['separate checks']['spelling'])
        self.assertTrue(self.entries['use-by date']['spelling'].startswith('YOOZ '))

    def test_initialisms_are_read_as_letters(self):
        for word in ('APR', 'APY', 'EV', 'IPA', 'RBI'):
            with self.subTest(word=word):
                entry = self.entries[normalize(word)]
                self.assertTrue(entry['spelling'].startswith('字母拼读 '))
        self.assertIn('AYCH OH VEE', self.entries['hov lane']['spelling'])

    def test_easy_to_confuse_american_terms_are_distinguished(self):
        for word, required in {
            'sleet': '冰粒', 'freezing rain': '液态雨滴',
            'entrée': '美国菜单', 'apple cider': '苹果汁',
            'hard cider': '含酒精', 'corked': '木塞污染',
            'impeachment': '不等于免职', 'disposable income': '税款后',
        }.items():
            with self.subTest(word=word):
                self.assertIn(required, self.entries[normalize(word)]['meaning'])


if __name__ == '__main__':
    unittest.main()
