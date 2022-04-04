fmt:
	autoflake -i -r --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables . \
	&& autopep8 -i -r . \
	&& isort -y \
	&& black .

# autoflake cannot be configured, this line should match the same line in fmt
# autopep8 doe snot have a means of checking files
lint:
	autoflake -c -r --expand-star-imports --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables . \
	&& isort --check-only \
	&& black . --check \
	&& flake8
