.PHONY: setup test clean tangle help

help:
	@echo "Available commands:"
	@echo "  make setup   - Create necessary directories"
	@echo "  make test    - Run all exercise scripts"
	@echo "  make clean   - Remove pycache"
	@echo "  make tangle  - Tangle org file (requires emacs)"

setup:
	mkdir -p src exercises diagrams images
	@echo "Setup complete."

tangle: setup
	@echo "Tangling setup.org and pulumi_workshop.org..."
	@# Ideally checks for emacs, otherwise warns
	@if command -v emacs >/dev/null 2>&1; then \
		emacs setup.org --batch -f org-babel-tangle; \
		emacs pulumi_workshop.org --batch -f org-babel-tangle; \
	else \
		echo "Emacs not found. Skipping automatic tangle. Ensure files are present."; \
	fi

test:
	@echo "--- Running Dependency Analyzer ---"
	python3 src/dependency_analyzer.py
	@echo "\n--- Running Exercise 1 ---"
	python3 exercises/ex1_dependency_map.py
	@echo "\n--- Running Exercise 2 ---"
	python3 exercises/ex2_layer_assignment.py
	@echo "\n--- Running Exercise 3 ---"
	python3 exercises/ex3_recovery_simulation.py

clean:
	rm -rf src/__pycache__ exercises/__pycache__
