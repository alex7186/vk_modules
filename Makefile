today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = vk_modules
path = $(CURDIR)

push:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .
	@echo "\n⚙️  pulling to git...\n"
	@git add .
	@git commit -m $(commit_name)
	@git push origin main
	@echo "\n✅ succussfully pulled as $(commit_name)"
	
setup:
	@echo "\n⚙️  making user config folders...\n"
	-@mkdir ~/.config
	-@mkdir ~/.config/systemd
	-@mkdir ~/.config/systemd/user
	@echo "\n⚙️  moving service to config folder..."
	@sudo cp $(path)/misc/$(app_name).service ~/.config/systemd/user/$(app_name).service

	@cd $(path)
	@echo "\n📝  installing dependencies...\n"
	@pip3 install -r ./misc/requirements.txt
	@echo "\n📅  adding service to systemd...\n"
	@systemctl --user enable $(app_name).service
	@echo "\n✅  configured successfully"

status:
	-@systemctl --user status $(app_name).service

service-stop:
	-@systemctl --user stop $(app_name).service
	@echo "\n❌  service stopped\n"

service-start:
	-@systemctl --user restart $(app_name).service
	@echo "\n✅  service started\n"
	@sleep .5
	@$(MAKE) status

service-cat:
	@cat ~/.config/systemd/user/$(app_name).service

restart:
	@$(MAKE) service-stop
	@$(MAKE) service-start

start:
	@$(MAKE) service-start

stop:
	@$(MAKE) service-stop