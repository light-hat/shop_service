# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end
  config.vm.provision "shell", inline: <<-SHELL
      apt-get update && apt-get upgrade -y

      apt-get install -y \
          ca-certificates \
          curl \
          gnupg \
          lsb-release

      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

      sudo apt-get update

      sudo apt-get install -y docker-ce docker-ce-cli containerd.io

      sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -sL https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d'"' -f4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose

      sudo apt-get install -y make
      sudo apt-get install -y python3 python3-pip

      pip3 install black isort

      cd /vagrant
      make build
  SHELL
end