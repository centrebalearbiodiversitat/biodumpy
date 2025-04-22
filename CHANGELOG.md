# Changelog

All notable changes to this project will be documented in this file 🐔.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.4] - Unreleased

### Added
- Crossref module.
- WORMS module.
- Function ``rm_dup`` to remove duplicate dictionaries from a list, including nested structures.
- ``dataset_key`` parameter in the COL module.
- ``taxonomy`` and ``taxonomy_only`` parameters in the NCBI module for more refined queries.
- ``sleep`` parameter in each module.
- New documentation sections: "The adaptation of biodumpy to R" and "Bibliography".
- Test coverage to ensure more robust and reliable code.

### Changed
- IUCN API updated from v3 to v4.
- Adapted IUCN module tests to comply with API v4.
- Documentation improved for better usability and clarity.
- Test enhancements across the following modules: BOLD, COL, Crossref, GBIF, iNaturalist, IUCN, OBIS, WORMS, and ZooBank.
- Changed endpoint taxonomy in GBIF module. 
- BOLD module simplified by removing the ``fasta`` boolean parameter.

### Fix

---

## [0.1.3] - 2024-09-20

### Added
- Initial release of biodumpy with support for downloading metadata from BOLD, COL, GBIF, iNaturalist, IUCN, NCBI, OBIS, and ZooBank.

### Changed
- Improved documentation.

### Fixed
- Bug fixes in the download modules.

---

## [0.1.2] - 2024-09-20

### Added
- Initial release for testing.

---

## [Unreleased]
