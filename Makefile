today =`date '+%Y-%m-%d  %H:%M:%S'`
commit_name = "autocommit $(today)"
app_name = vk_modules
path = $(CURDIR)

service-path = /etc/systemd/system

_black:
	@cd $(path)
	@echo "\n🧹 cleaning the code...\n"
	@python -m black .

_git_commit:
	@cd $(path)
	@echo "\n⚙️  pushing to git...\n"
	@git add .
	-@git commit -m $(commit_name)

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
	@$(MAKE) _reload-restart-service
	@echo "\n✅  done!"

_stop-service:
	-@systemctl stop non-user-$(app_name)
	@echo "\n❌  service stopped\n"


_start-service:
	
	@systemctl restart non-user-$(app_name)
	@echo "\n✅  service started\n"


_reload-restart-service:
	-@systemctl daemon-reload
	-@systemctl enable non-user-$(app_name)
	-@systemctl restart non-user-$(app_name)

start-python:
	@cd $(path)
	@python3 app.py

# cat-service:
# 	@systemctl --user cat $(app_name)

# cat-log:
# 	@journalctl --user-unit $(app_name) | less

setup:
	@$(MAKE) copy-service

	@cd $(path)
	@echo "\n📝  installing dependencies...\n"
	@pip3 install -r ./misc/requirements.txt
	
	@echo "\n✅ done!"

status:
	-@systemctl status non-user-$(app_name) | cat

start:
	@$(MAKE) _start-service
	@$(MAKE) status

stop:
	@$(MAKE) _stop-service