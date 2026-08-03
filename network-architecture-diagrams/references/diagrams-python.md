# The `diagrams` library (mingrammer) for provider-icon architecture images

Use this when the user wants **real AWS/GCP/Azure/Kubernetes service icons**
or a **presentation-quality PNG/SVG** for slides or formal docs. It renders
via Graphviz, so both Graphviz and the Python package must be installed.

## Setup (one time)

```bash
# Graphviz engine — pick the one for this environment:
#   Debian/Ubuntu:  sudo apt-get install -y graphviz
#   macOS:          brew install graphviz
#   (no sudo?)      conda install -c conda-forge graphviz  — or use Mermaid instead
pip install diagrams
```

If Graphviz can't be installed here, fall back to Mermaid
(`references/mermaid.md`) — it needs no system packages.

## How it works

You write a Python script; running it writes an image file. Nodes are Python
objects, `>>` / `<<` / `-` draw edges, and `Cluster` draws labeled
boundaries. `show=False` stops it trying to open a viewer.

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53

with Diagram("Web Service", show=False, filename="web_service", direction="LR"):
    dns = Route53("dns")
    lb = ELB("lb")
    with Cluster("App tier"):
        workers = [EC2("web1"), EC2("web2"), EC2("web3")]
    db = RDS("postgres")

    dns >> lb >> workers >> db
```

Run it:

```bash
python web_service.py        # writes web_service.png in the current dir
```

Key knobs:
- `direction=` — `"LR"` (default here for request flows), `"TB"`, `"RL"`, `"BT"`.
- `outformat="svg"` (or `"pdf"`) on `Diagram(...)` for vector output.
- `filename=` sets the output name (no extension).
- A list of nodes on one side of `>>` fans the edge out to all of them.
- `Edge(label="HTTPS 443", style="dashed", color="firebrick")` labels/styles
  a connection — use it to put ports/protocols on the wire, same as Mermaid.

## Edges with labels (do this — unlabeled edges are ambiguous)

```python
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("labeled", show=False, direction="LR"):
    app = EC2("app")
    db = RDS("db")
    app >> Edge(label="TCP 5432") >> db
    app >> Edge(label="async", style="dashed") >> db
```

## Node import cheat-sheet

Import paths follow `diagrams.<provider>.<category>`. The most common:

**AWS** (`diagrams.aws.*`)
- `compute`: `EC2`, `ECS`, `EKS`, `Lambda`, `Fargate`
- `database`: `RDS`, `Dynamodb`, `ElastiCache`, `Redshift`, `Aurora`
- `network`: `ELB`, `ALB`, `Route53`, `CloudFront`, `VPC`, `NATGateway`,
  `InternetGateway`, `APIGateway`
- `storage`: `S3`, `EBS`, `EFS`
- `integration`: `SQS`, `SNS`, `Eventbridge`
- `security`: `IAM`, `WAF`, `SecretsManager`

**GCP** (`diagrams.gcp.*`)
- `compute`: `ComputeEngine`, `GKE`, `Run`, `Functions`
- `database`: `SQL`, `Firestore`, `Bigtable`, `Spanner`
- `network`: `LoadBalancing`, `CDN`, `DNS`, `VPC`
- `storage`: `GCS`
- `analytics`: `Bigquery`, `Pubsub`

**Azure** (`diagrams.azure.*`)
- `compute`: `VM`, `AKS`, `FunctionApps`, `ContainerInstances`
- `database`: `SQLDatabases`, `CosmosDb`, `CacheForRedis`
- `network`: `LoadBalancers`, `ApplicationGateway`, `CDNProfiles`, `VirtualNetworks`
- `storage`: `BlobStorage`

**Kubernetes** (`diagrams.k8s.*`)
- `compute`: `Pod`, `Deployment`, `ReplicaSet`, `StatefulSet`, `DaemonSet`
- `network`: `Service`, `Ingress`
- `storage`: `PV`, `PVC`

**On-prem / generic** (`diagrams.onprem.*`)
- `compute`: `Server`
- `database`: `Postgresql`, `Mysql`, `Mongodb`
- `inmemory`: `Redis`
- `queue`: `Kafka`, `Rabbitmq`
- `network`: `Nginx`, `Haproxy`, `Internet`
- `client`: `Users`, `Client`
- `container`: `Docker`
- `ci`: `Jenkins`, `GithubActions`

If an exact node doesn't exist, use the closest match or a generic
`diagrams.onprem.compute.Server` / `diagrams.generic.*` node — the label
carries the meaning.

## Full example: clustered VPC with grouped tiers

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import Route53, CloudFront, ALB
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, ElastiCache

with Diagram("3-Tier VPC", show=False, filename="vpc_3tier", direction="LR"):
    dns = Route53("dns")
    cdn = CloudFront("cdn")

    with Cluster("VPC 10.0.0.0/16"):
        with Cluster("Public subnet"):
            lb = ALB("alb")
        with Cluster("Private subnet — app"):
            app = [EC2("web1"), EC2("web2"), EC2("web3")]
        with Cluster("Private subnet — data"):
            primary = RDS("primary")
            replica = RDS("replica")
            cache = ElastiCache("redis")
            primary - Edge(label="replication", style="dashed") - replica

    dns >> cdn >> Edge(label="HTTPS 443") >> lb
    lb >> Edge(label="HTTP 8080") >> app
    app >> Edge(label="TCP 5432") >> primary
    app >> Edge(label="TCP 6379") >> cache
```

## Kubernetes example

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Deployment, Pod

with Diagram("K8s app", show=False, filename="k8s_app", direction="LR"):
    ing = Ingress("ingress")
    with Cluster("namespace: prod"):
        svc = Service("orders-svc")
        with Cluster("Deployment"):
            pods = [Pod("pod1"), Pod("pod2")]
        svc >> pods
    ing >> Edge(label="HTTPS") >> svc
```

After running, confirm the output file exists and open/read it to verify the
arrows and clusters match the intended architecture.
