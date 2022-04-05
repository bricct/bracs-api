fmt:
	autoflake -i -r --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables . --exclude __init__ \
	&& autopep8 -i -r --exclude __init__.py . \
	&& isort --skip __init__.py -y \
	&& black .

# autoflake cannot be configured, this line should match the same line in fmt
# autopep8 doe snot have a means of checking files
lint:
	autoflake -c -r --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables . --exclude __init__ \
	&& isort --skip __init__.py --check-only \
	&& black . --check \
