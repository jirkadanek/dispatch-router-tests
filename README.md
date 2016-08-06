# dispatch-router-tests
Tests for https://github.com/apache/qpid-dispatch AMQP 1.0 message router

## Branches

The code is in the VMS and Docker branches.

### VMs

This used to be the master branch. Tests that require Vagrant VMs on certain IPs with sshd listening. Tests use Ansible to manage the VMs and perform operations like starting and stopping router, changing configuration files and so on.

This is hard to run on public open source infrastructure. VMs take much disk space and memory, I could run only about 5 or 6 on my laptop before I ran out.

### Docker

New approach to provisioning routers. Each router is a Docker container, configuration is changed by mounting files into the container, router is started and stopped by starting and stopping the container. Ansible is not needed (although it would be perfectly possible to run sshd in the container, if there was a reason).

This can run fine on Travis CI. It is also easier setup to manage locally. I already have the necessary Docker images from the dispatch-console-tests project.

### Master

Eventually, I hope to merge the two previous branches to give a choice between running in VMs and in Docker. The first tests OS compatibility, the second tests features better and is easier to run locally for test development.

I do not want to work on both at the same time now, because testing with VMs is much work, and because I do not have clear idea yet of the VM/Docker abstraction I will eventually create.
