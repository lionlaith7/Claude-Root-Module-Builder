# build-tools — a Claude skill

**Build a small tool that works, test it, then share it with simple docs.**

Works for phone modules (Magisk, KernelSU), scripts, command tools and web pages.

Original skill by Laith Harb (https://github.com/lionlaith7) · Maintained by Laith Harb (lionlaith7), Jordan.

## Install

One line (Linux, macOS, or Android Termux):

```sh
curl -fsSL https://raw.githubusercontent.com/lionlaith7/Claude-Root-Module-Builder/main/install.sh | sh
```

Or copy the `build-tools/` folder (with `SKILL.md`) into your Claude skills folder, then restart Claude.

## What it does
1. Asks what you want to build, and starts without long questions.
2. Builds the smallest version that works, one feature at a time.
3. Tests every feature. Leaves out anything it cannot test, and says why.
4. Writes a README (GitHub), README.txt (for people on the device), AI.md (for AI models) and CHANGELOG.md.
5. Gives credit to the original maker and to you.

## Rules
- Works 100% or is not shipped.
- Short and clear code. Every file starts with a kid-friendly note.
- Credits: `Original by <name> (<link>) · Enhanced by <name> (<username>)`.
- Offline by default. Online tools say which sites they contact.

## Files
| File | Purpose |
|---|---|
| `SKILL.md` | The instructions Claude follows |
| `AI.md` | Short map for AI models |
| `README.txt` | Plain-text guide (English, Arabic, Chinese) |
| `install.sh` | One-line installer |

## License
See the license of the original project before reusing its code.
