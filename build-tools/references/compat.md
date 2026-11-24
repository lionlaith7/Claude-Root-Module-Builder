# Compatibility matrix (what is known)

| Item | Magisk | KernelSU official | KernelSU-Next | FinaSU (user device) |
|---|---|---|---|---|
| module.prop/zip layout | T1 | T1 | T2 | T3 once canary runs |
| service.sh / post-fs-data.sh | T1 | T1 | T2 | T4 until canary |
| boot-completed.sh / post-mount.sh | - | T1 | T4 | T4 until canary |
| Metamodules | - | T1 | T4 | not applicable (built-in Magic Mount) |
| action.sh | T1 | T1 | T4 | T4 |

User device facts (T3, from manager screen): Redmi Note 10 Pro (sweet), Infinity X (AOSP-based), Android 16 / API 36, FinaSU manager v1.7.0 (33224-6), kernel 4.14.357 non-GKI built-in, SELinux enforcing, Magic Mount built-in, SUSFS v2.4.0, OnyxZygisk. The manager fingerprint (SWEET_GLOBAL:13 MIUI V14) is likely vendor firmware, not the running system.
Everything marked T4 is resolved by the canary log.
