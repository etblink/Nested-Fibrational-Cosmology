# NFC canon maintenance targets.
.PHONY: metadata validate compile dashboard all check

metadata:      ## Extract machine-readable claim corpus from canon .tex
	python3 scripts/extract_metadata.py

validate:      ## Structural checks: labels, refs, cycles, census stability
	python3 scripts/validate.py

compile:       ## Compile gate: all 17 canon files, twice each (fatal=fail)
	bash scripts/compile_check.sh

dashboard:     ## Rebuild the read-only local dashboard from current metadata
	python3 scripts/build_dashboard.py

check: validate compile ## Full edit-gate: structural validation + compile

all: metadata validate dashboard ## Regenerate metadata + validate + dashboard
state:          ## Regenerate NFC_STATE_OF_CANON.md snapshot from metadata
	python3 scripts/generate_state_of_canon.py
release:        ## Package git-free source archive with tracked-text manifest
	bash scripts/make_release.sh

release-test:   ## Extract archive to clean dir, assert no .git, run make check
	bash scripts/release_test.sh $(ARCHIVE)
