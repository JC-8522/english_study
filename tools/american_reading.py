"""Readable American pronunciation and Chinese syllable notes, using stdlib only.

The spelling is a learning aid defined in 分类词库/美式易读说明.md.
IPA remains the pronunciation reference; boundaries are aids for joining sounds.
"""
from dataclasses import dataclass
import re


# spelling, familiar English anchor, Chinese explanation
VOWELS = {
    'æ': ('a', 'cat', 'a'),
    'ɑ': ('ah', 'father', 'a'),
    'ɔ': ('aw', 'law', 'aw'),
    'ʌ': ('uh', 'cup', 'u'),
    'ə': ('uh', '', '嘴放松，短促轻读 /ə/'),
    'ɝ': ('ur', 'bird', 'ir（带美式 r 音）'),
    'ɚ': ('er', 'teacher', 'er（轻读，带美式 r 音）'),
    'ɛ': ('eh', 'bed', 'e'),
    'ɪ': ('ih', 'sit', 'i'),
    'i': ('ee', 'see', 'ee'),
    'ʊ': ('uu', 'book', 'oo（短音）'),
    'u': ('oo', 'moon', 'oo'),
    'eɪ': ('ay', 'day', 'ay'),
    'oʊ': ('oh', 'go', 'o'),
    'aɪ': ('eye', 'eye', '整个词的元音'),
    'aʊ': ('ow', 'cow', 'ow'),
    'ɔɪ': ('oy', 'boy', 'oy'),
}
CONSONANTS = {
    'b': 'b', 'tʃ': 'ch', 'd': 'd', 'ð': 'dh', 'f': 'f', 'ɡ': 'g',
    'h': 'h', 'dʒ': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
    'ŋ': 'ng', 'p': 'p', 'r': 'r', 's': 's', 'ʃ': 'sh', 't': 't',
    'θ': 'th', 'v': 'v', 'w': 'w', 'j': 'y', 'z': 'z', 'ʒ': 'zh',
    'ɾ': 'dd', 'ʔ': "'",
}
PHONEMES = sorted([*VOWELS, *CONSONANTS], key=len, reverse=True)
ONSETS = {
    tuple(value.split()) for value in (
        'b', 'tʃ', 'd', 'ð', 'f', 'ɡ', 'h', 'dʒ', 'k', 'l', 'm', 'n',
        'p', 'r', 's', 'ʃ', 't', 'θ', 'v', 'w', 'j', 'z', 'ʒ', 'ɾ', 'ʔ',
        'p l', 'p r', 'b l', 'b r', 't r', 'd r', 'k l', 'k r', 'ɡ l',
        'ɡ r', 'f l', 'f r', 'θ r', 'ʃ r', 's p', 's t', 's k', 's m',
        's n', 's l', 's w', 't w', 'd w', 'k w', 'ɡ w', 's p l',
        's p r', 's t r', 's k r', 's k w', 's k l', 'k j', 'm j',
        'b j', 'p j', 'f j', 'v j', 'h j',
    )
}
LETTER_IPA = dict(zip(
    'abcdefghijklmnopqrstuvwxyz',
    ('eɪ', 'bi', 'si', 'di', 'i', 'ɛf', 'dʒi', 'eɪtʃ', 'aɪ', 'dʒeɪ',
     'keɪ', 'ɛl', 'ɛm', 'ɛn', 'oʊ', 'pi', 'kju', 'ɑr', 'ɛs', 'ti',
     'ju', 'vi', 'ˈdʌb.əl.ju', 'ɛks', 'waɪ', 'zi')
))


@dataclass(frozen=True)
class Syllable:
    onset: tuple
    vowel: str
    coda: tuple
    stress: int
    single: bool

    @property
    def nucleus(self):
        if self.coda[:1] == ('r',):
            rhotic = {
                'ɪ': ('eer', 'near', 'ear'), 'i': ('eer', 'near', 'ear'),
                'ɛ': ('air', 'air', '整个词的读音'),
                'ɑ': ('ar', 'car', 'ar'), 'ɔ': ('or', 'more', 'ore'),
                'ə': ('er', 'teacher', 'er（轻读，带美式 r 音）'),
            }
            if self.vowel in rhotic:
                return (*rhotic[self.vowel], self.coda[1:])
        return (*VOWELS[self.vowel], self.coda)

    @property
    def spelling(self):
        vowel_spelling, _, _, remaining_coda = self.nucleus
        onset = ''.join(CONSONANTS[p] for p in self.onset)
        coda = ''.join(CONSONANTS[p] for p in remaining_coda)
        value = onset + vowel_spelling + coda
        return value.upper() if self.stress == 1 else value

    @property
    def note(self):
        emphasis = ('单音节' if self.single and self.stress == 1 else
                    '重读' if self.stress == 1 else
                    '次重读' if self.stress == 2 else
                    '轻读' if self.vowel in ('ə', 'ɚ') else '非重读')
        spelling, anchor, sound, remaining_coda = self.nucleus
        nucleus = (f'{spelling} 像 {anchor} 的读音' if sound.startswith('整个词') else
                   f'{spelling} 像 {anchor} 的 {sound}' if anchor else
                   'uh 是 /ə/，嘴放松、短促轻读')
        onset = ''.join(CONSONANTS[p] for p in self.onset)
        coda = ''.join(CONSONANTS[p] for p in remaining_coda)
        edges = []
        if onset:
            edges.append(f'前接 {onset} 的音')
        if coda:
            edges.append(f'后接 {coda} 的音')
        if 'ɾ' in self.onset + self.coda:
            edges.append('dd 表示美式 t/d 的轻弹音，舌尖轻碰一下')
        if 'ʔ' in self.onset + self.coda:
            edges.append("' 表示喉咙短暂闭合的停顿")
        ending = '，' + '、'.join(edges) if edges else ''
        return f'{self.spelling}：{emphasis}，{nucleus}{ending}'


@dataclass(frozen=True)
class ConsonantSound:
    phones: tuple

    @property
    def spelling(self):
        return ''.join(CONSONANTS[p] for p in self.phones)

    @property
    def note(self):
        if self.phones == ('ʃ',):
            return 'sh：辅音，像 ship 开头的 sh，不另加元音'
        if self.phones == ('h', 'm'):
            return 'hm：语气声，先轻呼气，再闭嘴发 m 的鼻音，表示思考或犹豫'
        return f'{self.spelling}：按所列辅音连读，不另加元音'


def canonical_ipa(text):
    """Normalize equivalent symbols used by the existing pronunciation sources."""
    return (text.replace('ɹ', 'r').replace('g', 'ɡ').replace('ә', 'ə')
            .replace('ɐ', 'ə').replace('ᵻ', 'ɪ').replace('ɜ', 'ɝ')
            .replace('n̩', 'ən').replace('l̩', 'əl')
            .replace('ː', '').replace(':', ''))


def tokenize(ipa):
    ipa = canonical_ipa(ipa)
    phones, stress, boundaries = [], {}, set()
    pending = 0
    pos = 0
    while pos < len(ipa):
        char = ipa[pos]
        if char in 'ˈˌ':
            pending = 1 if char == 'ˈ' else 2
            pos += 1
            continue
        if char == '.':
            boundaries.add(len(phones))
            pos += 1
            continue
        phone = next((p for p in PHONEMES if ipa.startswith(p, pos)), None)
        if phone is None:
            raise ValueError(f'Unsupported IPA symbol {ipa[pos:]!r} in {ipa!r}')
        if phone in VOWELS:
            stress[len(phones)] = pending
            pending = 0
        phones.append(phone)
        pos += len(phone)
    if pending:
        raise ValueError(f'Stress mark without a vowel: {ipa!r}')
    return phones, stress, boundaries


def syllables(ipa):
    phones, stress, boundaries = tokenize(ipa)
    vowels = [index for index, phone in enumerate(phones) if phone in VOWELS]
    if not vowels:
        if not phones:
            raise ValueError(f'Empty pronunciation: {ipa!r}')
        return [ConsonantSound(tuple(phones))]
    starts = [0]
    for left, right in zip(vowels, vowels[1:]):
        explicit = sorted(point for point in boundaries if left < point <= right)
        if explicit:
            starts.append(explicit[-1])
            continue
        cluster = phones[left + 1:right]
        onset = 0
        for size in range(1, len(cluster) + 1):
            if tuple(cluster[-size:]) in ONSETS:
                onset = size
        starts.append(right - onset)
    # Close a stressed short vowel with the following consonant (HAP-ee,
    # SHIHV-er). These are reading chunks, not a claim about lexical syllables.
    for index in range(len(vowels) - 1):
        left, right = vowels[index:index + 2]
        if (phones[left] in ('æ', 'ɛ', 'ɪ', 'ʌ', 'ʊ') and stress[left] == 1
                and stress[right] == 0 and starts[index + 1] == left + 1
                and starts[index + 1] < right):
            starts[index + 1] += 1
    result = []
    for index, vowel in enumerate(vowels):
        end = starts[index + 1] if index + 1 < len(starts) else len(phones)
        level = stress[vowel]
        # A full isolated monosyllable is stressed; reduced ə/ɚ keep their weak form.
        if len(vowels) == 1 and level == 0 and phones[vowel] not in ('ə', 'ɚ'):
            level = 1
        result.append(Syllable(tuple(phones[starts[index]:vowel]), phones[vowel],
                               tuple(phones[vowel + 1:end]), level, len(vowels) == 1))
    return result


def ipa_variants(pronunciation):
    variants = []
    matches = list(re.finditer(r'/([^/]+)/', pronunciation))
    if not matches:
        raise ValueError(f'Missing IPA: {pronunciation!r}')
    for index, match in enumerate(matches):
        following = pronunciation[match.end(): matches[index + 1].start() if index + 1 < len(matches) else None]
        label = re.match(r'（([^）]+)）', following)
        variants.append((match.group(1).strip(), label.group(1) if label else ''))
    return variants


def letter_spelling(word):
    return '/'+ ' '.join(LETTER_IPA[c] for c in word.lower()) + '/'


def is_letter_spelling(word, pronunciation, stress):
    if not re.fullmatch('[a-zA-Z]+', word):
        return False
    if '字母' in stress:
        return True
    def compact(value):
        readings = re.findall(r'/([^/]+)/', value)
        if readings:
            value = ''.join(readings)
        return re.sub(r'[\s/.ˈˌ]', '', canonical_ipa(value))
    return len(word) > 1 and compact(pronunciation) == compact(letter_spelling(word))


def make_reading(word, pronunciation, stress, override=None):
    reference = pronunciation.startswith('参考')
    letters = is_letter_spelling(word, pronunciation, stress)
    if override:
        pronunciation = override['pronunciation']
        reference = reference or override.get('reference', False)
        letters = override.get('letters', is_letter_spelling(word, pronunciation, stress))
    if letters:
        pronunciation = letter_spelling(word)
    spellings, notes = [], []
    for ipa, label in ipa_variants(pronunciation):
        words = ipa.split()
        chunks = [syllables(item) for item in words]
        spelling = ' '.join('-'.join(s.spelling for s in group) for group in chunks)
        note_groups = []
        for index, group in enumerate(chunks):
            note = '；'.join(s.note for s in group)
            if letters:
                note = f'字母 {word[index].upper()}：' + note
            note_groups.append(note)
        explanation = '；'.join(note_groups)
        if word.casefold() == 'burglary':
            # The format explicitly reviewed by the reader.
            spelling = 'BUR-gluh-ree'
            explanation = ('BUR：重读，类似 burger 开头的读音；'
                           'gluh：轻读，uh 表示很轻的 /ə/，前面加 gl 的音；'
                           'ree：非重读，像 see 里的 ee，前面加 r 的音')
        prefix = f'（{label}）' if label else ''
        spellings.append(prefix + spelling)
        notes.append(prefix + explanation)
    spelling = '；'.join(spellings)
    explanation = '；'.join(notes)
    if letters:
        spelling = '字母拼读 ' + spelling
    if reference:
        spelling = '参考 ' + spelling
    return spelling, explanation, reference, letters
