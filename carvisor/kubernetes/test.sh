#!/bin/bash

read -r -d '' output <<- EOM
    NAME KIND VERSION REPLACEMENT REMOVED DEPRECATED
    rbac-manager Deployment apps/v1beta1 apps/v1 true true
EOM

echo $output