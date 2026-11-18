"""Pronunciation examples independent of vocabulary chapter generation."""
import unittest

from american_reading import is_letter_spelling, letter_spelling, make_reading


class AmericanReadingTests(unittest.TestCase):
    def reading(self, word, ipa, stress=''):
        return make_reading(word, ipa, stress)

    def test_user_reviewed_burglary(self):
        spelling, notes, reference, letters = self.reading('burglary', '/ˈbɝɡləri/')
        self.assertEqual(spelling, 'BUR-gluh-ree')
        self.assertIn('burger', notes)
        self.assertIn('gluh：轻读', notes)
        self.assertIn('ree：非重读，像 see 里的 ee', notes)
        self.assertFalse(reference or letters)

    def test_unpredictable_english_spelling(self):
        examples = {
            'colonel': ('/ˈkɝ.nəl/', 'KUR-nuhl'),
            'receipt': ('/rɪˈsit/', 'rih-SEET'),
            'rough': ('/rʌf/', 'RUHF'),
            'thought': ('/θɔt/', 'THAWT'),
            'thorough': ('/ˈθɝ.oʊ/', 'THUR-oh'),
        }
        for word, (ipa, expected) in examples.items():
            with self.subTest(word=word):
                self.assertEqual(self.reading(word, ipa)[0], expected)

    def test_rhotic_vowels_have_matching_explanations(self):
        spelling, notes, *_ = self.reading('tear', '/tɪr/（眼泪）或 /tɛr/（撕裂）')
        self.assertEqual(spelling, '（眼泪）TEER；（撕裂）TAIR')
        self.assertIn('eer 像 near 的 ear', notes)
        self.assertIn('air 像 air 的读音', notes)
        self.assertNotIn('像 sit', notes)
        self.assertNotIn('像 bed', notes)
        self.assertEqual(self.reading('car', '/kɑr/')[0], 'KAR')
        self.assertIn('ar 像 car 的 ar', self.reading('car', '/kɑr/')[1])

    def test_distinct_short_oo_and_long_oo(self):
        self.assertEqual(self.reading('book', '/bʊk/')[0], 'BUUK')
        self.assertEqual(self.reading('moon', '/mun/')[0], 'MOON')
        self.assertIn('book', self.reading('book', '/bʊk/')[1])
        self.assertIn('moon', self.reading('moon', '/mun/')[1])

    def test_schwa_and_stressed_uh_are_explained_separately(self):
        self.assertEqual(self.reading('about', '/əˈbaʊt/')[0], 'uh-BOWT')
        self.assertIn('嘴放松、短促轻读', self.reading('about', '/əˈbaʊt/')[1])
        self.assertIn('uh 像 cup 的 u', self.reading('cup', '/kʌp/')[1])

    def test_closed_short_vowel_for_easy_reading(self):
        self.assertEqual(self.reading('happy', '/ˈhæ.pi/')[0], 'HAP-ee')
        self.assertEqual(self.reading('shiver', '/ˈʃɪ.vɚ/')[0], 'SHIHV-er')
        self.assertEqual(self.reading('referral', '/rɪˈfɝ.əl/')[0], 'rih-FUR-uhl')

    def test_initialisms_and_pronoun_i(self):
        spelling, notes, _, letters = self.reading('CNN', '/ˈsi.ˈɛ.ˈnɛn/')
        self.assertEqual(spelling, '字母拼读 SEE EHN EHN')
        self.assertEqual(notes.count('字母 N：'), 2)
        self.assertTrue(letters)
        spelling, notes, *_ = self.reading('BMW', letter_spelling('BMW'))
        self.assertEqual(spelling, '字母拼读 BEE EHM DUHB-uhl-yoo')
        self.assertIn('字母 W：', notes)
        self.assertFalse(is_letter_spelling('I', '/aɪ/', '单音节'))
        spelling, notes, *_ = make_reading('HMM', '/hm/', '', {
            'pronunciation': letter_spelling('HMM'), 'letters': True,
        })
        self.assertEqual(spelling, '字母拼读 AYCH EHM EHM')
        self.assertNotIn('犹豫', notes)
        spelling, notes, reference, letters = self.reading('rgb', '参考 /ˌɑːɹdʒˌiːbˈiː/')
        self.assertEqual(spelling, '参考 字母拼读 AR JEE BEE')
        self.assertTrue(reference and letters)

    def test_variants_retain_word_class_and_different_stress(self):
        spelling, notes, *_ = self.reading('convict', '/kənˈvɪkt/（动词）；/ˈkɑnvɪkt/（名词）')
        self.assertEqual(spelling, '（动词）kuhn-VIHKT；（名词）KAHN-vihkt')
        self.assertIn('VIHKT：重读', notes)
        self.assertIn('vihkt：非重读', notes)

    def test_phrase_boundaries_and_secondary_stress(self):
        spelling, notes, *_ = self.reading('have goosebumps', '/hæv ˈɡus.ˌbʌmps/')
        self.assertEqual(spelling, 'HAV GOOS-buhmps')
        self.assertIn('buhmps：次重读', notes)

    def test_unverified_input_stays_reference(self):
        spelling, _, reference, _ = self.reading('test label', '参考 /ˈtɛst ˈleɪ.bəl/')
        self.assertTrue(spelling.startswith('参考 '))
        self.assertTrue(reference)
        spelling, _, reference, _ = make_reading('test', '/tɛst/', '',
            {'pronunciation': '/tɛst/', 'reference': True})
        self.assertTrue(spelling.startswith('参考 '))
        self.assertTrue(reference)

    def test_consonant_only_speech_sounds(self):
        self.assertEqual(self.reading('hmm', '/hm/')[0], 'hm')
        self.assertIn('闭嘴发 m 的鼻音', self.reading('hmm', '/hm/')[1])
        self.assertEqual(self.reading('sch', '参考 /ʃ/')[0], '参考 sh')
        self.assertIn('不另加元音', self.reading('sch', '参考 /ʃ/')[1])

    def test_unknown_symbols_do_not_silently_disappear(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported IPA'):
            self.reading('bad input', '/kæt#/')
        with self.assertRaisesRegex(ValueError, 'Missing IPA'):
            self.reading('bad input', 'unknown')


if __name__ == '__main__':
    unittest.main()
