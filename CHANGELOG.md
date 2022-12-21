# Changelog

Every noteable change is logged here.

## v0.10.3 (2022-12-21)

### Fix

* use correct runner on linux (82ec0bbf8986)

### Chore

* upgrade requirements.txt (b5507810017a)
* upgrade pipeline (5bf38108c022)

## v0.10.2 (2022-09-29)

### Chore

* adjust worker count (b4ca1f38a567)
* adjust data generator (a007b7634f29)
* add missing dev requirement (89ed0c612696)

## v0.10.1 (2022-09-29)

### Fix

* catch internal exception (7b447929ee90)

### Chore

* upgrade requirements.txt (39c4f67d20f2)

## v0.10.0 (2022-09-28)

### Feature

* patch backend (f68bcb71ba4f)

### Fix

* adjust interface (d2db25ac54b0)

### Chore

* add separate generator step (cfffe94c02aa)
* use more cores on CI (8a55227da8f5)
* upgrade requirements.txt (fb16148e4f1f)
* add PyCryptoDome to decrypt pdf (4964fcfed3d8)
* upgrade requirements.txt (89ee9688f5b5)
* add missing resource (2a3237b10ce8)
* add Jenkinsfile (515562bbe965)
* upgrade requirements.txt (0037a6d1bbd2)

## v0.9.4

### Fix

* add missing page number (06a3919f6710)

## v0.9.3

### Feature

* do not detect peace of code as table (4bf277bd51f8)
* extend logging information (280952831dac)

## v0.9.2

## v0.9.1

### Fix

* decouple clustering (fc0d893318c6)

## v0.9.0

### Feature

* add separate judger (eb438e20f54d)
* increase debugging information (01ef818077c9)
* increase possible header (3147aabdd824)

### Fix

* adjust page selector (4628f34f3e51)

### Documentation

* Happy New Year! (55e7230ea662)
* adjust modules path (31e8c3170606)

## v0.8.3

## v0.8.2

### Fix

* avoid magic variables (d0864e0de4c7)

## v0.8.1

### Fix

* fix percent definition (ce6af3904648)

## v0.8.0

### Feature

* skip potential table with too height header (e4c0460d4e70)
* render detected lines (f1216030f711)
* increase required lines (d9fe375b54ff)
* skip very short lines (fcc9b3b4d952)

## v0.7.1

### Fix

* single lines can not build a table (c2624ca6ee0e)
* skip tablero row height check (b8334012162b)

## v0.7.0

### Feature

* skip potential table with too many columns (a0b21b056019)
* skip tables with to small table mean row (8388dd7716f6)
* skip groups with too many horizontal lines (e268f746dec4)
* convert cluster earlier (e41e8c189ab7)

## v0.6.1

### Fix

* make failing camelot less strict (d1ba965580c4)
* use default area if no area is given (be5a5f756cce)
* catch internal camelot error (489b9ead4701)

## v0.6.0

### Feature

* skip non-line pages (445f20db8a17)
* improve invalid table check (0cdbc4d1a21f)

### Fix

* suppress camelot logging (68cd24ab407e)

## v0.5.0

### Feature

* replace with ghost code (a71c1b888653)
* replace static file with parameter (8940f0e3a3ed)

## v0.4.1

### Fix

* add missing import (274c5110b3e7)
* reduce verbosity (2dcaafc0d5a5)

## v0.4.0

### Feature

* enable camelox decider (576dd54aad0b)
* use parsing report to improve parsing result (15aed98fc349)
* add error logger (3ed6366324ca)
* fill non content area with white (8a2c060515ef)
* shrink extraction to ptcn area (9f50bf5517b6)
* use contentbox to improve extraction result (9a34681a3986)

### Fix

* skip stream flavour (e62d4c2c83b7)
* handle empty parsing correctly (53c400032692)
* skip empty item to avoid parsing error (b01d35d87842)

## v0.3.0

### Feature

* skip potential table with too height header (3714275448ee)
* do not render no table pdf (8713eab3cecc)
* improve horizontal table strategy (34980300d604)
* add option to render detected table (8b987bc7eb72)
* skip non content horizontal lines (9693655a6643)
* use ptcn to skip page border area (b76642e7e49b)
* do not divide after improving clustering (91264bc170df)

### Fix

* skip too small header (275c5d134f0c)
* merge tables again, cause grouper does not work properly (8e42b67cf156)
* do not return cluster in result (88348ca5a09b)

### Documentation

* extend interface documentation (86fcc01e961c)

## v0.2.0

### Feature

* add separate extraction step (bd72db3b1c1b)

## v0.1.0

### Feature

* add cli (fd75f1859977)
* move code from rawmaker (8005eba77979)

## v0.0.0 Initial release
