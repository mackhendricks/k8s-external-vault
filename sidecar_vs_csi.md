# Definitions

- CSI = Container Storage Interface
- Sidecar = Vault Sidecar

# Reference Articles

- [Retrieve HashiCorp Vault Secrets with Kubernetes CSI](https://www.hashicorp.com/blog/retrieve-hashicorp-vault-secrets-with-kubernetes-csi)
- [Integrate a Kubernetes Cluster with an External Vault](https://learn.hashicorp.com/tutorials/vault/kubernetes-external-vault)

# Comparisons

|Feature | CSI  | Sidecar  |
|---|---|---|
| Developer uses anotations to specify the secrets they want to retrieve from Vault |  Yes  | Yes  |
| Secrets can be stored in an Environment variable   |  Yes | Yes   |
| Syncing of secrets to environment variables.  | Yes  | No  |
| Additional Containers Required | No | Yes |
| Sync secrets into environment variables and Kubernetes secrets | Yes | No |

