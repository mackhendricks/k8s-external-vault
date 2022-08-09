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

4) Download and add this application into your Artifactory: https://hub.docker.com/r/burtlo/devwebapp-ruby


## Installing with Internet Access

```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm install vault hashicorp/vault \
    --set "injector.externalVaultAddr=http://external-vault:8200" --namespace <k8s namespace> -f ./override.yaml
```

## Installing in Airgap Environment (no internet - Done by the Developer)
```
git clone https://github.com/hashicorp/vault-helm
cd vault-helm
helm install -f override.yaml  --set "injector.externalVaultAddr=http://external-vault:8200" --namespace <k8s namespace> vault .
```

## Setting up Kubernetes Auth Prerequsites ( for the k8s Administrator)

### Create a variable named VAULT_HELM_SECRET_NAME that stores the secret name.  
This command filters the secrets by those that start with vault-token- and returns the name of token.

```
VAULT_HELM_SECRET_NAME=$(kubectl get secrets --namespace <<yournamespace>>  --output=json | jq -r '.items[].metadata | select(.name|startswith("vault-token-")).name')
```

### Get the JSON web token (JWT) from the secret.

```
TOKEN_REVIEW_JWT=$(kubectl get secret $VAULT_HELM_SECRET_NAME --namespace <<yournamespace>> --output='go-template={{ .data.token }}' | base64 --decode)
```

### Retrieve the Kubernetes CA certificate

```
KUBE_CA_CERT=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.certificate-authority-data}' | base64 --decode)
```

### Retrieve the Kubernetes host URL
```
KUBE_HOST=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.server}')
```

## Get the Issuer address

You need obtain the iss field out of the returned JSON mesage

```
KUBE_ISSUER=echo '{"apiVersion": "authentication.k8s.io/v1", "kind": "TokenRequest"}' \
  | kubectl create -f- --raw /api/v1/namespaces/default/serviceaccounts/default/token \
  | jq -r '.status.token' \
  | cut -d . -f2 \
  | base64 -d| jq -r .iss
```

### Create a service account for your app(s)
```
kubectl create sa internal-app
```

### Enable Kubernetes Auth (for Vault Team)
```
vault auth enable kubernetes
```

### Configure Kubernetes Auth

```
vault write auth/kubernetes/config \
     token_reviewer_jwt="$TOKEN_REVIEW_JWT" \
     kubernetes_host="$KUBE_HOST" \
     kubernetes_ca_cert="$KUBE_CA_CERT" \
     issuer="https://kubernetes.default.svc.cluster.local"
```

### Create a Policy
```
vault policy write devwebapp - <<EOF
path "secret/data/devwebapp/config" {
  capabilities = ["read"]
}
```

### Create Role

```
vault write auth/kubernetes/role/devweb-app \
     bound_service_account_names=internal-app \
     bound_service_account_namespaces=<<yournamespace>> \
     policies=devwebapp \
     ttl=24h
```

## Injecting secrets into the pod (Done by Development Team)


## Create Secret for Pulling Images from a Registry

### Create yaml file to deploy sample example.  Please change the external-vault to the IP or DNS name of your Vault Instance.

```
cat > pod-devwebapp-with-annotations.yaml <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: devwebapp-with-annotations
  labels:
    app: devwebapp-with-annotations
  annotations:
    vault.hashicorp.com/agent-inject: 'true'
    vault.hashicorp.com/role: 'devweb-app'
    vault.hashicorp.com/agent-inject-secret-credentials.txt: 'secret/data/devwebapp/config'
spec:
  serviceAccountName: internal-app
  containers:
    - name: app
      image: burtlo/devwebapp-ruby:k8s
      env:
      - name: VAULT_ADDR
        value: "http://external-vault:8200"
  imagePullSecrets:
    - name: myregistrykey
EOF
```

### Apply Yaml

```
kubectl apply --filename pod-devwebapp-with-annotations.yaml --namespace <<yournamespace>>
```

### Validate that secrets were created
```
kubectl exec --namespace <<yournamespace>> -it devwebapp-with-annotations -c app -- cat /vault/secrets/credentials.txt
```
