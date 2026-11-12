# The Race to Standardize AI Observability

Demo for the talk by **Liudmila Molkova (Google)** and **Trask Stalnaker (Microsoft)** at KubeCon + CloudNativeCon North America 2026, Salt Lake City.

- [Official session page](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/program/schedule/?id=1246166)
- [Slides](https://docs.google.com/presentation/d/1nwmES8G-lnPtKkYeM_TrO1tkBLSkRjCOsPlz5rRYDiw/edit?usp=sharing)
- [Demo details](demos/kubecon-genai/README.md): one application, mixed instrumentation and OTel variants.

The talk follows a team trying to build dashboards from fragmented GenAI telemetry, then shows how semantic conventions, shared instrumentation utilities, and conformance testing help.

## Run the demo

Requires Docker with Compose and Python 3 for the telemetry inspection script. Model responses come from a local mock server; no model-provider credentials or cloud accounts are needed.

```sh
cd demos/kubecon-genai
docker compose up --build -d
curl --fail-with-body http://localhost:8000/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
python3 inspect_demo.py
```

Open [Aspire](http://localhost:18888) for the mixed-instrumentation demo.

For the parallel OTel instrumentation demo:

```sh
docker compose -f compose.otel.yaml up --build -d
curl --fail-with-body http://localhost:8010/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
ASPIRE_URL=http://localhost:18889 python3 inspect_demo.py
```

Open [Aspire for OTel](http://localhost:18889). Both stacks can run together. See the [demo README](demos/kubecon-genai/README.md) for scenarios, verification, and known behavior.

Stop them with:

```sh
docker compose down
docker compose -f compose.otel.yaml down
```

## License

[MIT](LICENSE) for the demo code. Referenced projects and dependencies retain their respective licenses and trademarks.
