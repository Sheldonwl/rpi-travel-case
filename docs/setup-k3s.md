# Setup K3s 

## Configure iptables
To use K3s we need to enable iptables-legacy, as K3s does not support iptables-nft. You will need to run this command on the server and all agents: 
```
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
```
That's it!

## Setup K3s Server
To setup the server all we need to do is run the following command. Keep in mind, you might need to change the IP addresses to fit your setup. 
```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--bind-address 192.168.3.10 --advertise-address 192.168.3.10" sh -s –
```
I've added **--bind-address** and **--advertise-address** so the correct IP is used for exposing the Kubernetes API. 

For demo'ing purposes I will be using the following command: 
```
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--bind-address 192.168.3.10 --advertise-address 192.168.3.10 --kube-apiserver-arg default-not-ready-toleration-seconds=10 --kube-apiserver-arg default-unreachable-toleration-seconds=10 --kube-controller-arg node-monitor-period=10s --kube-controller-arg node-monitor-grace-period=10s --kubelet-arg node-status-update-frequency=5s" sh -
```

This command let's the node-controller check the available nodes a lot faster. I might need to unplug a Pi and have some action happen, so I don't want to wait for the default 5 minutes before something finally happens. 

### What are all those extra arguments?
**API Server**  
*--default-not-ready-toleration-seconds int*  
Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration.  
*--default-unreachable-toleration-seconds int*  

**Kubelet**  
*--node-status-update-frequency duration*  
Specifies how often kubelet posts node status to master. Note: be cautious when changing the constant, it must work with nodeMonitorGracePeriod in nodecontroller. (default 10s)  

**Controller Manager**  
*--node-monitor-grace-period duration*  
Amount of time which we allow running Node to be unresponsive before marking it unhealthy. Must be N times more than kubelet's nodeStatusUpdateFrequency, where N means number of retries allowed for kubelet to post node status.  
*--node-monitor-period duration*  
The period for syncing NodeStatus in NodeController.

## Setup K3s Agent
To setup the agents you will need to first get the node-token from the host where you have setup the server. 
```
sudo cat /var/lib/rancher/k3s/server/node-token

E.g. K10c93f8c19514a653beb33b27e10c2cb4dcca4f6c92116e2d754450bbc9ee197c6::server:a4765a17f563ceadf529c8857263689b
```

Now you can use that token on the host you will be running the agent from. Let's first create an environment variable, to store the token. 
```
export NODE_TOKEN={PASTE TOKEN}

E.g. export NODE_TOKEN=K10c93f8c19514a653beb33b27e10c2cb4dcca4f6c92116e2d754450bbc9ee197c6::server:a4765a17f563ceadf529c8857263689b
```

Now let's install K3s and point it to the server. When we add the **K3S_URL** parameter, K3s will setup this instance as an Agent and not a Server. So we can run the following on the agent.
```
curl -sfL https://get.k3s.io | K3S_TOKEN=${NODE_TOKEN} K3S_URL="https://192.168.3.10:6443" sh -
```

Checkout the K3s docs if you need to edit any args: https://rancher.com/docs/k3s/latest/en/installation/install-options/
