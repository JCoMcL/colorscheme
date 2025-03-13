add-to-kak: colorscheme.kak
	cp $< ~/.config/kak/color.kak
	kak -l | while read sesh; do echo "colorscheme xvi" | kak -p $$sesh; done
add-to-site: colorscheme.css
	cp colorscheme.css ~/src/my-site/static/colorscheme.css

colorscheme.css: colorscheme.ppm
	python colorscheme.py css < $< > $@

colorscheme.kak: colorscheme.ppm
	python colorscheme.py kak < $< > $@

watch:
	$(MAKE)
	inotifywait . && $(MAKE) watch

.PHONY: watch add-to-site add-to-kak
