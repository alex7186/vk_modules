today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = vk_modules
path = ~/scripts/$(app_name)


push:
	@cd $(path)
	@python -m black .
	@git add .
	@git commit -m $(commit_name)
	@git push origin main
	@echo "\n✅ succussfully pulled as $(commit_name)"
	
setup:
	@mkdir ~/.config ||true
	@mkdir ~/.config/systemd ||true
	@mkdir ~/.config/systemd/user ||true

	@cd $(path)
	@pip3 install -r ./misc/requirements.txt
	@python3 back/crontab_manager.py start

	@sudo cp $(path)/misc/$(app_name).service ~/.config/systemd/user/$(app_name).service

service-status:
	systemctl --user status $(app_name).service || true

service-stop:
	systemctl --user stop $(app_name).service || true

service-start:
	systemctl --user restart $(app_name).service
	systemctl --user enable $(app_name).service
	systemctl --user start $(app_name).service

	$(MAKE) service-status

service-cat:
	cat ~/.config/systemd/user/$(app_name).service

start:
	$(MAKE) service-start
