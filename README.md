# json-to-rackdiag
create rack-diagram from json, which could be added to git repo or searched by kibana

# install
(tested on centos7)  
sudo pip install blockdiag  
sudo pip install nwdiag  
sudo yum install graphviz  
cd /var/tmp  
git clone git@github.com:tnaganawa/json-to-rackdiag.git  
cd json-to-rackdiag  
python json-to-rackdiag.py  
firefox /tmp/json-to-rackdiag.svg /tmp/json-to-rack-pos-diag.svg  


