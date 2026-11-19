"""Reader-facing checks for the supermarket vocabulary expansion."""
import json
from pathlib import Path
import re
import unittest

from check_active_words import canonical_spelling

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / '分类词库'


class SupermarketVocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = {}
        for path in (LIBRARY / '分册').glob('*.md'):
            text = path.read_text(encoding='utf8')
            for match in re.finditer(r'^\d+\. \*\*(.*?)\*\*，(.+)$', text, re.M):
                cls.entries[match.group(1).casefold()] = (text.splitlines()[0][2:], match.group(2))
        cls.manifest = json.loads((LIBRARY / '资料/manifest.json').read_text(encoding='utf8'))

    def test_fish_bass_is_not_pronounced_like_musical_bass(self):
        category, entry = self.entries['bass']
        self.assertEqual(category, '饮食 / 食材 / 水产 / 食用鱼类')
        self.assertIn('/bæs/（鲈鱼类）', entry)
        self.assertIn('/beɪs/（音乐低音）', entry)
        self.assertIn('（鲈鱼类）BAS', entry)
        self.assertIn('（音乐低音）BAYS', entry)
        self.assertIn('美式易读：SEE bas，', self.entries['sea bass'][1])
        self.assertNotIn('bays', self.entries['sea bass'][1].casefold())

    def test_preexisting_food_names_are_findable_as_food(self):
        expected = {
            'broccoli': '叶菜花菜与甘蓝', 'spinach': '叶菜花菜与甘蓝',
            'garlic': '根茎与葱蒜', 'mushroom': '菌菇芽苗与竹笋',
            'figs': '水果', 'almond': '坚果与种子', 'anchovy': '食用鱼类',
        }
        for word, group in expected.items():
            with self.subTest(word=word):
                self.assertTrue(self.entries[word][0].startswith('饮食 / 食材 / '))
                self.assertTrue(self.entries[word][0].endswith(group))
        self.assertNotIn('fig', self.entries)
        self.assertNotIn('diaper', self.manifest['supplemental_batches'][-1]['words'])

    def test_supermarket_coverage_and_distinct_citrus(self):
        for word in ('pomelo','grapefruit','cauliflower','bok choy','tempeh','ground beef',
                     'cottage cheese','unit price','free sample','laundry detergent',
                     'plastic wrap','baby formula','cat litter'):
            with self.subTest(word=word):
                self.assertIn(word, self.entries)
        self.assertIn('柚子', self.entries['pomelo'][1])
        self.assertIn('葡萄柚', self.entries['grapefruit'][1])
        self.assertEqual(self.entries['pomelo'][0], '饮食 / 食材 / 水果')
        self.assertEqual(self.entries['grapefruit'][0], '饮食 / 食材 / 水果')

    def test_reading_chunks_keep_r_with_the_following_stressed_vowel(self):
        for word, expected in {
            'aroma':'uh-ROH-muh', 'arugula':'uh-ROO-guh-luh',
            'oregano':'uh-REHG-uh-noh', 'tangerine':'tan-juh-REEN',
        }.items():
            with self.subTest(word=word):
                self.assertIn('美式易读：' + expected + '，', self.entries[word][1])

    def test_equivalent_spelling_variants_cannot_be_added_as_new_words(self):
        self.assertEqual(canonical_spelling('JALAPEÑO'), canonical_spelling('jalapeno'))
        self.assertEqual(canonical_spelling('Rib Eye'), canonical_spelling('rib-eye'))
        self.assertEqual(canonical_spelling('WHOLE GRAIN'), canonical_spelling('whole-grain'))


if __name__ == '__main__':
    unittest.main()
