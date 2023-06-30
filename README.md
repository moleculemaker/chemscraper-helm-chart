# chemscraper-helm-chart
Helm chart for running Chemscraper + YOLO + sscraper in a Kubernetes cluster


## References
* Source code branch: [dprl/graphics-extraction](https://gitlab.com/dprl/graphics-extraction/-/tree/mst_parser)
* Docker Compose recipe: [dprl/dprl-alphasynthesis](https://gitlab.com/dprl/dprl-alphasynthesis)


## PSA: Always check Pod `AGE` after deploying
You may need to delete the running Pod to trigger a new Pod to be created with the new config.


## Local
If you are running Docker + Kubernetes locally on your laptop, you can use the following to run chemscraper locally

To change the existing application in your local cluster, you can use the following command:
```bash
$ helm upgrade --install chemscraper -n staging . -f values.local.yaml
```

This will overwrite the configuration of the instance in your local cluster.

You should then be able to access the following URLs:
* Chemscraper: chemscraper.backend.localhost/docs
* YOLO: yolo.chemscraper.backend.localhost/swagger-ui
* Symbolscraper: symbolscraper.chemscraper.backend.localhost/docs

This example is currently configured to use the NGINX Ingress Controller, but you can adjust values.local.yaml to cahnge the ingress class.


## Staging
To change the existing application in the `staging` namespace, you can use the following command:
```bash
$ helm upgrade --install chemscraper -n staging . -f values.staging.yaml
```

This will overwrite the configuration of the current staging instance.

Swagger UI is available to test each service individually (if desired):
* Chemscraper: https://chemscraper.backend.staging.mmli1.ncsa.illinois.edu/docs
* YOLO: https://yolo.chemscraper.backend.staging.mmli1.ncsa.illinois.edu/swagger-ui
* Symbolscraper: https://symbolscraper.chemscraper.backend.staging.mmli1.ncsa.illinois.edu/docs


## Prod
TBD - prod should look almost identical to `staging`, and will be deployed automatically by ArgoCD once the necessary pieces are in place. Prod will have the same URLs as above, just without the `.staging` in each


## TODOs
* Create a (Cron?)Job that will prepull the Docker image for yolo
* Create ArgoCD apps for staging + prod
