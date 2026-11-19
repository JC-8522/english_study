# 资料、范围与阅读说明

原有词条由仓库的全部 37 份词汇文件合并而来；`INDEX.md` 只作为索引扫描，不作为词汇来源。原笔记与根目录的旧版主清单都保留原样。按用户后续要求，整理版移除了四个人名分类；这些词不在新主清单、分册或例句出处中保留。每个细分类存放在一个 [分册文件](../分册/) 中，可从 [分类阅读目录](../README.md) 直接打开。

同一拼写按 Unicode NFKC、大小写、弯引号、连字符和空格规范化后合并，保留释义与全部来源。不同词形、不同短语不强行合并。原表里误拆的 `Clef (Treble` 和 `Bass)` 修复为 `treble clef` 和 `bass clef`；旅游笔记里被误列为词条的两个栏目标题（四行）不当作单词。具体记录见 [manifest.json](manifest.json)。

原有词条的来源文件、原行号和原词头见 [word-provenance.tsv](word-provenance.tsv)。原行号指 manifest 所记录的合并前 Git 提交，避免主文件改写后产生混淆。保留的未释义标签只演示如何在对话中引用字符串，未替原资料猜造释义。

新增的进阶日常词汇按使用场景直接收入现有分册。新增词头记录在 [manifest.json](manifest.json) 的 `supplemental_words` 中，例句为新写。读音按美式标注。短语给出一种常见的重读方式，实际说话时重读可以随语境变化。

常用词查漏参考 [SUBTLEX-US 美式影视字幕词频](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus) 和 [New General Service List 1.2](https://www.newgeneralservicelist.com/new-general-service-list)。根据中级学习需求筛选，优先收录有实际使用场景、词库缺少的词头，如 `burglary`、`wheeze` 和 `snarky`。词频帮助发现缺口，释义和例句为自编。

## 超市场景补词

2026-11-19 按逛超市的场景补充 371 条词汇，范围参考 [Safeway 的果蔬货区](https://www.safeway.com/shop/mf/aisles/fruits-vegetables) 和 [Costco 的食品与家用品分区](https://www.costco.com/grocery-household.html)。覆盖食材、食品标签、熟食冷冻食品、清洁护理用品、包装规格、会员优惠与结账。按货区阅读可用[超市购物导览](../超市购物导览.md)。

新增词头记录在 `manifest.json` 的 `supplemental_batches` 中，每条新增词汇有两句自编日常口语例句。新增前与全库比对大小写、空格、连字符、重音符号等拼写差异，并检查常见单复数形式。已有的 `diaper` 继续使用原词条；已收录的 `figs` 移入水果类。本次不增加另一个 `fig` 词条。

同步复核食材分类：将西兰花、菠菜、葱蒜、可食用菌、常见水果与鱼类等 118 个已有词重新归类，拆分原来的肉蛋海鲜、蔬菜豆类及谷物坚果混合分册。保留原分册地址为跳转页；修正 27 个已有词的明确释义或例句问题，例如将 `anchovy` 的公园观察句改为点餐和调味用法，将 `cranberry` 明确为蔓越莓。全部原始来源文件保持原样。

鱼类名称参考 [FDA Seafood List](https://www.hfpappexternal.fda.gov/scripts/fdcc/index.cfm?set=SeafoodList&showAll=true&type=basic)，区分市场通称与具体鱼类。`bass` 在一个词条内列出 /bæs/ 的鱼义与 /beɪs/ 的音乐义；`sea bass`、`branzino` 等按各自常见用途收录。读音以 CMUdict 和编写的美式 IPA 为基础，并对照 Merriam-Webster 校对易混读法，例如 [bass](https://www.merriam-webster.com/dictionary/bass)、[clementine](https://www.merriam-webster.com/dictionary/clementine)、[fillet](https://www.merriam-webster.com/dictionary/fillet) 等。

`aroma` 的美式易读改为 **uh-ROH-muh**，对照 [Merriam-Webster 的读法](https://www.merriam-webster.com/dictionary/aroma)，让 r 与第二段的重读元音相连。原始笔记及原有音标不改写。

## 例句

优先选择较短的日常对话，并为原笔记短语、专业场景、专名和不合适的原句补写例句。原笔记里的非标准拼写、其他语言词形和不自然的组合仍可查到；条目注明更自然说法时，例句练习该自然说法，而不是重复错误。

带链接的句子取自 [Tatoeba](https://tatoeba.org/)，未改写原句文字；句子链接可查看原文。使用 2026-11-07 的 [英语详细导出](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_detailed.tsv.bz2) 和 [CC0 英语导出](https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_CC0.tsv.bz2)。

Tatoeba 句子按 [CC BY 2.0 FR](https://creativecommons.org/licenses/by/2.0/fr/) 或 [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) 使用。每句的作者、句子 ID、链接和适用许可完整列在 [example-attribution.tsv](example-attribution.tsv)。其中 `authored` 表示为本词单编写，`original note` 表示沿用原笔记例句。

## 发音与释义

每个整理版词条在读音后提供「美式易读」和「读法理解」。按音段给出可连读的英文字母提示，并说明重读、元音参照词及前后辅音。格式、符号和完整示例见[美式易读说明](../美式易读说明.md)。整理版的明确错误可复核校正，原始来源文件保留原样。

新增字段优先根据现有美式 IPA 转写。原音标来自英式补充资料时，另用 CMUdict 对应的美式拼写读法；无美式词典对应项时，使用 eSpeak NG en-us 参考并显式标「参考」。补充来源及专门处理的短语、缩写记录在 [american-reading-overrides.json](american-reading-overrides.json)。这份记录只用于新字段；原音标不改写。原来未核定的参考读音继续保留参考标记。

- [CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict)：美式发音及重音；将 ARPAbet 转写为 IPA。原音节重音保留，IPA 的点号用于辅助拆读。许可见 [CMUdict.txt](licenses/CMUdict.txt)。
- [ECDICT](https://github.com/skywind3000/ECDICT)：补充原资料缺少的音标和中文释义，采用其 MIT 许可；见 [ECDICT.txt](licenses/ECDICT.txt)。保留其音标的条目可能采用英式音值。IPA 中 ˈ 表示主重音，ˌ 表示次重音。拼读中的大写音节重读。
- [Princeton WordNet 3.0](https://wordnet.princeton.edu/)：辅助词性和语义分类，结合原专题笔记与人工修正；见 [WordNet.txt](licenses/WordNet.txt)。
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng)：仅补充词典未覆盖项目的参考读音，所有此类读音明确标为“参考”，不视作词典核定读音。未分发程序或音频。

专名存在地区和个人读法差异。缩写若无可确认的惯用读法，给出字母拼读。没有足够上下文的字符串不伪装成已确认的常用英语词。原资料中的书面片段、学术词与品牌名在相应谈话场景中学习，不表示它们本身都是高频口语。

## 分类复核

按词头、释义和语境检查全库。使用词典和 [Multilingual E5](https://huggingface.co/intfloat/multilingual-e5-small) 在本地对照主题，再复核易混项与过宽的分册。地名分组参考 [GeoNames](https://www.geonames.org/export/) 的行政区和城市数据，并按词条实际含义区分同名地点、机构和普通名词。

雪利酒词条中的 `flor` 用法参考[赫雷斯产区委员会的陈年说明](https://www.sherry.wine/sherry-wine/production/ageing)。

多义词保留一个主分册，优先选择和本条例句一致的词义。明确发现释义或例句错用时一并修正，例如把点啤酒时的 `beers` 和 `stout` 放在「啤酒与酿造」。无法可靠判定的词形和上下文放在「原始资料附录」。单个分册最多 100 条，原分册拆开后可通过旧地址查看对应的新分册。

饮食按食材、菜式、饮料、烹饪和营养组织。例如，椰子按日常饮食用法归入水果，维生素归入营养，点餐用语归入餐厅点餐与用餐。其他主题也按实际用途拆开，例如「酒店房型与入住退房」和「行程与观光」，以及「信用贷款与债务」和「账户转账与账单」。目录保留被拆分或更名的分册地址。

## 校验

在仓库根目录运行 `python tools/check_active_words.py`，检查原始来源覆盖（扣除用户明确排除的人名词条）、词头唯一、每类编号、读音与释义非空、美式易读与逐段解释覆盖、每条两句例句、分册条数上限、分类目录及旧分册跳转，以及全部原文件未被修改或删除。

修改词条读音或补充读音记录后，运行 `python tools/add_american_reading_guides.py` 更新两个新字段；运行时不需要网络或第三方 Python 包。用 `python tools/add_american_reading_guides.py --check` 检查是否存在未同步的字段。美式音段转换的专项测试命令为 `python -m unittest discover -s tools -p "test_american_reading.py"`。

运行 `python -m unittest discover -s tools -p "test_*.py"` 可同时检查超市场景的词义、分类、美式读法及拼写去重规则。

修改词条时，更新对应分册与出处记录。分类或条数变动时，同步更新目录和清单记录。校验报告见 [validation.json](validation.json)。
