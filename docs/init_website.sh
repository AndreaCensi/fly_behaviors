#!/bin/bash
set -e
git clone git@github.com:AndreaCensi/fly_behaviors.git  website
cd website
git checkout origin/gh-pages -b gh-pages
git branch -D master

