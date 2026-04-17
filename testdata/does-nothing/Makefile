BINARY := does-nothing
OUT := out
GOFLAGS := -trimpath -ldflags="-s -w"

ARTIFACTS := artifacts
SCRIPTS := scripts
PY := python3
JAVAC := javac

ARTIFACT_OFFICE := $(ARTIFACTS)/sample.docx $(ARTIFACTS)/sample.xlsx $(ARTIFACTS)/sample.pptx
ARTIFACT_ODF := $(ARTIFACTS)/sample.odt $(ARTIFACTS)/sample.ods $(ARTIFACTS)/sample.odp
ARTIFACT_DOCS := $(ARTIFACT_OFFICE) $(ARTIFACT_ODF) $(ARTIFACTS)/sample.pdf
ARTIFACT_IMAGES := $(ARTIFACTS)/sample.png $(ARTIFACTS)/sample.jpg
ARTIFACT_ARCHIVES := \
	$(ARTIFACTS)/sample.zip \
	$(ARTIFACTS)/sample.tar \
	$(ARTIFACTS)/sample.tar.gz \
	$(ARTIFACTS)/sample.tar.bz2 \
	$(ARTIFACTS)/sample.tar.xz \
	$(ARTIFACTS)/sample.tgz \
	$(ARTIFACTS)/sample.tbz2 \
	$(ARTIFACTS)/sample.txz \
	$(ARTIFACTS)/sample.tar.zst \
	$(ARTIFACTS)/sample.tzst \
	$(ARTIFACTS)/sample.gz \
	$(ARTIFACTS)/sample.bz2 \
	$(ARTIFACTS)/sample.xz \
	$(ARTIFACTS)/sample.zst \
	$(ARTIFACTS)/sample.7z
ARTIFACT_PACKAGES := \
	$(ARTIFACTS)/sample.jar \
	$(ARTIFACTS)/sample.war \
	$(ARTIFACTS)/sample.ear \
	$(ARTIFACTS)/sample.apk \
	$(ARTIFACTS)/sample.aar \
	$(ARTIFACTS)/sample.ipa \
	$(ARTIFACTS)/sample.xpi \
	$(ARTIFACTS)/sample.epub \
	$(ARTIFACTS)/sample.nupkg \
	$(ARTIFACTS)/sample.vsix \
	$(ARTIFACTS)/sample.whl \
	$(ARTIFACTS)/sample.egg \
	$(ARTIFACTS)/sample.crx \
	$(ARTIFACTS)/sample.crate \
	$(ARTIFACTS)/sample.gem \
	$(ARTIFACTS)/sample.deb
ARTIFACT_BYTECODE := $(ARTIFACTS)/sample.pyc $(ARTIFACTS)/sample.class
ARTIFACT_DATA := $(ARTIFACTS)/sample.pkl $(ARTIFACTS)/sample.lnk

ARTIFACT_GENERATED := \
	$(ARTIFACT_DOCS) \
	$(ARTIFACT_IMAGES) \
	$(ARTIFACT_ARCHIVES) \
	$(ARTIFACT_PACKAGES) \
	$(ARTIFACT_BYTECODE) \
	$(ARTIFACT_DATA) \
	$(ARTIFACTS)/sample.txt

.PHONY: all clean darwin windows linux openbsd artifacts artifacts-clean

all: darwin windows linux openbsd

darwin:
	GOOS=darwin GOARCH=arm64 go build $(GOFLAGS) -o $(OUT)/$(BINARY)-darwin-arm64 .
	xz -9 -f $(OUT)/$(BINARY)-darwin-arm64

windows:
	GOOS=windows GOARCH=amd64 go build $(GOFLAGS) -o $(OUT)/$(BINARY)-windows-amd64.exe .
	xz -9 -f $(OUT)/$(BINARY)-windows-amd64.exe

linux:
	GOOS=linux GOARCH=386 go build $(GOFLAGS) -o $(OUT)/$(BINARY)-linux-386 .
	xz -9 -f $(OUT)/$(BINARY)-linux-386

openbsd:
	GOOS=openbsd GOARCH=arm64 go build $(GOFLAGS) -o $(OUT)/$(BINARY)-openbsd-arm64 .
	xz -9 -f $(OUT)/$(BINARY)-openbsd-arm64

clean:
	rm -rf $(OUT)

artifacts: $(ARTIFACT_GENERATED)

$(ARTIFACTS)/sample.txt:
	printf 'this sample does nothing\n' > $@

$(ARTIFACTS)/sample.docx: $(SCRIPTS)/make_docx.py
	$(PY) $< $@

$(ARTIFACTS)/sample.xlsx: $(SCRIPTS)/make_xlsx.py
	$(PY) $< $@

$(ARTIFACTS)/sample.pptx: $(SCRIPTS)/make_pptx.py
	$(PY) $< $@

$(ARTIFACTS)/sample.odt: $(SCRIPTS)/make_odf.py
	$(PY) $< odt $@

$(ARTIFACTS)/sample.ods: $(SCRIPTS)/make_odf.py
	$(PY) $< ods $@

$(ARTIFACTS)/sample.odp: $(SCRIPTS)/make_odf.py
	$(PY) $< odp $@

$(ARTIFACTS)/sample.pdf: $(SCRIPTS)/make_pdf.py
	$(PY) $< $@

$(ARTIFACTS)/sample.png: $(SCRIPTS)/make_png.py
	$(PY) $< $@

$(ARTIFACTS)/sample.jpg: $(SCRIPTS)/make_jpg.py
	$(PY) $< $@

$(ARTIFACTS)/sample.pkl: $(SCRIPTS)/make_pickle.py
	$(PY) $< $@

$(ARTIFACTS)/sample.lnk: $(SCRIPTS)/make_lnk.py
	$(PY) $< $@

$(ARTIFACTS)/sample.zip: $(ARTIFACTS)/sample.txt
	cd $(ARTIFACTS) && rm -f sample.zip && zip -q sample.zip sample.txt

$(ARTIFACTS)/sample.tar: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -cf $@ sample.txt

$(ARTIFACTS)/sample.tar.gz: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -czf $@ sample.txt

$(ARTIFACTS)/sample.tar.bz2: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -cjf $@ sample.txt

$(ARTIFACTS)/sample.tar.xz: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -cJf $@ sample.txt

$(ARTIFACTS)/sample.tgz: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -czf $@ sample.txt

$(ARTIFACTS)/sample.tbz2: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -cjf $@ sample.txt

$(ARTIFACTS)/sample.txz: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) -cJf $@ sample.txt

$(ARTIFACTS)/sample.gz: $(ARTIFACTS)/sample.txt
	gzip -9 -c $< > $@

$(ARTIFACTS)/sample.bz2: $(ARTIFACTS)/sample.txt
	bzip2 -9 -c $< > $@

$(ARTIFACTS)/sample.xz: $(ARTIFACTS)/sample.txt
	xz -9 -c $< > $@

$(ARTIFACTS)/sample.zst: $(ARTIFACTS)/sample.txt
	zstd -q -19 -f -o $@ $<

$(ARTIFACTS)/sample.7z: $(ARTIFACTS)/sample.txt
	cd $(ARTIFACTS) && rm -f sample.7z && 7z a -bso0 -bsp0 sample.7z sample.txt >/dev/null

$(ARTIFACTS)/sample.tar.zst: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) --zstd -cf $@ sample.txt

$(ARTIFACTS)/sample.tzst: $(ARTIFACTS)/sample.txt
	tar -C $(ARTIFACTS) --zstd -cf $@ sample.txt

$(ARTIFACTS)/sample.jar: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< jar $@

$(ARTIFACTS)/sample.war: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< war $@

$(ARTIFACTS)/sample.ear: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< ear $@

$(ARTIFACTS)/sample.apk: $(SCRIPTS)/make_zip_bundle.py $(OUT)/$(BINARY)-linux-386.xz
	$(PY) $< apk $@ $(OUT)/$(BINARY)-linux-386.xz

$(ARTIFACTS)/sample.aar: $(SCRIPTS)/make_zip_bundle.py $(ARTIFACTS)/sample.class
	$(PY) $< aar $@ $(ARTIFACTS)/sample.class

$(ARTIFACTS)/sample.ipa: $(SCRIPTS)/make_zip_bundle.py $(OUT)/$(BINARY)-darwin-arm64.xz
	$(PY) $< ipa $@ $(OUT)/$(BINARY)-darwin-arm64.xz

$(ARTIFACTS)/sample.xpi: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< xpi $@

$(ARTIFACTS)/sample.epub: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< epub $@

$(ARTIFACTS)/sample.nupkg: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< nupkg $@

$(ARTIFACTS)/sample.vsix: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< vsix $@

$(ARTIFACTS)/sample.whl: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< whl $@

$(ARTIFACTS)/sample.egg: $(SCRIPTS)/make_zip_bundle.py
	$(PY) $< egg $@

$(ARTIFACTS)/sample.crx: $(SCRIPTS)/make_crx.py
	$(PY) $< $@

$(ARTIFACTS)/sample.crate: $(SCRIPTS)/make_crate.py
	$(PY) $< $@

$(ARTIFACTS)/sample.gem: $(SCRIPTS)/make_gem.py
	$(PY) $< $@

$(ARTIFACTS)/sample.deb: $(SCRIPTS)/make_deb.py
	$(PY) $< $@

$(ARTIFACTS)/sample.pyc: $(ARTIFACTS)/sample.py
	$(PY) -m py_compile $<
	mv $(ARTIFACTS)/__pycache__/sample.cpython-*.pyc $@
	rmdir $(ARTIFACTS)/__pycache__

$(ARTIFACTS)/sample.class: $(ARTIFACTS)/sample.java
	cd $(ARTIFACTS) && $(JAVAC) sample.java
	mv $(ARTIFACTS)/Sample.class $@

artifacts-clean:
	rm -f $(ARTIFACT_GENERATED)
	rm -rf $(ARTIFACTS)/__pycache__
