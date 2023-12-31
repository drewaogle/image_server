#!
. utils
. nginx_utils

has_nginx || die "No NGINX"

if  ! has_file "images/1.png" ;  then
    create_images "./images" 1000 "1024x768"
fi

# port http_root config
run_nginx_http 8080 "$(pwd)/images" "http_limited"
