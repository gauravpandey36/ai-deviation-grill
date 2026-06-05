
## Phase 1 — cases: human_error_masking_system

- Key: ...LgAA
- Calls: 22
- **Total cost: $1.8644**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| grill | claude-opus-4-8 | 1519 | 418 | 4864 | 0 | 0.14533 |
| defendant | claude-haiku-4-5-20251001 | 1496 | 115 | 0 | 0 | 0.00207 |
| grill | claude-opus-4-8 | 158 | 650 | 1935 | 4864 | 0.09470 |
| defendant | claude-haiku-4-5-20251001 | 2086 | 81 | 0 | 0 | 0.00249 |
| grill | claude-opus-4-8 | 917 | 631 | 1935 | 4864 | 0.10466 |
| defendant | claude-haiku-4-5-20251001 | 2618 | 191 | 0 | 0 | 0.00357 |
| grill | claude-opus-4-8 | 1000 | 768 | 1224 | 6381 | 0.10512 |
| defendant | claude-haiku-4-5-20251001 | 3368 | 123 | 0 | 0 | 0.00398 |
| grill | claude-opus-4-8 | 1190 | 652 | 1390 | 6955 | 0.10325 |
| defendant | claude-haiku-4-5-20251001 | 3963 | 238 | 0 | 0 | 0.00515 |
| grill | claude-opus-4-8 | 1129 | 1200 | 1657 | 7714 | 0.14958 |
| defendant | claude-haiku-4-5-20251001 | 5051 | 384 | 0 | 0 | 0.00697 |
| grill | claude-opus-4-8 | 2047 | 832 | 1582 | 8603 | 0.13567 |
| defendant | claude-haiku-4-5-20251001 | 6036 | 224 | 0 | 0 | 0.00716 |
| grill | claude-opus-4-8 | 1656 | 1050 | 2167 | 9533 | 0.15852 |
| defendant | claude-haiku-4-5-20251001 | 7046 | 130 | 0 | 0 | 0.00770 |
| grill | claude-opus-4-8 | 1502 | 1079 | 2564 | 10498 | 0.16728 |
| defendant | claude-haiku-4-5-20251001 | 7954 | 207 | 0 | 0 | 0.00899 |
| grill | claude-opus-4-8 | 1503 | 553 | 2174 | 12230 | 0.12313 |
| defendant | claude-haiku-4-5-20251001 | 8562 | 400 | 0 | 0 | 0.01056 |
| grill | claude-opus-4-8 | 1385 | 1200 | 2287 | 13354 | 0.17369 |
| judge | claude-opus-4-8 | 16836 | 1231 | 0 | 0 | 0.34486 |

- Cases this run: human_error_masking_system
- Per-case cost (USD): human_error_masking_system=$1.8644
- **Extrapolation:** 1 case = $1.8644 -> 6 cases ≈ $11.19, 7 cases ≈ $13.05 (both ablations would ~2x). Budget ceiling $5.00.

## Re-judge (transcript reuse)

- Key: ...LgAA
- Calls: 1
- **Total cost: $0.0432**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| judge | claude-sonnet-4-6 | 7427 | 1393 | 0 | 0 | 0.04318 |

## Phase 1 — cases: material_supplier, procedure_ambiguity, data_integrity_alcoa, planted_conflict, thin_but_clean

- Key: ...LgAA
- Calls: 24
- **Total cost: $0.8670**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| generator | claude-haiku-4-5-20251001 | 886 | 5065 | 0 | 0 | 0.02621 |
| grill | claude-opus-4-8 | 1291 | 163 | 0 | 4980 | 0.03906 |
| defendant | claude-haiku-4-5-20251001 | 3136 | 214 | 0 | 0 | 0.00421 |
| grill | claude-opus-4-8 | 285 | 178 | 1452 | 4980 | 0.05232 |
| defendant | claude-haiku-4-5-20251001 | 3490 | 220 | 0 | 0 | 0.00459 |
| grill | claude-opus-4-8 | 757 | 289 | 1452 | 4980 | 0.06772 |
| defendant | claude-haiku-4-5-20251001 | 3927 | 250 | 0 | 0 | 0.00518 |
| grill | claude-opus-4-8 | 882 | 216 | 624 | 6269 | 0.05053 |
| defendant | claude-haiku-4-5-20251001 | 4336 | 236 | 0 | 0 | 0.00552 |
| grill | claude-opus-4-8 | 839 | 352 | 761 | 6715 | 0.06333 |
| defendant | claude-haiku-4-5-20251001 | 4810 | 319 | 0 | 0 | 0.00641 |
| grill | claude-opus-4-8 | 1139 | 232 | 802 | 7187 | 0.06030 |
| defendant | claude-haiku-4-5-20251001 | 5291 | 274 | 0 | 0 | 0.00666 |
| grill | claude-opus-4-8 | 1105 | 267 | 892 | 7773 | 0.06499 |
| defendant | claude-haiku-4-5-20251001 | 5752 | 330 | 0 | 0 | 0.00740 |
| grill | claude-opus-4-8 | 1101 | 307 | 1045 | 8313 | 0.07160 |
| defendant | claude-haiku-4-5-20251001 | 6300 | 284 | 0 | 0 | 0.00772 |
| grill | claude-opus-4-8 | 1133 | 256 | 909 | 9126 | 0.06693 |
| defendant | claude-haiku-4-5-20251001 | 6752 | 352 | 0 | 0 | 0.00851 |
| grill | claude-opus-4-8 | 1174 | 343 | 996 | 9768 | 0.07666 |
| defendant | claude-haiku-4-5-20251001 | 7334 | 262 | 0 | 0 | 0.00864 |
| grill | claude-opus-4-8 | 1244 | 304 | 965 | 10457 | 0.07524 |
| defendant | claude-haiku-4-5-20251001 | 7803 | 304 | 0 | 0 | 0.00932 |
| grill | claude-opus-4-8 | 1124 | 313 | 1113 | 11166 | 0.07795 |

- Cases this run: material_supplier, procedure_ambiguity, data_integrity_alcoa, planted_conflict, thin_but_clean
- Per-case cost (USD): 

## Spend reconciliation & BLOCKER (2026-06-05)

**BLOCKER:** Anthropic account credit balance exhausted — `invalid_request_error: "Your credit
balance is too low to access the Anthropic API."` This is the real account balance, separate
from the agreed $10 logical ceiling. The run died mid-`material_supplier`; 4 archetypes never
generated. **Action required: add credits at https://console.anthropic.com/settings/billing.**

Approx. total actual spend before the wall (some early runs crashed before their cost_log
append, so reconstructed):
- Gate (all-Opus, human_error)        $1.8644  (logged)
- Re-judge (Sonnet)                   $0.0432  (logged)
- Terse re-measure (judge parse-fail) ~$0.74   (unlogged — crashed pre-append)
- equipment_calibration (run 1)       ~$1.07   (unlogged — crashed pre-append; printed in log)
- run 2 partial (material_supplier)   $0.8670  (logged)
- temperature-bug first attempt       ~$0.005  (unlogged)
- **Approx. total ≈ $4.6** of the $10 ceiling. Account is now at ~zero credits.

**Completed & judged:** human_error_masking_system (6/6), equipment_calibration (5/5).
**Not started (blocked):** 5 remaining archetypes, both ablations, Phase 2 real-records run.

## Phase 1 — cases: material_supplier, procedure_ambiguity, data_integrity_alcoa, planted_conflict, thin_but_clean

- Key: ...LgAA
- Calls: 117
- **Total cost: $4.8500**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| generator | claude-haiku-4-5-20251001 | 886 | 5386 | 0 | 0 | 0.02782 |
| grill | claude-opus-4-8 | 1242 | 190 | 4980 | 0 | 0.12626 |
| defendant | claude-haiku-4-5-20251001 | 3286 | 280 | 0 | 0 | 0.00469 |
| grill | claude-opus-4-8 | 417 | 232 | 1430 | 4980 | 0.05794 |
| defendant | claude-haiku-4-5-20251001 | 3737 | 400 | 0 | 0 | 0.00574 |
| grill | claude-opus-4-8 | 1128 | 244 | 1430 | 4980 | 0.06950 |
| defendant | claude-haiku-4-5-20251001 | 4323 | 358 | 0 | 0 | 0.00611 |
| grill | claude-opus-4-8 | 1181 | 365 | 837 | 6220 | 0.07011 |
| defendant | claude-haiku-4-5-20251001 | 4937 | 383 | 0 | 0 | 0.00685 |
| grill | claude-opus-4-8 | 1328 | 258 | 955 | 6825 | 0.06741 |
| defendant | claude-haiku-4-5-20251001 | 5501 | 340 | 0 | 0 | 0.00720 |
| grill | claude-opus-4-8 | 1277 | 374 | 1065 | 7536 | 0.07848 |
| defendant | claude-haiku-4-5-20251001 | 6092 | 333 | 0 | 0 | 0.00776 |
| grill | claude-opus-4-8 | 1394 | 256 | 1128 | 8236 | 0.07361 |
| defendant | claude-haiku-4-5-20251001 | 6602 | 359 | 0 | 0 | 0.00840 |
| grill | claude-opus-4-8 | 1289 | 424 | 1144 | 9106 | 0.08624 |
| defendant | claude-haiku-4-5-20251001 | 7260 | 373 | 0 | 0 | 0.00912 |
| grill | claude-opus-4-8 | 1445 | 383 | 1136 | 9876 | 0.08651 |
| defendant | claude-haiku-4-5-20251001 | 7902 | 372 | 0 | 0 | 0.00976 |
| grill | claude-opus-4-8 | 1440 | 385 | 1205 | 10756 | 0.08920 |
| defendant | claude-haiku-4-5-20251001 | 8547 | 384 | 0 | 0 | 0.01047 |
| grill | claude-opus-4-8 | 1512 | 361 | 1301 | 11537 | 0.09145 |
| defendant | claude-haiku-4-5-20251001 | 9188 | 361 | 0 | 0 | 0.01099 |
| grill | claude-opus-4-8 | 1374 | 700 | 1329 | 12455 | 0.11671 |
| judge | claude-sonnet-4-6 | 10468 | 1678 | 0 | 0 | 0.05657 |
| generator | claude-haiku-4-5-20251001 | 893 | 2589 | 0 | 0 | 0.01384 |
| grill | claude-opus-4-8 | 1170 | 172 | 0 | 4980 | 0.03792 |
| defendant | claude-haiku-4-5-20251001 | 1148 | 136 | 0 | 0 | 0.00183 |
| grill | claude-opus-4-8 | 180 | 150 | 1340 | 4980 | 0.04655 |
| defendant | claude-haiku-4-5-20251001 | 1398 | 204 | 0 | 0 | 0.00242 |
| grill | claude-opus-4-8 | 581 | 195 | 1340 | 4980 | 0.05593 |
| defendant | claude-haiku-4-5-20251001 | 1754 | 289 | 0 | 0 | 0.00320 |
| grill | claude-opus-4-8 | 801 | 320 | 500 | 6148 | 0.05461 |
| defendant | claude-haiku-4-5-20251001 | 2272 | 157 | 0 | 0 | 0.00306 |
| grill | claude-opus-4-8 | 871 | 283 | 596 | 6498 | 0.05521 |
| defendant | claude-haiku-4-5-20251001 | 2662 | 265 | 0 | 0 | 0.00399 |
| grill | claude-opus-4-8 | 818 | 442 | 868 | 6899 | 0.07204 |
| defendant | claude-haiku-4-5-20251001 | 3260 | 220 | 0 | 0 | 0.00436 |
| grill | claude-opus-4-8 | 1062 | 354 | 799 | 7447 | 0.06863 |
| defendant | claude-haiku-4-5-20251001 | 3748 | 361 | 0 | 0 | 0.00555 |
| grill | claude-opus-4-8 | 1111 | 328 | 1062 | 7963 | 0.07312 |
| defendant | claude-haiku-4-5-20251001 | 4346 | 313 | 0 | 0 | 0.00591 |
| grill | claude-opus-4-8 | 1219 | 327 | 1077 | 8583 | 0.07588 |
| defendant | claude-haiku-4-5-20251001 | 4887 | 178 | 0 | 0 | 0.00578 |
| grill | claude-opus-4-8 | 1001 | 293 | 1156 | 9306 | 0.07262 |
| defendant | claude-haiku-4-5-20251001 | 5266 | 288 | 0 | 0 | 0.00671 |
| grill | claude-opus-4-8 | 962 | 284 | 1070 | 10134 | 0.07099 |
| defendant | claude-haiku-4-5-20251001 | 5756 | 187 | 0 | 0 | 0.00669 |
| grill | claude-opus-4-8 | 961 | 348 | 877 | 10877 | 0.07327 |
| defendant | claude-haiku-4-5-20251001 | 6192 | 316 | 0 | 0 | 0.00777 |
| grill | claude-opus-4-8 | 1145 | 700 | 987 | 11461 | 0.10537 |
| judge | claude-sonnet-4-6 | 9064 | 1427 | 0 | 0 | 0.04860 |
| generator | claude-haiku-4-5-20251001 | 920 | 4532 | 0 | 0 | 0.02358 |
| grill | claude-opus-4-8 | 1220 | 194 | 0 | 4980 | 0.04032 |
| defendant | claude-haiku-4-5-20251001 | 2458 | 271 | 0 | 0 | 0.00381 |
| grill | claude-opus-4-8 | 352 | 241 | 1412 | 4980 | 0.05730 |
| defendant | claude-haiku-4-5-20251001 | 2917 | 145 | 0 | 0 | 0.00364 |
| grill | claude-opus-4-8 | 783 | 313 | 1412 | 4980 | 0.06917 |
| defendant | claude-haiku-4-5-20251001 | 3289 | 253 | 0 | 0 | 0.00455 |
| grill | claude-opus-4-8 | 829 | 400 | 785 | 6198 | 0.06645 |
| defendant | claude-haiku-4-5-20251001 | 3837 | 339 | 0 | 0 | 0.00553 |
| grill | claude-opus-4-8 | 1189 | 372 | 744 | 6742 | 0.06980 |
| defendant | claude-haiku-4-5-20251001 | 4459 | 362 | 0 | 0 | 0.00627 |
| grill | claude-opus-4-8 | 1344 | 387 | 1037 | 7173 | 0.07939 |
| defendant | claude-haiku-4-5-20251001 | 5104 | 253 | 0 | 0 | 0.00637 |
| grill | claude-opus-4-8 | 1234 | 366 | 1235 | 7810 | 0.08083 |
| defendant | claude-haiku-4-5-20251001 | 5602 | 287 | 0 | 0 | 0.00704 |
| grill | claude-opus-4-8 | 1104 | 344 | 1266 | 8673 | 0.07911 |
| defendant | claude-haiku-4-5-20251001 | 6120 | 235 | 0 | 0 | 0.00730 |
| grill | claude-opus-4-8 | 1082 | 700 | 1091 | 9552 | 0.10351 |
| judge | claude-sonnet-4-6 | 8114 | 1515 | 0 | 0 | 0.04707 |
| generator | claude-haiku-4-5-20251001 | 933 | 3300 | 0 | 0 | 0.01743 |
| grill | claude-opus-4-8 | 1763 | 217 | 0 | 4980 | 0.05019 |
| defendant | claude-haiku-4-5-20251001 | 1262 | 190 | 0 | 0 | 0.00221 |
| grill | claude-opus-4-8 | 271 | 370 | 1978 | 4980 | 0.07637 |
| defendant | claude-haiku-4-5-20251001 | 1735 | 58 | 0 | 0 | 0.00202 |
| grill | claude-opus-4-8 | 714 | 408 | 1978 | 4980 | 0.08587 |
| defendant | claude-haiku-4-5-20251001 | 2090 | 130 | 0 | 0 | 0.00274 |
| grill | claude-opus-4-8 | 659 | 546 | 856 | 6741 | 0.07700 |
| defendant | claude-haiku-4-5-20251001 | 2591 | 160 | 0 | 0 | 0.00339 |
| grill | claude-opus-4-8 | 957 | 407 | 851 | 7227 | 0.07168 |
| defendant | claude-haiku-4-5-20251001 | 3046 | 135 | 0 | 0 | 0.00372 |
| grill | claude-opus-4-8 | 826 | 346 | 1130 | 7670 | 0.07103 |
| defendant | claude-haiku-4-5-20251001 | 3433 | 91 | 0 | 0 | 0.00389 |
| grill | claude-opus-4-8 | 660 | 545 | 1186 | 8254 | 0.08539 |
| defendant | claude-haiku-4-5-20251001 | 3926 | 184 | 0 | 0 | 0.00485 |
| grill | claude-opus-4-8 | 922 | 481 | 937 | 9033 | 0.08102 |
| defendant | claude-haiku-4-5-20251001 | 4441 | 74 | 0 | 0 | 0.00481 |
| grill | claude-opus-4-8 | 837 | 419 | 1019 | 9624 | 0.07752 |
| defendant | claude-haiku-4-5-20251001 | 4795 | 168 | 0 | 0 | 0.00564 |
| grill | claude-opus-4-8 | 773 | 700 | 1273 | 10098 | 0.10311 |
| judge | claude-sonnet-4-6 | 7900 | 1343 | 0 | 0 | 0.04385 |
| generator | claude-haiku-4-5-20251001 | 922 | 3549 | 0 | 0 | 0.01867 |
| grill | claude-opus-4-8 | 1685 | 177 | 0 | 4980 | 0.04602 |
| defendant | claude-haiku-4-5-20251001 | 2564 | 269 | 0 | 0 | 0.00391 |
| grill | claude-opus-4-8 | 362 | 218 | 1860 | 4980 | 0.06413 |
| defendant | claude-haiku-4-5-20251001 | 2985 | 283 | 0 | 0 | 0.00440 |
| grill | claude-opus-4-8 | 957 | 247 | 1860 | 4980 | 0.07523 |
| defendant | claude-haiku-4-5-20251001 | 3441 | 341 | 0 | 0 | 0.00515 |
| grill | claude-opus-4-8 | 1077 | 302 | 755 | 6663 | 0.06296 |
| defendant | claude-haiku-4-5-20251001 | 3990 | 326 | 0 | 0 | 0.00562 |
| grill | claude-opus-4-8 | 1236 | 240 | 842 | 7200 | 0.06313 |
| defendant | claude-haiku-4-5-20251001 | 4471 | 398 | 0 | 0 | 0.00646 |
| grill | claude-opus-4-8 | 1270 | 324 | 1000 | 7795 | 0.07379 |
| defendant | claude-haiku-4-5-20251001 | 5098 | 392 | 0 | 0 | 0.00706 |
| grill | claude-opus-4-8 | 1405 | 292 | 1023 | 8493 | 0.07490 |
| defendant | claude-haiku-4-5-20251001 | 5697 | 354 | 0 | 0 | 0.00747 |
| grill | claude-opus-4-8 | 1307 | 313 | 1111 | 9276 | 0.07783 |
| defendant | claude-haiku-4-5-20251001 | 6270 | 390 | 0 | 0 | 0.00822 |
| grill | claude-opus-4-8 | 1335 | 323 | 1148 | 10063 | 0.08087 |
| defendant | claude-haiku-4-5-20251001 | 6891 | 389 | 0 | 0 | 0.00884 |
| grill | claude-opus-4-8 | 1397 | 314 | 1086 | 10919 | 0.08125 |
| defendant | claude-haiku-4-5-20251001 | 7492 | 379 | 0 | 0 | 0.00939 |
| grill | claude-opus-4-8 | 1390 | 315 | 1175 | 11692 | 0.08404 |
| defendant | claude-haiku-4-5-20251001 | 8068 | 334 | 0 | 0 | 0.00974 |
| grill | claude-opus-4-8 | 1357 | 700 | 1170 | 12544 | 0.11361 |
| judge | claude-sonnet-4-6 | 8970 | 1924 | 0 | 0 | 0.05577 |

- Cases this run: material_supplier, procedure_ambiguity, data_integrity_alcoa, planted_conflict, thin_but_clean
- Per-case cost (USD): material_supplier=$1.1849, procedure_ambiguity=$0.9819, data_integrity_alcoa=$0.761, planted_conflict=$0.8737, thin_but_clean=$1.0484

## Phase 1 — cases: human_error_masking_system

- Key: ...LgAA
- Calls: 20
- **Total cost: $0.6899**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| grill | claude-opus-4-8 | 1520 | 142 | 5063 | 0 | 0.12838 |
| defendant | claude-haiku-4-5-20251001 | 1290 | 101 | 0 | 0 | 0.00179 |
| grill | claude-opus-4-8 | 133 | 144 | 1660 | 5063 | 0.05151 |
| defendant | claude-haiku-4-5-20251001 | 1508 | 126 | 0 | 0 | 0.00214 |
| grill | claude-opus-4-8 | 447 | 202 | 1660 | 5063 | 0.06057 |
| defendant | claude-haiku-4-5-20251001 | 1785 | 86 | 0 | 0 | 0.00221 |
| grill | claude-opus-4-8 | 489 | 221 | 417 | 6581 | 0.04160 |
| defendant | claude-haiku-4-5-20251001 | 2028 | 75 | 0 | 0 | 0.00240 |
| grill | claude-opus-4-8 | 445 | 195 | 516 | 6854 | 0.04126 |
| defendant | claude-haiku-4-5-20251001 | 2233 | 129 | 0 | 0 | 0.00288 |
| grill | claude-opus-4-8 | 493 | 224 | 538 | 7168 | 0.04503 |
| defendant | claude-haiku-4-5-20251001 | 2511 | 165 | 0 | 0 | 0.00334 |
| grill | claude-opus-4-8 | 651 | 271 | 523 | 7485 | 0.05112 |
| defendant | claude-haiku-4-5-20251001 | 2881 | 192 | 0 | 0 | 0.00384 |
| grill | claude-opus-4-8 | 746 | 280 | 608 | 7813 | 0.05531 |
| defendant | claude-haiku-4-5-20251001 | 3275 | 152 | 0 | 0 | 0.00404 |
| grill | claude-opus-4-8 | 742 | 268 | 731 | 8197 | 0.05723 |
| defendant | claude-haiku-4-5-20251001 | 3611 | 163 | 0 | 0 | 0.00443 |
| grill | claude-opus-4-8 | 738 | 700 | 788 | 8657 | 0.09133 |
| judge | claude-sonnet-4-6 | 6655 | 1298 | 0 | 0 | 0.03943 |

- Cases this run: human_error_masking_system
- Per-case cost (USD): human_error_masking_system=$0.6899
- **Extrapolation:** 1 case = $0.6899 -> 6 cases ≈ $4.14, 7 cases ≈ $4.83 (both ablations would ~2x). Budget ceiling $5.00.

## Phase 1 — cases: human_error_masking_system

- Key: ...LgAA
- Calls: 18
- **Total cost: $0.7292**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| grill | claude-opus-4-8 | 1520 | 185 | 5105 | 0 | 0.13239 |
| defendant | claude-haiku-4-5-20251001 | 1322 | 193 | 0 | 0 | 0.00229 |
| grill | claude-opus-4-8 | 268 | 227 | 1703 | 5105 | 0.06063 |
| defendant | claude-haiku-4-5-20251001 | 1681 | 194 | 0 | 0 | 0.00265 |
| grill | claude-opus-4-8 | 756 | 225 | 1703 | 5105 | 0.06780 |
| defendant | claude-haiku-4-5-20251001 | 2041 | 156 | 0 | 0 | 0.00282 |
| grill | claude-opus-4-8 | 689 | 308 | 678 | 6623 | 0.05608 |
| defendant | claude-haiku-4-5-20251001 | 2426 | 317 | 0 | 0 | 0.00401 |
| grill | claude-opus-4-8 | 935 | 343 | 713 | 7074 | 0.06373 |
| defendant | claude-haiku-4-5-20251001 | 2978 | 163 | 0 | 0 | 0.00379 |
| grill | claude-opus-4-8 | 1006 | 262 | 734 | 7562 | 0.05985 |
| defendant | claude-haiku-4-5-20251001 | 3339 | 196 | 0 | 0 | 0.00432 |
| grill | claude-opus-4-8 | 759 | 247 | 1075 | 7988 | 0.06205 |
| defendant | claude-haiku-4-5-20251001 | 3713 | 192 | 0 | 0 | 0.00467 |
| grill | claude-opus-4-8 | 782 | 277 | 842 | 8720 | 0.06137 |
| defendant | claude-haiku-4-5-20251001 | 4114 | 220 | 0 | 0 | 0.00521 |
| grill | claude-opus-4-8 | 843 | 700 | 767 | 9300 | 0.09348 |
| judge | claude-sonnet-4-6 | 7195 | 1365 | 0 | 0 | 0.04206 |

- Cases this run: human_error_masking_system
- Per-case cost (USD): human_error_masking_system=$0.7292
- **Extrapolation:** 1 case = $0.7292 -> 6 cases ≈ $4.38, 7 cases ≈ $5.10 (both ablations would ~2x). Budget ceiling $5.00.

## Phase 2 — 13 real records

- Key: ...LgAA
- Calls: 13
- **Total cost: $3.4091**

| role | model | in | out | cache_w | cache_r | $ |
|---|---|--:|--:|--:|--:|--:|
| grill | claude-opus-4-8 | 2 | 3000 | 2109 | 5344 | 0.27259 |
| grill | claude-opus-4-8 | 2 | 3000 | 2195 | 5344 | 0.27420 |
| grill | claude-opus-4-8 | 2 | 3000 | 1801 | 5344 | 0.26682 |
| grill | claude-opus-4-8 | 2 | 3000 | 2171 | 5344 | 0.27375 |
| grill | claude-opus-4-8 | 1570 | 3000 | 0 | 5344 | 0.25657 |
| grill | claude-opus-4-8 | 1791 | 3000 | 0 | 5344 | 0.25988 |
| grill | claude-opus-4-8 | 1480 | 3000 | 0 | 5344 | 0.25522 |
| grill | claude-opus-4-8 | 1553 | 3000 | 0 | 5344 | 0.25631 |
| grill | claude-opus-4-8 | 1784 | 3000 | 0 | 5344 | 0.25978 |
| grill | claude-opus-4-8 | 1823 | 3000 | 0 | 5344 | 0.26036 |
| grill | claude-opus-4-8 | 1529 | 3000 | 0 | 5344 | 0.25595 |
| grill | claude-opus-4-8 | 1785 | 3000 | 0 | 5344 | 0.25979 |
| grill | claude-opus-4-8 | 1661 | 3000 | 0 | 5344 | 0.25793 |

## FINAL — fresh $10 (after credits added 2026-06-05)

| Run | $ |
|---|--:|
| Phase 1 — 5 remaining archetypes (Opus grill, Sonnet judge) | 4.85 |
| Ablation — hypotheses_off (human_error) | 0.69 |
| Ablation — hardstops_off (human_error) | 0.73 |
| Phase 2 — 13 real records (budget guard stopped at 13/16) | 3.41 |
| **Fresh-$10 total** | **9.68** |

Grand total real spend across the whole experiment (incl. the all-Opus gate, debugging
iterations, and the pre-credit runs): **≈ $14**. The clean reproducible run of the final
design is the $9.68 above.
