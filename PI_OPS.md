# Pi Ops

Operating the Pi Zero W that runs the Inky Impression scoreboard.

## SSH in

```bash
ssh normie@inkypi.local
```

If `.local` doesn't resolve, use the IP (check router for current one; last known: `192.168.188.83`):

```bash
ssh normie@192.168.188.83
```

If mDNS is dead on the Pi, restart it after logging in:

```bash
sudo systemctl restart avahi-daemon
```

### Optional Mac shortcut

Add to `~/.ssh/config` on the Mac:

```
Host inkypi
    HostName 192.168.188.83
    User normie
```

Then just `ssh inkypi`. Update `HostName` if router hands out a new IP (or reserve the IP in the router's DHCP).

## Service: `deep-work-scoreboard.service`

Unit lives at `/etc/systemd/system/deep-work-scoreboard.service`. Runs `~/deep-work-scoreboard/run-on-pi.sh`, restarts on failure, autostarts on boot.

### Check status

```bash
sudo systemctl status deep-work-scoreboard.service
```

### Live logs

```bash
sudo journalctl -u deep-work-scoreboard.service -f
```

Last 50 lines:

```bash
sudo journalctl -u deep-work-scoreboard.service -n 50
```

### After pulling new code

```bash
cd ~/deep-work-scoreboard
git pull
sudo systemctl restart deep-work-scoreboard.service
```

### After editing the unit file itself

```bash
sudo nano /etc/systemd/system/deep-work-scoreboard.service
sudo systemctl daemon-reload                          # re-parse the file
sudo systemctl restart deep-work-scoreboard.service   # apply
```

`daemon-reload` only needed when the `.service` file changed. Plain code changes → just `restart`.

### Stop / start / disable

```bash
sudo systemctl stop deep-work-scoreboard.service      # halt now
sudo systemctl start deep-work-scoreboard.service     # start now
sudo systemctl disable deep-work-scoreboard.service   # no autostart on boot
sudo systemctl enable deep-work-scoreboard.service    # autostart on boot
```

## Cron (legacy)

The old hourly cron entry is commented out in `crontab -e`. Systemd handles the hourly refresh inside `main.py` now. Uncomment only if the systemd service is disabled and you want cron back.
