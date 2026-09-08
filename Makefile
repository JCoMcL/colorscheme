add-to-all: add-to-kak add-to-site add-to-alacritty
add-to-kak: colorscheme.kak colorscheme-light.kak
	cp colorscheme.kak ~/.config/kak/color.kak
	cp colorscheme-light.kak ~/.config/kak/color-light.kak
	kak -l | while read sesh; do echo "colorscheme xvi" | kak -p $$sesh; done
add-to-site: colorscheme.css colorscheme-light.css
	cp colorscheme.css ~/src/my-site/static/colorscheme.css
	cp colorscheme-light.css ~/src/my-site/static/colorscheme-light.css
add-to-alacritty: colorscheme.toml colorscheme-light.toml
	cp colorscheme.toml ~/.config/alacritty
	cp colorscheme-light.toml ~/.config/alacritty

colorscheme.css: colorscheme.ppm colorscheme.py
	python colorscheme.py css < $< > $@

colorscheme-light.css: colorscheme.ppm colorscheme.py
	python colorscheme.py css --light < $< > $@

colorscheme.kak: colorscheme.ppm colorscheme.py
	python colorscheme.py kak < $< > $@

colorscheme-light.kak: colorscheme.ppm colorscheme.py
	python colorscheme.py kak --light < $< > $@

colorscheme.toml: colorscheme.ppm colorscheme.py
	python colorscheme.py alacritty < $< > $@

colorscheme-light.toml: colorscheme.ppm colorscheme.py
	python colorscheme.py alacritty --light < $< > $@

.PHONY: testcases
testcases: colorscheme.css colorscheme-light.css colorscheme.kak colorscheme-light.kak colorscheme.toml colorscheme-light.toml
	mkdir -p testcases
	mv $^ testcases

test: colorscheme.css colorscheme-light.css colorscheme.kak colorscheme-light.kak colorscheme.toml colorscheme-light.toml
	for file in $^; do diff $$file testcases/$$file; done

watch:
	$(MAKE)
	inotifywait . && $(MAKE) watch

.PHONY: watch add-to-site add-to-kak add-to-alacritty add-to-all
