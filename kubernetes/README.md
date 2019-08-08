# Server Configuration (Kubernetes)

This makes use of `kubectl kustomize` which is an integration of [Kustomize](https://github.com/kubernetes-sigs/kustomize) into `kubectl`.

Folder structure is as follows:
```
.
├── README.md
├── base
│   ├── SERVER-A
│   └── SERVER-B
└── overlays
    ├── SERVER-A
    │   ├── CLIENT-A
    │   └── CLIENT-B
    └── SERVER-B
        ├── CLIENT-A
        └── CLIENT-B
```

## Adding a new client

When adding a new client, a new `overlay` should be added for each server which the client is configured via the CI to interact with.

If no variation to the `base` configuration is required, a default `kustomization.yaml` can be used as shown below. 

```
bases:
- ../../base/<SERVER>
```

A job deployment can be created for building with a client in `../jobs` before being added to CI.

## Adding a new server

When adding a new server, a new 'base' should be added with a default working configuration. At least one client should be added as detailed above. These server configurations can be configued per client using the method detailed in the section above, patching the kubernetes configuration YAML files as appropriate. 

## Testing configuration

A configuration can be verified using `kubectl kustomize overlays/server/client` to see the merged YAML output. Simply piping this into `kubectl create -f -` with a local kubernetes cluster will start up the configured instances.

