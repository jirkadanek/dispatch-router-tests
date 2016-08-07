# dispatch-router-tests
Tests for https://github.com/apache/qpid-dispatch AMQP 1.0 message router

[![Build Status](https://travis-ci.org/jdanekrh/dispatch-router-tests.svg?branch=Docker)](https://travis-ci.org/jdanekrh/dispatch-router-tests)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jdanekrh/dispatch-router-tests/badges/quality-score.png?b=Docker)](https://scrutinizer-ci.com/g/jdanekrh/dispatch-router-tests/?branch=Docker)
[![Code Climate](https://codeclimate.com/github/jdanekrh/dispatch-router-tests/badges/gpa.svg)](https://codeclimate.com/github/jdanekrh/dispatch-router-tests)

## Description

The Docker version.

## Setup

### Python

Have Python 3.5 and do the usual

    pip install --user -r requirements.txt

Python 3 is used despite Ansible not supporting it. I may want to use Ansible in the future, to manage VMs. I'd have to do some IPC or something, to get there. In fact, I could gradually rebuild this into microservices ;) https://rominirani.com/grpc-some-thoughts-7543ce950765

No symbolic linking is necessary any more, since the relevant parts of the `Dtests` repository (router configuration templates written by me) are now part of this repository.

### Docker

Since images are fetched from hub.docker.com, it is not necessary to provision anything. In addition, the images are now based on Debian, not Red Hat Enterprise Linux 7.3. There will be a config option to use your own images.

#### Docker basics

(see dispatch-console-tests project)

## Use

## Managing State

It is extremely easy to blank the slate. Simply recreate the Docker container.

## Design options and decisions

### Qpid Proton Python

I do not really understand how AMQP maps onto that API. I probably should use two clients, preferably something close to AMQP, without much abstraction, to really understand.

### Docker (idiomatic)

Little problem with debugging. How do I interactively run test against what I compiled in my modified checkout of the router repository? I don't. Let's revisit when there are actual cases of revealed bugs.

### OpenStack

This would be ideal solution. Prepare one image with router and broker on it, deploy it, then create as many instances as needed, run tests, destroy VMs. The advantages of VMs with the manageability of Docker. OpenStack is hard to get. Would not work for testing on public infrastructure, of course.
