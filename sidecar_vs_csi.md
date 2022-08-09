# Definitions

- CSI = Container Storage Interface
- Sidecar = Vault Sidecar

# Reference Articles

- [Retrieve HashiCorp Vault Secrets with Kubernetes CSI](https://www.hashicorp.com/blog/retrieve-hashicorp-vault-secrets-with-kubernetes-csi)
- [Integrate a Kubernetes Cluster with an External Vault](https://learn.hashicorp.com/tutorials/vault/kubernetes-external-vault)

# Comparisons

|Feature | CSI  | Sidecar  |
|---|---|---|
| Developer uses anotations to specify the secrets they want to retrieve from Vault |  No  | Yes  |
| Additional Containers Required | No | Yes |
| Sync secrets into environment variables and Kubernetes secrets** | Yes | No |


** If your security requirements require you to disable **hostPath** volumes, you should be aware that this method uses hostPath volumes to communicate with the CSI driver. Some Kubernetes distributions may disable this due to the level of access it gives to the node’s filesystem.

