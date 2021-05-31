#!/bin/bash
cd /home/
export TF_XLA_FLAGS=--tf_xla_cpu_global_jit
/usr/bin/supervisord -c /etc/supervisord.conf > log/app.log 2>&1 > /dev/null