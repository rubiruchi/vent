vent
====

> Network Visibility (an anagram)

[![CircleCI](https://circleci.com/gh/CyberReboot/vent.svg?style=shield)](https://circleci.com/gh/CyberReboot/vent)
[![Documentation Status](https://readthedocs.org/projects/vent/badge/?version=latest)](http://vent.readthedocs.io/en/latest/?badge=latest)
[![GitHub release](https://img.shields.io/github/release/cyberreboot/vent.svg?maxAge=2592000)](https://github.com/CyberReboot/vent/releases)
[![codecov](https://codecov.io/gh/CyberReboot/vent/branch/master/graph/badge.svg)](https://codecov.io/gh/CyberReboot/vent)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/ffe3b2d6a9254b98a12de6b3273676b3/badge.svg)](https://www.quantifiedcode.com/app/project/ffe3b2d6a9254b98a12de6b3273676b3)
[![Github Releases](https://img.shields.io/github/downloads/cyberreboot/vent/latest/total.svg?maxAge=2592000)](https://github.com/CyberReboot/vent/releases)


download pre-compiled ISO
====

[releases](https://github.com/CyberReboot/vent/releases)


build the ISO
====

### build dependencies

```
docker
make
zip
```

### getting the bits

```
git clone --recursive https://github.com/CyberReboot/vent.git
cd vent
```

### building

```
make
```

easy ways to build a VM out of the ISO
====

with docker-machine cli:

```
# in a terminal from the path where the ISO file is (usually inside of the vent directory)
python -m SimpleHTTPServer

# from another terminal while the previous command is still running, execute the
# following, with optional additional arguments prior to the last vent in the command
docker-machine create -d virtualbox --virtualbox-boot2docker-url http://localhost:8000/vent.iso vent
# other options to customize the size of the vm are available as well:
# --virtualbox-cpu-count "1"
# --virtualbox-disk-size "20000"
# --virtualbox-memory "1024"

# finally once the previous command is finished, execute this for the vent user interface
docker-machine ssh vent
```

of course traditional ways of deploying an ISO work as well, including VMWare, OpenStack, and booting from it to install on bare metal.  a couple of things to note: it will automatically install and provision the disk and then restart when done.  vent runs in RAM, so changes need to be made under `/var/lib/docker` or `/var/lib/boot2docker` as those are persistent (see boot2docker [documentation](https://github.com/boot2docker/boot2docker/blob/master/README.md) for more information).  it's possible that `vent-management` won't automatically get added and run, if you run `docker ps` and it's not running, execute `sudo /data/custom`.

getting started
====

from within the vent interface (once SSH'd in) first `build` the core.  it might take a little while to download and compile everything.

once it's built you're ready to start the `core` from the `mode` menu option.

after starting, you should be able to go into `system info` and see that everything is running as expected.  once that looks good, you're ready to copy up pcaps.  that's it!

copy up new pcaps
====

install the `vent` script locally first:
```
sudo make install
```

if using docker-machine cli to provision:

```
# from the directory that contains your pcaps
# optionally add an argument of the name for vent in
#     docker-machine if you called it something other than vent
cd /path/where/pcaps/are/
vent
```

if deploying as a self-configured machine (VMWare, OpenStack, bare metal, etc.):

```
# from the directory that contains your pcaps
# optionally add an argument of the name/ip for vent on your network
cd vent
cp vent-generic /usr/local/bin/vent
cd /path/where/pcaps/are/
vent
```

otherwise edit the `ssh` and `scp` lines in `vent` specific to docker-machine and change to suit your needs

copy up new templates and plugins
====

if using docker-machine cli to provision:

```
docker-machine scp modes.template vent:/var/lib/docker/data/templates/modes.template
```

if using boot2docker cli to provision (DEPRECATED):

```
scp -r -i ~/.ssh/id_boot2docker -P 2022 modes.template docker@localhost:/var/lib/docker/data/templates/modes.template
```

if deploying as a self-configured machine (VMWare, OpenStack, bare metal, etc.):

```
scp modes.template docker@vent:/var/lib/docker/data/templates/modes.template
```

documentation
====

- [Docs](https://github.com/CyberReboot/vent/tree/master/docs)
- [Diagrams](https://github.com/CyberReboot/vent/tree/master/docs/images)

contributing to vent
====

Want to contribute?  Awesome!  Issue a pull request or see more details [here](https://github.com/CyberReboot/vent/blob/master/CONTRIBUTING.md).

FAQ
====

**Q**: What are the credentials to login if I don't use certificates/keys?

**A**: docker/tcuser

**Q**: I went into the shell and did a `docker ps` but no containers are running, how do I get it working again?

**A**: Execute `docker rm vent-management; sudo /data/custom`, if that doesn't work, restart the machine.
