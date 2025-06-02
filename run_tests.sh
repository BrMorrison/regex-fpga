#!/bin/bash

# I'm sure there's a better way of doing this, but this works
PYTHONPATH="$(pwd)/Recompile" swim test
