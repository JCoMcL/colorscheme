add-to-all: add-to-kak add-to-site add-to-alacritty
add-to-kak: colorscheme.kak
	cp $< ~/.config/kak/color.kak
	kak -l | while read sesh; do echo "colorscheme xvi" | kak -p $$sesh; done
add-to-site: colorscheme.css
	cp $< ~/src/my-site/static/colorscheme.css
add-to-alacritty: colorscheme.toml
	cp $< ~/.config/alacritty

colorscheme.css: colorscheme.ppm colorscheme.py
	python colorscheme.py css < $< > $@

colorscheme.kak: colorscheme.ppm colorscheme.py
	python colorscheme.py kak < $< > $@

colorscheme.toml: colorscheme.ppm colorscheme.py
	python colorscheme.py alacritty < $< > $@

.PHONY: testcases
testcases: colorscheme.css colorscheme.kak colorscheme.toml
	mkdir -p testcases
	mv $^ testcases

test: colorscheme.css colorscheme.kak colorscheme.toml
	for file in $^; do diff $$file testcases/$$file; done

watch:
	$(MAKE)
	inotifywait . && $(MAKE) watch

.PHONY: watch add-to-site add-to-kak add-to-alacritty add-to-all
