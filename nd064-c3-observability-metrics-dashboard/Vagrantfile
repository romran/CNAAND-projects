# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  config.vm.box = "15.2.31.309"

  config.vm.network 'private_network', ip: "192.168.33.10",  virtualbox__intnet: true
  config.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh", disabled: true
  config.vm.network "forwarded_port", guest: 22, host: 2000 # Master Node SSH
  config.vm.network "forwarded_port", guest: 6443, host: 6443 # Kubectl API Access
  config.vm.network "forwarded_port", guest: 8080, host: 8080 # API Access
  config.vm.network "forwarded_port", guest: 16686, host: 16686 # Jaeger HTTP Access
  config.vm.network "forwarded_port", guest: 16687, host: 16687 # Jaeger CR Access
  config.vm.network "forwarded_port", guest: 32368 , host: 32368
  config.vm.network "forwarded_port", guest: 3000, host: 3000
  config.vm.network "forwarded_port", guest: 3030, host: 3030
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8081, host: 8081
  config.vm.network "forwarded_port", guest: 8082, host: 8082
  config.vm.network "forwarded_port", guest: 8083, host: 8083  
  config.vm.network "forwarded_port", guest: 9090, host: 9090

  for p in 30000..30100 # expose NodePort IP's
    config.vm.network "forwarded_port", guest: p, host: p, protocol: "tcp"
  end

  config.vm.provider "virtualbox" do |vb|
    # vb.memory = "8192"
    vb.memory = "4096"
    vb.cpus = 3
    vb.name = "k3s"
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
  
    config.vm.provision "shell", inline: <<-SHELL
    echo "******** Step 1: Installing dependencies ********"
    sudo zypper refresh
    sudo zypper --non-interactive install bzip2
    sudo zypper --non-interactive install etcd
    sudo zypper --non-interactive install lsof
    sudo zypper --non-interactive install htop
    sudo zypper --non-interactive install net-tools
    sudo zypper --non-interactive install wget
    sudo zypper --non-interactive install apparmor-parser
    sudo zypper --non-interactive install k9s
    sudo zypper --non-interactive install bind-utils
    echo -e "******** Begin installing k3s ********\n"
    curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
    mkdir -p /home/vagrant/.kube
    /usr/local/bin/kubectl config view --raw >/home/vagrant/.kube/config
    echo -e "******** End installing k3s ********\n\n"
    echo -e "******** Step 2: Setting up Observability ********\n\n"
    echo -e "******** Begin installing Helm ********\n"
    export PATH=$PATH:/usr/local/bin
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    echo -e "******** End installing Helm ********\n\n"
    echo -e "******** Begin installing Grafana and Prometheus ********\n"
    /usr/local/bin/kubectl create namespace monitoring
    /usr/local/bin/helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    /usr/local/bin/helm repo add stable https://charts.helm.sh/stable
    /usr/local/bin/helm repo update
    /usr/local/bin/helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml
    echo -e "******** End installing Grafana and Prometheus ********\n\n"
    echo -e "******** Begin installing Jaeger ********\n"
    /usr/local/bin/kubectl create namespace observability
    /usr/local/bin/kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/crds/jaegertracing.io_jaegers_crd.yaml
    /usr/local/bin/kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/service_account.yaml
    /usr/local/bin/kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml
    /usr/local/bin/kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role_binding.yaml
    /usr/local/bin/kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/operator.yaml
    echo -e "******** End installing Jaeger ********\n\n"
    echo -e "******** Begin configuring Cluster wide Jaeger ********\n"
    /usr/local/bin/kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/cluster_role.yaml
    /usr/local/bin/kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/cluster_role_binding.yaml
    echo -e "******** End configuring Cluster wide Jaeger ********\n\n"
    echo "******** Verify helm is installed ********"
    /usr/local/bin/helm ls --kubeconfig /etc/rancher/k3s/k3s.yaml --namespace=monitoring
    echo "******** Verify prometheus is installed ********"
    /usr/local/bin/kubectl get pods --namespace=monitoring
    echo "******** Verify jaeger is running ********"
    /usr/local/bin/kubectl get pods --namespace=observability
  SHELL

end