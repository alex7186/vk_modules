today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = vk_modules
path = $(CURDIR)

push:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	@git commit -m $(commit_name)
	echo "\n⚙️ pushing as $(commit_name)"
	@git push origin main || true
	@echo "\n✅ done!"

push-force:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	@git commit -m $(commit_name)
	@echo "\n🚩 FORCE 🚩 pushing as $(commit_name)"
	@git push --force origin main
	@echo "\n✅ done!"
	
setup:
	@echo "\n⚙️  making user config folders...\n"
	-@mkdir ~/.config
	-@mkdir ~/.config/systemd
	-@mkdir ~/.config/systemd/user
	
	@$(MAKE) service-copy

	@cd $(path)
	@echo "\n📝  installing dependencies...\n"
	@pip3 install -r ./misc/requirements.txt
	@echo "\n📅  adding service to systemd...\n"
	@systemctl --user enable $(app_name).service
	@echo "\n✅ done!"

status:
	-@systemctl --user status $(app_name).service | cat

service-copy:
	@echo "\n⚙️  moving service to config folder...\n"
	@sudo cp $(path)/service/$(app_name).service ~/.config/systemd/user/$(app_name).service
	@systemctl --user daemon-reload
	@echo "\n✅ done!"

service-stop:
	-@systemctl --user stop $(app_name).service
	@echo "\n❌  service stopped\n"

service-start:
	-@systemctl --user restart $(app_name).service
	@echo "\n✅  service started\n"

service-cat:
	@cat ~/.config/systemd/user/$(app_name).service

start:
	@$(MAKE) service-start
	@sleep 2
	@$(MAKE) status

stop:
	@$(MAKE) service-stop