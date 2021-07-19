# changelog

Every noteable change is logged here.

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
