# build-tools

**A helper for Claude that builds small tools that work.**

Original skill by Laith Harb (https://github.com/lionlaith7) · Maintained by Laith Harb (lionlaith7), Jordan.

## What is this?

A **skill** is a set of instructions that you give to Claude, the AI.
This skill tells Claude how to build a small tool, test it, and write simple notes about it.

A **tool** can be:
- a module for an Android phone (Magisk or KernelSU),
- a script (a list of commands that a computer runs),
- a command-line program (you type commands in a terminal),
- a web page (you open it in a browser).

## Why was it made?

Many tools break, or they do things nobody tested.
This skill makes Claude check every part before saying "it works".
It also makes sure the notes are clear, so anyone can understand the tool.

## What does it do?

1. **Asks only what it needs.** It starts with simple choices, not long questions.
2. **Builds a small version first.** Then it adds one feature at a time.
3. **Tests each feature.** If a feature cannot be tested, it is left out, and Claude says why.
4. **Writes the notes:**
   - `README.md` for GitHub visitors,
   - `README.txt` for people using the tool on their device,
   - `AI.md` for AI models that will change the tool later,
   - `CHANGELOG.md` for the list of changes.
5. **Gives credit** to the first maker of the tool, and to the person who improved it.

## Install

Run this in a terminal (Linux, macOS, or Android Termux):

```sh
curl -fsSL https://raw.githubusercontent.com/lionlaith7/Claude-Root-Module-Builder/main/install.sh | sh
```

Or copy the `build-tools` folder (the one with `SKILL.md` inside) into your Claude skills folder, then restart Claude.

## Simple rules

- If it does not work, it is not shipped.
- Each code file starts with a short note that a child can understand.
- Credits look like this: `Original by <name> (<link>) · Enhanced by <name> (<username>)`.
- Tools that work offline make no internet calls.

## Files in this folder

| File | What it is for |
|---|---|
| `SKILL.md` | The instructions Claude reads |
| `README.md` | This page |
| `README.txt` | Plain text version, in English, Arabic and Chinese |
| `AI.md` | A short map for AI models |
| `install.sh` | The one-line installer |

## License

Check the license of the original project before you reuse its code.

---

## العربية

**مساعد لـ Claude يبني أدوات صغيرة تعمل.**

**ما هذا؟** المهارة (Skill) هي تعليمات تعطيها لـ Claude، وهو ذكاء اصطناعي. تخبره هذه التعليمات كيف يبني أداة صغيرة، ويختبرها، ويكتب عنها ملاحظات بسيطة.

**الأداة** قد تكون: وحدة لهاتف أندرويد (Magisk أو KernelSU)، أو سكربت (قائمة أوامر ينفذها الكمبيوتر)، أو برنامج أوامر، أو صفحة ويب.

**لماذا؟** كثير من الأدوات تتعطل أو تعمل بميزات لم يجربها أحد. هذه المهارة تجعل Claude يختبر كل جزء قبل أن يقول "يعمل".

**ماذا تفعل؟**
1. تسأل فقط عما تحتاجه.
2. تبني نسخة صغيرة تعمل أولاً، ثم تضيف ميزة واحدة في كل مرة.
3. تختبر كل ميزة. الميزة التي لا تُختبر تُحذف ويُذكر السبب.
4. تكتب الملاحظات: `README.md` للموقع، و`README.txt` لمستخدم الجهاز، و`AI.md` للنماذج، و`CHANGELOG.md` لقائمة التغييرات.
5. تنسب الفضل للمطور الأصلي ولمن طوّر الأداة.

**التثبيت:** شغّل هذا الأمر في الطرفية:
```sh
curl -fsSL https://raw.githubusercontent.com/lionlaith7/Claude-Root-Module-Builder/main/install.sh | sh
```

**قواعد بسيطة:** إذا لم تعمل الميزة فلا تُنشر. كل ملف برمجي يبدأ بملاحظة يفهمها الطفل. الاعتمادات: `Original by <name> (<link>) · Enhanced by <name> (<username>)`.

---

## 中文

**一个帮 Claude 制作小工具的技能。**

**这是什么？** 技能是你交给 Claude（一个人工智能）的一组说明。它告诉 Claude 如何制作一个小工具、测试它，并写下简单的说明。

**工具可以是：** 安卓手机模块（Magisk 或 KernelSU）、脚本（电脑执行的命令清单）、命令行程序，或网页。

**为什么要做？** 很多工具会出错，或者包含没人测试过的功能。这个技能让 Claude 在说“可以用”之前，先测试每个部分。

**它做什么？**
1. 只问必要的问题。
2. 先做一个能工作的小版本，然后每次只增加一个功能。
3. 测试每个功能。无法测试的功能会被去掉，并说明原因。
4. 写下说明：`README.md`（给 GitHub 访客）、`README.txt`（给设备用户）、`AI.md`（给 AI 模型）、`CHANGELOG.md`（更改记录）。
5. 注明原作者和改进者。

**安装：** 在终端运行：
```sh
curl -fsSL https://raw.githubusercontent.com/lionlaith7/Claude-Root-Module-Builder/main/install.sh | sh
```

**简单规则：** 不能工作的功能不发布。每个代码文件开头都有一句孩子也能懂的说明。署名格式：`Original by <name> (<link>) · Enhanced by <name> (<username>)`。
