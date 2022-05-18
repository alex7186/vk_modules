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

	@$(MAKE) --no-print-directory copy-service

	@echo "\n✅ setup complete!"

status:
	-@systemctl status $(app_name) | cat

start:
	@$(MAKE) --no-print-directory _start-service
	@$(MAKE) --no-print-directory status

stop:
	@$(MAKE) _stop-service

restart-service:
	-@systemctl restart $(app_name)

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
	@sudo cp $(path)/service/$(app_name).service $(service-path)/$(app_name).service
	@echo "\n⚙️  enabling service \n"
	-@systemctl daemon-reload
	-@systemctl enable $(app_name)
	@echo "\n✅  done!"

cat-service:
	@systemctl cat $(app_name)

cat-log:
	@journalctl --unit=vk_modules.service

_stop-service:
	-@systemctl stop $(app_name)
	@echo "\n❌  service stopped\n"


_start-service:
	
	@systemctl restart $(app_name)
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
