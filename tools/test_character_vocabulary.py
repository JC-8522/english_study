"""Reader-facing regressions for abstract character words and easily confused senses."""
from pathlib import Path
import unittest

from add_american_reading_guides import ENTRY
from check_active_words import canonical_spelling, normalize

LIBRARY=Path(__file__).resolve().parents[1]/'分类词库'


class CharacterVocabularyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries={}
        for path in (LIBRARY/'分册').glob('*.md'):
            text=path.read_text(encoding='utf8')
            category=text.splitlines()[0][2:]
            for match in ENTRY.finditer(text):
                _,word,ipa,spelling,notes,stress,meaning,first,second=match.groups()
                cls.entries[normalize(word)]=dict(category=category,ipa=ipa,spelling=spelling,
                    notes=notes,stress=stress,meaning=meaning,first=first,second=second)

    def test_requested_cupidity_has_a_wealth_sense_and_clear_register(self):
        e=self.entries['cupidity']
        self.assertIn('财富',e['meaning'])
        self.assertIn('偏书面',e['meaning'])
        self.assertIn('greed',e['meaning'])
        self.assertEqual(e['spelling'],'kyoo-PIHD-uh-tee')
        self.assertEqual(e['stress'],'主重音第2音节')
        self.assertTrue(e['category'].endswith('金钱欲望与物质观'))

    def test_colloquial_and_literary_words_are_both_present_without_flattening_register(self):
        for word in ('entitled','hypocrisy','gullible','stingy','grudge','tact','empathy',
                     'insecurity','resilience','tenacity','disingenuous','avarice'):
            with self.subTest(word=word):
                self.assertIn(word,self.entries)
        self.assertIn('偏书面',self.entries['avarice']['meaning'])
        self.assertIn('贬义口语',self.entries['brown-noser']['meaning'])
        self.assertIn('偏书面',self.entries['sycophant']['meaning'])
        self.assertIn('贬义',self.entries['stingy']['meaning'])

    def test_contrasting_psychological_senses_are_explained(self):
        self.assertIn('证据',self.entries['skeptical']['meaning'])
        self.assertIn('私利',self.entries['cynical']['meaning'])
        self.assertIn('冲突',self.entries['ambivalent']['meaning'])
        self.assertIn('不在意',self.entries['indifferent']['meaning'])
        self.assertIn('优待',self.entries['entitlement']['meaning'])
        self.assertIn('资格',self.entries['entitled']['meaning'])
        self.assertIn('自豪',self.entries['proudly']['meaning'])

    def test_old_personality_words_are_findable_by_their_actual_meanings(self):
        for word,category in {
            'greed':'金钱欲望与物质观','greedy':'金钱欲望与物质观',
            'vain':'自负虚荣与优越感','vanity':'自负虚荣与优越感',
            'conceit':'自负虚荣与优越感','patronizing':'自负虚荣与优越感',
            'petty':'嫉妒怨怼与报复心','empathetic':'同理心善意与冷漠',
            'cynicism':'信任怀疑与轻信','autobiography':'书籍文学与写作',
        }.items():
            with self.subTest(word=word):
                self.assertTrue(self.entries[word]['category'].endswith(category))
        self.assertIn('虚荣',self.entries['vain']['meaning'])
        self.assertIn('小心眼',self.entries['petty']['meaning'])
        self.assertIn('勇气',self.entries['guts']['meaning'])

    def test_spelling_alternatives_use_one_headword(self):
        for head,variants in {
            'naivete':('naïveté','naivety'), 'pretense':('pretence',),
            'skepticism':('scepticism',), 'rancor':('rancour',),
            'tightfisted':('tight-fisted',),
        }.items():
            with self.subTest(word=head):
                self.assertIn(head,self.entries)
                for variant in variants:
                    self.assertNotIn(variant,self.entries)
                same=[key for key in self.entries if canonical_spelling(key)==canonical_spelling(head)]
                self.assertEqual(same,[head])


if __name__=='__main__':unittest.main()
