#!
. utils
. nginx_utils
. certificates

has_nginx || die "No NGINX"

if ! has_file 'ca/miniAD.pem' ; then
  make_ca
fi

if ! has_file 'certs/http.key' || ! has_file 'certs/http.crt' ; then
    echo "Need to create key and cert"
    #make_self_signed_cert "certs/http.crt" "certs/http.key"   
    make_ca_signed_cert "certs/http.crt" "certs/http.key"  "certs/http.csr" "certs/http.ext"
fi

if  ! has_file "images/1.png" ;  then
    create_images "$(pwd)/images" 1000 "1024x768"
fi
# port http_root config
run_nginx_https 8443 "$(pwd)/images" "https"
