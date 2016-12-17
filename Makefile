pre-commit:
	@cp ./scripts/pre-commit .git/hooks/

pip:
	@make pre-commit
	@pip install -r ./merge-table/demo/requirements.txt

lint:
	@sh scripts/check_lint.sh
