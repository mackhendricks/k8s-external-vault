# Steps to setup k8s to obtain secrets from an external Vault

## Prerequisites

1) We need a k8s Namespace with the following:

- k8s CA Certificate
- Service Account ID
- HTTPS URL to k8s cluster

2) Need to have the ability to deploy the vault-k8s injector via Vault HELM

- Download and Store the vault-k8s image in Artifactory.  The image is located here: https://hub.docker.com/r/hashicorp/vault-k8s
- Have credentials to access Artifactory to obtain the image 

3) Have permissions to enable the k8s auth method on your test Vault server and the ability to set up a policy.


## 

```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault \
    --set "injector.externalVaultAddr=http://external-vault:8200"
```
