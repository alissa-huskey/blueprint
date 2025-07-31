BUILD_DIR=build
DIST_DIR=releases
INSTALL_DIR=$(HOME)/projects/phpbb/forum/ext

VENDOR={{ VENDOR | to_smooshed_case }}
EXTENSION={{ NAME | to_smooshed_case }}
VERSION=0.1.0

EXT_ROOT=$(BUILD_DIR)/$(VENDOR)/$(EXTENSION)
ZIPFILE=$(VENDOR)-$(EXTENSION)-$(VERSION).zip

SRCS=license.txt README.md
SRCS+=config
# SRCS+=acp adm core cron event language migrations notification services styles

.PHONY: build
build: clean                    ## build the extension
	@mkdir -p $(EXT_ROOT)
	@mkdir -p $(DIST_DIR)
	@cp -r $(SRCS) $(EXT_ROOT)
	@jq 'del(. ["autoload", "autoload-dev"])' composer.json > $(EXT_ROOT)/composer.json
	@cd $(BUILD_DIR) && zip -r $(ZIPFILE) $(VENDOR) && cd -

.PHONY: release
release: build                  ## create a zipfile and update version numbers to $VERSION
	@echo
	@echo "Preparing release for v $(VERSION)"
	@echo "(Don't forget to edit the CHANGELOG.md)"
	@mv $(BUILD_DIR)/$(ZIPFILE) $(DIST_DIR)
	@sed -i'' -Ee "/^\[latest-release\]/ s/ra-$(EXTENSION)-*.zip\s*/ra-$(EXTENSION)-$(VERSION).zip/" README.md
	@sed -i'' -Ee '/^\s*"version":/ s/"[0-9]+\.[0-9]+\.[0-9]+"/"$(VERSION)"/' .composer-test.json
	@sed -i'' -Ee '/^\s*"version":/ s/"[0-9]+\.[0-9]+\.[0-9]+"/"$(VERSION)"/' .composer-dev.json

.PHONY: install
install: build                  ## install locally to $INSTALL_DIR
	@cp $(BUILD_DIR)/$(ZIPFILE) $(INSTALL_DIR)
	@cd $(INSTALL_DIR) && unzip -o $(ZIPFILE)
	@rm $(INSTALL_DIR)/$(ZIPFILE)

.PHONY: help
help:                            ## list targets
	@echo
	@echo $(EXTENSION) Makefile
	@echo
	@sed -ne '/^[a-z%-]\+:.*##/ s/:.*##/\t/p' $(word 1, $(MAKEFILE_LIST)) \
		| awk -F $$'\t' '{printf("\033[36m%s\033[0m \t%s\n", $$1, $$2)}' \
		| column -ts $$'\t'
	@echo

.PHONY: clean
clean:                          ## remove the build directory
	@rm -rf $(BUILD_DIR)

.DEFAULT_GOAL := help
