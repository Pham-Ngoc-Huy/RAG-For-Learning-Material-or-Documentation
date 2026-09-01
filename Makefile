.PHONY: clean find-clean clean-root

# find-clean: show matching directories that would be removed
find-clean:
	@echo "Finding __pycache__ and checkpoint directories..."
	@echo ""
	@for root in . src tests api docs config temp; do \
		if [ -d "$$root" ]; then \
			echo "Checking $$root/:"; \
			found=$$(find $$root -type d \( -name "__pycache__" -o -name "Icon?" -o -name ".ipycheckpoints" -o -name ".ipynb_checkpoints" \) 2>/dev/null); \
			if [ -n "$$found" ]; then \
				echo "$$found" | sed 's/^/  /'; \
			else \
				echo "  (none found)"; \
			fi; \
			echo ""; \
		fi; \
	done

# clean-root: remove __pycache__ and checkpoint directories from each root
clean-root:
	@echo "Removing __pycache__ and checkpoint directories from each root..."
	@echo ""
	@for root in . src tests api docs config temp; do \
		if [ -d "$$root" ]; then \
			echo "Cleaning $$root/:"; \
			find $$root -type d \( -name "__pycache__" -o -name "Icon?" -o -name ".ipycheckpoints" -o -name ".ipynb_checkpoints" \) -prune -exec rm -rf {} + 2>/dev/null; \
			echo "  ✓ Done"; \
			echo ""; \
		fi; \
	done

# clean: remove __pycache__ and Jupyter checkpoint directories (recursive)
clean:
	@echo "Removing __pycache__ and checkpoint directories recursively..."
	@find . -type d \( -name "__pycache__" -o -name "Icon?" -o -name ".ipycheckpoints" -o -name ".ipynb_checkpoints" \) -prune -exec rm -rf {} + 2>/dev/null
	@echo "✓ Cleanup complete"