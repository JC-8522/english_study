# 资料、范围与阅读说明

词条由仓库原有的全部 37 份词汇文件合并而来；`INDEX.md` 只作为索引扫描，不作为词汇来源。原笔记与根目录的旧版主清单都保留原样。按用户后续要求，整理版移除了四个人名分类；这些词不在新主清单、分册或例句出处中保留。每个细分类存放在一个 [分册文件](../分册/) 中，可从 [分类阅读目录](../README.md) 直接打开。

同一拼写按 Unicode NFKC、大小写、弯引号、连字符和空格规范化后合并，保留释义与全部来源。不同词形、不同短语不强行合并。原表里误拆的 `Clef (Treble` 和 `Bass)` 修复为 `treble clef` 和 `bass clef`；旅游笔记里被误列为词条的两个栏目标题（四行）不当作单词。具体记录见 [manifest.json](manifest.json)。

每条词的来源文件、原行号和原词头见 [word-provenance.tsv](word-provenance.tsv)。原行号指 manifest 所记录的合并前 Git 提交，避免主文件改写后产生混淆。保留的未释义标签只演示如何在对话中引用字符串，未替原资料猜造释义。

## 例句

优先选择较短的日常对话，并为原笔记短语、专业场景、专名和不合适的原句补写例句。原笔记里的非标准拼写、其他语言词形和不自然的组合仍可查到；条目注明更自然说法时，例句练习该自然说法，而不是重复错误。

带链接的句子取自 [Tatoeba](https://tatoeba.org/)，未改写原句文字；句子链接可查看原文。使用 2026-11-07 的 [英语详细导出](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_detailed.tsv.bz2) 和 [CC0 英语导出](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_CC0.tsv.bz2)。

Tatoeba 句子按 [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) 或 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 使用。每句的作者、句子 ID、链接和适用许可完整列在 [example-attribution.tsv](example-attribution.tsv)。其中 `authored` 表示为本词单编写，`original note` 表示沿用原笔记例句。

## 发音与释义

- [CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict)：美式发音及重音；将 ARPAbet 转写为 IPA。原音节重音保留，IPA 的点号用于辅助拆读。许可见 [CMUdict.txt](licenses/CMUdict.txt)。
- [ECDICT](https://github.com/skywind3000/ECDICT)：补充原资料缺少的音标和中文释义，采用其 MIT 许可；见 [ECDICT.txt](licenses/ECDICT.txt)。保留其音标的条目可能采用英式音值。IPA 中 ˈ 表示主重音，ˌ 表示次重音。拼读中的大写音节重读。
- [Princeton WordNet 3.0](https://wordnet.princeton.edu/)：辅助词性和语义分类，结合原专题笔记与人工修正；见 [WordNet.txt](licenses/WordNet.txt)。
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng)：仅补充词典未覆盖项目的参考读音，所有此类读音明确标为“参考”，不视作词典核定读音。未分发程序或音频。

专名存在地区和个人读法差异。缩写若无可确认的惯用读法，给出字母拼读。没有足够上下文的字符串不伪装成已确认的常用英语词。原资料中的书面片段、学术词与品牌名在相应谈话场景中学习，不表示它们本身都是高频口语。

## 校验

在仓库根目录运行 `python tools/check_active_words.py`，检查原始来源覆盖（扣除用户明确排除的人名词条）、词头唯一、每类编号、读音与释义非空、每条两句例句、分类目录覆盖所有分册、所有本地目录链接，以及全部原文件未被修改或删除。

修改词条时，更新对应分册与出处记录。分类或条数变动时，同步更新目录和清单记录。校验报告见 [validation.json](validation.json)。
