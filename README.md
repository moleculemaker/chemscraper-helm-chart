# chemscraper-helm-chart
Helm chart for running Chemscraper + YOLO + sscraper + LGAP in a Kubernetes cluster


## References
* Source code:
  * Chemscraper: [dprl/graphics-extraction](https://gitlab.com/dprl/graphics-extraction)
  * YOLO: [dprl/yolov8sever](https://gitlab.com/dprl/yolov8sever)
  * Symbolscraper: [dprl/symbolscraper-server](https://gitlab.com/dprl/symbolscraper-server)
  * LGAP: [dprl/lgap-parser](https://gitlab.com/dprl/lgap-parser)
* Docker Compose recipe: [dprl/dprl-alphasynthesis](https://gitlab.com/dprl/dprl-alphasynthesis)


## PSA: Always check Pod `AGE` after deploying
You may need to delete the running Pod to trigger a new Pod to be created with the new config.


## Local
If you are running Docker + Kubernetes locally on your laptop, you can use the following to run chemscraper locally

To change the existing application in your local cluster, you can use the following command:
```bash
$ kubectl config use-context docker-desktop
$ helm upgrade --install chemscraper -n staging . -f values.local.yaml
```

This will overwrite the configuration of the instance in your local cluster.

You should then be able to access the following URLs:
* Chemscraper: http://chemscraper.backend.localhost/docs
* YOLO: http://yolo.chemscraper.backend.localhost/swagger-ui
* Symbolscraper: http://symbolscraper.chemscraper.backend.localhost/docs
* LGAP: http://lgap.chemscraper.backend.localhost/docs

This example is currently configured to use the NGINX Ingress Controller, but you can adjust values.local.yaml to cahnge the ingress class.


## Staging
To change the existing application in the `staging` namespace, you can use the following command:
```bash
$ kubectl config use-context mmli1
$ helm upgrade --install chemscraper -n staging . -f values.staging.yaml
```

This will overwrite the configuration of the current staging instance.

Swagger UI is available to test each service individually (if desired):
* Chemscraper: https://chemscraper.backend.staging.mmli1.ncsa.illinois.edu/docs
* YOLO: https://yolo.chemscraper.backend.staging.mmli1.ncsa.illinois.edu/swagger-ui
* Symbolscraper: https://symbolscraper.chemscraper.backend.staging.mmli1.ncsa.illinois.edu/docs
* LGAP: https://lgap.chemscraper.backend.staging.mmli1.ncsa.illinois.edu/docs


## Production
To change the existing application in the `alphasynthesis` namespace, you can use the following command:
```bash
$ kubectl config use-context mmli1
$ helm upgrade --install chemscraper -n alphasynthesis . -f values.prod.yaml
```

This will overwrite the configuration of the current production instance.

Swagger UI is available to test each service individually (if desired):
* Chemscraper: https://chemscraper.backend.mmli1.ncsa.illinois.edu/docs
* YOLO: https://yolo.chemscraper.backend.mmli1.ncsa.illinois.edu/swagger-ui
* Symbolscraper: https://symbolscraper.chemscraper.backend.mmli1.ncsa.illinois.edu/docs
* LGAP: https://lgap.chemscraper.backend.mmli1.ncsa.illinois.edu/docs

