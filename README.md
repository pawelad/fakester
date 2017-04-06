<p align="center">
    <img src="https://cdn.rawgit.com/pawelad/fakester/d542da1e/fakester/fakester/static/img/logo.png" alt="Fakester logo">
</p>

[![Build status](https://img.shields.io/travis/pawelad/fakester.svg)][travis]
[![GitHub release](https://img.shields.io/github/release/pawelad/fakester.svg)][github]
[![Test coverage](https://img.shields.io/coveralls/pawelad/fakester.svg)][coveralls]
[![License](https://img.shields.io/github/license/pawelad/fakester.svg)][license]

Have you ever wanted to rickyroll your boss but found that links like
[goo.gl/ejKmN3](https://goo.gl/ejKmN3), [bit.ly/LEcVV7](https://bit.ly/LEcVV7)
and (*ekhm*) [youtu.be/I6OXjnBIW-4](https://youtu.be/I6OXjnBIW-4) were way too
obvious? Well, I did. A couple of times actually.

So I made this. And now you can trick your boss too. You're welcome.

Last seen at [fakester.pawelad.xyz][fakester] (and all 
domains listed below).

## Domains
Domains are meant to be interchangeable - I bought current ones for 2 cents
each and will probably change them when they expire. Each redirect works on 
all domains.

Currently linked domains:
- http://amishweekly.xyz
- http://deepersteeper.xyz
- http://estrogenesis.xyz
- http://funkinthetrunk.xyz
- http://fuzzfeet.xyz
- http://isitstd.xyz
- http://masterexploder.xyz
- http://momcorp.xyz
- http://mortifex.xyz
- http://mrmeeseeks.xyz
- http://notporn.xyz
- http://spottieottiedopaliscious.xyz
- http://thedeuce.xyz
- http://thefiggisagency.xyz
- http://theflabbergaster.xyz
- http://thekrappinger.xyz
- http://uphole.xyz

Feel free to contact me and 'donate' new ones : -)

## Malicious redirects
Please contact me if you found a redirect that was malicious, as I realize that 
this can possibly be used in such way. It's the opposite of my intentions
and I try to prevent that in a couple of ways but (unfortunately) nothing is 
perfect.

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes. Thanks!

Also, take a look [here][fakester running locally] if you want to run Fakester
locally.

## Tests
Package was tested with the help of `py.test` and `tox` on Python 3.4, 3.5
and 3.6 with Django 1.10 (see `tox.ini`).

Code coverage is available at [Coveralls][coveralls].

To run tests yourself you need to set environment variable with Django secret
key before running `tox` inside the repository:

```shell
$ pip install -r requirements/dev.txt
$ export SECRET_KEY='...'
$ tox
```

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [MIT License][license].


[coveralls]: https://coveralls.io/github/pawelad/fakester
[fakester]: https://fakester.pawelad.xyz
[fakester running locally]: https://github.com/pawelad/fakester/wiki/Running-Fakester-locally
[github]: https://github.com/pawelad/fakester
[license]: https://github.com/pawelad/fakester/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[travis]: https://travis-ci.org/pawelad/fakester
