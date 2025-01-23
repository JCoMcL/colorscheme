add-to-site: colorscheme.css
	cp colorscheme.css ~/src/my-site/static/colorscheme.css

colorscheme.css: colorscheme.png
	python colorscheme.py < colorscheme.png > $@

watch:
	$(MAKE)
	inotifywait . && $(MAKE) watch

.PHONY: watch add-to-site
