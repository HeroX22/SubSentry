#installation
apt install theharvester -y
apt install sublist3r -y 
apt install subfinder -y 
apt install git -y 
apt install wget -y

#vul_detecition installation
mkdir vuln_subsnipe
cd vuln_subsnipe
wget https://github.com/dub-flow/subsnipe/releases/download/v0.1.2/subsnipe-linux-amd64
mv subsnipe-linux-amd64 subsnipe
chmod +x subsnipe
git clone https://github.com/EdOverflow/can-i-take-over-xyz
mv can-i-take-over-xyz fingerprints
cd fingerprints
mv fingerprints.json can-i-take-over-xyz_fingerprints.json
cd ..
