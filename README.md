# Container Training 2 - MapServer Deployment

This project contains the configuration for deploying MapServer on Kubernetes, using **Tilt** for local development and **Rancher Desktop** as the Kubernetes environment.

## Prerequisites

### 1. Install Rancher Desktop (Linux - Ubuntu/Debian)

Rancher Desktop provides a local Kubernetes cluster (based on k3s).

```bash
# 1. Add GPG key
curl -s https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/Release.key | gpg --dearmor | sudo dd status=none of=/usr/share/keyrings/isv-rancher-stable-archive-keyring.gpg

# 2. Add repository
echo 'deb [signed-by=/usr/share/keyrings/isv-rancher-stable-archive-keyring.gpg] https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/ ./' | sudo dd status=none of=/etc/apt/sources.list.d/isv-rancher-stable.list

# 3. Update and install
sudo apt update
sudo apt install rancher-desktop
```

Launch Rancher Desktop and ensure **Kubernetes** and **Traefik** (Ingress Controller) are enabled in the settings.

### 2. CLI Tools

Ensure you have the following installed:
- `kubectl` (bundled with Rancher Desktop or installed separately)
- `tilt` (for running the dev environment)

#### Install Tilt

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Verify the cluster status:

```bash
kubectl get pods -A
```

## Running MapServer

We use **Tilt** to spin up the MapServer stack.

1. Navigate to the mapserver directory:
   ```bash
   cd mapserver
   ```

2. Start Tilt:
   ```bash
   tilt up
   ```

3. Open the Tilt interface (usually `http://localhost:10350`) to monitor the build and deployment.

## Accessing the Service

Once up, MapServer is available via:

*   **WMS URL (Local):** `http://localhost:8080/mapserver?...` (via Tilt port-forwarding). If you need to port-forward manually, prefer the CLI (`kubectl -n mapserver port-forward svc/mapserver 8080:80`) over the Rancher Desktop GUI port-forward to avoid extra proxy latency.
*   **Ingress Host:** `mapserver.local` (requires adding `127.0.0.1 mapserver.local` to your `/etc/hosts`).

**Example WMS Request:**
```
http://localhost:8080/mapserver?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=2914994,4969954,3129956,5152659&CRS=EPSG:3035&WIDTH=800&HEIGHT=600&LAYERS=URBAN_ATLAS_COG&STYLES=&FORMAT=image/png
```
