today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = vk_modules
path = $(CURDIR)

service-path = /etc/systemd/system

setup:
	@cd $(path)
	@echo "\n📝  installing dependencies...\n"
	@pip3 install -r ./misc/requirements.txt
	@sudo apt-get install python3-systemd

	@$(MAKE) copy-service

	@echo "\n✅ done!"

status:
	-@systemctl status non-user-$(app_name) | cat

start:
	@$(MAKE) _start-service
	@$(MAKE) status

stop:
	@$(MAKE) _stop-service

restart-service:
	-@systemctl restart non-user-$(app_name)

push:
	@$(MAKE) _black
	@$(MAKE) _git_commit
	@echo "\n⚙️  pushing as $(commit_name)\n"
	@git push origin main
	@echo "\n✅  done!"

push-force:
	@$(MAKE) _black
	@$(MAKE) _git_commit
	@echo "\n⚙️  🚩FORCE🚩  pushing as $(commit_name)\n"
	@git push --force origin main
	@echo "\n✅  done!"
	
copy-service:
	@echo "\n⚙️  moving service to $(service-path)\n"
	@sudo cp $(path)/service/$(app_name).service $(non-user-service-path)/non-user-$(app_name).service
	@echo "\n⚙️  enabling service \n"
	-@systemctl daemon-reload
	-@systemctl enable non-user-$(app_name)
	@echo "\n✅  done!"

cat-service:
	@systemctl cat non-user-$(app_name)

cat-log:
	@journalctl --unit=non-user-vk_modules.service

_stop-service:
	-@systemctl stop non-user-$(app_name)
	@echo "\n❌  service stopped\n"


_start-service:
	
	@systemctl restart non-user-$(app_name)
	@echo "\n✅  service started\n"

_black:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .

_git_commit:
	@cd $(path)
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	-@git commit -m $(commit_name)
